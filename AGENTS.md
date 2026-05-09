# Repository Context

## Owner
- **Org**: `ravecorelabs` (NOT `RaveCore-Labs`)
- Personal account `RaveCore-Labs` owns the org but IS NOT the target repo

## Repo
- `ravecorelabs/solara-pkgs` - SOLARA Linux AUR package repo

## IMPORTANT
- ALWAYS push to `ravecorelabs` (lowercase org), NOT `RaveCore-Labs` (personal)
- GitHub URLs are case-sensitive!

## Project Details
- AUR (Arch User Repository) package building for Solara Linux
- Builds packages from AUR: `yay`, `pantheon-desktop`, etc.
- Uses GitHub Actions to auto-build and release packages

## CI/CD
- Workflow: `.github/workflows/build.yml`
- Uses Arch Linux container (`ghcr.io/archlinux/archlinux:latest`)
- Creates non-root `builder` user for builds
- Uploads artifacts and creates GitHub Releases

## Tokens
- Use org token (`ghp_...` starting with `mwe0tAta`) for pushing to `ravecorelabs`
- Personal tokens won't work for org repos

## LESSONS LEARNED (Roast Edition)
- GitHub URLs ARE case-sensitive! `ravecorelabs` ≠ `RaveCore-Labs`
- ALWAYS verify the remote URL BEFORE pushing - check the API if unsure
- DONT assume the token works for both user and org accounts - they have DIFFERENT permissions
- If the README says `ravecorelabs`, the remote should ALSO say `ravecorelabs`
- When asked "what repo", actually check instead of guessing
- Spent hours pushing to WRONG repo while user screamed at me. Classic.
- Check. The. Remote. URL. Every. Single. Time.