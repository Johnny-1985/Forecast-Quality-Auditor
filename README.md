# Forecast Quality Auditor

**Status: 🚧 Phase 1 (MVP) complete.**

**Upload any forecast-vs-actual file. Get a quality score computed by algorithm — not guessed by an AI.**

> The numbers are math. The interpretation is optional, and only runs when you ask for it.

---

## Why this exists

Most "AI forecasting" demos ask a language model to eyeball a number and pronounce it good or bad. That's backwards. Forecast accuracy is arithmetic — WMAPE, bias, and outlier detection are well-defined statistics that don't need an LLM to compute, and shouldn't be left to one to "judge."

This tool draws a hard line: **all scoring is deterministic**, computed in the browser with plain JavaScript. An AI is only invoked if you explicitly click "Explain with AI" — and even then, it only interprets numbers that have already been calculated; it never touches the raw data or the scoring formula.

## What it does

1. Upload a `.xlsx`, `.xls`, or `.csv` file — any column names, any industry. Nothing is uploaded to a server; parsing happens entirely in your browser.
2. Map your columns (Period, Forecast, Actual) from a dropdown built from your file's actual headers.
3. Get an instant **Forecast Quality Score (0-100)**, broken into three weighted components:

   | Component | Weight | Formula |
   |---|---|---|
   | WMAPE (weighted accuracy) | 60 pts | `max(0, 60 - (WMAPE/30)*60)` |
   | \|Bias\| (systematic over/under-forecast) | 25 pts | `max(0, 25 - (|Bias|/15)*25)` |
   | Outlier ratio (IQR method on % error) | 15 pts | `max(0, 15 - (ratio/0.2)*15)` |

   The formula is shown, not hidden — an approver can check the math themselves.
4. See exactly which periods were flagged as outliers, and why (IQR bounds on the percentage-error distribution).
5. Optionally click **Explain with AI** to get a plain-language interpretation of what the numbers mean and 2-3 concrete recommendations — grounded in the specific figures, not generic advice.

## Try it with the included sample

`sample-data/sample_forecast_actual.csv` is 24 months of synthetic monthly demand with a mild built-in over-forecasting bias and three deliberately planted outlier months. Running it through the tool correctly identifies all three outliers and lands on a score of ~63 ("Fair") — a realistic result for a forecast that's accurate on average but has a few uncontrolled misses.

## Why WMAPE over MAPE as the primary metric

MAPE blows up (or becomes undefined) when actuals are near zero — a real problem for slow-moving or intermittent-demand items. WMAPE weights errors by volume, so it stays meaningful even with sparse data, and is the metric most demand-planning teams actually use in practice.

## Tech stack

- Single HTML file, no build step, no backend
- [SheetJS](https://sheetjs.com) (via cdnjs) for parsing `.xlsx`/`.xls`/`.csv` client-side
- Plain JavaScript for all statistics (WMAPE, MAPE, MPE/bias, IQR outlier detection, weighted scoring)
- Anthropic API (`claude-sonnet-4-6`), called only on demand, for the optional narrative interpretation

## Roadmap

| Phase | Scope |
|---|---|
| **Phase 1 (this repo)** | WMAPE / Bias / Outlier detection, quality score with transparent formula, on-demand AI narrative |
| **Phase 2** | Missing-data detection, seasonality/trend diagnostics, intermittent-demand handling |
| **Phase 3** | Batch mode for multiple products/columns at once, exportable audit report (PDF) |

---

*This tool does not store, transmit, or log any uploaded data. All file parsing and statistical computation happen locally in the browser.*
