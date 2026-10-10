# Saudi Aviation Analytics | تحليلات الطيران السعودي

An interactive Streamlit dashboard exploring Saudi airport air traffic from 2020–2025, built with SQL, Python, Pandas and Plotly.

## Setup
1. Place `air_traffic.sqlite` in the repository root next to `app.py`.
2. On Streamlit Community Cloud select this repository, `main` branch, and entry point `app.py`.
3. Or run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features
- National passenger and flight-movement indicators
- Airport rankings, shares and year-over-year comparisons
- Monthly analytics with interactive filters
- Data-coverage and quality review
- CSV export of report tables

## Source and methodology
Compiled from publicly published Saudi General Authority of Civil Aviation air-traffic files covering 2020–2025. Source files vary by year: 2022 contains annual data, while other selected years have monthly detail. Use caution when comparing national totals across changing source coverage or airport activity. Flight movements are not unique round trips, and passengers per movement is not seat load factor.

## Data file
`air_traffic.sqlite` (about 12 MB) contains the `air_traffic` table and must be added separately to GitHub if absent.
