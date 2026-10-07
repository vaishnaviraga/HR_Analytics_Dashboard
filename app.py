import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="HR Analytics Dashboard", page_icon="📊", layout="wide")

DATA_FILE = os.path.join(os.path.dirname(__file__), "HR_Analytics_Final_Cleaned.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    # Normalize duplicate/variant column names used in the cleaned dataset.
    if "Age Group" in df.columns and "AgeGroup" not in df.columns:
        df["AgeGroup"] = df["Age Group"]
    if "Salary Slab" in df.columns and "SalarySlab" not in df.columns:
        df["SalarySlab"] = df["Salary Slab"]
    if "Attrition Count" not in df.columns:
        df["Attrition Count"] = (df["Attrition"].astype(str).str.upper() == "YES").astype(int)
    for col in ["Age", "MonthlyIncome", "YearsAtCompany", "Attrition Count", "JobSatisfaction"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

df = load_data()

# ---------- Header ----------
st.markdown("""
<style>
.block-container {padding-top: 1rem; padding-bottom: 1rem;}
.dashboard-title {
    background: #17365D;
    color: white;
    padding: 18px 24px;
    border-radius: 8px;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 12px;
}
.kpi {background:#F4F6F8;border-radius:8px;padding:12px 8px;text-align:center;border:1px solid #D9DEE5;}
.kpi-label {font-weight:700;font-size:15px;color:#333;}
.kpi-value {font-size:26px;font-weight:800;color:#17365D;margin-top:5px;}
</style>
<div class="dashboard-title">HR ANALYTICS DASHBOARD</div>
""", unsafe_allow_html=True)

# ---------- Filter ----------
st.markdown("### Department Filter")
departments = ["All"] + sorted(df["Department"].dropna().astype(str).unique().tolist())
selected_department = st.selectbox("Department", departments, label_visibility="collapsed")

filtered = df.copy()
if selected_department != "All":
    filtered = filtered[filtered["Department"].astype(str) == selected_department]

# ---------- KPIs ----------
employees = filtered["EmpID"].nunique() if "EmpID" in filtered else len(filtered)
attrition = int(filtered["Attrition Count"].sum())
attrition_rate = (attrition / len(filtered) * 100) if len(filtered) else 0
avg_age = filtered["Age"].mean() if len(filtered) else 0
avg_salary = filtered["MonthlyIncome"].mean() if len(filtered) else 0
avg_years = filtered["YearsAtCompany"].mean() if len(filtered) else 0

kpis = [
    ("Employee Count", f"{employees:,}"),
    ("Attrition", f"{attrition:,}"),
    ("Attrition Rate", f"{attrition_rate:.2f}%"),
    ("Average Age", f"{avg_age:.1f}"),
    ("Avg Salary", f"₹{avg_salary:,.0f}"),
    ("Years At Company", f"{avg_years:.1f}"),
]
cols = st.columns(6)
for col, (label, value) in zip(cols, kpis):
    col.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>', unsafe_allow_html=True)

st.write("")

# ---------- Middle row ----------
left, mid, right = st.columns([1.2, 1.1, 0.8])

with left:
    edu = filtered.groupby("EducationField", dropna=False)["Attrition Count"].sum().reset_index()
    edu = edu.sort_values("Attrition Count", ascending=False)
    fig = px.pie(edu, names="EducationField", values="Attrition Count", hole=0.48,
                 title="Attrition by Education Field")
    fig.update_traces(textposition="inside", textinfo="label+value+percent")
    fig.update_layout(height=330, margin=dict(l=10,r=10,t=55,b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with mid:
    age = filtered.groupby("AgeGroup", dropna=False)["Attrition Count"].sum().reset_index()
    age_order = ["18-25", "26-35", "36-45", "46-55", "56-65"]
    age["order"] = age["AgeGroup"].map({v:i for i,v in enumerate(age_order)}).fillna(99)
    age = age.sort_values("order")
    fig = px.bar(age, x="AgeGroup", y="Attrition Count", title="Attrition by Age Group")
    fig.update_layout(height=330, margin=dict(l=10,r=10,t=55,b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    gender = filtered.groupby("Gender", dropna=False)["Attrition Count"].sum().reset_index()
    fig = px.treemap(gender, path=["Gender"], values="Attrition Count", title="Attrition by Gender")
    fig.update_layout(height=330, margin=dict(l=5,r=5,t=55,b=5))
    st.plotly_chart(fig, use_container_width=True)

# ---------- Job satisfaction table ----------
left2, right2 = st.columns([1.1, 1.0])
with left2:
    sat = filtered.groupby(["JobRole", "JobSatisfaction"], dropna=False)["Attrition Count"].sum().reset_index()
    sat = sat.sort_values("Attrition Count", ascending=False)
    pivot = sat.pivot_table(index="JobRole", columns="JobSatisfaction", values="Attrition Count", aggfunc="sum", fill_value=0)
    pivot.columns = [f"Satisfaction {int(c)}" for c in pivot.columns]
    pivot["Total Attrition"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("Total Attrition", ascending=False).reset_index()
    st.subheader("Job Role & Job Satisfaction")
    st.dataframe(pivot, use_container_width=True, hide_index=True, height=320)

with right2:
    role = filtered.groupby("JobRole", dropna=False)["Attrition Count"].sum().reset_index()
    role = role.sort_values("Attrition Count", ascending=True)
    fig = px.bar(role, x="Attrition Count", y="JobRole", orientation="h", title="Attrition by Job Role")
    fig.update_layout(height=360, margin=dict(l=10,r=10,t=55,b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------- Bottom row ----------
a, b = st.columns([1.0, 1.25])
with a:
    salary = filtered.groupby("SalarySlab", dropna=False)["Attrition Count"].sum().reset_index()
    salary_order = ["Up to 5K", "5K-10K", "10K-15K", "15K+"]
    salary["order"] = salary["SalarySlab"].map({v:i for i,v in enumerate(salary_order)}).fillna(99)
    salary = salary.sort_values("order")
    fig = px.bar(salary, x="SalarySlab", y="Attrition Count", title="Attrition by Salary Slab")
    fig.update_layout(height=330, margin=dict(l=10,r=10,t=55,b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with b:
    years = filtered.groupby("YearsAtCompany", dropna=False)["Attrition Count"].sum().reset_index()
    years = years.sort_values("YearsAtCompany")
    fig = px.area(years, x="YearsAtCompany", y="Attrition Count", title="Attrition by Years At Company")
    fig.update_layout(height=330, margin=dict(l=10,r=10,t=55,b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.caption("HR Analytics Dashboard | Python + Streamlit + Pandas + Plotly")
