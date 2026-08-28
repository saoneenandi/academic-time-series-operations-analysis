import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.integrate import solve_ivp

# --- Page Layout & Configuration ---
st.set_page_config(
    page_title="Academic Workload & Stress Analytics Platform",
    page_icon="⚡",
    layout="wide"
)

# --- Modern Light/White CSS Styling ---
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
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
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
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
    .advisory-box {
        background-color: #FEF3C7;
        border-left: 4px solid #D97706;
        padding: 14px 18px;
        border-radius: 6px;
        color: #92400E;
        font-weight: 500;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# --- Differential Simulation Engine ---
class StressSimulationEngine:
    def __init__(self, semester_days=110, alpha=0.22, beta=0.08):
        self.T = semester_days
        self.alpha = alpha
        self.beta = beta

    def stress_heuristic(self, t, assessments):
        S_0 = 0.5
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

    def subject_stress_breakdown(self, t, assessments, courses):
        breakdown = {c['code']: 0.0 for c in courses}
        for item in assessments:
            t_i = item['day']
            w_i = item['weight']
            eval_type = item['type']
            code = item.get('code', 'GENERAL')
            
            val = 0.0
            if eval_type in ["Exam", "Theory"]:
                sigma = 2.5
                val = w_i * np.exp(-0.5 * ((t - t_i) / sigma) ** 2)
            else:
                lambda_p = 3.0
                tau = t - t_i
                if tau <= 0:
                    val = w_i * np.exp(tau / lambda_p)
            
            if code in breakdown:
                breakdown[code] += val
            else:
                breakdown['EXAMS'] = breakdown.get('EXAMS', 0.0) + val
        return breakdown

    def fatigue_ode(self, t, F, assessments, holiday_mask):
        day_idx = min(int(t), self.T - 1)
        H_t = holiday_mask[day_idx]
        S_t = self.stress_heuristic(t, assessments)
        return [self.alpha * S_t - self.beta * F[0] * (1.0 - H_t)]

    def solve(self, assessments, holiday_mask, courses):
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
        
        df = pd.DataFrame({'time_day': sol.t, 'stress_index': stress_vals, 'fatigue_level': sol.y[0]})
        
        # Calculate course-wise stress contribution
        breakdowns = [self.subject_stress_breakdown(t, assessments, courses) for t in sol.t]
        df_bd = pd.DataFrame(breakdowns)
        return pd.concat([df, df_bd], axis=1)


# --- Complete Integrated M.Sc Curriculum Dataset (Semesters 1 - 10) ---
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
            {"code": "PE309", "name": "Project Management", "credits": 3.0, "type": "Theory"},
            {"code": "PH112", "name": "Physics II Lab", "credits": 2.0, "type": "Lab"}
        ],
        "Semester 4": [
            {"code": "MA206R1", "name": "Linear Algebra", "credits": 3.0, "type": "Theory"},
            {"code": "MA210", "name": "Discrete Mathematics & Graph Theory", "credits": 4.0, "type": "Theory"},
            {"code": "CS233", "name": "Object Oriented Programming & Design", "credits": 3.0, "type": "Theory"},
            {"code": "CH213", "name": "Chemistry II", "credits": 4.0, "type": "Theory"},
            {"code": "CS234", "name": "OOP Lab", "credits": 1.5, "type": "Lab"}
        ],
        "Semester 5": [
            {"code": "MA311R1", "name": "Numerical Techniques", "credits": 3.0, "type": "Theory"},
            {"code": "MA301R1", "name": "Probability & Statistics", "credits": 3.0, "type": "Theory"},
            {"code": "CS241", "name": "Design & Analysis of Algorithms", "credits": 3.0, "type": "Theory"},
            {"code": "CS242", "name": "DAA Lab", "credits": 1.0, "type": "Lab"},
            {"code": "MA312R1", "name": "Numerical Techniques Lab", "credits": 1.0, "type": "Lab"}
        ],
        "Semester 6": [
            {"code": "MA305", "name": "Optimization Techniques", "credits": 4.0, "type": "Theory"},
            {"code": "MA307", "name": "Functional Analysis", "credits": 4.0, "type": "Theory"},
            {"code": "CS301", "name": "Database Management Systems", "credits": 3.0, "type": "Theory"},
            {"code": "CS302", "name": "DBMS Lab", "credits": 1.5, "type": "Lab"}
        ],
        "Semester 7": [
            {"code": "MA401R1", "name": "Measure Theory & Integration", "credits": 3.0, "type": "Theory"},
            {"code": "MA402R1", "name": "Advanced Complex Analysis", "credits": 3.0, "type": "Theory"},
            {"code": "CS310", "name": "Formal Languages & Automata", "credits": 3.0, "type": "Theory"},
            {"code": "CA505", "name": "Software Engineering", "credits": 4.0, "type": "Theory"}
        ],
        "Semester 8": [
            {"code": "MA408", "name": "Topology", "credits": 4.0, "type": "Theory"},
            {"code": "MA410", "name": "Stochastic Processes", "credits": 4.0, "type": "Theory"},
            {"code": "CS401", "name": "Operating Systems", "credits": 3.0, "type": "Theory"},
            {"code": "CS402", "name": "Operating Systems Lab", "credits": 1.5, "type": "Lab"}
        ],
        "Semester 9": [
            {"code": "MA414R1", "name": "Advanced Operations Research", "credits": 3.0, "type": "Theory"},
            {"code": "CA511", "name": "Basics of Machine Learning", "credits": 3.0, "type": "Theory"},
            {"code": "CA601", "name": "Computer Graphics", "credits": 3.0, "type": "Theory"},
            {"code": "CA512", "name": "Machine Learning Lab", "credits": 1.5, "type": "Lab"},
            {"code": "CA602", "name": "Computer Graphics Lab", "credits": 1.5, "type": "Lab"}
        ],
        "Semester 10": [
            {"code": "MA500", "name": "Master's Thesis / Project", "credits": 16.0, "type": "Sessional"},
            {"code": "MA502", "name": "Comprehensive Seminar & Viva", "credits": 4.0, "type": "Sessional"}
        ]
    }


def generate_semester_timeline(courses, mid_sem_day=45, end_sem_day=100, spacing_factor=0):
    assessments = []
    for idx, course in enumerate(courses):
        w = course['credits']
        code = course['code']
        assessments.append({
            "code": code,
            "name": f"Quiz 1: {code}",
            "day": max(10, 20 + (idx % 4) * 2 + spacing_factor),
            "weight": w * 0.5,
            "type": "Quiz"
        })
        assessments.append({
            "code": code,
            "name": f"Quiz 2 / Lab: {code}",
            "day": min(90, 75 + (idx % 4) * 2 + spacing_factor),
            "weight": w * 0.6,
            "type": "Assignment" if course['type'] == 'Lab' else "Quiz"
        })

    total_credits = sum(c['credits'] for c in courses)
    assessments.append({"code": "EXAMS", "name": "Mid-Semester Examinations", "day": mid_sem_day, "weight": total_credits * 0.35, "type": "Exam"})
    assessments.append({"code": "EXAMS", "name": "End-Semester Examinations", "day": end_sem_day, "weight": total_credits * 0.50, "type": "Exam"})
    return assessments


# --- Main Dashboard Application ---
def main():
    st.markdown("<h1 class='main-header'>⚡ Advanced Academic Workload & Stress Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Dynamic Course Customization, Stress Decomposition & Operational Optimization</p>", unsafe_allow_html=True)

    curriculum_presets = get_curriculum()

    # --- Sidebar Controls ---
    st.sidebar.header("⚙️ Term Configuration")
    selected_sem = st.sidebar.selectbox("Load Preset Term", list(curriculum_presets.keys()))
    
    # Session state initialization for editable courses
    if 'custom_courses' not in st.session_state or st.sidebar.button("Reset Course Preset"):
        st.session_state.custom_courses = curriculum_presets[selected_sem]

    mid_sem_day = st.sidebar.number_input("Mid-Sem Day Target", min_value=30, max_value=60, value=45)
    end_sem_day = st.sidebar.number_input("End-Sem Day Target", min_value=85, max_value=110, value=100)

    st.sidebar.markdown("---")
    st.sidebar.header("🔀 What-If Comparison")
    enable_scenario_b = st.sidebar.checkbox("Enable Scenario B", value=True)
    scen_b_mid_day = st.sidebar.number_input("Scenario B Mid-Sem Day", min_value=30, max_value=60, value=52)
    scen_b_spacing = st.sidebar.slider("Quiz Buffer Offset (Days)", -5, 10, 3)

    st.sidebar.markdown("---")
    st.sidebar.header("🔬 Model Sensitivity")
    alpha = st.sidebar.slider("Stress Sensitivity (α)", 0.05, 0.50, 0.22, 0.01)
    beta = st.sidebar.slider("Recovery Rate (β)", 0.01, 0.20, 0.08, 0.01)
    burnout_limit = st.sidebar.slider("Burnout Alert Threshold", 5.0, 20.0, 12.0, 0.5)

    # Rest capacity mask (Weekends + Mid-term break)
    holiday_mask = np.zeros(110)
    for t in range(110):
        if t % 7 in [5, 6]: 
            holiday_mask[t] = 0.5
        if t in range(50, 56):
            holiday_mask[t] = 1.0

    # Dynamic Course & Credit Editor
    with st.expander("📝 Edit Courses & Credits Dynamically", expanded=False):
        st.write("Modify course credits or types below to observe real-time impact on workload curves.")
        df_edit = pd.DataFrame(st.session_state.custom_courses)
        edited_df = st.data_editor(df_edit, num_rows="dynamic", use_container_width=True)
        active_courses = edited_df.to_dict('records')

    engine = StressSimulationEngine(alpha=alpha, beta=beta)

    # --- Run Simulations ---
    assess_a = generate_semester_timeline(active_courses, mid_sem_day, end_sem_day, spacing_factor=0)
    df_sim_a = engine.solve(assess_a, holiday_mask, active_courses)
    max_fatigue_a = df_sim_a['fatigue_level'].max()

    if enable_scenario_b:
        assess_b = generate_semester_timeline(active_courses, scen_b_mid_day, end_sem_day, spacing_factor=scen_b_spacing)
        df_sim_b = engine.solve(assess_b, holiday_mask, active_courses)
        max_fatigue_b = df_sim_b['fatigue_level'].max()
        fatigue_diff = max_fatigue_b - max_fatigue_a

    # --- KPI Metric Row ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Selected Term", selected_sem)
    c2.metric("Baseline Peak Fatigue", f"{max_fatigue_a:.2f}")
    if enable_scenario_b:
        c3.metric("Scenario B Peak Fatigue", f"{max_fatigue_b:.2f}", delta=f"{fatigue_diff:.2f}", delta_color="inverse")
        c4.metric("Comparison Verdict", "✅ Load Reduced" if fatigue_diff < 0 else "🚨 Higher Stress")
    else:
        c3.metric("Burnout Limit", f"{burnout_limit:.1f}")
        c4.metric("Status", "🚨 High Risk" if max_fatigue_a > burnout_limit else "✅ Operational")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Automated Mitigation Advisory ---
    if max_fatigue_a > burnout_limit:
        over_days = df_sim_a[df_sim_a['fatigue_level'] > burnout_limit]['time_day']
        start_day, end_day = int(over_days.min()), int(over_days.max())
        st.markdown(f"""
        <div class='advisory-box'>
            🚨 <strong>Automated Workload Advisory:</strong> Critical fatigue breach predicted between <strong>Day {start_day} and Day {end_day}</strong>. 
            Consider increasing recovery dissipation (β), shifting Mid-Sem exams by +5 days, or spacing out Quiz 2 submissions.
        </div>
        """, unsafe_allow_html=True)

    # --- Visualization Tabs ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Scenario Comparison", 
        "📊 Subject Stress Breakdown", 
        "🤖 Automated Schedule Optimizer", 
        "🔥 Weekly Heatmap", 
        "📥 Data Export"
    ])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_sim_a['time_day'], y=df_sim_a['fatigue_level'],
            name='Baseline Fatigue (Scenario A)', line=dict(color='#DC2626', width=3)
        ))
        if enable_scenario_b:
            fig.add_trace(go.Scatter(
                x=df_sim_b['time_day'], y=df_sim_b['fatigue_level'],
                name='Modified Fatigue (Scenario B)', line=dict(color='#2563EB', width=3, dash='dash')
            ))
        fig.add_hline(
            y=burnout_limit, line_dash="dot", line_color="#D97706",
            annotation_text="Burnout Threshold", annotation_position="top right"
        )
        fig.update_layout(
            template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Academic Days", yaxis_title="Fatigue Level", hovermode="x unified", height=480
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("📊 Course-Wise Stress Contribution")
        st.write("Decomposition of stress contribution per registered course across the semester.")
        course_codes = [c['code'] for c in active_courses] + ['EXAMS']
        valid_codes = [c for c in course_codes if c in df_sim_a.columns]
        
        fig_stack = px.area(
            df_sim_a, x='time_day', y=valid_codes,
            labels={'value': 'Stress Index', 'variable': 'Course Code'},
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_stack.update_layout(
            template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Academic Days", yaxis_title="Stress Magnitude", height=450
        )
        st.plotly_chart(fig_stack, use_container_width=True)

    with tab3:
        st.subheader("🤖 Schedule Optimization Engine")
        st.write("Evaluates schedule permutations to minimize peak fatigue below burnout threshold.")
        
        if st.button("⚡ Run Schedule Optimizer", type="primary"):
            best_fatigue = float('inf')
            best_params = {}
            
            for test_mid in range(38, 55, 2):
                for test_offset in range(-3, 6, 2):
                    test_assess = generate_semester_timeline(active_courses, test_mid, end_sem_day, spacing_factor=test_offset)
                    test_df = engine.solve(test_assess, holiday_mask, active_courses)
                    peak_f = test_df['fatigue_level'].max()
                    
                    if peak_f < best_fatigue:
                        best_fatigue = peak_f
                        best_params = {"mid_sem_day": test_mid, "quiz_offset": test_offset}
            
            st.success("Optimization Complete!")
            o1, o2, o3 = st.columns(3)
            o1.metric("Recommended Mid-Sem Day", f"Day {best_params['mid_sem_day']}")
            o2.metric("Recommended Quiz Offset", f"{best_params['quiz_offset']} Days")
            o3.metric("Optimized Peak Fatigue", f"{best_fatigue:.2f}", delta=f"{best_fatigue - max_fatigue_a:.2f}", delta_color="inverse")

    with tab4:
        df_sim_a['day_int'] = df_sim_a['time_day'].astype(int)
        daily = df_sim_a.groupby('day_int')['fatigue_level'].mean().reset_index()
        daily['week'] = daily['day_int'] // 7 + 1
        daily['day_of_week'] = daily['day_int'] % 7
        
        heatmap_piv = daily.pivot(index='day_of_week', columns='week', values='fatigue_level')
        fig_heat = px.imshow(
            heatmap_piv,
            labels=dict(x="Academic Week", y="Day", color="Fatigue"),
            y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            color_continuous_scale="Reds", aspect="auto"
        )
        fig_heat.update_layout(template="plotly_white", height=420)
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab5:
        st.subheader("📥 Export Simulation Data")
        st.dataframe(df_sim_a, use_container_width=True)
        csv_data = df_sim_a.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Baseline Simulation CSV",
            data=csv_data,
            file_name=f"{selected_sem}_simulation_export.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
