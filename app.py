
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Healthcare Analytics",
    page_icon="🏥",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>
.stApp {
    background-color: #F3F6FA;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #17365D;
}

[data-testid="stSidebar"] {
    background-color: #17365D;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DCE5EF;
    text-align: center;
}

.metric-label {
    color: #64748B;
    font-size: 14px;
}

.metric-value {
    color: #17365D;
    font-size: 26px;
    font-weight: bold;
}

.section {
    font-size: 23px;
    font-weight: bold;
    color: #17365D;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)


# LOAD DATA
@st.cache_data
def load_data():
    data = pd.read_csv(
        "data/cleaned_hospital_patients.csv"
    )

    data["Admission_Date"] = pd.to_datetime(
        data["Admission_Date"]
    )

    return data


df = load_data()


# SIDEBAR
st.sidebar.title("🏥 Healthcare Analytics")
st.sidebar.write("Hospital Management Dashboard")
st.sidebar.divider()

st.sidebar.subheader("Dashboard Filters")

department = st.sidebar.selectbox(
    "Select Department",
    ["All"] + sorted(df["Department"].dropna().unique().tolist())
)

gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df["Gender"].dropna().unique().tolist())
)

outcome = st.sidebar.selectbox(
    "Select Outcome",
    ["All"] + sorted(df["Outcome"].dropna().unique().tolist())
)

st.sidebar.divider()
st.sidebar.caption("Python | Pandas | Streamlit")


# FILTER DATA
filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[
        filtered_df["Department"] == department
    ]

if gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == gender
    ]

if outcome != "All":
    filtered_df = filtered_df[
        filtered_df["Outcome"] == outcome
    ]


# HEADER
st.title("🏥 Healthcare Data Analytics")
st.caption(
    "Hospital Patient Statistics and Performance Dashboard"
)

st.markdown(
    '<div class="section">Key Performance Indicators</div>',
    unsafe_allow_html=True
)


# KPI CARDS
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-label">Total Patients</div>
    <div class="metric-value">{len(filtered_df)}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-label">Total Medical Cost</div>
    <div class="metric-value">₹{filtered_df['Medical_Cost'].sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    avg_age = filtered_df["Age"].mean()

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-label">Average Age</div>
    <div class="metric-value">{avg_age:.2f} Years</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    avg_stay = filtered_df["Length_of_Stay"].mean()

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-label">Average Stay</div>
    <div class="metric-value">{avg_stay:.2f} Days</div>
    </div>
    """, unsafe_allow_html=True)


# CHART SETTINGS
plt.rcParams["font.size"] = 10


# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "💰 Cost Analysis",
    "👥 Patient Analysis",
    "📋 Patient Records"
])


# OVERVIEW TAB
with tab1:

    st.subheader("Department & Outcome Analysis")

    col1, col2 = st.columns(2)

    with col1:
        dept_data = filtered_df["Department"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 4))

        bars = ax.bar(
            dept_data.index,
            dept_data.values,
            color=["#2874A6", "#17A589", "#F39C12", "#8E44AD"]
        )

        ax.bar_label(bars, padding=3)
        ax.set_title("Patients by Department", fontweight="bold")
        ax.set_ylabel("Number of Patients")
        ax.tick_params(axis="x", rotation=20)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        outcome_data = filtered_df["Outcome"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.pie(
            outcome_data.values,
            labels=outcome_data.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#17A589", "#F39C12"],
            wedgeprops={"width": 0.45, "edgecolor": "white"}
        )

        ax.set_title("Patient Outcome Distribution", fontweight="bold")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Monthly Patient Admissions")

    monthly = (
        filtered_df.groupby(
            filtered_df["Admission_Date"].dt.strftime("%B")
        )["Patient_ID"].count()
    )

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    monthly = monthly.reindex(month_order).dropna()

    fig, ax = plt.subplots(figsize=(11, 4))

    ax.plot(
        monthly.index,
        monthly.values,
        marker="o",
        linewidth=3,
        markersize=9,
        color="#2874A6"
    )

    for x, y in zip(monthly.index, monthly.values):
        ax.annotate(
            str(y),
            (x, y),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center"
        )

    ax.set_title("Monthly Patient Admissions", fontweight="bold")
    ax.set_ylabel("Patients")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# COST ANALYSIS TAB
with tab2:

    st.subheader("💰 Department-wise Medical Cost")

    cost_data = (
        filtered_df.groupby("Department")["Medical_Cost"]
        .sum()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.barh(
        cost_data.index,
        cost_data.values,
        color="#2874A6"
    )

    ax.bar_label(
        bars,
        labels=[f"₹{v:,.0f}" for v in cost_data.values],
        padding=5
    )

    ax.set_title("Medical Cost by Department", fontweight="bold")
    ax.set_xlabel("Medical Cost (₹)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Top 5 Highest Medical Cost Patients")

    top_patients = filtered_df.nlargest(5, "Medical_Cost")

    st.dataframe(
        top_patients[
            ["Patient_ID", "Age", "Department",
             "Medical_Cost", "Outcome"]
        ],
        use_container_width=True,
        hide_index=True
    )

    if not cost_data.empty:
        st.metric(
            "Highest Cost Department",
            cost_data.idxmax(),
            f"₹{cost_data.max():,}"
        )


# PATIENT ANALYSIS TAB
with tab3:

    st.subheader("👥 Patient Demographics")

    col1, col2 = st.columns(2)

    with col1:
        gender_data = filtered_df["Gender"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.pie(
            gender_data.values,
            labels=gender_data.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#2874A6", "#E67E22"],
            wedgeprops={"width": 0.45, "edgecolor": "white"}
        )

        ax.set_title("Gender Distribution", fontweight="bold")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        age_group = pd.cut(
            filtered_df["Age"],
            bins=[0, 18, 35, 50, 65, 120],
            labels=["0-18", "19-35", "36-50", "51-65", "65+"]
        )

        age_data = age_group.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(7, 4))

        bars = ax.bar(
            age_data.index.astype(str),
            age_data.values,
            color="#17A589"
        )

        ax.bar_label(bars, padding=3)
        ax.set_title("Patients by Age Group", fontweight="bold")
        ax.set_ylabel("Patients")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Patient Outcome Percentage")

    if not filtered_df.empty:
        percentage = (
            filtered_df["Outcome"].value_counts(normalize=True) * 100
        )

        st.dataframe(
            percentage.round(2).rename("Percentage (%)"),
            use_container_width=True
        )


# PATIENT RECORDS TAB
with tab4:

    st.subheader("📋 Patient Records")

    st.write("Total Records:", len(filtered_df))

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Patient Data",
        data=csv,
        file_name="healthcare_patient_data.csv",
        mime="text/csv"
    )


# FOOTER
st.divider()

st.caption(
    "Healthcare Data Analytics | Python | Pandas | Matplotlib | Streamlit"
)
