# Nationwide election-data import

Snapshot: 10 November 2026. This extends the Kerala import across the available upstream result bundles and mapping tables. It is **not** a scrape of IndiaVotes, and does not claim to reproduce that site's entire historical or politician-career database. The application atlas and live website are unchanged.

## Available files

All downloads are under [`data/imports/india/`](../data/imports/india/).

| Dataset | Coverage | Files |
| --- | --- | --- |
| Historical assembly bundle | 161,760 source result rows, 119 election IDs, 31 state/UT labels; source years 2009–2026 | `assembly-source.parquet`, `assembly-by-state/*.csv` |
| Separate recent assembly results | 20 source CSVs, 32,563 result rows, source years 2022–2026 | `recent-assembly/*.csv` |
| Lok Sabha 2024 | 8,902 source rows, 543 constituencies | `lok-sabha-2024-source.csv` (semicolon-delimited) |
| Lok Sabha 2019 | 8,570 retained atlas result rows, 543 constituencies | `lok-sabha-2019-atlas-export.csv` |
| Assembly → parliamentary references | 4,109 pre-2008 rows and 4,119 post-2008 rows | `ac_pc_pre2008.csv`, `ac_pc_post2008.csv` |
| Coverage and validation | Per-source election and state coverage, matching/skipped counts, mapping coverage | `assembly-coverage.csv`, `validation.json` |
| Unresolved issues | Vote-value issues and differences against the current atlas | `historical-vote-issues.json`, `assembly-winner-discrepancies.json` |
| Provenance | Pinned URLs, SHA-256 hashes, output sizes and hashes | `manifest.json` |

**Do not add the two assembly row counts together as unique candidates.** Recent files overlap the historical bundle. Rows include NOTA where present. The source's 119 election IDs are not a verified count of general elections; some source-year/date cohorts require review. Missing source elections are not filled with fabricated records.

The 2019 national CSV is an export of the already-retained application data, not a fresh independent download or new validation. Earlier national elections and pre-2009 assembly cycles are not supplied by these bundles. By-election histories, candidate biographies, legislative activity and manifesto assessments are not newly imported here.

## Quality findings

The historical source contains:

- **542 missing** total-vote values.
- **2,703 fractional** total-vote values, retained verbatim and flagged because counts should be integers.
- **12,091 rows with missing election month**, requiring date/election-type review before using a source-year cohort for comparisons.

These categories may overlap. We do not round fractional counts, turn missing values into zero, or silently relabel uncertain election dates. The raw parquet and CSVs preserve the source. `historical-vote-issues.json` identifies affected rows; missing-month counts are reported by source election in `validation.json`.

For overlapping atlas snapshots, the audit compares winner vote totals by state, election year and constituency number, excluding unresolved historical seats/date cohorts. It performs **8,729 source-seat comparisons**, of which **8,466 match and 263 differ**. Overlapping source bundles mean these are not necessarily distinct constituency-election comparisons. All differences remain unresolved and no displayed values have been replaced. Matching counts do not establish candidate identity, party/coalition accuracy, runner-up accuracy or complete rosters. These are consistency checks against our atlas, not an independent official-results audit; the atlas already uses some of the same upstream sources.

For Lok Sabha 2024, state/constituency names match all 543 atlas seats after explicit normalisation of NCT of Delhi and Jammu and Kashmir labels. The 542 contested-seat winner totals match; Surat is preserved as the source's nonnumeric unopposed entry, not interpreted as zero votes. Source constituency IDs are retained but not used for that join because their numbering is known to be unreliable.

## Mapping limitations

Pre- and post-2008 tables describe different constituency systems. They are parent-seat reference tables, **not** cross-boundary population crosswalks. Never join eras using constituency numbers alone. Recent Assam and J&K delimitation require their own mappings; the all-India post-2008 table is not automatically appropriate for every 2024–2026 seat.

The Kerala pre-2008 table's 140 ACs resolve to only 18 distinct parent IDs and remain quarantined pending independent review. Nationwide counts in `validation.json` are descriptive and are not a certification of every mapping. This import does not automatically use these mappings to change the UI.

## Provenance and reuse

- Historical results: [skthewimp/elections](https://github.com/skthewimp/elections), commit `1fe9a2e00d3ca451e95be46e753d71af0ede78fe`. Original source fields remain in the exports. Retain `licenses/results-archive-MIT.txt` and applicable upstream terms for ECI/TCPD-derived material.
- Recent assembly and 2024 national archive: [thecont1/india-votes-data](https://github.com/thecont1/india-votes-data), commit `7d8cf637f83d223b178d11659103a1f52647367a`. Retain `licenses/india-votes-MIT.txt`.
- Mappings: [skthewimp/india-constituency-maps](https://github.com/skthewimp/india-constituency-maps), commit `efceae39d3922f04fc5ea91106b7b316bf8ddf8f`. Retain `licenses/map-tools-MIT.txt`, boundary attribution and underlying third-party terms.
- 2019 national export: retained atlas provenance and limitations remain applicable. No additional raw mirror or new licence grant is asserted.

Archive-level licences do not override third-party underlying rights. No new candidate-scoring, manifesto or private working datasets are included.

## Reproduce and check

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements-import.txt
.venv/bin/python scripts/import_india.py
python3 scripts/check_india_import.py
```

The importer uses `curl` with normal certificate verification to fetch the pinned files into ignored `.cache/india-import/`. Every input must match the committed SHA-256 lock; recent source files also match their upstream Git blob hashes. Outputs retain separate source families rather than silently deduplicating inconsistent records. The offline checker verifies output hashes, record counts, state partitions and reconciliation accounting. It does not require pandas or a network connection.
