[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/J3J41UVIX7)

## vpnSelector

Small terminal TUI helper to quickly choose and start a Hack The Box (HTB) VPN configuration with `openvpn`.

## Description

`vpnselect` scans a directory for `.ovpn` files, shows them in a simple curses menu, and then replaces itself with:

```bash
sudo openvpn <selected-config.ovpn>
```

This makes it behave the same as running `sudo openvpn` manually, but with a nicer selection step.

## Requirements

- Python 3
- `openvpn`
- A set of `.ovpn` configuration files

## Installation

1. Clone or copy this repository.
2. Make the script executable and put it on your `PATH`:

```bash
chmod +x vpnselect.py
mkdir -p "$HOME/bin"
cp vpnselect.py "$HOME/bin/vpnselect"
```

3. Ensure `~/bin` is on your `PATH`, e.g. in `~/.zshrc`:

```bash
export PATH="$HOME/bin:$PATH"
```

Reload your shell:

```bash
source ~/.zshrc
```

## Configuration

By default, `vpnselect` looks for `.ovpn` files in:

```bash
~/Documents/CTF/HTB/VPNs
```

You can override this in two ways:

- **Environment variable**:

```bash
export VPN_DIR="~/some/other/dir"
vpnselect
```

- **Command‑line argument**:

```bash
vpnselect ~/some/other/dir
```

## Usage

Run:

```bash
vpnselect
```

Then:

- Use **↑/↓** or **k/j** to move between configs.
- Press **Enter** to start the selected VPN.
- Press **q** or **Esc** to quit without starting anything.

