# ⚡ Academic Time-Series Operational Analytics: Student Fatigue Dynamics & Campus Stress Modeling

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://academic-time-series-operations-analysis.streamlit.app/)
[![SciPy](https://img.shields.io/badge/SciPy-ODE%20Solver-green.svg)](https://scipy.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> An end-to-end mathematical modeling and time-series forecasting engine built to map campus operational velocity, simulate student burnout trajectories, and optimize assessment placement across academic terms.

🌐 **Live Interactive App:** [academic-time-series-operations-analysis.streamlit.app](https://academic-time-series-operations-analysis.streamlit.app/)

---

## 📌 Executive Summary

Traditional institutional scheduling tools treat academic calendars as static, discrete events. This framework models campus stress and student fatigue as **continuous dynamical systems** governed by non-linear kernel functions and ordinary differential equations (ODEs).

By coupling numerical ODE integration ($\text{RK45}$) with real-time parameter tuning, the platform converts discrete curriculum structures—exam dates, quiz buffers, project deadlines, course credit weights, and holiday recovery intervals—into actionable time-series analytics, subject-wise stress decompositions, weekly fatigue heatmaps, and automated scheduling optimizations.

---

## 🌟 Key Features

* **Continuous ODE Stress Engine:** Simulates real-time fatigue accumulation and exponential decay using continuous differential equations.
* **Full 10-Semester Curriculum Presets:** Pre-loaded with complete course codes, credit distributions, and course types (Theory, Lab, Sessional) for a 5-year Integrated M.Sc. Mathematics & Computing program.
* **Dynamic Course & Credit Editor:** Interactive table editor allowing users to add custom subjects, adjust credit weights, or modify evaluation types on the fly.
* **Subject-Wise Stress Decomposition:** Stacked area visualizations isolating which specific courses drive fatigue peaks across the 110-day term.
* **What-If Scenario Simulator:** Real-time overlay of baseline vs. modified exam timelines to evaluate schedule changes before implementation.
* **Automated Schedule Optimizer:** Grid-search optimization heuristic that finds ideal exam placements to suppress peak fatigue below burnout thresholds.
* **Automated AI Advisory:** Real-time risk detection flagging continuous high-fatigue windows with targeted intervention strategies.
* **Weekly Heatmap Matrix:** Visual representation of workload density across a 7-day, multi-week academic matrix.
* **Data Export:** Instant CSV data downloads for downstream operational research and reporting.

---

## 🧮 Mathematical Formulation

### 1. Cumulative Campus Stress Signal $S(t)$
Let $t \in [0, T]$ denote time in continuous academic days across a term. The instantaneous workload stress $S(t)$ is formulated as a continuous heuristic function:

$$S(t) = S_0 + \sum_{i \in \text{Exams}} w_i \cdot \exp\left(-\frac{(t - t_i)^2}{2\sigma^2}\right) + \sum_{j \in \text{Quizzes}} w_j \cdot \exp\left(\frac{t - t_j}{\lambda}\right) \quad \text{for } t \le t_j$$

Where:
* $S_0$: Baseline daily academic friction ($S_0 = 0.5$).
* $w_i, w_j$: Course credit weights (derived from curriculum allocations).
* $\sigma$: Symmetric preparation/review window parameter for major exams ($\sigma = 2.5$).
* $\lambda$: Asymmetric exponential deadline pressure accumulation parameter ($\lambda = 3.0$).

### 2. Student Fatigue Differential Equation $\frac{dF(t)}{dt}$
Fatigue $F(t)$ represents the cumulative psychological and cognitive strain on the student body. The rate of change $\frac{dF(t)}{dt}$ is governed by a non-linear ODE:

$$\frac{dF(t)}{dt} = \alpha \cdot S(t) - \beta \cdot F(t) \cdot \Big(1 - H(t)\Big)$$

Where:
* $\alpha$: Stress vulnerability coefficient ($0.05 \le \alpha \le 0.50$).
* $\beta$: Recovery/dissipation rate coefficient ($0.01 \le \beta \le 0.20$).
* $H(t) \in [0, 1]$: Institutional rest capacity mask ($0.5$ on weekends, $1.0$ during mid-term breaks, $0.0$ on instructional days).

### 3. Numerical Integration Scheme
The continuous trajectory $F(t)$ is evaluated numerically over $t \in [0, T]$ using an explicit **Runge-Kutta 4th/5th Order (RK45)** adaptive step-size scheme:

$$F_{n+1} = F_n + h \sum_{i=1}^s b_i k_i, \quad k_i = f\left(t_n + c_i h, \, F_n + h \sum_{j=1}^{i-1} a_{ij} k_j\right)$$

---

## 🏗️ System Architecture

```text
                  CURRICULUM & CALENDAR CONFIGURATION
            (Integrated M.Sc. Semesters 1-10 / Custom Input)
                                  │
                                  ▼
               ┌─────────────────────────────────────┐
               │         streamlit_app.py            │
               │  • Interactive Dashboard & UI       │
               │  • Dynamic Course & Credit Editor   │
               └──────────────────┬──────────────────┘
                                  │
                                  ▼
               ┌─────────────────────────────────────┐
               │       StressSimulationEngine        │
               │  • Stress Heuristic Kernels S(t)    │
               │  • Subject-Level Decomposition      │
               │  • SciPy RK45 ODE Numerical Solver  │
               └──────────────────┬──────────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│     What-If & Optimization      │       │     Visualizations & Exports    │
│ • Scenario Comparison Curves    │       │ • Subject Area Stacked Plots    │
│ • Burnout Threshold Advisory    │       │ • Weekly Burnout Heatmaps       │
│ • Grid-Search Exam Optimizer    │       │ • CSV Simulation Data Download  │
└─────────────────────────────────┘       └─────────────────────────────────┘

## 📂 Repository Structure

```text
academic-time-series-operations-analysis/
├── .streamlit/
│   └── config.toml          # Custom Streamlit layout and theme settings
├── app/
│   └── streamlit_app.py      # Main application, math engine, & UI dashboard
├── Dockerfile               # Containerization configuration
├── README.md                # Project documentation
└── requirements.txt         # Dependencies (Streamlit, SciPy, Plotly, NumPy, Pandas)


cat << 'EOF' > README.md
## 🚀 Quick Start & Installation

### 1. Online Access
The application is live and accessible directly in your browser:  
👉 **[Launch Streamlit Dashboard](https://academic-time-series-operations-analysis.streamlit.app/)**

### 2. Local Installation

```bash
# Clone the repository
git clone [https://github.com/saoneenandi/academic-time-series-operations-analysis.git](https://github.com/saoneenandi/academic-time-series-operations-analysis.git)
cd academic-time-series-operations-analysis

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app/streamlit_app.py

#Yes. Below is a **single clean `README.md`** you can copy-paste directly into GitHub. I’ve removed the stray code fences, fixed the LaTeX formatting, corrected the table, and kept the mathematical/technical character of the project.

````markdown
# Academic Time-Series Operational Analytics: Student Fatigue Dynamics & Campus Stress Modeling

An end-to-end mathematical modeling and time-series forecasting engine designed to model academic workload, simulate student fatigue dynamics, and analyze assessment scheduling across academic terms.

🌐 **Live Interactive App:**  
https://academic-time-series-operations-analysis.streamlit.app

📂 **GitHub Repository:**  
https://github.com/saoneenandi/academic-time-series-operations-analysis

---

## 📌 Executive Summary

Traditional academic scheduling systems generally represent calendars as collections of discrete events such as examinations, quizzes, assignments, and holidays.

This project takes a different approach by modeling academic workload and student fatigue as a **continuous dynamical system**.

Discrete academic events are converted into continuous workload signals using mathematical kernel functions. These signals are then coupled with an ordinary differential equation (ODE) describing fatigue accumulation and recovery.

The system combines:

- Mathematical modeling
- Time-series analysis
- Numerical ODE integration
- Interactive parameter tuning
- Scenario simulation
- Schedule optimization
- Data visualization

The computational pipeline can be summarized as:

**Academic Calendar → Workload Stress Signal → Fatigue ODE → Numerical Integration → Risk Analysis → Schedule Optimization**

The platform converts curriculum structures such as examination dates, quiz deadlines, course credit weights, and recovery intervals into continuous time-series analytics.

---

# 🌟 Key Features

## 1. Continuous ODE Stress Engine

Models fatigue accumulation and recovery using a continuous differential equation rather than treating academic events as independent observations.

## 2. Full 10-Semester Curriculum Presets

The application includes curriculum presets covering all 10 semesters of a **5-year Integrated M.Sc. Mathematics & Computing program**.

Courses are categorized into:

- Theory
- Laboratory
- Sessional

Course credit weights are incorporated into the workload model.

## 3. Dynamic Course & Credit Editor

The interactive dashboard allows users to:

- Add custom subjects
- Modify course credits
- Change evaluation types
- Adjust assessment schedules
- Experiment with different curriculum configurations

## 4. Subject-Wise Stress Decomposition

The model decomposes the total workload signal into individual course contributions.

Stacked-area visualizations help identify which subjects contribute most strongly to workload peaks.

## 5. What-If Scenario Simulator

Users can modify assessment schedules and compare the resulting fatigue trajectories against a baseline configuration.

This enables schedule changes to be evaluated computationally before implementation.

## 6. Automated Schedule Optimizer

A grid-search optimization heuristic evaluates alternative examination placements and searches for schedules that reduce peak modeled fatigue.

## 7. Automated Risk Advisory

The system detects sustained high-fatigue windows and generates risk indicators based on configurable fatigue thresholds.

> The advisory system is a mathematical simulation tool and should not be interpreted as a clinical assessment of student mental health.

## 8. Weekly Fatigue Heatmap

The application generates a weekly workload/fatigue matrix representing academic intensity across days of the week and academic weeks.

## 9. Data Export

Simulation results can be exported as CSV files for:

- Further statistical analysis
- Operational research
- Reporting
- Visualization
- Downstream modeling

---

# 🧮 Mathematical Formulation

## 1. Cumulative Campus Stress Signal $S(t)$

Let

$$
t \in [0,T]
$$

denote continuous academic time measured in days across an academic term.

The instantaneous workload stress is modeled using a baseline component together with Gaussian examination kernels and asymmetric quiz/deadline pressure:

$$
S(t)
=
S_0
+
\sum_{i \in \text{Exams}}
w_i
\exp\left(
-\frac{(t-t_i)^2}{2\sigma^2}
\right)
+
\sum_{j \in \text{Quizzes}}
w_j
\exp\left(
\frac{t-t_j}{\lambda}
\right),
\qquad t \leq t_j
$$

where:

| Parameter | Description | Default / Range |
|---|---|---|
| $S_0$ | Baseline daily academic friction | $0.5$ |
| $w_i, w_j$ | Course credit weights | Curriculum-dependent |
| $t_i$ | Examination date | Schedule-dependent |
| $t_j$ | Quiz/deadline date | Schedule-dependent |
| $\sigma$ | Examination preparation/review window | $2.5$ |
| $\lambda$ | Deadline-pressure accumulation parameter | $3.0$ |

The Gaussian kernel represents preparation and recovery pressure surrounding major examinations, while the asymmetric exponential term represents increasing pressure as a quiz or deadline approaches.

---

# 2. Student Fatigue Differential Equation

Let $F(t)$ represent the modeled cumulative academic fatigue.

Its evolution is governed by:

$$
\frac{dF(t)}{dt}
=
\alpha S(t)
-
\beta F(t)\left(1-H(t)\right)
$$

where:

| Parameter | Description | Value / Range |
|---|---|---|
| $\alpha$ | Stress vulnerability coefficient | $0.05 \leq \alpha \leq 0.50$ |
| $\beta$ | Recovery/dissipation coefficient | $0.01 \leq \beta \leq 0.20$ |
| $H(t)$ | Institutional rest-capacity mask | $[0,1]$ |

The rest-capacity mask is modeled approximately as:

$$
H(t)=
\begin{cases}
0.5, & \text{weekends} \\
1.0, & \text{mid-term breaks} \\
0.0, & \text{instructional days}
\end{cases}
$$

The first term,

$$
\alpha S(t),
$$

represents fatigue accumulation caused by academic workload.

The second term,

$$
\beta F(t)(1-H(t)),
$$

represents modeled fatigue dissipation.

---

# 3. Numerical Integration

The fatigue trajectory $F(t)$ is evaluated numerically over:

$$
t \in [0,T]
$$

using an adaptive **Runge-Kutta 4th/5th Order (RK45)** numerical integration scheme.

The general RK formulation is:

$$
F_{n+1}
=
F_n
+
h
\sum_{i=1}^{s}b_i k_i
$$

with

$$
k_i
=
f
\left(
t_n+c_i h,
F_n+h\sum_{j=1}^{i-1}a_{ij}k_j
\right)
$$

The adaptive solver allows the system to resolve changes in the fatigue trajectory while maintaining numerical accuracy.

---

# 🏗️ System Architecture

```text
             CURRICULUM & CALENDAR CONFIGURATION
             (Integrated M.Sc. Semesters 1–10 / Custom Input)
                                │
                                ▼
             ┌─────────────────────────────────────┐
             │          streamlit_app.py            │
             │                                     │
             │  • Interactive Dashboard & UI       │
             │  • Dynamic Course & Credit Editor   │
             └──────────────────┬──────────────────┘
                                │
                                ▼
             ┌─────────────────────────────────────┐
             │       StressSimulationEngine        │
             │                                     │
             │  • Stress Heuristic Kernels S(t)    │
             │  • Subject-Level Decomposition      │
             │  • SciPy RK45 ODE Numerical Solver  │
             └──────────────────┬──────────────────┘
                                │
                ┌───────────────┴────────────────┐
                ▼                                ▼
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│      What-If & Optimization      │  │     Visualizations & Exports    │
│                                 │  │                                 │
│ • Scenario Comparison Curves    │  │ • Subject Stress Plots          │
│ • Fatigue Threshold Analysis    │  │ • Weekly Fatigue Heatmaps      │
│ • Grid-Search Schedule Optimizer│  │ • CSV Simulation Data Export   │
└─────────────────────────────────┘  └─────────────────────────────────┘
```

---

# 📂 Repository Structure

```text
academic-time-series-operations-analysis/
│
├── .streamlit/
│   └── config.toml
│       # Custom Streamlit layout and theme settings
│
├── app/
│   └── streamlit_app.py
│       # Main application, mathematical engine & UI dashboard
│
├── Dockerfile
│   # Containerization configuration
│
├── README.md
│   # Project documentation
│
└── requirements.txt
    # Python dependencies
```

---

# 🚀 Quick Start

## 1. Online Access

The application is available as an interactive Streamlit dashboard:

**Live Dashboard:**  
https://academic-time-series-operations-analysis.streamlit.app

---

## 2. Local Installation

### Clone the Repository

```bash
git clone https://github.com/saoneenandi/academic-time-series-operations-analysis.git
cd academic-time-series-operations-analysis
```

### Create a Virtual Environment

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app/streamlit_app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

---

# 🐳 Docker Deployment

## Build the Docker Image

```bash
docker build -t academic-stress-analytics .
```

## Run the Container

```bash
docker run -p 8501:8501 academic-stress-analytics
```

Then access the application at:

```text
http://localhost:8501
```

---

# 💻 Usage Guide

## 1. Launch the Interactive Dashboard

Run:

```bash
streamlit run app/streamlit_app.py
```

The dashboard allows users to:

- Adjust stress parameters
- Tune $\alpha$ and $\beta$
- Modify examination schedules
- Add or remove courses
- Change credit weights
- Inspect stress trajectories
- Analyze fatigue accumulation
- Compare alternative schedules

---

## 2. Explore Parameter Sensitivity

Users can investigate how changes in:

- Stress vulnerability $\alpha$
- Recovery rate $\beta$
- Examination spacing
- Credit distribution
- Rest intervals

affect the resulting fatigue trajectory.

This provides a simple sensitivity-analysis framework for understanding how model parameters influence system behavior.

---

## 3. Run What-If Scenarios

Users can modify assessment dates and compare:

$$
F_{\text{baseline}}(t)
$$

against:

$$
F_{\text{modified}}(t)
$$

to evaluate the modeled effect of alternative schedules.

---

# 📈 Sample Outputs & Visualizations

## Operational Velocity & Stress vs. Fatigue

Chronological time-series visualizations track:

- Workload stress $S(t)$
- Fatigue trajectory $F(t)$
- Examination and assessment pressure
- Changes in workload intensity

## Weekly Structural Fatigue Heatmap

A:

$$
7 \times 17
$$

matrix maps modeled workload/fatigue intensity across:

- 7 days of the week
- 17 academic weeks

## Subject-Level Stress Decomposition

Stacked-area plots decompose the overall workload signal into individual subject contributions.

This allows users to identify which courses are responsible for major workload peaks.

---

# 💡 Key Results & Insights

## Non-Linear Burnout Dynamics

The simulation indicates that tightly clustered examination schedules can produce compounding fatigue peaks.

For example, in the tested model configurations, examination intervals of fewer than approximately **3 days** can result in:

$$
F(t) > 2.5 \times \text{baseline}
$$

Increasing examination intervals by approximately **48–72 hours** allows the modeled recovery mechanism to operate for longer periods.

Under the tested parameter configurations, this produced peak-fatigue reductions of up to approximately **42%**.

> These figures are simulation results produced by the mathematical model and should not be interpreted as empirically validated measurements of actual student burnout.

---

## Subject-Level Stress Drivers

In the tested curriculum configuration, higher-credit core theory courses contribute more than approximately **65% of modeled peak stress**.

Spreading quiz and assessment timelines for lower-credit laboratory courses can also reduce short-term workload concentration and smooth the modeled fatigue trajectory.

---

# 🔬 Modeling Interpretation

The project can be viewed as a compact **academic operations research and scientific computing framework**.

Instead of representing an academic calendar as a static sequence of events, the system treats it as a continuous dynamical process:

$$
\text{Academic Calendar}
\rightarrow
S(t)
\rightarrow
F(t)
\rightarrow
\text{Risk Analysis}
\rightarrow
\text{Optimization}
$$

The complete modeling pipeline is:

```text
Discrete Academic Events
          │
          ▼
Continuous Workload Kernels
          │
          ▼
Academic Stress Signal S(t)
          │
          ▼
Fatigue Differential Equation
          │
          ▼
Numerical ODE Integration
          │
          ▼
Time-Series Analytics
          │
          ▼
Risk Detection & Visualization
          │
          ▼
Assessment Schedule Optimization
```

---

# 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **NumPy** | Numerical computation |
| **SciPy** | RK45 ODE integration |
| **Pandas** | Data manipulation |
| **Plotly** | Interactive visualization |
| **Streamlit** | Interactive web application |
| **Docker** | Containerization |

---

# 📊 Potential Applications

The framework can potentially be extended to:

- Academic timetable optimization
- Examination scheduling
- Workload balancing
- Curriculum design
- Assessment-spacing analysis
- Student-support analytics
- Institutional operations research
- Scenario-based academic planning

More generally, the mathematical structure can be adapted to other systems in which workload accumulates over time and subsequently dissipates through recovery mechanisms.

---

# 🔮 Future Extensions

Potential future directions include:

- Multi-student heterogeneous fatigue models
- Empirical calibration using anonymized workload data
- Stochastic stress models
- Reinforcement-learning-based schedule optimization
- Bayesian parameter estimation
- Multi-objective schedule optimization
- Semester-to-semester fatigue carryover
- Course dependency modeling
- Real-world institutional timetable integration
- Statistical validation against observed academic outcomes

---

# ⚠️ Model Scope & Limitations

This project is a **mathematical and computational simulation framework**, not a validated psychological or medical model.

The fatigue variable $F(t)$ represents a modeled quantity derived from academic workload and recovery assumptions. It does not directly measure:

- Clinical burnout
- Mental health
- Psychological well-being
- Individual student behavior
- Sleep
- Personal circumstances

The current model is therefore best interpreted as an **operational workload simulation and scheduling-analysis tool**.

Future empirical calibration and validation would be required before using the framework for real-world institutional decision-making.

---

# 📜 License

This project is distributed under the **MIT License**.

See the `LICENSE` file for details.

---

# 👤 Author

**Saonee Nandi**

Integrated M.Sc. Mathematics & Computing  
Birla Institute of Technology, Mesra

**GitHub:**  
https://github.com/saoneenandi
````
