# Sample RAG Queries - Legal + Financial Corpus

Corpus: `borrower_quarterly_financials.csv` (60 records) + `master_credit_facility_agreement.pdf`.

| ID | Type | Difficulty | Query |
|---|---|---|---|
| Q01 | csv_only | easy | What was Halcyon Precision Manufacturing's revenue in Q4-2024? |
| Q02 | csv_only | easy | Which borrower carried the highest total debt at the end of Q2-2026, and how much? |
| Q03 | csv_only | medium | What was Lumen Ridge Software's average quarterly EBITDA across fiscal 2025? |
| Q04 | pdf_only | easy | Which law governs the credit agreement and where must disputes be heard? |
| Q05 | pdf_only | easy | What interest rate applies after an Event of Default? |
| Q06 | pdf_only | medium | What are the limits on a borrower's equity cure right? |
| Q07 | pdf_only | easy | What is the maximum leverage ratio covenant for Tidewater Logistics, and how is leverage defined? |
| Q08 | cross_document | medium | Which borrowers breached their Maximum Leverage Ratio covenant, and in which quarters? |
| Q09 | cross_document | hard | Is Tidewater Logistics currently in an Event of Default? Explain. |
| Q10 | cross_document | medium | Did Castlepoint Health Services ever breach a financial covenant, and what happened? |
| Q11 | cross_document | hard | Did any borrower trigger the margin step-up without actually breaching its leverage covenant? |
| Q12 | cross_document | hard | Which compliance certificates were delivered late, and what are the consequences? |
| Q13 | cross_document | medium | Estimate Halcyon's quarterly commitment fee for Q2-2026 based on its drawn balance at quarter end. |
| Q14 | cross_document | hard | Ironwood Energy's Q2-2026 leverage exceeds its covenant. Can it use an equity cure, and roughly how much debt reduction is needed? |
| Q15 | cross_document | medium | Did any borrower exceed the capital expenditure limit in any quarter? |
| Q16 | cross_document | medium | If 3-month Term SOFR is 4.30%, what interest rate does Verdant Grove Foods pay on its revolver? |
| Q17 | cross_document | medium | What was overall facility utilization at the end of Q2-2026? |
| Q18 | pdf_only | medium | Does Tidewater's default allow the bank to accelerate Halcyon's loans? |
| Q19 | unanswerable | easy | What was Ironwood Energy's dividend payout ratio in 2025? |

---

## Q01. What was Halcyon Precision Manufacturing's revenue in Q4-2024?
**Type:** csv_only | **Difficulty:** easy

**Expected answer:** $235.58 million.

**Sources:** borrower_quarterly_financials.csv: FIN-004

## Q02. Which borrower carried the highest total debt at the end of Q2-2026, and how much?
**Type:** csv_only | **Difficulty:** easy

**Expected answer:** Ironwood Energy Partners LLC (B06) with $945.06 million.

**Sources:** borrower_quarterly_financials.csv: Q2-2026 rows

## Q03. What was Lumen Ridge Software's average quarterly EBITDA across fiscal 2025?
**Type:** csv_only | **Difficulty:** medium

**Expected answer:** $16.70 million (average of Q1-Q4 2025: 16.36, 17.46, 16.11, 16.88).

**Sources:** borrower_quarterly_financials.csv: FIN-035, FIN-036, FIN-037, FIN-038

## Q04. Which law governs the credit agreement and where must disputes be heard?
**Type:** pdf_only | **Difficulty:** easy

**Expected answer:** New York law (Section 8.1). Exclusive jurisdiction of state and federal courts in Manhattan, New York City; jury trial is waived (Section 8.2).

**Sources:** master_credit_facility_agreement.pdf: Sections 8.1, 8.2

## Q05. What interest rate applies after an Event of Default?
**Type:** pdf_only | **Difficulty:** easy

**Expected answer:** The otherwise-applicable rate (Term SOFR + Applicable Margin) plus 2.00% per annum, for the defaulting Borrower (Section 2.4).

**Sources:** master_credit_facility_agreement.pdf: Section 2.4, 2.3

## Q06. What are the limits on a borrower's equity cure right?
**Type:** pdf_only | **Difficulty:** medium

**Expected answer:** A cash equity contribution within 15 Business Days after the Compliance Certificate is due. It cannot be used in two consecutive Fiscal Quarters or more than twice over the agreement term. Cure amounts are ignored when setting the margin under Section 2.5 (Section 6.3).

**Sources:** master_credit_facility_agreement.pdf: Section 6.3

## Q07. What is the maximum leverage ratio covenant for Tidewater Logistics, and how is leverage defined?
**Type:** pdf_only | **Difficulty:** easy

**Expected answer:** 4.00x (Schedule 2). Leverage Ratio = Total Debt / Annualized EBITDA, where Annualized EBITDA = latest quarter EBITDA x 4 (Sections 1.6, 1.7).

**Sources:** master_credit_facility_agreement.pdf: Schedule 2, Sections 1.6-1.7

## Q08. Which borrowers breached their Maximum Leverage Ratio covenant, and in which quarters?
**Type:** cross_document | **Difficulty:** medium

**Expected answer:** Tidewater Logistics Holdings Corp. (B03) in Q3-2025: 4.74x vs 4.00x max; Tidewater Logistics Holdings Corp. (B03) in Q4-2025: 4.83x vs 4.00x max; Ironwood Energy Partners LLC (B06) in Q2-2026: 4.51x vs 4.25x max.

**Sources:** borrower_quarterly_financials.csv: FIN-027, FIN-028, FIN-060; master_credit_facility_agreement.pdf: Schedule 2, Section 6.1

## Q09. Is Tidewater Logistics currently in an Event of Default? Explain.
**Type:** cross_document | **Difficulty:** hard

**Expected answer:** Yes. It breached the leverage covenant (max 4.00x) in Q3-2025 (4.74x) and Q4-2025 (4.83x). Interest coverage stayed just above its 2.50x minimum (2.63x and 2.51x), so only leverage was breached. An equity cure cannot be used in two consecutive quarters (Section 6.3(a)), and Schedule 3 lists no cure for Tidewater, so the Q4-2025 breach at minimum is uncured. That is a Financial Covenant Default (Section 7.2), and the Agent may terminate the Commitment and accelerate the loans (Section 7.7). Default interest of +2.00% applies (Section 2.4). Other borrowers are not affected (Section 7.7).

**Sources:** borrower_quarterly_financials.csv: FIN-027, FIN-028; master_credit_facility_agreement.pdf: Sections 6.3, 7.2, 7.7, 2.4, Schedules 2-3

## Q10. Did Castlepoint Health Services ever breach a financial covenant, and what happened?
**Type:** cross_document | **Difficulty:** medium

**Expected answer:** Yes. In Q1-2025 its interest coverage was 2.69x against a 2.75x minimum (Schedule 2). Per Schedule 3, it was cured by a $4.10 million equity contribution accepted on 2025-05-29. That is one of its two permitted cures (Section 6.3), so no Event of Default occurred.

**Sources:** borrower_quarterly_financials.csv: FIN-045; master_credit_facility_agreement.pdf: Schedules 2-3, Section 6.3

## Q11. Did any borrower trigger the margin step-up without actually breaching its leverage covenant?
**Type:** cross_document | **Difficulty:** hard

**Expected answer:** Yes. Ironwood Energy Partners LLC (B06) had leverage of 3.87x in Q1-2024. That is above the 90% step-up threshold of 3.825x but below its 4.25x maximum. Under Section 2.5, its margin rose from 3.00% to 3.50% starting the next quarter (Q2-2024).

**Sources:** borrower_quarterly_financials.csv: FIN-051; master_credit_facility_agreement.pdf: Section 2.5, Schedules 1-2

## Q12. Which compliance certificates were delivered late, and what are the consequences?
**Type:** cross_document | **Difficulty:** hard

**Expected answer:** Certificates are due within 45 days of quarter end (Section 5.1). Verdant Grove Foods LLC (B02) Q4-2024: submitted 2025-02-27, 58 days after quarter end (13 days late) -> beyond the 10-day grace period, so a Reporting Event of Default (Section 7.3); Lumen Ridge Software Inc. (B04) Q3-2025: submitted 2025-11-20, 51 days after quarter end (6 days late) -> within the 10-day grace period, a single 'Late Delivery', not an Event of Default.

**Sources:** borrower_quarterly_financials.csv: FIN-014, FIN-037; master_credit_facility_agreement.pdf: Sections 5.1, 7.3

## Q13. Estimate Halcyon's quarterly commitment fee for Q2-2026 based on its drawn balance at quarter end.
**Type:** cross_document | **Difficulty:** medium

**Expected answer:** Commitment $150m (Schedule 1) - drawn $71.00m = $79.00m undrawn. x 0.35% / 4 = approx. $69.1 thousand (Section 2.6). This assumes the quarter-end balance stands in for the average daily balance.

**Sources:** borrower_quarterly_financials.csv: FIN-010; master_credit_facility_agreement.pdf: Section 2.6, Schedule 1

## Q14. Ironwood Energy's Q2-2026 leverage exceeds its covenant. Can it use an equity cure, and roughly how much debt reduction is needed?
**Type:** cross_document | **Difficulty:** hard

**Expected answer:** Leverage is 4.51x vs a 4.25x max. Ironwood has no prior cures (Schedule 3) and did not breach in Q1-2026, so a cure is available (Section 6.3). To comply: Total Debt <= 4.25 x ($52.35m x 4) = $889.95m. So roughly $55.11m of debt reduction or equivalent cure is needed vs $945.06m current debt.

**Sources:** borrower_quarterly_financials.csv: FIN-060; master_credit_facility_agreement.pdf: Sections 1.6-1.7, 6.1, 6.3, Schedules 2-3

## Q15. Did any borrower exceed the capital expenditure limit in any quarter?
**Type:** cross_document | **Difficulty:** medium

**Expected answer:** No. The limit is 8% of quarterly revenue (Section 6.4). The highest ratio was Lumen Ridge Software Inc. in Q2-2024 at 7.00%.

**Sources:** borrower_quarterly_financials.csv: all rows (capex_usd_m / revenue_usd_m); master_credit_facility_agreement.pdf: Section 6.4

## Q16. If 3-month Term SOFR is 4.30%, what interest rate does Verdant Grove Foods pay on its revolver?
**Type:** cross_document | **Difficulty:** medium

**Expected answer:** 6.30% per annum = 4.30% SOFR + 2.00% Applicable Margin (Schedule 1, Section 2.3). Its leverage never exceeded 90% of its 3.25x max, so no step-up applies. Interest is calculated on a 360-day year.

**Sources:** master_credit_facility_agreement.pdf: Section 2.3, Schedule 1; borrower_quarterly_financials.csv: B02 rows

## Q17. What was overall facility utilization at the end of Q2-2026?
**Type:** cross_document | **Difficulty:** medium

**Expected answer:** Total drawn $588.57m out of $885m total commitments (Schedule 1) = 66.5% utilization.

**Sources:** borrower_quarterly_financials.csv: Q2-2026 rows; master_credit_facility_agreement.pdf: Schedule 1

## Q18. Does Tidewater's default allow the bank to accelerate Halcyon's loans?
**Type:** pdf_only | **Difficulty:** medium

**Expected answer:** No. Commitments are several, not joint (Section 2.1). An Event of Default for one Borrower is not an Event of Default for any other Borrower (Section 7.7).

**Sources:** master_credit_facility_agreement.pdf: Sections 2.1, 7.7

## Q19. What was Ironwood Energy's dividend payout ratio in 2025?
**Type:** unanswerable | **Difficulty:** easy

**Expected answer:** Not answerable. Neither document contains dividend data; the system should say so rather than guess.

**Sources:** none
