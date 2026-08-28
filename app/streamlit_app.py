import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.integrate import solve_ivp

# --- Page Configuration ---
st.set_page_config(
    page_title="BIT Mesra Integrated M.Sc. Math & Computing - Stress Analytics",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
<style>
    .main-header {
        color: #800000;
        font-weight: 700;
        font-size: 2.2rem;
    }
    .sub-header {
        color: #4A4A4A;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# --- Differential Equation Simulation Engine ---
class BITMesraSimulationEngine:
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
            
            # Exams (Mid-Sem / End-Sem): Gaussian kernel modeling prep & exam period
            if eval_type in ["Exam", "Theory"]:
                sigma = 2.5
                stress += w_i * np.exp(-0.5 * ((t - t_i) / sigma) ** 2)
            # Quizzes / Assignments / Sessional Vivas: Asymmetric decay kernel
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


# --- BIT Mesra Integrated M.Sc. Curriculum Database ---
def get_bit_mesra_curriculum():
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
            {"code": "PH110R1", "name": "Physics I Lab", "credits": 2.0, "type": "Lab"},
            {"code": "CS102", "name": "Programming for Problem Solving Lab", "credits": 1.5, "type": "Lab"}
        ],
        "Semester 3": [
            {"code": "MA202R1", "name": "Abstract Algebra", "credits": 3.0, "type": "Theory"},
            {"code": "MA201R1", "name": "Partial Differential Equations", "credits": 3.0, "type": "Theory"},
            {"code": "PH111", "name": "Physics II", "credits": 4.0, "type": "Theory"},
            {"code": "CS231", "name": "Data Structures", "credits": 4.0, "type": "Theory"},
            {"code": "PE309", "name": "Project Management", "credits": 3.0, "type": "Theory"},
            {"code": "PH112", "name": "Physics II Lab", "credits": 2.0, "type": "Lab"},
            {"code": "CS232", "name": "Data Structures Lab", "credits": 1.5, "type": "Lab"}
        ],
        "Semester 4": [
            {"code": "MA206R1", "name": "Linear Algebra", "credits": 3.0, "type": "Theory"},
            {"code": "MA210", "name": "DMS and Graph Theory", "credits": 4.0, "type": "Theory"},
            {"code": "CS233", "name": "OOP and Design Pattern", "credits": 3.0, "type": "Theory"},
            {"code": "CH213", "name": "Chemistry II", "credits": 4.0, "type": "Theory"},
            {"code": "CS234", "name": "OOP and Design Pattern Lab", "credits": 1.5, "type": "Lab"},
            {"code": "CH214", "name": "Chemistry II Lab", "credits": 2.0, "type": "Lab"}
        ],
        "Semester 5": [
            {"code": "MA311R1", "name": "Numerical Techniques", "credits": 3.0, "type": "Theory"},
            {"code": "MA301R1", "name": "Probability and Statistics", "credits": 3.0, "type": "Theory"},
            {"code": "CS241", "name": "Design and Analysis of Algorithms", "credits": 3.0, "type": "Theory"},
            {"code": "CS242", "name": "Design and Analysis of Algorithms Lab", "credits": 1.0, "type": "Lab"},
            {"code": "MA312R1", "name": "Numerical Techniques Lab", "credits": 1.0, "type": "Lab"}
        ],
        "Semester 9": [
            {"code": "MA414R1", "name": "Advanced Operation Research", "credits": 3.0, "type": "Theory"},
            {"code": "CA511", "name": "Basics of Machine Learning", "credits": 3.0, "type": "Theory"},
            {"code": "CA601", "name": "Computer Graphics", "credits": 3.0, "type": "Theory"},
            {"code": "CA512", "name": "Basics of Machine Learning Lab", "credits": 1.5, "type": "Lab"},
            {"code": "CA602", "name": "Computer Graphics Lab", "credits": 1.5, "type": "Lab"}
        ]
    }


def generate_semester_timeline(courses, mid_sem_day=45, end_sem_day=100):
    """Dynamically converts subject list into calendar evaluation events based on course weights."""
    assessments = []
    
    # 1. Quizzes & Mid-Sems
    for idx, course in enumerate(courses):
        w = course['credits']
        # Quiz 1 before Mid-Sems
        assessments.append({
            "name": f"Quiz 1: {course['code']} ({course['name']})",
            "day": 20 + (idx % 4) * 2,
            "weight": w * 0.5,
            "type": "Quiz"
        })
        # Quiz 2 before End-Sems
        assessments.append({
            "name": f"Quiz 2 / Lab Viva: {course['code']}",
            "day": 75 + (idx % 4) * 2,
            "weight": w * 0.6,
            "type": "Assignment" if course['type'] == 'Lab' else "Quiz"
        })

    # 2. Centralized Mid-Sem & End-Sem Windows
    total_credits = sum(c['credits'] for c in courses)
    assessments.append({
        "name": "Mid-Semester Examinations",
        "day": mid_sem_day,
        "weight": total_credits * 0.35,
        "type": "Exam"
    })
    assessments.append({
        "name": "End-Semester Examinations & Vivas",
        "day": end_sem_day,
        "weight": total_credits * 0.50,
        "type": "Exam"
    })
    
    return assessments


# --- Application Layout ---
def main():
    st.markdown("<h1 class='main-header'>🏛️ BIT Mesra Operational Fatigue Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Integrated M.Sc. in Mathematics and Computing Academic Term Stress Modeling</p>", unsafe_allow_html=True)
    st.divider()

    curriculum = get_bit_mesra_curriculum()

    # --- Sidebar Controls ---
    st.sidebar.header("📚 Semester & Curriculum Preset")
    selected_sem = st.sidebar.selectbox("Select Academic Term", list(curriculum.keys()))
    courses = curriculum[selected_sem]

    st.sidebar.header("📅 Timeline Configuration")
    mid_sem_day = st.sidebar.number_input("Mid-Sem Exam Day", min_value=30, max_value=60, value=45)
    end_sem_day = st.sidebar.number_input("End-Sem Exam Day", min_value=85, max_value=110, value=100)

    st.sidebar.header("⚙️ Stress ODE Parameters")
    alpha = st.sidebar.slider("Stress Sensitivity (α)", 0.05, 0.50, 0.22, 0.01, help="Rate at which course workload converts into student fatigue.")
    beta = st.sidebar.slider("Recovery Rate (β)", 0.01, 0.20, 0.08, 0.01, help="Recovery dissipation during weekends & Bitotsav / Festival breaks.")
    burnout_limit = st.sidebar.slider("Burnout Alert Threshold", 5.0, 20.0, 12.0, 0.5)

    # --- Construct Holiday Mask (Weekends + Bitotsav/Puja Break) ---
    holiday_mask = np.zeros(110)
    for t in range(110):
        if t % 7 in [5, 6]: 
            holiday_mask[t] = 0.5  # Weekend rest
        if t in range(50, 56):      # Mid-Sem Break / Fest Window
            holiday_mask[t] = 1.0

    # Build evaluation schedule and run ODE simulation
    assessments = generate_semester_timeline(courses, mid_sem_day, end_sem_day)
    engine = BITMesraSimulationEngine(alpha=alpha, beta=beta)
    df_sim = engine.solve(assessments, holiday_mask)

    # --- Metrics KPI Row ---
    max_stress = df_sim['stress_index'].max()
    max_fatigue = df_sim['fatigue_level'].max()
    overload_hours = (df_sim['fatigue_level'] > burnout_limit).sum() * (24 / 5)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Selected Term", selected_sem)
    c2.metric("Peak Stress Index", f"{max_stress:.2f}")
    c3.metric("Peak Student Fatigue", f"{max_fatigue:.2f}", delta=f"{max_fatigue - burnout_limit:.2f}", delta_color="inverse")
    c4.metric("Status", "🚨 High Burnout Risk" if max_fatigue > burnout_limit else "✅ Operational Velocity Normal")

    st.markdown("###")

    # --- Dashboard Navigation Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Operational Velocity Plot", 
        "🔥 Weekly Fatigue Heatmap", 
        "📖 Enrolled Subjects", 
        "🗓️ Generated Assessment Schedule"
    ])

    with tab1:
        fig = go.Figure()
        
        # Stress Line
        fig.add_trace(go.Scatter(
            x=df_sim['time_day'], y=df_sim['stress_index'],
            name='Stress Index S(t)', line=dict(color='#E65100', width=2)
        ))
        
        # Fatigue Line
        fig.add_trace(go.Scatter(
            x=df_sim['time_day'], y=df_sim['fatigue_level'],
            name='Student Fatigue F(t)', line=dict(color='#800000', width=3)
        ))
        
        # Burnout Limit Line
        fig.add_hline(
            y=burnout_limit, line_dash="dash", line_color="black",
            annotation_text="Systemic Overload Limit"
        )

        fig.update_layout(
            title=f"Continuous Trajectory ({selected_sem} - Integrated M.Sc. Math & Computing)",
            xaxis_title="Academic Days", yaxis_title="Magnitude Index",
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
            labels=dict(x="Academic Week", y="Day", color="Fatigue Level"),
            y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            color_continuous_scale="Reds", aspect="auto"
        )
        fig_heat.update_layout(title=f"BIT Mesra Weekly Fatigue Density ({selected_sem})", height=450)
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab3:
        st.subheader(f"Registered Courses - {selected_sem}")
        df_courses = pd.DataFrame(courses)
        st.dataframe(df_courses, use_container_width=True)

    with tab4:
        st.subheader("Simulated Evaluation Schedule")
        df_assess = pd.DataFrame(assessments)
        st.dataframe(df_assess, use_container_width=True)


if __name__ == "__main__":
    main()
