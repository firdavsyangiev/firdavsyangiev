# Ray's GitHub profile

Prepared for **firdavsyangiev**. The starting workspace contained no Git repository, origin remote, or README; the username was supplied by you and verified against GitHub's public API.

## Enable the profile

1. Create the public repository **firdavsyangiev/firdavsyangiev** on GitHub. Copy the contents of this package to its root, including the hidden `.github` directory. Commit them to the default branch.
2. In **Settings → Actions → General**, enable GitHub Actions and allow `actions/checkout` and `Platane/snk`. The workflow explicitly requests `contents: write`; organization policy must permit it. No personal access token or manually created secret is required.
3. Open **Actions → Refresh profile and contribution snake → Run workflow** on the default branch. The initial push of the workflow also triggers a run.
4. A successful run creates the `output` branch with both snake SVGs, then updates the README's picture URLs and the two stats cards on the default branch.
5. Keep branch rules compatible with this bot's pushes to the default and output branches. If rules require pull requests, those rules must be accommodated before automatic updates can be saved; this workflow does not bypass branch protection.

The daily schedule is **00:23 UTC / 09:23 Seoul time**. Scheduled Actions can be delayed, and GitHub can disable schedules on public repositories after 60 days without activity. Manual dispatch remains available after re-enabling the workflow.

## Replace social placeholders

Edit the Connect line in `README.md`:

- LinkedIn: replace `LinkedIn: YOUR_LINKEDIN_URL` with `[LinkedIn](https://your-linkedin-url)`.
- Instagram: replace `Instagram: YOUR_INSTAGRAM_URL` with `[Instagram](https://your-instagram-url)`.
- Email: replace `Email: YOUR_EMAIL` with `[Email](mailto:you@example.com)`.
- Portfolio: replace `Portfolio: YOUR_PORTFOLIO_URL` with `[Portfolio](https://your-portfolio-url)`.

The actual placeholders are inline code in the README so they never resolve to broken links. Replace the complete text including its backticks when inserting the Markdown links. GitHub already points to `https://github.com/firdavsyangiev`.

## Data and maintenance

`USERNAME` in `scripts/update_profile.py` is the shared data source for the API updater and snake action. The workflow's repository guard intentionally restricts execution to `firdavsyangiev/firdavsyangiev`.

- **Commits:** GitHub GraphQL `contributionsCollection.totalCommitContributions`, covering its default past-year interval. This is not a lifetime total or every commit in every branch. It follows GitHub's contribution attribution and visibility rules. The local initial card says **Unavailable**, because GraphQL requires authentication. The workflow uses its automatic `GITHUB_TOKEN`.
- **Followers and public repositories:** current counts from GitHub's user API.
- **Stars:** total stars on publicly visible, owned, non-fork repositories.
- **Languages:** byte counts summed across all public, owned, non-fork repositories, with pagination. The top five percentages use the total across all languages, so the displayed five need not sum to 100%. This measures repository composition, not developer skill or personally authored code.
- **Snake:** Platane/snk reads this account's actual contribution graph; no illustrative cells or fabricated counts are included. Light/dark variants use GitHub greens. The pending asset remains visible until the first successful publish, avoiding broken future URLs.
- **Projects:** all public repositories are checked daily. The requested `space-rental-platform`, `real-estate-platform`, and `portfolio` names were absent at initial verification. Descriptions remain visible without fake links. Links appear automatically when those public repositories exist. To change project names, descriptions, or technologies, edit `PROJECTS` in the Python script; the marked README project block is generated.

Only marked project/snake blocks and generated stats cards are rewritten. Manual edits elsewhere in the README are preserved. An API error fails the update before writing those files, retaining prior valid data. Dates on the cards indicate freshness. Stats may reflect API visibility limits; no private repository token is requested.

Run a local public-data update with `python3 scripts/update_profile.py` (Python 3.10+). Without `GITHUB_TOKEN`, commit data is unavailable. The updater has no third-party Python dependencies. Network/API limits can cause a run to fail; inspect the Actions log and rerun. The action dependencies are pinned to the verified v4 checkout and v3 snk commit SHAs.

## Rendering and verification

The design uses supported Markdown/HTML and self-contained SVG images. Desktop has a subtle mountain banner; a smaller-screen `<picture>` source keeps the hero readable. Technology tiles wrap naturally, stats cards wrap/scale, and projects use a single column. The SVG artwork stays dark in both themes; only the snake switches its palette.

GitHub controls the surrounding page, fonts, heading rules, link colors, and image sizing. A README cannot reproduce the reference's sidebar, full-page black background, or arbitrary CSS dashboard grid. No external stylesheets, scripts, iframes, external SVG fonts, or embedded HTML inside SVGs are used. SVG text has alternative descriptions, but GitHub image rendering does not make text selectable. GitHub caching can delay visible updates.

Completed locally: Markdown parsing and HTML nesting, every local SVG/image reference, XML parsing, YAML syntax, workflow permissions and pinned actions, Python syntax, empty-data and missing-marker behavior, project link selection, public account/repository API checks, and desktop/mobile preview inspection. Live authenticated GraphQL and the complete hosted workflow require the first Actions run. Output branch URLs intentionally do not activate before publication. The local preview approximates GitHub rendering; it is not a screenshot of an uploaded profile.

Brand paths are from [Simple Icons v16](https://github.com/simple-icons/simple-icons/tree/16.0.0), distributed under [CC0](https://github.com/simple-icons/simple-icons/blob/16.0.0/LICENSE.md). AWS uses a plain typographic label. Brand names and marks belong to their owners.

References: [Platane/snk](https://github.com/Platane/snk), [GitHub profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme), [workflow token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token), [scheduled workflow behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [GitHub GraphQL user contributions](https://docs.github.com/en/graphql/reference/users).
