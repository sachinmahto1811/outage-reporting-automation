# Pan-India Outage Reporting Automation

Sanitized telecom outage-reporting pipeline built with Python, Pandas and Excel output.

## Problem

Operational teams repeatedly need clean open-outage views, ageing buckets and circle-level summaries. Manual filtering and summarization becomes slow and inconsistent when input volume is high.

## Demo flow

1. Load synthetic alarm / TT data
2. Keep open outage records
3. Calculate down-ageing hours
4. Create ageing buckets
5. Deduplicate at site level
6. Build circle-by-ageing summary
7. Export detailed and summary sheets to Excel

## Public-safe note

This repository uses synthetic data and simplified rules. It contains no credentials, client names, internal contacts, mail recipients or production endpoints.
