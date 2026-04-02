import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import random

# 1. Page Configuration
st.set_page_config(page_title="The Lagos Hustle Levy", layout="wide", page_icon="🇳🇬")

# 2. Load External CSS
# Make sure your 'assets/style.css' file contains the .persona-box styling
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("CSS file not found. Please ensure 'assets/style.css' exists in your project folder.")

# 3. Data Connection & Name Pool
def load_data():
    conn = sqlite3.connect('data/lagos_commute.db')
    df = pd.read_sql('SELECT * FROM commuter_metrics', conn)
    # Combine hubs for a cleaner Route label
    df['Route'] = df['Home_Hub'] + " ➔ " + df['Work_Hub']
    conn.close()
    return df

nigerian_names = ["Emeka", "Oluwaseun", "Fatima", "Chidi", "Abike", "Tunde", "Ngozi", "Ayo", "Ifeanyi", "Zainab", "Bisi", "Jide"]
df = load_data()

# 4. Sidebar (The Control Room)
st.sidebar.header("🕹️ Control Room")

st.sidebar.markdown("### 🏠 Home Hub")
all_hubs = sorted(df['Home_Hub'].unique().tolist())
select_all_hub = st.sidebar.checkbox("Select All Home Hubs", value=True)
selected_hub = st.sidebar.multiselect("Filter Home:", all_hubs, all_hubs if select_all_hub else [])

st.sidebar.markdown("### 💼 Work Hub")
all_work = sorted(df['Work_Hub'].unique().tolist())
select_all_work = st.sidebar.checkbox("Select All Work Hubs", value=True)
selected_work = st.sidebar.multiselect("Filter Work:", all_work, all_work if select_all_work else [])

st.sidebar.markdown("### 🚗 Transport Mode")
all_modes = df['Mode'].unique().tolist()
select_all_mode = st.sidebar.checkbox("Select All Modes", value=True)
selected_mode = st.sidebar.multiselect("Filter Mode:", all_modes, all_modes if select_all_mode else [])

# Apply Logic Filters
filtered_df = df[
    (df['Home_Hub'].isin(selected_hub)) & 
    (df['Work_Hub'].isin(selected_work)) & 
    (df['Mode'].isin(selected_mode))
]

# 5. Header Section
st.title("🇳🇬 The Lagos Hustle Levy")
st.markdown("""
    **Tracking the cost of the grind.** This index measures the **Total Economic Leakage** from a Lagosian's potential monthly value. 
    ---
""")

# 6. KPI Metrics
if not filtered_df.empty:
    avg_burden = filtered_df['Tax_Percentage_of_Income'].mean()
    avg_cash = filtered_df['Monthly_Cash_Spend'].mean()
    avg_hours = filtered_df['Monthly_Hours_Lost'].mean()

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Wealth Vanishing Monthly</div><div class='metric-value'>{avg_burden:.1f}%</div><div class='metric-sub'>Income Lost to the Road</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Burned on Transport</div><div class='metric-value'>₦{avg_cash:,.0f}</div><div class='metric-sub'>Hard-Earned Cash Spent</div></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Life Stolen by Traffic</div><div class='metric-value'>{avg_hours:.0f} Hours</div><div class='metric-sub'>Time You’ll Never Get Back</div></div>", unsafe_allow_html=True)

    # 7. Visualizations
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Income vs. The Hustle Levy")
        fig_scatter = px.scatter(
            filtered_df, x="Monthly_Income", y="Tax_Percentage_of_Income",
            color="Mode", hover_data=['Route'],
            template="plotly_dark", 
            color_discrete_map={"Danfo": "#FF4B4B", "Private Car": "#00D4FF", "BRT": "#3FB950"},
            labels={"Tax_Percentage_of_Income": "Hustle Levy (%)", "Monthly_Income": "Monthly Salary (₦)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    with c2:
        st.subheader("Which Route Steals the Most Time?")
        route_data = filtered_df.groupby('Route')['Monthly_Hours_Lost'].mean().reset_index()
        fig_bar = px.bar(
            route_data, x="Route", y="Monthly_Hours_Lost",
            template="plotly_dark", color_discrete_sequence=["#FF4B4B"],
            labels={"Monthly_Hours_Lost": "Avg. Monthly Hours Lost"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # 8. IMPACT ANALYSIS (THE HUMAN COST)
    st.markdown("---")
    st.header("👤 Impact Analysis")
    
    persona = filtered_df.sample(1).iloc[0]
    commuter_name = random.choice(nigerian_names)
    
    gross_salary = persona['Monthly_Income']
    total_levy_amount = persona['Total_Commute_Tax'] 
    true_value = gross_salary - total_levy_amount

    # IMPORTANT: The HTML below is flush-left to prevent Streamlit from 
    # interpreting it as an indented code block.
    html_impact = f"""
<div class="persona-box">
<h3>Meet {commuter_name}</h3>
<p><b>{commuter_name}</b> commutes from <b>{persona['Home_Hub']}</b> to <b>{persona['Work_Hub']}</b> using <b>{persona['Mode']}</b>.</p>
<div style="display: flex; justify-content: space-between; margin-top: 20px; gap: 15px;">
<div style="flex: 1; background: #161B22; padding: 15px; border-radius: 8px; border: 1px solid #30363D; text-align: center;">
<span style="color: #8B949E; font-size: 0.8em; text-transform: uppercase;">Gross Monthly Salary</span><br>
<span style="font-size: 1.5em; font-weight: bold; color: #FAFAFA;">₦{gross_salary:,.0f}</span>
</div>
<div style="flex: 1; background: #161B22; padding: 15px; border-radius: 8px; border: 1px solid #FF4B4B; text-align: center;">
<span style="color: #FF4B4B; font-size: 0.8em; text-transform: uppercase;">The Hustle Levy (Loss)</span><br>
<span style="font-size: 1.5em; font-weight: bold; color: #FF4B4B;">- ₦{total_levy_amount:,.0f}</span>
</div>
<div style="flex: 1; background: rgba(63, 185, 80, 0.1); padding: 15px; border-radius: 8px; border: 1px solid #3FB950; text-align: center;">
<span style="color: #3FB950; font-size: 0.8em; text-transform: uppercase;">True Economic Value</span><br>
<span style="font-size: 1.5em; font-weight: bold; color: #3FB950;">₦{true_value:,.0f}</span>
</div>
</div>
<p style="margin-top: 25px; color: #8B949E; font-style: italic;">
<b>The "Invisible" Theft:</b> In a 30-day month, {commuter_name} spends <b>{persona['Monthly_Hours_Lost']:.1f} hours</b> 
trapped in transit. Between direct transport costs and the value of that stolen time, their salary is 
effectively slashed by <b>{persona['Tax_Percentage_of_Income']:.1f}%</b>.
</p>
</div>
"""
    st.markdown(html_impact, unsafe_allow_html=True)

else:
    st.warning("The road is empty. Please check your Control Room filters.")