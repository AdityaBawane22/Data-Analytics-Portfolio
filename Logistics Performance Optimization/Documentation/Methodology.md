# Project Methodology: Logistics Performance Optimization

This document outlines the end-to-end technical workflow used to transform raw delivery data into an actionable carrier recommendation engine and executive dashboard.

---

### 1. Data Integration & Centralization
The foundation of the project involved merging three disparate datasets using **Python (Pandas)**:
* **Logistics Data:** Delivery IDs, carrier types, and actual vs. promised arrival times.
* **Route Data:** Geographic identifiers and specific route regions.
* **Weather Data:** Environmental conditions (Storm, Rain, Fog, Clear) mapped to delivery timestamps.

**Key Outcome:** A centralized "Source of Truth" dataframe containing 24 variables, enabling multi-dimensional correlation analysis.

---

### 2. Operational Logic & Recommendation Engine
To isolate risk, the project utilized a custom recommendation algorithm developed in the Jupyter Notebook:
* **Performance Grouping:** Data was grouped by `route_name` and `weather_condition`.
* **Optimization Metric:** The **Mean Delay (minutes)** was calculated for every carrier type within these groups.
* **Selection Logic:** The system identifies the "Optimal Carrier" by applying the `.idxmin()` function to the delay averages, ensuring the carrier with the lowest historical delay is selected for each specific scenario.

#### Optimal Carrier Matrix (Sample)
| route_name | Clear | Rain | Storm |
| :--- | :--- | :--- | :--- |
| **Route_1** | Truck | 3PL Partner | Van |
| **Route_2** | Truck | Bike | Truck |
| **Route_3** | Van | 3PL Partner | Bike |

---

### 3. Impact Validation (Before vs. After)
Before finalizing the dashboard, a validation script was run to quantify potential improvements:
* **Baseline Calculation:** Average delays under the existing "random/fixed" carrier strategy.
* **Projected Performance:** Simulated delays using the new "Optimal Carrier" selections.
* **Result:** The analysis demonstrated a significant reduction in global delivery delays (calculated as a percentage reduction), proving the viability of the logic.

---

### 4. Visual Intelligence & BI Implementation
The final stage involved porting the processed results into **Power BI** to create a management-ready interface:
* **DAX Integration:** Custom measures were used to track real-time KPIs and delay variances.
* **Interactive Filtering:** Slicers allow viewers to filter by region and weather to see which carrier should be dispatched.
* **User Experience:** Complex statistical correlations were converted into simple visual alerts (Red/Green indicators) for non-technical stakeholders.
