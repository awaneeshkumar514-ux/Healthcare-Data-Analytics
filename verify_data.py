
import pandas as pd

files = [
    "data/hospital_patients.csv",
    "data/cleaned_hospital_patients.csv"
]

for file in files:
    print("\nFILE:", file)

    try:
        df = pd.read_csv(file)

        print("Total Patients:", len(df))
        print("Total Medical Cost:", df["Medical_Cost"].sum())
        print("Average Age:", round(df["Age"].mean(), 2))
        print("Average Stay:", round(df["Length_of_Stay"].mean(), 2))

        print("\nDepartment-wise Cost:")
        print(df.groupby("Department")["Medical_Cost"].sum())

    except Exception as e:
        print("Error:", e)
