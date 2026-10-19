# Artwork

The launcher ships **no pictures**. Everything you see is either read from your
own game dump or from a folder you fill yourself, so the repository never
carries artwork that belongs to FromSoftware, Sony or a SteamGridDB uploader.

## Where the pictures come from

| What | Source |
|---|---|
| The banner | Your dump's `sce_sys/pic1.png`, unless you override it |
| Everything else | `art/` in the port folder (next to `Bloodborne.exe`), or `%APPDATA%\bbport-launcher\art` |

The port folder wins when a name exists in both places.

## Names the launcher looks for

| File | Used for |
|---|---|
| `hero.png` | The banner on the first page (any of `.png`, `.jpg`, `.jpeg`, `.webp`) |
| `empty.png` | The empty patch list on “Mods & patches” |

Names are matched case-insensitively; the extension must be one of the four
above. A new file is picked up on the next launch (the lookup is cached against
the folder's timestamp, so no restart loop is needed while it is open).

## Where to get one — SteamGridDB

<https://www.steamgriddb.com/search/grids?term=bloodborne> has hero, grid and
logo images made by the community for Bloodborne. Pick one you like, download
the file, rename it to `hero.png` and drop it into `art/`.

Two honest caveats:

- **SteamGridDB is a gallery, not a licence.** Every upload belongs to whoever
  made it; a few are derivative of official art. For personal use that is
  normally fine, but they are *not* redistributable — which is exactly why the
  launcher reads them from your disk instead of bundling them, and why releases
  never contain them.
- **The launcher cannot download them for you.** SteamGridDB's API needs a
  per-user key and its pages are rendered in the browser, so automated fetching
  would mean asking every player for a key. Dropping a file in a folder is the
  version that works for everyone.

## How it fits the design

`docs/UI-BRIEF.md` asks for one picture, not a collage: the banner is the only
place a photo belongs. If you skip it entirely the first page still has a
composition (a procedural radial backdrop with the tracked `BLOODBORNE`
wordmark), because the blank case was designed first and the photo second.
