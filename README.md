# ⚡ Academic Time-Series Operational Analytics: Student Fatigue Dynamics & Campus Stress Modeling

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://academic-time-series-operations-analysis.streamlit.app/)
[![SciPy](https://img.shields.io/badge/SciPy-ODE%20Solver-green.svg)](https://scipy.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> An end-to-end mathematical modeling and time-series forecasting engine built to map campus operational velocity, simulate student fatigue trajectories, and optimize assessment placement across academic terms.

🌐 **Live Interactive App:**  
[academic-time-series-operations-analysis.streamlit.app](https://academic-time-series-operations-analysis.streamlit.app/)

📂 **GitHub Repository:**  
[github.com/saoneenandi/academic-time-series-operations-analysis](https://github.com/saoneenandi/academic-time-series-operations-analysis)

---

## 📌 Executive Summary

Traditional institutional scheduling tools treat academic calendars as static, discrete events. This framework models campus stress and student fatigue as **continuous dynamical systems** governed by non-linear kernel functions and ordinary differential equations (ODEs).

By coupling numerical ODE integration using **RK45** with real-time parameter tuning, the platform converts discrete curriculum structures — including exam dates, quiz buffers, project deadlines, course credit weights, and holiday recovery intervals — into actionable time-series analytics.

The framework generates:

- Subject-wise stress decompositions
- Continuous fatigue trajectories
- Weekly fatigue heatmaps
- Baseline vs. modified schedule comparisons
- Automated assessment scheduling recommendations
- Fatigue-risk indicators
- CSV simulation exports

The overall modeling pipeline is:

**Academic Calendar → Stress Signal → Fatigue Dynamics → Numerical Integration → Risk Analysis → Schedule Optimization**

---

## 🌟 Key Features

### ⚙️ Continuous ODE Stress Engine

Simulates fatigue accumulation and recovery using continuous differential equations.

### 📚 Full 10-Semester Curriculum Presets

Pre-loaded with complete course codes, credit distributions, and course types:

- Theory
- Lab
- Sessional

The presets cover a **5-year Integrated M.Sc. Mathematics & Computing program**.

### ✏️ Dynamic Course & Credit Editor

An interactive editor allows users to:

- Add custom subjects
- Adjust credit weights
- Modify evaluation types
- Change assessment schedules
- Experiment with different curriculum configurations

### 📊 Subject-Wise Stress Decomposition

Stacked-area visualizations isolate individual course contributions to workload and fatigue peaks across the academic term.

### 🔄 What-If Scenario Simulator

Compare baseline and modified examination schedules to evaluate the modeled impact of schedule changes before implementation.

### 🔎 Automated Schedule Optimizer

A grid-search optimization heuristic evaluates alternative examination placements to identify schedules that minimize peak modeled fatigue.

### 🤖 Automated Risk Advisory

Detects sustained high-fatigue windows and generates risk indicators based on configurable thresholds.

> The advisory component is a mathematical simulation tool and is not intended to provide clinical or psychological diagnoses.

### 🗓️ Weekly Heatmap Matrix

Provides a visual representation of workload density across a 7-day, multi-week academic calendar.

### 📥 Data Export

Simulation results can be exported as CSV files for downstream:

- Statistical analysis
- Operational research
- Reporting
- Visualization
- Modeling

---

# 🧮 Mathematical Formulation

## 1. Cumulative Campus Stress Signal $S(t)$

Let

$$
t \in [0,T]
$$

denote continuous academic time measured in days across an academic term.

The instantaneous workload stress $S(t)$ is modeled using a baseline component together with Gaussian examination kernels and asymmetric quiz/deadline pressure:

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

Where:

| Parameter | Description | Default / Range |
|---|---|---|
| $S_0$ | Baseline daily academic friction | $0.5$ |
| $w_i, w_j$ | Course credit weights | Curriculum-dependent |
| $t_i$ | Examination date | Schedule-dependent |
| $t_j$ | Quiz/deadline date | Schedule-dependent |
| $\sigma$ | Symmetric preparation/review window for major exams | $2.5$ |
| $\lambda$ | Asymmetric deadline-pressure accumulation parameter | $3.0$ |

The Gaussian kernel models preparation and review pressure surrounding major examinations, while the asymmetric exponential term models increasing pressure as a quiz or deadline approaches.

---

## 2. Student Fatigue Differential Equation

Fatigue $F(t)$ represents the **modeled cumulative academic strain** generated by workload and recovery dynamics.

The rate of change is governed by:

$$
\frac{dF(t)}{dt}
=
\alpha S(t)
-
\beta F(t)\left(1-H(t)\right)
$$

Where:

| Parameter | Description | Value / Range |
|---|---|---|
| $\alpha$ | Stress vulnerability coefficient | $0.05 \leq \alpha \leq 0.50$ |
| $\beta$ | Recovery/dissipation rate coefficient | $0.01 \leq \beta \leq 0.20$ |
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

The workload-driven accumulation component is:

$$
\alpha S(t)
$$

while the recovery component is:

$$
\beta F(t)(1-H(t))
$$

---

## 3. Numerical Integration Scheme

The continuous trajectory $F(t)$ is evaluated numerically over:

$$
t \in [0,T]
$$

using an adaptive **Runge-Kutta 4th/5th Order (RK45)** numerical integration scheme.

The general update is:

$$
F_{n+1}
=
F_n
+
h\sum_{i=1}^{s}b_i k_i
$$

where:

$$
k_i
=
f
\left(
t_n+c_i h,
F_n+h\sum_{j=1}^{i-1}a_{ij}k_j
\right)
$$

The adaptive numerical solver allows the fatigue trajectory to be integrated while adjusting the step size according to the behavior of the system.

---

# 🏗️ System Architecture

The application follows a computational pipeline connecting curriculum configuration, mathematical simulation, optimization, visualization, and data export.

```text
                  CURRICULUM & CALENDAR CONFIGURATION
            (Integrated M.Sc. Semesters 1-10 / Custom Input)
                                  │
                                  ▼
               ┌─────────────────────────────────────┐
               │         streamlit_app.py            │
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
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│     What-If & Optimization      │       │     Visualizations & Exports    │
│                                 │       │                                 │
│ • Scenario Comparison Curves    │       │ • Subject Stress Plots          │
│ • Fatigue Threshold Analysis    │       │ • Weekly Fatigue Heatmaps      │
│ • Grid-Search Exam Optimizer    │       │ • CSV Simulation Data Download  │
└─────────────────────────────────┘       └─────────────────────────────────┘
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
    # Dependencies
```

---

# 🚀 Quick Start & Installation

## 1. Online Access

The application is live and accessible directly in your browser:

👉 **[Launch Streamlit Dashboard](https://academic-time-series-operations-analysis.streamlit.app/)**

---

## 2. Local Installation

### Clone the Repository

```bash
git clone https://github.com/saoneenandi/academic-time-series-operations-analysis.git
cd academic-time-series-operations-analysis
```

### Create and Activate a Virtual Environment

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

### Run the Streamlit Application

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

## Run the Docker Container

```bash
docker run -p 8501:8501 academic-stress-analytics
```

Access the application at:

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

Users can study how changes in:

- Stress vulnerability $\alpha$
- Recovery rate $\beta$
- Examination spacing
- Credit distribution
- Rest intervals

affect the resulting fatigue trajectory.

This provides a simple sensitivity-analysis framework for studying the behavior of the mathematical model.

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
- Examination pressure
- Assessment workload
- Changes in academic intensity

---

## Weekly Structural Fatigue Heatmap

A:

$$
7 \times 17
$$

matrix maps modeled workload and fatigue intensity across:

- 7 days of the week
- 17 academic weeks

---

## Subject-Level Stress Decomposition

Stacked-area visualizations decompose the overall workload signal into individual subject contributions.

This allows users to identify which courses contribute most strongly to modeled workload peaks.

---

# 💡 Key Results & Insights

## Non-Linear Fatigue Dynamics

The simulation indicates that tightly clustered examination schedules can produce compounding fatigue peaks.

In tested model configurations, examination intervals of fewer than approximately **3 days** can produce:

$$
F(t) > 2.5 \times \text{baseline}
$$

Increasing examination intervals by approximately **48–72 hours** allows the modeled recovery mechanism to operate for longer periods.

Under the tested parameter configurations, this produced peak-fatigue reductions of up to approximately **42%**.

> These values are simulation results produced by the mathematical model and should not be interpreted as empirically validated measurements of actual student burnout.

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

The complete computational pipeline is:

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

The current model should therefore be interpreted as an **operational workload simulation and scheduling-analysis tool**.

Empirical calibration and statistical validation would be required before using the framework for real-world institutional decision-making.

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
[github.com/saoneenandi](https://github.com/saoneenandi)
