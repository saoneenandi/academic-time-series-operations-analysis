import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.integrate import solve_ivp

# --- Page Layout & Configuration ---
st.set_page_config(
    page_title="Academic Workload & Stress Analytics",
    page_icon="⚡",
    layout="wide"
)

# --- Clean Light/White CSS Styling ---
st.markdown("""
<style>
    /* Global Page Styling */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* Headers */
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    /* Metric Cards - Clean White Glassmorphism */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
    }
    div[data-testid="stMetricLabel"] {
        color: #2563EB;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* Tab Styling */
    button[data-baseweb="tab"] {
        color: #64748B !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    button[aria-selected="true"] {
        color: #2563EB !important;
        background-color: #EFF6FF !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Simulation Engine ---
class StressSimulationEngine:
    def __init__(self, semester_days=110, alpha=0.22, beta=0.08):
        self.T = semester_days
        self.alpha = alpha  # Stress impact coefficient
        self.beta = beta    # Recovery rate coefficient

    def stress_heuristic(self, t, assessments):
        S_0 = 0.5  # Baseline academic stress
        stress = S_0
        
        for item in assessments:
            t_i = item['day']
            w_i = item['weight']
            eval_type = item['type']
            
            if eval_type in ["Exam", "Theory"]:
                sigma = 2.5
                stress += w_i * np.exp(-0.5 * ((t - t_i) / sigma) ** 2)
            else:
                lambda_p = 3.0
                tau = t - t_i
                if tau <= 0:
                    stress += w_i * np.exp(tau / lambda_p)
        return stress

    def fatigue_ode(self, t, F, assessments, holiday_mask):
        day_idx = min(int(t), self.T - 1)
        H_t = holiday_mask[day_idx]
        S_t = self.stress_heuristic(t, assessments)
        return [self.alpha * S_t - self.beta * F[0] * (1.0 - H_t)]

    def solve(self, assessments, holiday_mask):
        t_eval = np.linspace(0, self.T, self.T * 5)
        sol = solve_ivp(
            fun=self.fatigue_ode,
            t_span=(0, self.T),
            y0=[0.0],
            t_eval=t_eval,
            args=(assessments, holiday_mask),
            method='RK45'
        )
        stress_vals = [self.stress_heuristic(t, assessments) for t in sol.t]
        return pd.DataFrame({'time_day': sol.t, 'stress_index': stress_vals, 'fatigue_level': sol.y[0]})


# --- Academic Curriculum Database ---
def get_curriculum():
    return {
        "Semester 1": [
            {"code": "MA101", "name": "Calculus-I", "credits": 4.0, "type": "Theory"},
            {"code": "MA102", "name": "Real Analysis", "credits": 4.0, "type": "Theory"},
            {"code": "MA109", "name": "Matrix Theory", "credits": 4.0, "type": "Theory"},
            {"code": "CH111", "name": "Chemistry I", "credits": 4.0, "type": "Theory"},
            {"code": "CH112", "name": "Chemistry I Lab", "credits": 2.0, "type": "Lab"},
            {"code": "MT132", "name": "Communication Skill I", "credits": 1.5, "type": "Sessional"}
        ],
        "Semester 2": [
            {"code": "MA105R1", "name": "Calculus-II", "credits": 3.0, "type": "Theory"},
            {"code": "MA106R1", "name": "Ordinary Differential Equations", "credits": 3.0, "type": "Theory"},
            {"code": "MA110R1", "name": "Complex Analysis", "credits": 3.0, "type": "Theory"},
            {"code": "PH109", "name": "Physics I", "credits": 4.0, "type": "Theory"},
            {"code": "CS101", "name": "Programming for Problem Solving", "credits": 4.0, "type": "Theory"},
            {"code": "PH110R1", "name": "Physics I Lab", "credits": 2.0, "type": "Lab"}
        ],
        "Semester 3": [
            {"code": "MA202R1", "name": "Abstract Algebra", "credits": 3.0, "type": "Theory"},
            {"code": "MA201R1", "name": "Partial Differential Equations", "credits": 3.0, "type": "Theory"},
            {"code": "PH111", "name": "Physics II", "credits": 4.0, "type": "Theory"},
            {"code": "CS231", "name": "Data Structures", "credits": 4.0, "type": "Theory"},
            {"code": "PE309", "name": "Project Management", "credits": 3.0, "type": "Theory"}
        ],
        "Semester 4": [
            {"code": "MA206R1", "name": "Linear Algebra", "credits": 3.0, "type": "Theory"},
            {"code": "MA210", "name": "DMS and Graph Theory", "credits": 4.0, "type": "Theory"},
            {"code": "CS233", "name": "OOP and Design Pattern", "credits": 3.0, "type": "Theory"},
            {"code": "CH213", "name": "Chemistry II", "credits": 4.0, "type": "Theory"}
        ]
    }


def generate_semester_timeline(courses, mid_sem_day=45, end_sem_day=100):
    assessments = []
    for idx, course in enumerate(courses):
        w = course['credits']
        assessments.append({
            "name": f"Quiz 1: {course['code']}",
            "day": 20 + (idx % 4) * 2,
            "weight": w * 0.5,
            "type": "Quiz"
        })
        assessments.append({
            "name": f"Quiz 2 / Lab Viva: {course['code']}",
            "day": 75 + (idx % 4) * 2,
            "weight": w * 0.6,
            "type": "Assignment" if course['type'] == 'Lab' else "Quiz"
        })

    total_credits = sum(c['credits'] for c in courses)
    assessments.append({"name": "Mid-Semester Examinations", "day": mid_sem_day, "weight": total_credits * 0.35, "type": "Exam"})
    assessments.append({"name": "End-Semester Examinations", "day": end_sem_day, "weight": total_credits * 0.50, "type": "Exam"})
    return assessments


# --- Main Dashboard Application ---
def main():
    st.markdown("<h1 class='main-header'>⚡ Continuous Academic Workload Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Time-Series Operational Stress & Fatigue Dynamics Simulation</p>", unsafe_allow_html=True)

    curriculum = get_curriculum()

    # --- Sidebar Controls ---
    st.sidebar.header("⚙️ Configuration Controls")
    selected_sem = st.sidebar.selectbox("Academic Term", list(curriculum.keys()))
    courses = curriculum[selected_sem]

    mid_sem_day = st.sidebar.number_input("Mid-Sem Target Day", min_value=30, max_value=60, value=45)
    end_sem_day = st.sidebar.number_input("End-Sem Target Day", min_value=85, max_value=110, value=100)

    st.sidebar.markdown("---")
    st.sidebar.header("🔬 Model Sensitivity")
    alpha = st.sidebar.slider("Stress Sensitivity (α)", 0.05, 0.50, 0.22, 0.01)
    beta = st.sidebar.slider("Recovery Dissipation (β)", 0.01, 0.20, 0.08, 0.01)
    burnout_limit = st.sidebar.slider("Burnout Alert Threshold", 5.0, 20.0, 12.0, 0.5)

    # Rest capacity mask (Weekends + Mid-term break)
    holiday_mask = np.zeros(110)
    for t in range(110):
        if t % 7 in [5, 6]: 
            holiday_mask[t] = 0.5
        if t in range(50, 56):
            holiday_mask[t] = 1.0

    assessments = generate_semester_timeline(courses, mid_sem_day, end_sem_day)
    engine = StressSimulationEngine(alpha=alpha, beta=beta)
    df_sim = engine.solve(assessments, holiday_mask)

    max_stress = df_sim['stress_index'].max()
    max_fatigue = df_sim['fatigue_level'].max()

    # --- KPI Metric Row ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Selected Term", selected_sem)
    c2.metric("Peak Stress Index", f"{max_stress:.2f}")
    c3.metric("Peak Cumulative Fatigue", f"{max_fatigue:.2f}", delta=f"{max_fatigue - burnout_limit:.2f}", delta_color="inverse")
    c4.metric("Operational Status", "🚨 Critical Load" if max_fatigue > burnout_limit else "✅ Optimal Velocity")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Visualization Tabs ---
    tab1, tab2, tab3 = st.tabs(["📈 Operational Velocity Plot", "🔥 Weekly Heatmap", "📚 Enrolled Courses"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_sim['time_day'], y=df_sim['stress_index'],
            name='Stress Index S(t)', line=dict(color='#2563EB', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df_sim['time_day'], y=df_sim['fatigue_level'],
            name='Student Fatigue F(t)', line=dict(color='#DC2626', width=3)
        ))
        fig.add_hline(
            y=burnout_limit, line_dash="dash", line_color="#D97706",
            annotation_text="Burnout Threshold", annotation_position="top right"
        )
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Academic Days",
            yaxis_title="Magnitude Index",
            hovermode="x unified",
            height=480
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
            labels=dict(x="Academic Week", y="Day", color="Fatigue"),
            y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            color_continuous_scale="Reds", aspect="auto"
        )
        fig_heat.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=420
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab3:
        st.dataframe(pd.DataFrame(courses), use_container_width=True)


if __name__ == "__main__":
    main()
