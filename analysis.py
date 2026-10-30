
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned_hospital_patients.csv")

print("Total Patients:", len(df))
print("Total Medical Cost:", df["Medical_Cost"].sum())
print("Average Age:", df["Age"].mean())

department_count = df["Department"].value_counts()

plt.figure(figsize=(8, 5))
department_count.plot(kind="bar")
plt.title("Department-wise Patient Count")
plt.xlabel("Department")
plt.ylabel("Number of Patients")
plt.tight_layout()
plt.savefig("department_patients.png")
plt.close()

department_cost = df.groupby("Department")["Medical_Cost"].sum()

plt.figure(figsize=(8, 5))
department_cost.plot(kind="bar")
plt.title("Department-wise Medical Cost")
plt.xlabel("Department")
plt.ylabel("Total Medical Cost")
plt.tight_layout()
plt.savefig("department_cost.png")
plt.close()

print("Analysis completed!")
