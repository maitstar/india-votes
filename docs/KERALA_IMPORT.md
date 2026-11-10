# Kerala upstream data import

Retrieved 10 November 2026. This import uses the public upstream archives, **not a scrape of IndiaVotes**. It is a research/source layer; the application atlas and live site are not overwritten by this import.

## Downloaded results

[CSV](../data/imports/kerala/candidate-results.csv) · [Validation report](../data/imports/kerala/validation.json) · [Pinned sources and checksums](../data/imports/kerala/manifest.json)

| Election | Assembly seats | Result rows | Winner vote totals matching our atlas | Differing |
| --- | ---: | ---: | ---: | ---: |
| 2011 | 140 | 971 | 137 | 3 |
| 2016 | 140 | 1,343 | 133 | 7 |
| 2021 | 140 | 1,096 | 140 | 0 |
| 2026 | 140 | 1,023 | 140 | 0 |

Rows include NOTA where retained by the source; they are not counts of human candidates. An equal winner vote count is a limited consistency check, not independent official verification. Candidate identities, full-roster completeness, runner-up totals and coalition labels were not comprehensively adjudicated here. The upstream archive includes no pre-2011 Kerala election results in this bundle.

The ten discrepancies are preserved in the validation report. Neither source has been declared correct solely because it is newer. The next step is checking official statistical reports for each disputed record before updating the UI. Source election-month metadata is also retained without endorsement; do not treat it as a verified polling date.

## Constituency mappings

- [Post-2008 CSV](../data/imports/kerala/assembly-to-parliament-post2008.csv): 140 distinct Assembly seats and 20 distinct parent Lok Sabha seats. Ponnani Assembly seat 48 maps to Ponnani parliamentary seat 7.
- [Pre-2008 CSV](../data/imports/kerala/assembly-to-parliament-pre2008.csv): 140 distinct Assembly seats but only 18 distinct parent parliamentary IDs. **Quarantined pending independent review; not integrated into the application.**

These tables associate an Assembly seat with a parent parliamentary seat within an era. They do **not** translate old constituencies to new constituencies across delimitation. For example, Assembly number 48 is Malampuzha in the pre-2008 table and Ponnani in the post-2008 table. Joining eras by number would produce a false match. The post-2008 mapping is a reference table, not a certification of every geographic boundary.

## Source and licence

Results: [skthewimp/elections](https://github.com/skthewimp/elections), commit `1fe9a2e00d3ca451e95be46e753d71af0ede78fe`. The archive carries an MIT licence; retain `licenses/results-archive-MIT.txt`. Row-level `source_kind`, `source_dataset`, `source_url` and other provenance fields remain in the CSV. Missing source URLs remain blank rather than invented. This archive combines historical ECI tables, TCPD-derived records and ECI live scrapes; check applicable upstream terms for separate redistribution.

Mappings: [skthewimp/india-constituency-maps](https://github.com/skthewimp/india-constituency-maps), commit `efceae39d3922f04fc5ea91106b7b316bf8ddf8f`. Retain `licenses/map-tools-MIT.txt` and `licenses/boundary-attribution.txt`; underlying third-party material retains its own terms. No additional shapefiles or restricted raw datasets are included in this import.

## Reproduce

The app build still needs only Python's standard library. This separate import additionally needs pandas and pyarrow:

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements-import.txt
.venv/bin/python scripts/import_kerala.py
python3 scripts/check_kerala_import.py
```

The importer downloads three pinned files into ignored `.cache/kerala-import/`, verifies their SHA-256 hashes, selects Kerala, exports CSVs and compares winner vote totals with `data/atlas.json`. Output manifests record source and output checksums. The national 4 MB results parquet is cached locally, not republished in this repository.
