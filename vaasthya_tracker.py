import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Vaasthya",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.hero{
    background:linear-gradient(135deg,#0f172a,#1e293b);
    padding:30px;
    border-radius:16px;
    color:white;
}

.info{
    background:#f8fafc;
    padding:20px;
    border-radius:12px;
    border:1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# DATABASE
# ==================================================

conn = sqlite3.connect(
    "vaasthya_expansion.db",
    check_same_thread=False
)

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS responses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    state TEXT,
    user_type TEXT,
    problem TEXT,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <h1>Vaasthya</h1>

    Help us identify the next cities where trusted
    property verification and real estate services
    are needed most.
    
</div>
""", unsafe_allow_html=True)

# ==================================================
# LAYOUT
# ==================================================

left, right = st.columns([2,1])

# ==================================================
# FORM SECTION
# ==================================================

with left:

    st.subheader("📍 Request Vaasthya In Your City")

    with st.form("expansion_form"):

        city = st.text_input("City")

        state = st.text_input("State")

        user_type = st.selectbox(
            "You Are",
            [
                "Buyer",
                "Seller",
                "Property Owner",
                "Tenant",
                "Real Estate Agent",
                "Just Interested"
            ]
        )

        problem = st.selectbox(
            "Biggest Challenge In Your City",
            [
                "Property Verification",
                "High Brokerage",
                "Fake Listings",
                "Finding Genuine Buyers",
                "Finding Genuine Tenants",
                "Legal Documentation",
                "Other"
            ]
        )

        feedback = st.text_area(
            "Additional Feedback (Optional)",
            placeholder="Tell us what would make you use Vaasthya..."
        )

        submit = st.form_submit_button(
            "🚀 Submit Interest"
        )

        if submit:

            if city and state:

                c.execute(
                    """
                    INSERT INTO responses
                    (city,state,user_type,problem,feedback)
                    VALUES(?,?,?,?,?)
                    """,
                    (
                        city,
                        state,
                        user_type,
                        problem,
                        feedback
                    )
                )

                conn.commit()

                st.success(
                    "✅ Thank you! Your response has been recorded."
                )

            else:
                st.error(
                    "Please enter both City and State."
                )

# ==================================================
# INFO SECTION
# ==================================================

with right:

    st.markdown("""
    <div class="info">

    <h3>🚀 Platform Under Development</h3>

    <p>
    Vaasthya is building a trusted real estate ecosystem
    focused on property verification, transparency,
    and seamless property transactions.
    </p>

    <p>
    Building India's trusted real estate network, driven by community demand. Visit our website to learn more about Vaasthya. 🚀
    </p>

    <p>
    🌐
    <a href="https://www.vaasthya.com" target="_blank">
    www.vaasthya.com
    </a>
    </p>

    <p>
    Thank you for supporting Vaasthya's growth.
    </p>

    </div>
    """, unsafe_allow_html=True)

# ==================================================
# DASHBOARD
# ==================================================

st.divider()

st.subheader("📊 Community Demand Dashboard")

df = pd.read_sql_query(
    "SELECT * FROM responses",
    conn
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Responses",
    len(df)
)

c2.metric(
    "Cities Covered",
    df["city"].nunique() if not df.empty else 0
)

top_city = "N/A"

if not df.empty:
    top_city = df["city"].value_counts().idxmax()

c3.metric(
    "Top Requested City",
    top_city
)

# ==================================================
# ANALYTICS
# ==================================================
if not df.empty:

    st.subheader("🏆 Most Requested Cities")

    city_stats = (
        df.groupby("city")
        .size()
        .reset_index(name="Requests")
        .sort_values(
            "Requests",
            ascending=False
        )
    )

    st.dataframe(
        city_stats,
        use_container_width=True
    )

    # Pie Chart - Cities

    fig, ax = plt.subplots()

    ax.pie(
        city_stats["Requests"],
        labels=city_stats["city"],
        autopct="%1.1f%%"
    )

    ax.set_title("Most Requested Cities")

    st.pyplot(fig)

    # =========================================

    st.subheader("Most Common Problems")

    problem_stats = (
        df.groupby("problem")
        .size()
        .reset_index(name="Mentions")
        .sort_values(
            "Mentions",
            ascending=False
        )
    )

    st.dataframe(
        problem_stats,
        use_container_width=True
    )

    # Pie Chart - Problems

    fig, ax = plt.subplots()

    ax.pie(
        problem_stats["Mentions"],
        labels=problem_stats["problem"],
        autopct="%1.1f%%"
    )

    ax.set_title("Most Common Problems")

    st.pyplot(fig)

    # =========================================

    st.subheader("👥 User Intent")

    user_counts = df["user_type"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        user_counts.values,
        labels=user_counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title("User Intent")

    st.pyplot(fig)

    # =========================================

    st.subheader("💬 Recent Community Feedback")

    feedback_df = df[
        df["feedback"].fillna("").str.strip() != ""
    ][
        ["city", "feedback"]
    ].tail(10)

    if len(feedback_df):

        st.dataframe(
            feedback_df,
            use_container_width=True
        )

    else:

        st.info(
            "No feedback submitted yet."
        )

else:

    st.info(
        "No responses collected yet. Share this page to start collecting demand data."
        )

#----------------------------
#Metric
#----------------------------
if not df.empty:

    st.info(
        f"{len(df)} people have already requested Vaasthya in their cities."
    )

target = 100

progress = min(len(df)/target,1.0)

st.subheader("📈 Expansion Goal Progress")

st.progress(progress)

st.caption(
    f"{len(df)} / {target} responses collected"
)

#------------------------
#Analytics
#------------------------
if not df.empty:

    recommended_city = (
        df["city"]
        .value_counts()
        .idxmax()
    )

    st.success(
        f"🚀 Recommended Next Expansion City: {recommended_city}"
    )

#-----------------------
#Dataframe
#-----------------------
city_stats["Demand Score"] = city_stats["Requests"] * 10

st.subheader("⭐ City Demand Score")

st.dataframe(
    city_stats,
    use_container_width=True
)

#------------------------
#State Wise Demand
#------------------------
st.subheader("🗺️ State Wise Demand")

state_stats = (
    df.groupby("state")
    .size()
    .reset_index(name="Requests")
    .sort_values("Requests", ascending=False)
)

st.dataframe(
    state_stats,
    use_container_width=True
)

#------------------------
#Top 5 Cities
#------------------------
st.subheader("🏆 Top 5 Cities")

st.table(
    city_stats.head(5)
)

#------------------------
#Feedback
#------------------------
search = st.text_input("🔍 Search Feedback")

if search:
    feedback_df = feedback_df[
        feedback_df["feedback"]
        .str.contains(search, case=False, na=False)
    ]

#------------------------
#CSV
#------------------------
csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Responses CSV",
    csv,
    "vaasthya_responses.csv",
    "text/csv"
)
