# Methodology and limitations

Snapshot: 6 November 2026. This describes the retained implementation, not a claim that every comparison has been audited.

## Unit of analysis

An observation is a candidate result within a constituency and election. State Assembly and Lok Sabha elections are different contests. Constituency identifiers are local to their chamber/state and election; they are not universal longitudinal identifiers. Results describe the election date, not subsequent party switches or current membership.

## Winners, margins and shares

Candidates are retained in source order, generally descending recorded votes; the interface takes the first non-NOTA candidate as winner. This ordering is an assumption that should be checked in a full source audit. The winning margin is the difference between winner and runner-up votes. Percentage-point margins divide that difference by recorded candidate votes, including NOTA where present. A partial candidate roster limits the denominator and is flagged. Votes are counts; shares and changes in shares are percentages and percentage points respectively.

Comparisons use matched prior-election records and suppress some unsupported comparisons. A party not contesting under its own label, an alliance reshuffle or an incomplete roster can change what a share means. Apparent changes should not be interpreted as individual voter switching.

## Parties and coalitions

Party labels are standardised for display. Coalition membership is stored with the election and candidate, rather than assigned from a single timeless national alliance table. Some memberships are editorial mappings supported by the references in the data. Party splits, independents, renamed parties and different state-level arrangements require care. A systematic coalition audit remains outstanding.

The party directory mixes historical survey measurements with labelled editorial descriptions. An unmeasured party has no invented survey coordinate. An ideological position is not an objective measure of quality or a claim that all policies lie on one axis.

## Geography

Geometry comes from community archives and their upstream sources, with constituency identifiers reconciled to results. Country overview outlines are simplified for performance; constituency polygons remain in the retained display format. Some elections reuse geometry from another snapshot. Direct geometry counts in `data/coverage.json` are not final rendered coverage: `mapRef` and `mapReuseYear` can supply additional shapes.

Redistricting, especially Assam and Jammu and Kashmir, limits historical comparability. A visual match is not a validated population crosswalk. The project does not claim that its maps are official survey boundaries.

## Contextual data

Selected Kerala religion comparisons use Census 2011 community-archive estimates aggregated to assembly boundaries. Some constituencies use district-urban proxies. These are resident estimates, not current surveys or voter characteristics. The provenance note and fallback flag are retained in the data. The full upstream aggregation pipeline is not included here. No individual religion or caste is inferred from election results.

Selected Kerala national-versus-state comparisons use assembly-segment data; postal votes are excluded where national postal ballots could not be assigned to assembly segments. This does not make the two electoral contests equivalent.

Kerala 2021 turnout was reconciled using official elector denominators. Turnout is suppressed in other views without a verified denominator. Missing values are not zero.

## Reproducibility

`python3 build.py` rebuilds the application from `data/atlas.json`. Source references and upstream commit hashes are retained. This is reproducibility from a derived archive, not a complete raw-download-to-final-data pipeline. The repository does not yet supply every acquisition, cleaning and manual reconciliation step.

The coverage manifest reports record counts, not an accuracy certificate. UI tests verify loading and interactions, not the truth of each election result. A full audit should compare winners, vote totals, coalition mappings and geometry joins with official election reports and publish discrepancies by election.

## Scope of the public release

Unfinished candidate-background reviews, composite scores and manifesto assessments are excluded. Their dormant interface code is not an endorsed research output. Strategy Lab is hidden and is not a forecast. None of these pages should be treated as findings from this release.

## Next research steps

1. Audit results and mapping coverage against official statistical reports.
2. Publish acquisition scripts, transformation logs and comparison exceptions.
3. Define a focused substantive question and report descriptive findings with denominators.
4. Test comprehension of margin, swing and transfer encodings with users.
5. Keep descriptive electoral patterns separate from causal and predictive claims.
