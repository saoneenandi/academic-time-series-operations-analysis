import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.integrate import solve_ivp

# Page Layout Configuration
st.set_page_config(page_title="Campus Analytics Dashboard", layout="wide", page_icon="🎓")

# Custom Metric Card Styling
st.markdown("""
<style>
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

class CampusSimulationEngine:
    def __init__(self, semester_days=120, alpha=0.18, beta=0.07):
        self.T = semester_days
        self.alpha = alpha
        self.beta = beta

    def stress_heuristic(self, t, exams, projects):
        S_0 = 0.5
        stress = S_0
        for exam in exams:
            t_i, w_i = exam['day'], exam['weight']
            stress += w_i * np.exp(-0.5 * ((t - t_i) / 2.5) ** 2)
        for proj in projects:
            t_j, w_j = proj['day'], proj['weight']
            tau = t - t_j
            if tau <= 0:
                stress += w_j * np.exp(tau / 3.0)
        return stress

    def fatigue_ode(self, t, F, exams, projects, holiday_mask):
        day_idx = min(int(t), self.T - 1)
        H_t = holiday_mask[day_idx]
        S_t = self.stress_heuristic(t, exams, projects)
        return [self.alpha * S_t - self.beta * F[0] * (1.0 - H_t)]

    def solve(self, exams, projects, holiday_mask):
        t_eval = np.linspace(0, self.T, self.T * 5)
        sol = solve_ivp(
            fun=self.fatigue_ode,
            t_span=(0, self.T),
            y0=[0.0],
            t_eval=t_eval,
            args=(exams, projects, holiday_mask),
            method='RK45'
        )
        stress_vals = [self.stress_heuristic(t, exams, projects) for t in sol.t]
        return pd.DataFrame({'time_day': sol.t, 'stress_index': stress_vals, 'fatigue_level': sol.y[0]})


def main():
    st.title("🎓 Academic Time-Series Operational Analytics")
    st.markdown("---")

    # --- Sidebar Controls ---
    st.sidebar.header("⚙️ Differential Equation Parameters")
    alpha = st.sidebar.slider("Stress Vulnerability (α)", 0.05, 0.50, 0.24, 0.01)
    beta = st.sidebar.slider("Recovery Rate (β)", 0.01, 0.20, 0.07, 0.01)
    burnout_limit = st.sidebar.slider("Burnout Alert Threshold", 5.0, 15.0, 8.0, 0.5)

    st.sidebar.header("📅 Schedule Adjustments")
    with st.sidebar.expander("Configure Midterms & Finals"):
        exam_1_day = st.number_input("Midterm 1 Day", value=35)
        exam_1_wt = st.number_input("Midterm 1 Weight", value=4.0)
        exam_2_day = st.number_input("Final Exam Day", value=110)
        exam_2_wt = st.number_input("Final Exam Weight", value=5.0)

    exams = [{"day": exam_1_day, "weight": exam_1_wt}, {"day": exam_2_day, "weight": exam_2_wt}]
    projects = [{"day": 30, "weight": 2.5}, {"day": 105, "weight": 4.5}]

    holiday_mask = np.zeros(120)
    for t in range(120):
        if t % 7 in [5, 6]: holiday_mask[t] = 0.5
        if t in [45, 46, 47, 48, 49]: holiday_mask[t] = 1.0

    # --- Run Simulation ---
    engine = CampusSimulationEngine(alpha=alpha, beta=beta)
    df_sim = engine.solve(exams, projects, holiday_mask)

    # --- Executive KPI Row ---
    max_stress = df_sim['stress_index'].max()
    max_fatigue = df_sim['fatigue_level'].max()
    overload_days = (df_sim['fatigue_level'] > burnout_limit).sum() / 5

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Peak Stress Index", f"{max_stress:.2f}")
    col2.metric("Peak Fatigue", f"{max_fatigue:.2f}", delta=f"{max_fatigue - burnout_limit:.2f}", delta_color="inverse")
    col3.metric("Burnout Duration", f"{overload_days:.1f} Days")
    col4.metric("Status", "🚨 Overload Risk" if max_fatigue > burnout_limit else "✅ Operational")

    st.markdown("###")

    # --- Dashboard Tabs ---
    tab1, tab2, tab3 = st.tabs(["📈 Velocity Plot", "🔥 Weekly Heatmap", "📊 Raw Simulation Data"])

    with tab1:
        fig = go.Figure()
        
        # Stress Line
        fig.add_trace(go.Scatter(
            x=df_sim['time_day'], y=df_sim['stress_index'], 
            name='Stress Index S(t)', line=dict(color='#0066CC', width=2)
        ))
        
        # Fatigue Line
        fig.add_trace(go.Scatter(
            x=df_sim['time_day'], y=df_sim['fatigue_level'], 
            name='Student Fatigue F(t)', line=dict(color='#FF3333', width=3)
        ))
        
        # Alert Threshold Line
        fig.add_hline(
            y=burnout_limit, line_dash="dash", line_color="black",
            annotation_text="Burnout Threshold"
        )

        fig.update_layout(
            title="Operational Velocity Trajectory (Continuous RK45 Solution)",
            xaxis_title="Academic Day", yaxis_title="Magnitude Index",
            hovermode="x unified", height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        df_sim['day_int'] = df_sim['time_day'].astype(int)
        daily = df_sim.groupby('day_int')['fatigue_level'].mean().reset_index()
        daily['week'] = daily['day_int'] // 7 + 1
        daily['day_of_week'] = daily['day_int'] % 7
        
        heatmap_piv = daily.pivot(index='day_of_week', columns='week', values='fatigue_level')
        
        fig_heat = px.imshow(
            heatmap_piv,
            labels=dict(x="Academic Week", y="Day of Week", color="Fatigue Level"),
            y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            color_continuous_scale="YlOrRd", aspect="auto"
        )
        fig_heat.update_layout(title="Weekly Campus Fatigue Density Matrix", height=450)
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab3:
        st.dataframe(df_sim, use_container_width=True)
        csv = df_sim.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Simulation Data (CSV)", csv, "simulation_results.csv", "text/csv")

if __name__ == "__main__":
    main()
