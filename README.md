# India Votes

**An interactive atlas of Indian state and national elections.**

[Explore the live site](https://india-votes-opal.vercel.app/) · [Methodology](docs/METHODOLOGY.md) · [Data dictionary](docs/DATA_DICTIONARY.md) · [Sources and licences](docs/SOURCES.md) · [Coverage manifest](data/coverage.json)

India Votes helps readers explore who won, how close the contest was, and how results changed across elections. It brings constituency maps, party and coalition views, historical comparisons and a plain-language party directory into one static website.

This is an independent, exploratory portfolio project. It is not an official election service, a live count, a forecast or a validated measure of political performance. The archive records election outcomes, not current legislative membership.

## What you can explore

- Lok Sabha elections in 2019 and 2024, with 543 constituency outcomes per election.
- State/UT assembly results for 31 elected assemblies, with historical coverage varying by state.
- Party and election-specific coalition totals, winners, runners-up and vote margins.
- Historical vote-share changes and seats that changed hands, where comparisons are supported.
- Searchable constituency results, selected seat details and CSV exports.
- Major-party profiles, regional context and explanations for readers unfamiliar with Indian politics.
- A light default theme, an optional dark theme and layouts for desktop and mobile.

The current UI still has rough edges: swing shows a selected party at a time, and the margin palette and transfer controls need refinement. Candidate reviews, manifesto assessments and Strategy Lab are hidden. Unfinished candidate and manifesto datasets are excluded from this public repository; dormant interface code is retained. The public repository is a curated, reproducible portfolio snapshot, not a backup of every private working file or an exact copy of every hidden asset on the deployed site.

## The data-science problem

The difficult part is making comparisons meaningful across inconsistent party labels, election-specific alliances and changing constituency boundaries. This repository exposes the derived data, source references, coverage metadata and rendering code so those decisions can be inspected. It does not claim that every source record or geographic join has been independently validated.

Useful questions include: Where are contests consistently close? Which seats changed winning party or coalition? How does an election look under party versus alliance grouping? A difference in constituency vote share does **not** identify individual voter movement or explain its cause.

## Run locally

Requires Python 3 and Node.js 22 or later (for the development tests). The website itself needs no backend, API key or paid map service.

```sh
npm ci
python3 build.py
npm test
python3 -m http.server 8765 --directory dist
```

Open **http://localhost:8765**. Serve the site over HTTP; opening the HTML directly cannot reliably load its JSON assets.

The build uses Python's standard library. It converts the retained atlas into an HTML entry point and election-specific JSON files loaded on demand. `dist/` is generated and is not committed. The data is already local, so building does not depend on upstream election websites being online.

## Deploy on Vercel

Import this repository in Vercel. The included configuration runs `python3 build.py` and publishes `dist/`. No environment variables are required. This repository does not automatically replace or connect to the existing production deployment.

## Repository guide

| Path | Purpose |
| --- | --- |
| `data/atlas.json` | Derived results, geometry, party metadata and selected contextual data |
| `data/coverage.json` | Election-level seat, geometry and partial-roster coverage |
| `data/source-manifest.json` | Retained upstream commits and atlas checksum |
| `app.js`, `redesign.js`, `clarity.js` | Application and interface layers |
| `template.html`, `*.css` | Page structure and appearance |
| `build.py` | Static-site builder |
| `docs/` | Methodology, data definitions, sources and limitations |
| `licenses/` | Retained upstream attribution and licence notices |

## Validation and next steps

Automated checks exercise national geometry loading, election navigation, themes, seat selection, comparisons and hidden-page routing. They test application behaviour; they do not prove source accuracy. Priorities are a systematic official-results audit, quantified geographic-match coverage, clearer swing/transfer displays and a complete raw-source ingestion pipeline. See [methodology](docs/METHODOLOGY.md).

## Licence and attribution

The combined application is distributed under [GPL-3.0](LICENSE). Upstream datasets, maps and other material retain their own applicable terms; GPL is not a blanket relicensing of third-party data. See [sources](docs/SOURCES.md) and [retained notices](licenses/). This project is independent of the Election Commission of India and the upstream data maintainers.

## Kerala source import — 10 November 2026

[Download the imported results and mappings](data/imports/kerala/) · [Import methodology and discrepancies](docs/KERALA_IMPORT.md)

A pinned upstream import now provides 4,433 result rows across Kerala’s 2011, 2016, 2021 and 2026 Assembly elections, plus Assembly–Lok Sabha mapping tables. All 140 seats are represented per election. Ten older winner-vote discrepancies against the application atlas are recorded for review; the import does not overwrite displayed results. The pre-2008 mapping is quarantined pending review.

## Nationwide source import — 10 November 2026

[Download the national/state import](data/imports/india/) · [Coverage, quality findings and reproduction](docs/INDIA_IMPORT.md)

The repository now includes the complete available upstream assembly bundle (161,760 rows; 119 source election IDs; 31 state/UT labels), 20 separate recent assembly files, national 2024 source results, a clearly labelled export of retained national 2019 results, and nationwide era-specific seat mappings. Source families overlap and contain unresolved records; they are retained separately from the live atlas. This is not a complete historical archive of every Indian election.
