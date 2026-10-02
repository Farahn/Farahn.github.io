# Dr Farah Nadeem: personal website

Everything needed to put the site online and keep it current.

## What is in this folder

- `index.html`: the website, a single self-contained file
- `og-image.png`: the preview image shown when the link is shared on LinkedIn, WhatsApp or X
- `farah-nadeem.jpg`: your portrait, referenced in the site's structured data for search engines
- `llms.txt`: a plain-text summary of your work for AI assistants
- `robots.txt` and `sitemap.xml`: tell search engines and AI crawlers what to read
- `source/build.py` and `source/portrait.webp`: the content, code and photo the site is built from

## Put it online with GitHub Pages (free, about 10 minutes)

1. Sign in to GitHub as Farahn.
2. Create a new public repository named exactly `Farahn.github.io`.
3. Upload `index.html`, `og-image.png`, `farah-nadeem.jpg`, `llms.txt`, `robots.txt` and `sitemap.xml` to the repository root (Add file, then Upload files, then Commit).
4. Open Settings, then Pages. Under Build and deployment, choose Deploy from a branch, select `main` and `/ (root)`, and save.
5. After a few minutes the site is live at https://farahn.github.io/

To use a custom domain instead (for example farahnadeem.com), change `SITE_URL` at the top of `source/build.py`, rebuild, and add the domain under Settings, then Pages.

## Help search engines and AI tools find you

1. Link the site from every profile: LinkedIn (Contact info, then Website), Google Scholar (Homepage field), your GitHub profile, and your LUMS faculty page (ask the SOE web team). These links tell search engines the site is the authoritative page about you.
2. Point your old Google Site (sites.google.com/site/nadeemf0755) to the new site, or unpublish it. It still describes you as a World Bank consultant.
3. Add the site to Google Search Console and Bing Webmaster Tools, verify ownership, and submit `https://farahn.github.io/sitemap.xml`. Bing's index also feeds several AI search tools.
4. Add the website to your ORCID record (Websites and social links). The site already links to your ORCID iD, so the two will point to each other. A Pakistani actress shares your name, and this two-way link between persistent profiles helps search engines and AI assistants keep the two of you apart. The `llms.txt` file also states the distinction.

## Updating the site

All content lives in `source/build.py`: projects, publications, talks, teaching and bio. To add a publication, copy an existing entry in `PUBS`, edit it, then run:

    python3 source/build.py

This regenerates `index.html`, `llms.txt`, `robots.txt` and `sitemap.xml`, so the page and its machine-readable summaries stay in step. Upload the changed files to GitHub. Small text edits can also go straight into `index.html`, but the next build will overwrite them.

To change the photo, replace `source/portrait.webp` (square, about 300 by 300 pixels) and `farah-nadeem.jpg`, then rebuild.

Give a talk a full date (YYYY-MM-DD) and the site marks it Upcoming until the day passes, and shows the next one under your name.

## Accessibility

Letters are set in Atkinson Hyperlegible Next, designed by the Braille Institute for readers with low vision, and numerals in Public Sans. The site was checked with the axe accessibility engine with no violations in light, dark and mobile views. It supports keyboard and screen reader use, respects reduced-motion settings, and its content remains readable without JavaScript.
