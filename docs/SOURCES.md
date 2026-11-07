# Sources, attribution and reuse

The application combines public election records and community archives. References embedded in individual records are the closest available provenance. The retained commit hashes are in `data/source-manifest.json`. Historical coverage and official-source verification vary.

| Material | Source | Notes |
| --- | --- | --- |
| Election results | [thecont1/india-votes-data](https://github.com/thecont1/india-votes-data) | MIT notice retained |
| Historical election archive | [skthewimp/elections](https://github.com/skthewimp/elections) | MIT notice retained |
| Constituency boundaries | [skthewimp/india-constituency-maps](https://github.com/skthewimp/india-constituency-maps) | Underlying layers have their own terms; see boundary attribution |
| 2019 Lok Sabha archive | [r21meghashyam/indian-election-2019-dataset](https://github.com/r21meghashyam/indian-election-2019-dataset) | Reference retained in national snapshot records |
| 2023 assembly archive | [azadecon/assembly_elections_2023](https://github.com/azadecon/assembly_elections_2023) | GPL-3.0 notice retained |
| Kerala archive | [nvlsr/kerala-2026](https://github.com/nvlsr/kerala-2026) | MIT notice retained; includes selected historical context |
| Kerala 2021 statistical report | [Chief Electoral Officer, Kerala](https://www.ceo.kerala.gov.in/pdf/GE-2021/statistical_report.pdf) | Official results and turnout reference |
| Official results and statistical reports | [Election Commission of India](https://www.eci.gov.in/) | Individual result source URLs retained where available |
| Party ideology | [Global Party Survey](https://www.globalpartysurvey.org/download-data) | Historical 2019 survey values only where matched; editorial descriptions are distinct |
| Party platforms and descriptions | Individual links in `guide` records | Descriptions are selective summaries, not complete policy inventories |

## Licences

The combined application is licensed under GPL-3.0; see the root `LICENSE`. This does not override the licences or rights attached to upstream data. Original notices are retained under `licenses/`, including the archive's GPL-3.0 and MIT notices. The `elections2023` commit refers to `azadecon/assembly_elections_2023`; its GPL-3.0 notice is retained.

Boundary compilation code being MIT does not make all underlying geometry MIT. DataMeet assembly boundaries are attributed under [CC BY 2.5 India](https://creativecommons.org/licenses/by/2.5/in/). Other geometry references and qualifications are recorded in `licenses/boundary-attribution.txt` and the upstream map repository. Shapes are projected/displayed and overview paths simplified; no claim of official survey accuracy is made.

Kerala demographic estimates retain their Census/SHRUG aggregation note and district-urban fallback flags. The repository does not claim ownership of the underlying Census or SHRUG data, or include raw restricted downloads. Review upstream terms before extracting contextual datasets for separate redistribution. Attribution is not a substitute for any applicable permission.

The candidate-affidavit attribution notice is retained because some dormant code references that research. The underlying unfinished candidate-review records and manifesto assessments are not included in this public release.
