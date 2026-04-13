# Westside Retail: Strategic Lifecycle Analysis

## Business Problem Statement
Westside Nagpur is facing a **"Leaky Bucket" syndrome**—a high volume of transactions with a **0% customer return rate**. Currently, 100% of the customer base consists of one-time buyers, which prevents the brand from building long-term loyalty and significantly limits revenue growth potential. 

**The Goal:** To identify the geographic and behavioral factors driving this retention crisis and develop a data-backed strategy to transition from a "transaction-based" model to a "relationship-based" model.

---

## Quantified Business Impact (Projected)
| Metric | Current State | Target State | Business Gain |
| :--- | :--- | :--- | :--- |
| **Total Revenue** | ₹1,498,504 | ₹1,725,982 | **+15.2% Revenue Growth** |
| **Customer Retention** | 0% (Repeat Rate) | 10% (Repeat Rate) | **10% Loyalty Lift** |
| **Transaction Value** | 51.5% (Below Avg) | 42.0% (Below Avg) | **9.5% Upsell Success** |
| **Store Consistency** | High Variance (Sadar) | Standardized Ops | **Brand Reliability** |

---

## Key Results & Analyst Insights
* **Isolated Location Failure:** Identified **Sadar** as the primary underperformer with a **-₹67.16 performance gap** compared to the city average.
* **Service Inconsistency:** Discovered that **Sadar** has the highest spending volatility (Std Dev: ₹623), suggesting unstandardized customer experiences.
* **Statistical Validation:** Ran A/B test simulations confirming that the proposed 10% loyalty lift is **Statistically Significant** (P-Value: 6.03e-08).
* **Data Reliability:** Audit results are backed by a **99.9% Confidence Level**, ensuring findings are systemic and not due to random chance.

---

## Project Flow
1.  **Exploratory Data Analysis (EDA):** Profiled Statistical DNA (Mean, Median, Skewness) to understand spending distributions.
2.  **Root Cause Analysis:** Used measures of dispersion (Std Dev) and Performance Gaps to isolate geographic inefficiencies.
3.  **Statistical Modeling:** Applied bootstrapping and A/B testing to project financial impact and validate strategy trust scores.
4.  **Data Visualization:** Developed an interactive 3-page Power BI Dashboard to communicate findings to stakeholders.

---

## Data Flow
1.  **Ingestion:** Raw CSV -> Python (Pandas) -> SQLite Database (`database_1.db`) for structured storage.
2.  **Processing:** SQL-based data retrieval and SciPy statistical audits to verify relationship significance (Chi-Square).
3.  **ETL for BI:** Transformation of raw data into "Wide" and "Long" format tables optimized for Power BI visuals.
4.  **Interactive BI Layer:** Dynamic reporting using DAX for real-time performance gap tracking.
