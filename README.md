# solara-pkgs

AUR package repository for Solara Linux.

## What's in here

This repo builds and hosts AUR-only packages that aren't in the official Arch repos. If a package exists in `extra` or `core`, it doesn't belong here.

**Note on Pantheon:** Pantheon is NOT on the AUR. The entire `pantheon` group and all its apps (`pantheon-session`, `gala`, `wingpanel`, etc.) are in the official Arch `extra` repo. Install with `pacman -S pantheon`.

## Packages

- `yay` — AUR helper
- `visual-studio-code-bin` — official Microsoft VS Code binary

## Usage

Add to `/etc/pacman.conf`:

```
[solara-pkgs]
SigLevel = Optional TrustAll
Server = https://github.com/ravecorelabs/solara-pkgs/releases/download/latest
```

Then `pacman -Sy` and install packages normally.

## License

GPL-3.0
