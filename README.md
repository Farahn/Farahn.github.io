# Dr Farah Nadeem: personal website

Everything needed to put the site online and keep it current.

## What is in this folder

- `index.html`: the website, a single self-contained file
- `og-image.png`: the preview image shown when the link is shared on LinkedIn, WhatsApp or X
- `farah-nadeem.jpg`: your portrait, referenced in the site's structured data for search engines
- `llms.txt`: a plain-text summary of your work for AI assistants
- `robots.txt` and `sitemap.xml`: tell search engines and AI crawlers what to read
- `source/build.py` and `source/portrait.webp`: the content, code and photo the site is built from


## Updating the site

All content lives in `source/build.py`: projects, publications, talks, teaching and bio. To add a publication, copy an existing entry in `PUBS`, edit it, then run:

    python3 source/build.py

This regenerates `index.html`, `llms.txt`, `robots.txt` and `sitemap.xml`, so the page and its machine-readable summaries stay in step. Upload the changed files to GitHub. Small text edits can also go straight into `index.html`, but the next build will overwrite them.

To change the photo, replace `source/portrait.webp` (square, about 300 by 300 pixels) and `farah-nadeem.jpg`, then rebuild.

Give a talk a full date (YYYY-MM-DD) and the site marks it Upcoming until the day passes, and shows the next one under your name.

## Accessibility

Letters are set in Atkinson Hyperlegible Next, designed by the Braille Institute for readers with low vision, and numerals in Public Sans. The site was checked with the axe accessibility engine with no violations in light, dark and mobile views. It supports keyboard and screen reader use, respects reduced-motion settings, and its content remains readable without JavaScript.
