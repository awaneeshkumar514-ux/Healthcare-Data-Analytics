# Healthcare Data Analytics Dashboard

## Project Overview
Healthcare Data Analytics is a Python-based data analytics project that analyzes hospital patient records and presents important insights through an interactive Streamlit dashboard.

## Technologies Used
- Python
- Pandas
- Matplotlib
- Streamlit

## Project Features
- Hospital patient data analysis
- Data cleaning and preprocessing
- Department-wise patient analysis
- Medical cost analysis
- Gender and patient outcome analysis
- Average patient age and hospital stay
- Interactive dashboard with filters
- CSV data download

## Key Insights
- Total Patients: 15
- Total Medical Cost: ₹337,000
- Average Patient Age: 45.67 years
- Average Length of Stay: 4.47 days
- Discharged Patients: 13
- Transferred Patients: 2
- Highest Medical Cost Department: Neurology

## Project Structure

```text
Healthcare-Data-Analytics/
│
├── data/
│   ├── hospital_patients.csv
│   └── cleaned_hospital_patients.csv
│
├── charts/
│
├── analysis.py
├── app.py
├── verify_data.py
└── README.md
```

## How to Run the Project

1. Clone this repository.
2. Install the required libraries:

```bash
pip install pandas streamlit matplotlib
```

3. Run the dashboard:

```bash
python -m streamlit run app.py
```

4. Open the local URL displayed in your terminal.

## Project Objective
The objective is to analyze hospital patient data and convert raw records into meaningful insights that can support healthcare performance monitoring and decision-making.

## Author
Awaneesh Kumar

