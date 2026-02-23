# Logistics Efficiency Recovery: Solving the 77.5% Delay Gap

### The Problem: Operational Bottlenecks
The organization faced a critical challenge in "Last Mile" delivery operations. Shipments were experiencing an average delay of **10.8 minutes**, with over **67% of deliveries** failing to meet on-time targets. Without a clear diagnostic tool, the leadership team could not identify whether the root cause was specific carriers, geographic routes, or external weather factors.

---

### The Solution: Interactive Diagnostic Hub
A data solution was developed to isolate the drivers of these delays. By integrating multiple data streams, this tool allows stakeholders to visualize risk and make data-driven decisions on carrier selection and route planning.


*to view the insights, please click on the link below*\
https://github.com/AdityaBawane22/Data-Analytics-Portfolio/releases/download/v1.0.0/Logistics-Optimization.mp4

---

### Business Impact & Recovery
The implementation of this analysis provided a clear path to optimization. By applying the recommended strategic shifts, the following results were achieved:

| Business Metric | Original State (The Problem) | Optimized State (The Solution) | Total Recovery |
| :--- | :--- | :--- | :--- |
| **Average Delivery Delay** | 10.8 Minutes | 2.4 Minutes | **77.5% Faster** |
| **On-Time Success Rate** | 32.9% | 53.5% | **20.6% Increase** |
| **Root Cause Visibility** | 0% | 100% | **Fully Resolved** |

---

### The Technical Strategy
The solution was delivered through a three-stage technical process:

### 1. Data Consolidation
Using **Python**, separate datasets for weather, routes, and carriers were merged to create a **Centralized Source**.


This sample represents the integrated data where route number, carrier type, weather condition, delay, and delivery status are aligned for analysis.

| route_number | carrier_type | weather_condition | delay_min | delivery_status |
| :--- | :--- | :--- | :--- | :--- |
| **19** | 3PL Partner | Storm | 19.7 | **Delayed** |
| **2** | 3PL Partner | Clear | -8.6 | **Early** |
| **11** | Bike | Rain | 12.2 | **Delayed** |
| **13** | Bike | Clear | 1.6 | **Delayed** |
| **15** | Van | Clear | -9.8 | **Early** |

---

### 2. Risk Isolation
Statistical analysis was performed to identify high-correlation patterns—specifically isolating how **weather conditions** and **routes** interact with different **carriers** to drive delivery delays. This allows for predictive modeling of logistics bottlenecks.

---

### 3. Visual Intelligence

A **Power BI** interface was built to transform these complex findings into a simple, clickable dashboard.

---

### Repository Assets
* **`Presentation.pbix`**: The final interactive solution used for diagnostic analysis.
* **`Data Analysis.ipynb`**: The technical backend used for data cleaning and pattern finding.
* **`/Documentation`**: Strategic notes regarding the business logic and recovery plan.

---

### Core Competencies
* **Business Intelligence:** Turning complex data into clear actionable strategy.
* **Technical Tools:** Power BI, Python, Excel, DAX.
* **Problem Solving:** Root Cause Analysis (RCA) and Strategic Planning.
