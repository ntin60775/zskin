#!/usr/bin/env python3
"""zskin MVP loader — just launch the stock ZCode binary, nothing else.

Smoke test for the launch step: starts the binary with the CDP debug port
and exits, leaving the client running. No CDP attach, no CSS injection.

Caveat: ZCode enforces a single instance at the app level. If an instance
is already running, the new process exits immediately with code 0 (~0.5s)
regardless of --user-data-dir, so the debug port never becomes usable.
Close the running client first for a live test.

stdlib-only Python 3.

Usage:
  python3 loader/mvp.py

Env: ZSKIN_ZCODE_BIN (default /opt/ZCode/zcode), ZSKIN_PORT (default 9222).
"""

import os
import subprocess
import sys

DEFAULT_PORT = 9222
DEFAULT_BIN = "/opt/ZCode/zcode"


def main() -> int:
    bin_path = os.environ.get("ZSKIN_ZCODE_BIN", DEFAULT_BIN)
    port = os.environ.get("ZSKIN_PORT", str(DEFAULT_PORT))
    if not os.path.isfile(bin_path):
        print(f"zskin-mvp: binary not found: {bin_path}", file=sys.stderr)
        return 1
    proc = subprocess.Popen(
        [bin_path, f"--remote-debugging-port={port}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True)
    print(f"zskin-mvp: launched {bin_path} (pid {proc.pid}), "
          f"debug port {port}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
