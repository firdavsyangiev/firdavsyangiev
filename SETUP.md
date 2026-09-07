# Ray's GitHub profile

Public profile repository: **firdavsyangiev/firdavsyangiev**. The profile uses a responsive monochrome header, contribution snake, technology tiles, current interests, and social links.

## Automation

The workflow `.github/workflows/snake.yml` runs daily at **00:23 UTC / 09:23 Seoul time**, on relevant code pushes, or manually through **Actions → Refresh profile and contribution snake → Run workflow**.

Enable GitHub Actions and allow `actions/checkout` and `Platane/snk`. The workflow requests `contents: write` and uses the automatic `GITHUB_TOKEN`; no personal token is needed. Branch rules must allow the workflow to push to `main` and `output`.

Platane/snk generates both light and dark SVGs from the account's real contribution data and publishes them to `output`. The README selects the appropriate image using `<picture>`. GitHub scheduling and image caching can delay visible updates; inactive public repositories may have their schedules disabled after 60 days.

`USERNAME` in `scripts/update_profile.py` is the shared account source. The Python updater updates only the marked snake block. It does not generate project sections, statistics, or language cards.

## Social links

Replace the Connect placeholders in `README.md`, including their backticks, with Markdown links:

- `YOUR_LINKEDIN_URL`
- `YOUR_INSTAGRAM_URL`
- `YOUR_EMAIL` — use a `mailto:` link.
- `YOUR_PORTFOLIO_URL`

The GitHub link already uses `firdavsyangiev`.

## Rendering

GitHub controls the surrounding page layout. The README uses Markdown, supported HTML, and self-contained SVG assets; it does not depend on CSS, JavaScript, or iframes. Tech Stack and Currently share two border-lined dark panels on desktop, with a stacked mobile variant. Their artwork is in `assets/overview.svg` and `assets/overview-mobile.svg`; the hero also has a mobile variant. Artwork remains dark in both themes; the snake switches palettes.

Brand paths are from [Simple Icons v16](https://github.com/simple-icons/simple-icons/tree/16.0.0), under [CC0](https://github.com/simple-icons/simple-icons/blob/16.0.0/LICENSE.md). AWS uses a typographic label.
