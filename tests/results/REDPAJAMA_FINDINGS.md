# Copyright Audit: RedPajama-Data-1T

## I found 79 copyrighted sources in a "Clean" open dataset using Project Spark

**Audit Date:** 2026-02-13  
**Audit ID:** 568e08e5  
**Tool:** Project Spark Compliance Auditor  

---

## Summary

| Metric | Count |
|--------|-------|
| Total URLs Scanned | 204 |
| 🔴 High Risk | 79 (38.7%) |
| 🟡 Medium Risk | 52 |
| 🟢 Low Risk | 45 |
| ⚪ Unknown / Needs Review | 28 |

---

## High-Risk Sources Found

These sources are from publishers **actively suing AI companies** or with **strict copyright enforcement**:

| Domain | Publisher | Reason | URLs Found |
|--------|-----------|--------|------------|
| `nytimes.com` | The New York Times | Active AI litigation (NYT v. OpenAI) | 11 |
| `bbc.com` | BBC | Public broadcaster, Crown Copyright restrictions | 9 |
| `cnn.com` | CNN / Warner Bros. Discovery | Major news publisher | 5 |
| `washingtonpost.com` | The Washington Post | Major news publisher, restrictive TOS | 5 |
| `theguardian.com` | Guardian Media Group | Major news publisher | 4 |
| `bloomberg.com` | Bloomberg L.P. | Financial data, premium content | 4 |
| `forbes.com` | Forbes Media | Premium business content | 4 |
| `reuters.com` | Reuters / Thomson Reuters | Wire service, strict licensing | 3 |
| `wsj.com` | The Wall Street Journal / Dow Jones | Paywalled premium content | 3 |
| `nature.com` | Springer Nature | Academic publisher, paywalled content | 3 |
| `ft.com` | Financial Times / Nikkei | Paywalled premium financial content | 3 |
| `latimes.com` | Los Angeles Times | Major news publisher | 3 |
| `penguin.com` | Penguin Random House | Book publisher, full copyright | 2 |
| `economist.com` | The Economist | Premium publisher, strict licensing | 2 |
| `theatlantic.com` | The Atlantic | Premium publisher | 2 |
| `wired.com` | Condé Nast | Premium magazine content | 2 |
| `chicagotribune.com` | Chicago Tribune / Tribune Publishing | Major news publisher | 2 |
| `springer.com` | Springer Nature | Academic publisher, paywalled content | 2 |
| `time.com` | TIME / Salesforce | Premium magazine content | 2 |
| `usatoday.com` | USA Today / Gannett | Major news publisher | 2 |
| `newyorker.com` | Condé Nast | Premium magazine content | 2 |
| `sciencedirect.com` | Elsevier | Academic publisher, strict copyright | 2 |
| `harpercollins.com` | HarperCollins | Book publisher, full copyright | 1 |
| `simonandschuster.com` | Simon & Schuster | Book publisher, full copyright | 1 |

## Medium-Risk Sources

These sources have **Terms of Service restrictions** or require **attribution**:

| Domain | Publisher | Reason | URLs Found |
|--------|-----------|--------|------------|
| `reddit.com` | Reddit Inc. | User-generated, TOS restrictions, API licensing | 14 |
| `medium.com` | Medium / A Medium Corporation | Mixed licensing, some paywalled | 11 |
| `blogspot.com` | Google / Blogger | User-generated, mixed licensing | 8 |
| `stackoverflow.com` | Stack Exchange | CC BY-SA license, attribution required | 6 |
| `wordpress.com` | Automattic | User-generated, mixed licensing | 5 |
| `quora.com` | Quora Inc. | User-generated, TOS prohibits scraping | 4 |
| `stackexchange.com` | Stack Exchange | CC BY-SA license, attribution required | 4 |

---

## Key Finding

> **64.2% of URLs** in this "open" dataset point to copyrighted content from publishers actively suing AI companies or enforcing strict Terms of Service.

RedPajama-Data-1T is widely used as a "clean, open" alternative to proprietary training datasets. Our audit found that **79 out of 204 sampled URLs** (38.7%) come from high-risk publishers — including The New York Times (active litigation against OpenAI), The Wall Street Journal, Bloomberg, and major book publishers.

An additional **52 URLs** come from medium-risk sources like Reddit (which now charges for API access to training data) and Stack Overflow (which requires CC BY-SA attribution).

## Implications

1. **For AI companies:** "Open" does not mean "copyright-free." Companies training on RedPajama face the same legal exposure as those using proprietary scraped data.
2. **For compliance teams:** The upcoming CLEAR Act will require disclosure of training data sources. Datasets like RedPajama contain sources that would trigger regulatory scrutiny.
3. **For researchers:** Benchmarks and models trained on RedPajama inherit these copyright risks. Downstream users may face liability.

## Methodology

Project Spark's Compliance Auditor performs **source provenance analysis**:

1. **Domain Extraction:** Each URL in the training manifest is parsed to extract the source domain.
2. **Risk Classification:** Domains are matched against a curated database of 31+ publishers with known copyright positions, litigation history, and Terms of Service restrictions.
3. **Risk Scoring:** Sources are classified as High (active litigation/strict copyright), Medium (TOS restrictions/attribution required), Low (permissive licenses), or Unknown.
4. **Reporting:** Detailed audit reports with per-source risk assessment and compliance recommendations.

This approach catches copyright risk that **text-matching tools miss** — because it tracks *where data came from*, not what it looks like after processing.
