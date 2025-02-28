LogInsight
=========

Personal CLI tool to analyze local log files and extract quick insights: error rates, top messages, time buckets, and simple anomaly hints. Solo, hobby cadence; code is intentionally lightweight and does not require running during development.

Goals
- Provide a small, hackable CLI for grepping patterns from logs and summarizing counts over time.
- Keep zero-runtime requirements beyond Python 3.9+ (no third-party deps).
- Favor incremental, readable code that can grow.

Planned features
- Parse lines with optional timestamp prefix.
- Basic counters: errors/warnings/info, top messages, top sources.
- Time-bucket histogram (minute/hour/day).
- Simple heuristics for spikes (z-score-ish with rolling mean).
- JSON and plain-text output.

Usage (planned)
- `python -m loginsight scan path/to/log --pattern ERROR`
- `python -m loginsight summary path/to/log --bucket hour --spikes`

Notes
- This repo mimics a real solo workflow with incremental commits.
- See `scripts/sample.log` to try commands locally without setup.
