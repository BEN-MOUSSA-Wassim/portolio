# Portfolio evidence and asset provenance

This file documents the source and public-safety status of the evidence used by the portfolio. It is intentionally kept with the site so future updates do not blur the line between authentic captures and illustrative diagrams.

## QoD Tools

The published captures come from the local QoD Tools release material. They show the real desktop application with synthetic data and blanked or redacted paths.

| Published asset | Source file | Evidence type |
| --- | --- | --- |
| `assets/images/qod-control.png` | `commercial_release/12_LINKEDIN_CAMPAIGN/14_VIDEO_PROMO_90S_REPORTING/assets/capture_control.png` | Authentic application capture; inputs redacted |
| `assets/images/qod-result.png` | `commercial_release/12_LINKEDIN_CAMPAIGN/14_VIDEO_PROMO_90S_REPORTING/assets/capture_result.png` | Authentic completed-run capture; output path redacted |
| `assets/images/qod-reporting.png` | `commercial_release/12_LINKEDIN_CAMPAIGN/14_VIDEO_PROMO_90S_REPORTING/assets/reporting_04_erreurs_par_type.png` | Authentic reporting UI; synthetic dataset |
| `assets/images/qod-filtering.png` | `commercial_release/12_LINKEDIN_CAMPAIGN/14_VIDEO_PROMO_90S_REPORTING/assets/reporting_08_filtres_tableau.png` | Authentic reporting UI; synthetic dataset |

The catalogue count and technical descriptions were verified against the current QoD Tools README, tool catalogue, business-rule reference, and test documentation. Conflicting historical automated-test totals were deliberately omitted from the public portfolio.

## QoD Quiz Tounsi

`demos/qod-quiz-tounsi.html` is a copy of the self-contained working application. It has no external scripts, images, APIs, or network calls. The application labels its 57 learning scenarios as fictional and stores progress only in the browser.

## Existing portfolio evidence

The following assets were retained from the previous public portfolio export:

- `wassim-portrait.png` — portrait cutout.
- `wassim-speaking.png` — event/presentation photograph.
- `field-survey.png` — topographic field photograph.
- `remote-sensing-water.png` — legacy Landsat water-detection project visual.
- `photogrammetry-dsm-dtm.png` — DSM/DTM project output (retained for future use, not currently displayed).
- `rando-maamoura.png` — mobile GIS application capture.

## Illustrative elements

The workflow/pipeline and infrastructure-automation diagrams in `index.html` are code-derived diagrams. They explain architecture and are not presented as application screenshots.

## Public-safety notes

- No production telecom dataset is included.
- No customer network identifiers, coordinates, credentials, or private source code are published.
- The previous portfolio's full residential address and phone number are not displayed.
- QoD Tools is described as an engineering release candidate, not as certified or commercially released software.
