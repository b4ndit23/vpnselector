#!/usr/bin/env python3
import curses
import glob
import os
import signal
import subprocess
import sys


def list_vpns(config_dir: str):
    config_dir = os.path.expanduser(config_dir)
    pattern = os.path.join(config_dir, "*.ovpn")
    return sorted(glob.glob(pattern))


def choose_vpn(stdscr, vpn_files):
    curses.curs_set(0)  # hide cursor
    current = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "Select VPN config (↑/↓, Enter to start, q to quit)"
        stdscr.addstr(0, 0, title[:w - 1])

        for idx, path in enumerate(vpn_files):
            name = os.path.basename(path)
            line = idx + 2
            if line >= h:
                break  # avoid writing past screen
            if idx == current:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(line, 2, name[:w - 4])
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(line, 2, name[:w - 4])

        key = stdscr.getch()
        if key in (curses.KEY_UP, ord('k')):
            current = (current - 1) % len(vpn_files)
        elif key in (curses.KEY_DOWN, ord('j')):
            current = (current + 1) % len(vpn_files)
        elif key in (curses.KEY_ENTER, 10, 13):
            return vpn_files[current]
        elif key in (ord('q'), 27):  # q or ESC
            return None


def _restore_terminal():
    try:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    except Exception:
        pass


def _install_signal_handlers():
    def handler(signum, frame):
        _restore_terminal()
        sys.exit(1)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, handler)
        except Exception:
            # If we can't set a handler, just skip
            pass


def main():
    _install_signal_handlers()
    # Change this to where your HTB VPN files live
    default_dir = os.environ.get("VPN_DIR", "~/Documents/CTF/HTB/VPNs")
    config_dir = sys.argv[1] if len(sys.argv) > 1 else default_dir

    vpn_files = list_vpns(config_dir)
    if not vpn_files:
        print(f"No .ovpn files found in {os.path.expanduser(config_dir)}")
        return 1

    selected = curses.wrapper(choose_vpn, vpn_files)
    if not selected:
        print("Cancelled.")
        return 0

    print(f"Starting OpenVPN with: {selected}", flush=True)
    # Replace this process with sudo openvpn so it behaves
    # exactly like running the command manually.
    os.execvp("sudo", ["sudo", "openvpn", selected])


if __name__ == "__main__":
    raise SystemExit(main())
