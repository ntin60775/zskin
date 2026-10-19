#!/usr/bin/env bash
# zskin menu launcher — target of loader/zskin.desktop (application menu).
# Runs the full pipeline: launch the stock ZCode binary with the CDP debug
# port, then inject the theme. Guards against the app-level single-instance
# caveat so a click never ends in a silent 60s hang.

set -u

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOADER="$REPO_DIR/loader/zskin.py"
THEME="$REPO_DIR/themes/gruvbox.css"
# Composer silhouette shipped by default (user-picked 2026-10-19);
# ZSKIN_COMPOSER overrides, set it empty for the stock shell.
COMPOSER="${ZSKIN_COMPOSER-$REPO_DIR/themes/composer/rule.css}"
LOG_FILE="$HOME/.local/state/zskin-launcher.log"
LOCK_FILE="$HOME/.config/ZCode/SingletonLock"

mkdir -p "$(dirname "$LOG_FILE")"

notify() {
    # Best-effort desktop notification; silently skip when unavailable.
    command -v notify-send >/dev/null 2>&1 || return 0
    notify-send -a zskin "$1" "${2:-}"
}

client_running() {
    # SingletonLock is a "hostname-pid" symlink held by the live instance;
    # verify the pid is alive and really is zcode (not a recycled pid).
    local lock pid
    lock="$(readlink "$LOCK_FILE" 2>/dev/null)" || return 1
    pid="${lock##*-}"
    [ -n "$pid" ] && [ "$pid" != "$lock" ] || return 1
    kill -0 "$pid" 2>/dev/null || return 1
    grep -qi '^zcode$' "/proc/$pid/comm" 2>/dev/null
}

if client_running; then
    echo "$(date '+%F %T') client already running, launch skipped" >>"$LOG_FILE"
    notify "zskin" "ZCode уже запущен — закройте его и нажмите ярлык снова"
    exit 1
fi

echo "$(date '+%F %T') launching: zskin.py run --theme $THEME${COMPOSER:+ --composer $COMPOSER} --watch" >>"$LOG_FILE"
# --watch keeps the loader resident: project colors regenerate when the
# project set changes, and page reloads get re-injected. When the client
# exits, CDP dies and the watch loop returns.
if out="$(python3 "$LOADER" run --theme "$THEME" ${COMPOSER:+--composer "$COMPOSER"} --watch 2>&1)"; then
    printf '%s %s\n' "$(date '+%F %T')" "$out" >>"$LOG_FILE"
    exit 0
fi

rc=$?
printf '%s FAILED rc=%s\n%s\n\n' "$(date '+%F %T')" "$rc" "$out" >>"$LOG_FILE"
notify "zskin: не удалось запустить" \
    "$(printf '%s\n' "$out" | tail -n 2) — подробности: $LOG_FILE"
exit "$rc"
