# Data dictionary

`data/atlas.json` is a derived JSON archive. Optional fields vary across source elections. Consult the individual record before assuming a field is present.

| Root field | Meaning |
| --- | --- |
| `states` | Selected/latest archived snapshot for each elected state/UT assembly |
| `elections` | State code → year → snapshot, or `latestRef` pointing to `states` |
| `national` | Year → Lok Sabha snapshot |
| `partyNames` | Abbreviation → display name |
| `nationalMap` | Country overview region outlines |
| `sources` | Retained upstream commit references |
| `coalitionSources` | References used for coalition mappings |
| `guide` | Editorial party profiles and source links |
| `kerala` | Selected historical religion estimates and national assembly-segment comparisons |
| `candidateReview` | Empty placeholder; unfinished research excluded |
| `manifestos` | Empty array; unfinished assessments excluded |

## Election snapshots

- `code`, `name`, `eci`: archive/display identifiers; codes are not universal cross-dataset keys.
- `year`, `previousYear`: election and comparison year.
- `total`: expected chamber constituency count for that snapshot.
- `seats`: constituency ID → result object.
- `previous`: matched earlier results used in the comparison.
- `previousComparable`: snapshot-level comparability flag; not a guarantee of complete seat-level matching.
- `map`: constituency ID → SVG path coordinates for display.
- `mapRef`, `mapReuseYear`: references to shared geometry.
- `mapNote`, `historyNote`, `sources`: qualifications and source links.
- `coalitionMembers`, `coalitionNote`, `coalitionReviewed`: retained mapping metadata; review is not an independent audit certificate.
- `counts`, `largest`: cached summary fields. Inspect candidate-level data when conducting analysis.

## Constituency results

- `id`, `name`, `region`: local seat identifier, seat label and district/region where supplied.
- `candidates`: result records in source order (normally highest votes first).
- `source`: result provenance URL where available.
- `partialCandidates`: true when the archived roster is incomplete.
- `previousMatched`: whether an earlier seat record was matched for comparison.

## Candidate result records

- `name`: source candidate name; not a verified persistent person identifier.
- `party`: election-time party label.
- `coalition`: election-specific grouping, where supplied.
- `votes`: recorded total votes.
- `evm`, `postal`: components where supplied; absence does not imply zero.
- `NOTA`: a voting option retained among candidate-like result records; not a party or person.

Other source-specific fields remain in the archive. Vote totals and assembly-segment EVM-only comparisons are different denominators.

## Coverage and provenance

`data/coverage.json` contains one row per retained election snapshot, with expected/recorded seats, direct geometry count, geometry reuse references, partial-roster count and available source links. It does not measure every seat-level join or certify accuracy.

`data/source-manifest.json` records retained upstream commits, the public atlas SHA-256 checksum and public-release exclusions. A checksum identifies a version; it does not validate its contents.

## Separate Kerala upstream import

`data/imports/kerala/` contains raw-schema Kerala result CSVs and era-specific seat mappings, plus source/output checksums and a discrepancy report. It is separate from `atlas.json`; see [import methodology](KERALA_IMPORT.md). Blank CSV cells represent missing upstream fields. These imports are not automatically substituted into displayed results.

## Nationwide source import

`data/imports/india/` retains the original historical assembly parquet and equivalent state CSV partitions, recent-source CSVs and national results. `assembly-coverage.csv` is the spreadsheet-friendly coverage index. Input schemas differ: recent assembly totals require adding `evm_votes` and `postal_votes`; the 2024 national source uses semicolon delimiters and an unopposed text entry. Do not coerce unresolved values or append overlapping bundles without reconciliation. See [nationwide import methodology](INDIA_IMPORT.md).
