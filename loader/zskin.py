#!/usr/bin/env python3
"""zskin loader — live CSS theming for the official ZCode desktop client.

Launches the stock ZCode binary with a CDP (Chrome DevTools Protocol) debug
port, attaches to the main window renderer and injects a CSS file as a
<style> element. No product file is modified; the client stays the official
binary with its own auth, updates and plan machinery.

stdlib-only Python 3 (no dependencies), same bar as sot-zcode-marketplace
runner.

Usage:
  zskin.py run    --theme themes/example.css [--port 9222] [--bin /opt/ZCode/zcode]
  zskin.py inject --theme themes/example.css [--port 9222]
  zskin.py list   [--port 9222]

  run     start ZCode with the debug port, wait for it, inject, then exit
          (the injected <style> lives as long as the window does)
  inject  attach to an already running instance (started with the port)
  list    show CDP page targets
"""

import argparse
import base64
import json
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.request

DEFAULT_PORT = 9222
DEFAULT_BIN = "/opt/ZCode/zcode"
STYLE_ID = "zskin-style"
WAIT_TIMEOUT = 60.0

INJECT_JS = (
    "(function(css) {"
    "  let el = document.getElementById('%s');"
    "  if (!el) { el = document.createElement('style'); el.id = '%s';"
    "    (document.head || document.documentElement).appendChild(el); }"
    "  el.textContent = css;"
    "  return el.id;"
    "})(%%s)" % (STYLE_ID, STYLE_ID)
)


def http_json(port: int, path: str):
    url = f"http://127.0.0.1:{port}{path}"
    with urllib.request.urlopen(url, timeout=5) as r:
        return json.load(r)


def wait_debug_port(port: int, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    last_err = None
    while time.monotonic() < deadline:
        try:
            http_json(port, "/json/version")
            return
        except OSError as e:
            last_err = e
            time.sleep(0.4)
    raise TimeoutError(f"CDP port {port} did not come up: {last_err}")


def pick_page_target(port: int) -> dict:
    targets = http_json(port, "/json/list")
    pages = [t for t in targets
             if t.get("type") == "page" and not t.get("url", "").startswith("devtools:")]
    if not pages:
        raise RuntimeError(f"no page targets: {[t.get('type') for t in targets]}")
    return pages[0]


class WsClient:
    """Minimal RFC 6455 client for localhost CDP: text frames, ping handling."""

    def __init__(self, host: str, port: int, path: str):
        self.s = socket.create_connection((host, port), timeout=10)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
               "Upgrade: websocket\r\nConnection: Upgrade\r\n"
               f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.s.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = self.s.recv(4096)
            if not chunk:
                raise ConnectionError("handshake failed: connection closed")
            buf += chunk
        head, _, rest = buf.partition(b"\r\n\r\n")
        status = head.split(b"\r\n")[0]
        if b" 101 " not in status:
            raise ConnectionError(f"handshake failed: {status!r}")
        self.buf = rest
        self._next_id = 0

    def _recv_exact(self, n: int) -> bytes:
        while len(self.buf) < n:
            chunk = self.s.recv(65536)
            if not chunk:
                raise ConnectionError("connection closed")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _recv_frame(self):
        b1, b2 = self._recv_exact(2)
        opcode = b1 & 0x0F
        ln = b2 & 0x7F
        if ln == 126:
            ln = struct.unpack(">H", self._recv_exact(2))[0]
        elif ln == 127:
            ln = struct.unpack(">Q", self._recv_exact(8))[0]
        payload = self._recv_exact(ln)
        return opcode, payload

    def call(self, method: str, params: dict, timeout: float = 15.0) -> dict:
        self._next_id += 1
        msg_id = self._next_id
        self.send_text(json.dumps({"id": msg_id, "method": method, "params": params}))
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            opcode, payload = self._recv_frame()
            if opcode == 0x9:  # ping -> pong
                mask = os.urandom(4)
                masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
                self.s.sendall(bytes([0x8A, 0x80 | len(payload)]) + mask + masked)
                continue
            if opcode == 0x8:
                raise ConnectionError("closed by peer")
            if opcode != 0x1:
                continue
            data = json.loads(payload.decode())
            if data.get("id") == msg_id:
                if "error" in data:
                    raise RuntimeError(f"CDP error: {data['error']}")
                return data.get("result", {})
        raise TimeoutError(f"no response for {method}")

    def send_text(self, text: str) -> None:
        payload = text.encode()
        mask = os.urandom(4)
        ln = len(payload)
        if ln < 126:
            header = struct.pack(">BB", 0x81, 0x80 | ln)
        elif ln < 65536:
            header = struct.pack(">BBH", 0x81, 0x80 | 126, ln)
        else:
            header = struct.pack(">BBQ", 0x81, 0x80 | 127, ln)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.s.sendall(header + mask + masked)


def inject_css(port: int, css: str) -> None:
    target = pick_page_target(port)
    ws_url = target["webSocketDebuggerUrl"]
    rest = ws_url.split("://", 1)[1]
    host, rest = rest.split(":", 1)
    port_ws, path = rest.split("/", 1)
    ws = WsClient(host, int(port_ws), "/" + path)
    expression = INJECT_JS % json.dumps(css)
    result = ws.call("Runtime.evaluate",
                     {"expression": expression, "returnByValue": True})
    if result.get("result", {}).get("value") != STYLE_ID:
        raise RuntimeError(f"unexpected inject result: {result}")
    print(f"zskin: injected {len(css)} bytes of CSS into "
          f"{target.get('url', '?')[:80]}")


def cmd_run(args) -> int:
    css = load_css(args.theme)
    proc = subprocess.Popen(
        [args.bin, f"--remote-debugging-port={args.port}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True)
    print(f"zskin: launched {args.bin} (pid {proc.pid}), "
          f"debug port {args.port}")
    wait_debug_port(args.port, WAIT_TIMEOUT)
    # The first window may appear slightly after the port answers.
    time.sleep(3)
    inject_css(args.port, css)
    return 0


def cmd_inject(args) -> int:
    css = load_css(args.theme)
    inject_css(args.port, css)
    return 0


def cmd_list(args) -> int:
    for t in http_json(args.port, "/json/list"):
        print(f"{t.get('type', '?'):10} {t.get('title', '')[:40]:40} "
              f"{t.get('url', '')[:60]}")
    return 0


def load_css(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="zskin",
                                description="Live CSS theming for ZCode via CDP")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("run", "inject", "list"):
        sp = sub.add_parser(name)
        if name in ("run", "inject"):
            sp.add_argument("--theme", required=True, help="path to CSS file")
        sp.add_argument("--port", type=int, default=int(
            os.environ.get("ZSKIN_PORT", DEFAULT_PORT)))
        if name == "run":
            sp.add_argument("--bin", default=os.environ.get(
                "ZSKIN_ZCODE_BIN", DEFAULT_BIN))
    args = p.parse_args(argv)
    return {"run": cmd_run, "inject": cmd_inject, "list": cmd_list}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
