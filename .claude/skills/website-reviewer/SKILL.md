---
name: website-reviewer
description: Review a school's page on this ballet-school template after it is built or changed, against everything the user has corrected before (hero cutout, photos, clips, teachers, reviews, contact, layout, copy). Fixes the objective faults itself, proposes options for the matters of taste, and never pushes or merges unasked. Use when a school page is finished or edited, or when the user asks for a review ("trece-l prin reviewer", "e perfect site-ul?").
---

# Website reviewer — ballet-school template

Run this after building or editing a school (`src/schools/<slug>/`). The bar is
the user's own past corrections, collected below; CLAUDE.md still applies in
full and is not repeated here. Every rule exists because the user caught it on
a live page.

## How the user wants this to go

1. **Look first, change nothing.** Open the page in Chrome on the dev server
   (`npx vite --port 5199` inside `scoala_balet_alice/`, then
   `http://localhost:5199/<slug>`). Turn off the scroll-in animation before
   screenshots:
   `.reveal{animation:none!important;opacity:1!important;translate:none!important}`
   and set `document.documentElement.style.scrollBehavior='auto'`.
   Check every section at desktop width **and** phone width.
2. **Report in Romanian**, section by section: what passes, what fails and why.
3. **Objective faults: fix them, then re-check in the browser.** These are the
   ones marked *(fix)* below — overflow, duplicates, misaligned lone cards,
   oversized files, missing alt text, broken links, contact details in the
   wrong place.
4. **Matters of taste: propose, don't decide.** Hero cutout, photos, clips,
   wording. Build a local review page (a throwaway folder served by Vite, e.g.
   `scoala_balet_alice/.preview/`, deleted afterwards) with lettered options
   (A, B, C…) and the current choice marked "acum"; wait for the user's pick
   ("A / 3 / niciuna"). Their link always beats your search.
5. **Commit locally per school branch. Never push or merge to `main` unless
   told** — merging publishes the site.
6. Don't go searching or downloading on your own initiative mid-review; ask
   first. Downloading the photos/clips the user points to is fine.

## Checklist

### Hero
- One dancer (or a tight duo) clearly in a dance pose, cut out cleanly — no
  halo, "spume" (frothy fringe), leftover backdrop or sponsor logos. *(taste)*
- Not a child holding a diploma or trophy at a photo wall; not a blurry video
  frame when a real photo exists; source at least ~600 px tall, ideally
  1000. *(taste)*
- The swash under the name and the motto fit on one screen on phones. *(fix)*

### Photos
- No stock photos (Shutterstock watermarks, "too perfect" studio shots), no
  AI-made posters, no historic photos that aren't the school's. *(fix: remove)*
- No photographer watermarks or app logos (TikTok, "© …", "Photography by …")
  visible — crop them off or drop the photo. *(fix)*
- The same photo never appears twice on the page (courses photo vs gallery).
  *(fix)*
- Gallery: stage photos first, 10–13 of them, varied costumes and shots.
  *(taste)*

### Studio clip (`courses.video`)
- mp4, never WebP or GIF (animated WebP is 5–20× bigger and never pauses).
- Around 20 s, under ~3 MB; 540×960 is plenty. Short reels (≤15 s) can stay
  whole. *(fix: trim/re-encode)*
- No burned-in subtitles, app logos or watermarks in the sharp copy beside the
  cards; landscape clips crop to their centre there. *(taste)*
- `avconvert` bloats Instagram clips and rejects Facebook DASH files: re-encode
  in the browser (canvas → `MediaRecorder`, `video/mp4;codecs=avc1`, ~1.5
  Mbps) instead.

### Teachers
- Names only from the school's own posts, posters or the teacher's profile.
  Unknown → empty `teachers` (section and nav link drop out) and tell the
  user; never guess. *(fix)*
- Photos: the whole photo, children and others included, as long as the
  teacher is recognisable — don't crop to a face. *(taste)*
- Notes: one or two lines, sourced (studies, certifications, roles the school
  or the teacher states). Flag anything inferred, e.g. "founder". *(taste)*
- Three or more teachers share one row on desktop; a lone teacher with no
  photo is centred. *(fix — CSS already handles it; check it renders.)*

### Results and reviews
- No placements published → look for reviews instead: the school's Facebook
  reviews tab and Google Maps. First names only, no dates, the parent's own
  words (light diacritic fixes allowed, cuts marked by choosing whole
  sentences). Skip one-word or descriptive "reviews". *(propose)*
- A single result or review card is centred. *(fix)*

### Contact
- All phone numbers live in the phone card (`contact.phones`, each labelled),
  never in the intro text or other sections. *(fix)*
- Facebook/Instagram/WhatsApp cards only for channels the school actually
  uses; an Instagram account with a couple of posts is left out. *(fix)*
- Nothing overflows a card at any width (long handles break at `.` and `_`).
  *(fix)*
- Address and maps link point to where classes are held.

### Copy
- Romanian with full diacritics (ș ț ă î â), in the school's own words; no
  invented prices, schedules or claims. *(fix: remove; flag what's missing)*
- No eyebrow labels, no filler, no tiny tracked caps, each section only its
  own content (see CLAUDE.md). *(fix)*
- The video's `aria-label` comes from `courses.photoAlt` — make it describe
  the clip when there is one. *(fix)*

### Build, preview, publish
- `npx tsc -b`, `npx oxlint src`, `npm run build` all clean. *(fix)*
- `meta.shareImage` is 1200×630 and `dist/<slug>/index.html` carries its
  `og:` tags. *(fix)*
- After a merge (only when told): watch the Pages deploy, then load the live
  page at `https://ochianiulian.github.io/scoala_balet/<slug>/` and confirm
  the new content is there. The repo was renamed once — check that links
  already sent to clients still resolve.

## Tools

In `scripts/` next to this file:

- `cutout.js` — subject lifting with Apple Vision, no Xcode needed:
  `osascript -l JavaScript scripts/cutout.js in.jpg out.png`
- `prep.py` — resize/compress for the site (`photo`, `cutout`, `share` modes).
- `sheet.py` — labelled contact sheet of many images, for picking.

Run the Python helpers with `python3 -P` (Pillow lives in user
site-packages). Getting media off Facebook/Instagram: full-size image is
`img[data-visualcompletion="media-vc-image"]` on a Facebook photo page;
Instagram reels expose `video_versions` in the page scripts; Facebook reels
list DASH `base_url`s per `video_id` (pick the representation whose duration
matches the player). Chrome blocks repeated script downloads per site — when it
does, hand the URLs to `http://localhost:5199/__dl#…` and download from there.
