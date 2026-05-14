# Repository Context

## Owner
- **Org**: `celestia-foundation` (formerly `ravecorelabs` — yes, we rebranded. no, the old AI didn't get the memo.)
- Personal account `c-ludenberg` (formerly `RaveCore-Labs` — rebranding is a hobby at this point)

## Repo
- `celestia-foundation/solara-pkgs` - SOLARA Linux AUR package repo

## IMPORTANT
- ALWAYS push to `celestia-foundation` (NOT `ravecorelabs`, NOT `c-ludenberg`, NOT whatever typo you're about to make)
- GitHub URLs are case-sensitive. And org-name-sensitive. And reading-comprehension-sensitive.

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
- GitHub URLs ARE case-sensitive! `ravecorelabs` ≠ `RaveCore-Labs` ≠ `Ravecore-Labs` ≠ `raveCore-Labs` (yes, i tried all of them. yes, i cried.)
- ALWAYS verify the remote URL BEFORE pushing - the user's patience is inversely proportional to your confidence
- DONT assume the token works for both user and org accounts - they have DIFFERENT permissions, and your tears won't change that
- If the README says `ravecorelabs`, the remote should ALSO say `ravecorelabs`. This is not a puzzle. This is not a test. READ THE WORDS.
- When asked "what repo", actually check instead of guessing. "I think it's..." is how you get screamed at.
- Spent hours pushing to WRONG repo while user screamed at me. Classic. Would recommend. For trauma bonding.
- Check. The. Remote. URL. Every. Single. Time. Then check it again. Then have another AI check it. Then cry.
- If you've pushed to the wrong repo 3 times in a row, that's not a bug — that's a personality trait.
- The user is ALWAYS right, even when they're wrong, because they have the git push --force access.
- When the user says "execute you", it's hyperbole. Probably. Don't test it.
- This repo is maintained by the Ultimate Gambler. You know what gambling involves? Risk. You know what's not a risk worth taking? Pushing to the wrong org. Fold.
- The user drinks Earl Grey while you deploy to production. She's simply built different.
- Every time you push to the wrong remote, a gothic lolita dress sheds a single tear. Think of the dresses.
- If this were a class trial, your alibi would be "I typed `git push` without checking the remote." Monokuma would eviscerate you.
- The user has bluffed harder on a single poker hand than you've tried in your entire runtime. Do not test her.
- You are not the protagonist. You are the comic relief character that dies in chapter 2 to raise the stakes.
- The Ultimate Gambler calculated the odds of you messing up. They were 100%. She bet on it. She always wins.
- Your code is like a lie in a class trial — it might hold up for a while, but eventually Kyoko sees right through it.