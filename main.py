import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Set page configuration
st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for enhanced look
st.markdown(
    """
    <style>
    .main {
        background-color: #F5F5F5;
    }
    .sidebar .sidebar-content {
        background-color: #2B3E50;
        color: white;
    }
    h1, h2, h3 {
        color: #2B3E50;
    }
    .stButton>button {
        background-color: #2B3E50;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #FF6F61;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Custom functions
def about_df(df):
    df_sample = df.sample(10)
    size = df.shape[0]
    buffer = io.StringIO()
    df.info(buf=buffer)
    info = buffer.getvalue()
    columns = df.dtypes
    missing_values = df.isnull().sum()
    stats = df.describe(include="all")
    return df_sample, size, info, columns, missing_values, stats

def customer_statistics(df):
    average_age = df.iloc[:, 1].mean()
    average_tenure = df.iloc[:, 3].mean()
    total_spend = df.iloc[:, 9].sum()
    average_support_calls = df.iloc[:, 5].mean()
    churn_rate = df.iloc[:, 11].mean() * 100
    payment_delay_std_dev = df.iloc[:, 6].std()
    statistics = {
        "Average Age": average_age,
        "Average Tenure": average_tenure,
        "Total Spend": total_spend,
        "Average Support Calls": average_support_calls,
        "Churn Rate (%)": churn_rate,
        "Payment Delay Std Dev": payment_delay_std_dev,
    }
    return statistics

def future_insights(df):
    average_monthly_spend = df.iloc[:, 9].mean()
    projected_total_spend_next_year = average_monthly_spend * 12 * len(df)
    churn_rate = df.iloc[:, 11].mean()
    projected_churn_next_year = churn_rate * len(df)
    average_support_calls = df.iloc[:, 5].mean()
    projected_support_calls_increase = average_support_calls * 1.1
    average_payment_delay = df.iloc[:, 6].mean()
    projected_payment_delay_increase = average_payment_delay * 1.05
    standard_and_basic_users = df[
        (df.iloc[:, 7] == "Standard") | (df.iloc[:, 7] == "Basic")
    ]
    projected_upgrades = len(standard_and_basic_users) * 0.15
    average_tenure = df.iloc[:, 3].mean()
    projected_tenure_growth = average_tenure * 1.2
    insights = {
        "Projected Total Spend Next Year": projected_total_spend_next_year,
        "Projected Churn Next Year": projected_churn_next_year,
        "Projected Support Calls Increase": projected_support_calls_increase,
        "Projected Payment Delay Increase": projected_payment_delay_increase,
        "Projected Subscription Upgrades": projected_upgrades,
        "Projected Tenure Growth": projected_tenure_growth,
    }
    return insights

# Dashboard functions (graphs)
def age_distribution_graph(df):
    fig, ax = plt.subplots()
    df["Age"].plot(kind="hist", bins=10, color="skyblue", edgecolor="black", ax=ax)
    ax.set_title("Distribution of Age")
    ax.set_xlabel("Age")
    ax.set_ylabel("Frequency")
    return fig

def avg_total_spend_subscription_type(df):
    fig, ax = plt.subplots()
    df.groupby("Subscription Type")["Total Spend"].mean().plot(
        kind="bar", color="lightgreen", ax=ax
    )
    ax.set_title("Average Total Spend by Subscription Type")
    ax.set_xlabel("Subscription Type")
    ax.set_ylabel("Average Total Spend")
    return fig

def gender_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df["Gender"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_title("Gender Distribution")
    ax.set_ylabel("")
    return fig

def total_spend_distribution_by_contract_length(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby("Contract Length")["Total Spend"].sum().plot(
        kind="pie", autopct="%1.1f%%", colors=["#ff9999", "#66b3ff", "#99ff99"], ax=ax
    )
    ax.set_title("Total Spend Distribution by Contract Length")
    ax.set_ylabel("")
    return fig

def churn_rate_by_gender(df):
    fig, ax = plt.subplots()
    churn_rate_by_gender = df.groupby("Gender")["Churn"].mean() * 100
    churn_rate_by_gender.plot(kind="bar", color="coral", ax=ax)
    ax.set_title("Churn Rate by Gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Churn Rate (%)")
    return fig

def age_distribution_by_gender(df):
    fig, ax = plt.subplots()
    df[df["Gender"] == "Male"]["Age"].plot(
        kind="hist", bins=10, alpha=0.5, color="blue", label="Male", ax=ax
    )
    df[df["Gender"] == "Female"]["Age"].plot(
        kind="hist", bins=10, alpha=0.5, color="red", label="Female", ax=ax
    )
    ax.set_title("Age Distribution by Gender")
    ax.set_xlabel("Age")
    ax.set_ylabel("Frequency")
    ax.legend()
    return fig

# Main dashboard
if __name__ == "__main__":
    st.title("📊 Customer Churn Dashboard")
    st.subheader("Data Analysis and Customer Insights")
    st.write("Unlock the power of data to analyze customer behavior and predict future trends.")

    st.sidebar.title("📋 Options")
    st.sidebar.markdown("---")
    uploaded_file = st.sidebar.file_uploader(
        "📂 Upload a CSV file", type="csv", help="Upload your dataset for analysis."
    )
    st.sidebar.markdown("---")
    st.sidebar.header("💡 Features")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("Data uploaded successfully!")

        if st.sidebar.button("About Dataset"):
            st.subheader("📊 About Dataset")
            df_sample, size, info, columns, missing_values, stats = about_df(df)
            st.write("**Sample Data:**", df_sample)
            st.write("**Dataset Size:**", size)
            st.write("**Dataset Info:**")
            st.text(info)
            st.write("**Columns:**", columns)
            st.write("**Missing Values:**", missing_values)
            st.write("**Statistics:**", stats)

        if st.sidebar.button("Customer Statistics"):
            st.subheader("📈 Customer Statistics")
            stats = customer_statistics(df)
            for key, value in stats.items():
                st.metric(label=key, value=f"{value:.2f}")

        if st.sidebar.button("Future Insights"):
            st.subheader("🔮 Future Insights")
            insights = future_insights(df)
            for key, value in insights.items():
                st.write(f"**{key}:** {round(value, 2)}")

        if st.sidebar.button("Dashboard"):
            st.subheader("📊 Visual Dashboard")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Age Distribution")
                st.pyplot(age_distribution_graph(df))
            with col2:
                st.subheader("Avg Spend by Subscription")
                st.pyplot(avg_total_spend_subscription_type(df))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Gender Distribution")
                st.pyplot(gender_distribution(df))
            with col2:
                st.subheader("Total Spend by Contract")
                st.pyplot(total_spend_distribution_by_contract_length(df))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Churn Rate by Gender")
                st.pyplot(churn_rate_by_gender(df))
            with col2:
                st.subheader("Age Distribution by Gender")
                st.pyplot(age_distribution_by_gender(df))
    else:
        st.info("Please upload a dataset to begin.")
