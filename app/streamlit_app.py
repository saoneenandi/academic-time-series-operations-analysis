import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.integrate import solve_ivp

st.set_page_config(page_title="Campus Analytics", layout="wide")

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
    
    st.sidebar.header("Parameters")
    alpha = st.sidebar.slider("Stress Vulnerability (α)", 0.05, 0.50, 0.18, 0.01)
    beta = st.sidebar.slider("Recovery Rate (β)", 0.01, 0.20, 0.07, 0.01)
    
    exams = [{"day": 35, "weight": 3.5}, {"day": 38, "weight": 4.0}, {"day": 110, "weight": 5.0}]
    projects = [{"day": 30, "weight": 2.5}, {"day": 105, "weight": 4.5}]
    
    holiday_mask = np.zeros(120)
    for t in range(120):
        if t % 7 in [5, 6]: holiday_mask[t] = 0.5
        if t in [45, 46, 47, 48, 49]: holiday_mask[t] = 1.0

    engine = CampusSimulationEngine(alpha=alpha, beta=beta)
    df_sim = engine.solve(exams, projects, holiday_mask)

    st.subheader("Operational Velocity: Stress vs Fatigue")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_sim['time_day'], y=df_sim['stress_index'], name='Stress S(t)'))
    fig.add_trace(go.Scatter(x=df_sim['time_day'], y=df_sim['fatigue_level'], name='Fatigue F(t)'))
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
