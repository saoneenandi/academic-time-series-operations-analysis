# ⚡ Academic Time-Series Operational Analytics
### Student Fatigue Dynamics & Campus Stress Modeling

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://academic-time-series-operations-analysis.streamlit.app/)
[![SciPy](https://img.shields.io/badge/SciPy-ODE%20Solver-green.svg)](https://scipy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75.svg)](https://plotly.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> **A mathematical and computational framework for representing academic workload as a continuous dynamical system, simulating modeled fatigue trajectories, performing sensitivity analysis, and exploring assessment-schedule optimization.**

🌐 **Live Interactive App:**  
https://academic-time-series-operations-analysis.streamlit.app/

💻 **GitHub Repository:**  
https://github.com/saoneenandi/academic-time-series-operations-analysis

---

# 📌 Executive Summary

Academic workload is commonly represented as a discrete collection of classes, assignments, quizzes, projects, and examinations.

This project explores an alternative mathematical representation:

> **Can a discrete academic calendar be transformed into a continuous workload signal and subsequently analyzed as a dynamical system?**

The framework maps academic events into a continuous stress signal \(S(t)\), which acts as a forcing function for a fatigue state \(F(t)\).

The resulting system is solved numerically using an adaptive Runge–Kutta method.

The overall computational pipeline is:

```text
Academic Calendar
       ↓
Assessment / Workload Events
       ↓
Continuous Stress Signal S(t)
       ↓
Fatigue Differential Equation
       ↓
Numerical ODE Integration
       ↓
Time-Series Analysis
       ↓
Scenario Comparison
       ↓
Schedule Optimization
```

The project combines:

- Mathematical modeling
- Ordinary differential equations
- Numerical analysis
- Time-series simulation
- Parameter sensitivity
- Scenario analysis
- Schedule optimization
- Scientific visualization
- Interactive scientific computing

---

# 🎯 Research Motivation

The project investigates several mathematical and computational questions:

1. How can discrete academic events be represented as continuous forcing functions?
2. How does a dynamical system respond to different workload distributions?
3. How sensitive are modeled fatigue trajectories to system parameters?
4. How does assessment spacing influence maximum modeled fatigue?
5. Can numerical simulation be combined with schedule search to identify lower-peak workload configurations?
6. How can mathematical models be exposed through an interactive computational environment?

The project therefore sits at the intersection of:

- **Ordinary Differential Equations**
- **Dynamical Systems**
- **Numerical Analysis**
- **Computational Mathematics**
- **Time-Series Modeling**
- **Operations Research**
- **Optimization**
- **Scientific Computing**

---

# 🧮 Mathematical Formulation

## 1. Continuous Academic Stress Signal

Let

$$
t \in [0,T]
$$

represent continuous academic time measured in days over an academic term.

The instantaneous workload stress is modeled as:

**S(t) = S₀ + Σᵢ wᵢ exp(−(t − tᵢ)² / (2σ²)) + Σⱼ wⱼ exp((t − tⱼ) / λ),  t ≤ tⱼ**

### Parameters

| Parameter | Meaning | Default / Range |
|---|---|---|
| **S₀** | Baseline daily academic workload | 0.5 |
| **wᵢ, wⱼ** | Course / assessment weights | Curriculum-dependent |
| **tᵢ** | Examination date | Schedule-dependent |
| **tⱼ** | Quiz or deadline date | Schedule-dependent |
| **σ** | Examination preparation/review width | 2.5 |
| **λ** | Deadline-pressure accumulation parameter | 3.0 |

The Gaussian kernel represents distributed preparation and review pressure around major examinations.

The asymmetric exponential component represents increasing pressure as a quiz or deadline approaches.

This transformation is important because it converts a **discrete event schedule into a continuous forcing function** that can be studied using differential equations.

---

## 2. Fatigue Dynamical Model

Let **F(t)** represent the modeled cumulative academic fatigue or strain state.

Its evolution is governed by the following differential equation:

$$
\frac{dF(t)}{dt} = \alpha S(t) - \beta F(t)(1-H(t))
$$

where:

| Parameter | Meaning | Range |
|---|---|---|
| **α** | Workload-to-fatigue accumulation coefficient | 0.05 ≤ α ≤ 0.50 |
| **β** | Fatigue dissipation / recovery coefficient | 0.01 ≤ β ≤ 0.20 |
| **H(t)** | Institutional rest-capacity function | 0 ≤ H(t) ≤ 1 |

The model contains two competing mechanisms:

$$
\alpha S(t)
$$

**Workload-driven accumulation**

and

$$
\beta F(t)(1-H(t))
$$

**Fatigue dissipation / recovery**

The first term increases the modeled fatigue state in response to academic workload.

The second term represents modeled fatigue dissipation, with the rest-capacity function **H(t)** modifying the effective recovery available to the system.

---

# 3. Rest-Capacity Function

The current model uses a simple calendar-dependent rest-capacity function:

$$
H(t)=
\begin{cases}
1.0, & \text{during mid-term breaks},\\
0.5, & \text{during weekends},\\
0.0, & \text{during instructional days}.
\end{cases}
$$

For an instructional day:

$$
H(t)=0
$$

and therefore:

**dF/dt = αS(t) − βF(t)**

where **dF/dt** represents the rate of change of the modeled fatigue state, **αS(t)** represents workload-driven accumulation, and **βF(t)** represents fatigue dissipation.

This provides a simple mechanism for incorporating calendar-dependent recovery into the dynamical system.

---

# 4. Numerical Integration

The fatigue trajectory is computed over:

$$
t \in [0,T]
$$

using an adaptive **Runge–Kutta 4th/5th-order (RK45)** numerical integration scheme.

The general Runge–Kutta update is:

<div align="center">

**Fₙ₊₁ = Fₙ + h Σᵢ₌₁ˢ bᵢ kᵢ**

</div>

where the stage evaluations are:

<div align="center">

**kᵢ = f(tₙ + cᵢh, Fₙ + h Σⱼ₌₁ⁱ⁻¹ aᵢⱼkⱼ)**

</div>

The implementation uses SciPy's adaptive **RK45** solver to numerically integrate the fatigue ODE.

---

# 5. Parameter Sensitivity

The model exposes \(\alpha\) and \(\beta\) for controlled sensitivity experiments.

Increasing \(\alpha\):

$$
\alpha \uparrow
\quad\Longrightarrow\quad
\text{stronger workload-driven accumulation}
$$

Increasing \(\beta\):

$$
\beta \uparrow
\quad\Longrightarrow\quad
\text{faster modeled dissipation}
$$

Sensitivity experiments can investigate:

- Examination spacing
- Course credit distribution
- Quiz placement
- Recovery intervals
- Baseline workload

---

# 6. Schedule Optimization

For a candidate schedule \(\mathcal{S}\), let the resulting fatigue trajectory be:

$$
F_{\mathcal{S}}(t).
$$

A natural optimization objective is to minimize the maximum modeled fatigue over the academic term:

$$
\boxed{
\min_{\mathcal{S}}
\;
\max_{t\in[0,T]}
F_{\mathcal{S}}(t)
}
$$

subject to the relevant scheduling constraints.

The computational mapping is:

$$
\mathcal{S}
\longrightarrow
S_{\mathcal{S}}(t)
\longrightarrow
F_{\mathcal{S}}(t)
\longrightarrow
\max_t F_{\mathcal{S}}(t).
$$

The current implementation uses **grid search** as an interpretable optimization baseline rather than presenting the problem as a general optimal-control solution.

---

# 🔬 Computational Experiments

A typical experiment follows:

```text
Baseline Schedule
        ↓
Generate S(t)
        ↓
Integrate F(t)
        ↓
Measure Peak Fatigue
        ↓
Modify Schedule
        ↓
Re-run Simulation
        ↓
Compare Trajectories
```

The framework allows controlled modification of:

- Examination dates
- Quiz dates
- Course weights
- Recovery intervals
- \(\alpha\)
- \(\beta\)

This makes the application useful as a computational sandbox for studying the behavior of the proposed mathematical model.

---

# 🔄 What-If Scenario Analysis

Alternative assessment schedules can be compared against a baseline.

For example:

```text
Scenario A
Closely clustered examinations

        versus

Scenario B
Examinations separated by additional recovery time
```

The resulting trajectories can be compared using:

- Peak modeled fatigue
- Timing of fatigue peaks
- Duration of high-fatigue intervals
- Subject-level contributions
- Overall workload distribution

---

# 🔎 Schedule Optimization

Candidate examination schedules are generated and evaluated through numerical simulation.

The optimization workflow is:

```text
Candidate Schedule
       ↓
Generate S(t)
       ↓
Numerically Integrate F(t)
       ↓
Calculate Peak F(t)
       ↓
Compare Candidate Schedules
       ↓
Select Lower-Peak Schedule
```

This is intended as an interpretable baseline for future optimization research.

---

# 📊 Key Outputs

## 📈 Stress and Fatigue Time Series

The dashboard visualizes:

- Workload stress \(S(t)\)
- Modeled fatigue \(F(t)\)
- Examination pressure
- Assessment workload
- Changes in academic intensity

---

## 📚 Subject-Level Decomposition

Stacked-area plots decompose the total workload signal into individual course contributions.

This allows inspection of which subjects contribute most strongly to modeled workload peaks.

---

## 🗓️ Weekly Heatmap

The application represents modeled workload and fatigue intensity using a:

$$
7 \times 17
$$

matrix corresponding to:

- 7 days of the week
- 17 academic weeks

---

## ⚠️ Risk Windows

The advisory component identifies sustained high-fatigue regions using configurable thresholds.

> **Important:** This is a mathematical simulation component and is not a clinical, psychological, or medical diagnostic system.

---

# 📈 Simulation Findings

Under the tested model configurations, tightly clustered examinations can produce larger modeled fatigue peaks because the recovery mechanism has less time to act between workload events.

In the tested configurations, examination intervals below approximately **3 days** produced substantially larger modeled peaks than more widely separated schedules.

Increasing examination spacing by approximately **48–72 hours** produced peak-fatigue reductions of up to approximately **42%** under the tested parameter configurations.

### Interpretation

These values are **simulation outputs**, not empirical measurements of student burnout or psychological well-being.

They should therefore be interpreted as observations about the behavior of the implemented mathematical model.

---

# 📚 Subject-Level Stress Drivers

In the tested curriculum configuration, higher-credit core theory courses contributed more than approximately **65% of modeled peak stress**.

This demonstrates how course weighting and assessment placement influence the simulated workload trajectory.

Again, this is a property of the mathematical model rather than an empirical conclusion about student psychology.

---

# 🏗️ System Architecture

```text
                    CURRICULUM & CALENDAR
                 CONFIGURATION / USER INPUT
                           │
                           ▼
              ┌─────────────────────────────┐
              │      streamlit_app.py       │
              │                             │
              │  Interactive Dashboard      │
              │  Course / Credit Editor     │
              │  Scenario Configuration     │
              └──────────────┬──────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │    StressSimulationEngine   │
              │                             │
              │  Stress Kernels S(t)        │
              │  Subject Decomposition      │
              │  SciPy RK45 ODE Solver      │
              └──────────────┬──────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
   ┌─────────────────────┐       ┌────────────────────────┐
   │ Scenario &          │       │ Visualization &        │
   │ Optimization        │       │ Data Export             │
   │                     │       │                        │
   │ What-If Analysis    │       │ Time-Series Plots      │
   │ Threshold Analysis  │       │ Heatmaps               │
   │ Grid Search         │       │ Subject Decomposition  │
   └─────────────────────┘       │ CSV Export             │
                                 └────────────────────────┘
```

---

# 📂 Repository Structure

```text
academic-time-series-operations-analysis/
│
├── .streamlit/
│   └── config.toml
│       └── Streamlit layout and theme configuration
│
├── app/
│   └── streamlit_app.py
│       └── Mathematical engine, simulation logic and dashboard
│
├── Dockerfile
│   └── Containerization configuration
│
├── README.md
│   └── Project documentation
│
├── requirements.txt
│   └── Python dependencies
│
└── LICENSE
```

---

# 🚀 Quick Start

## Clone the Repository

```bash
git clone https://github.com/saoneenandi/academic-time-series-operations-analysis.git
cd academic-time-series-operations-analysis
```

## Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app/streamlit_app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

---

# 🐳 Docker Deployment

## Build

```bash
docker build -t academic-stress-analytics .
```

## Run

```bash
docker run -p 8501:8501 academic-stress-analytics
```

Then open:

```text
http://localhost:8501
```

---

# 🧪 Reproducibility

A typical computational experiment consists of:

1. Select a curriculum configuration.
2. Define assessment dates and course weights.
3. Select model parameters \(\alpha\) and \(\beta\).
4. Generate the continuous stress signal.
5. Integrate the fatigue ODE using RK45.
6. Inspect the resulting trajectory.
7. Modify the assessment schedule.
8. Re-run the simulation.
9. Compare the resulting trajectories.
10. Export simulation data for further analysis.

The explicit model formulation makes the computational assumptions inspectable and reproducible.

---

# 🧰 Technology Stack

| Technology | Role |
|---|---|
| **Python** | Core programming language |
| **NumPy** | Numerical computation |
| **SciPy** | Adaptive RK45 ODE integration |
| **Pandas** | Data manipulation and export |
| **Plotly** | Interactive scientific visualization |
| **Streamlit** | Scientific-computing dashboard |
| **Docker** | Reproducible deployment |

---

# 🔬 Potential Research Extensions

## 1. Empirical Parameter Calibration

Estimate model parameters from anonymized workload observations rather than selecting them manually.

Possible methods include:

- Maximum likelihood estimation
- Bayesian parameter inference
- Hierarchical modeling
- Uncertainty estimation

---

## 2. Uncertainty Quantification

Treat parameters as uncertain quantities:

$$
\alpha \sim p(\alpha)
$$

and

$$
\beta \sim p(\beta).
$$

The resulting uncertainty in:

$$
F(t)
$$

could then be investigated using Monte Carlo simulation or Bayesian methods.

---

## 3. Stochastic Dynamics

A stochastic extension could take the form:

<div align="center">

**dF = [αS(t) − βF(t)(1 − H(t))]dt + σ_F dW_t**

</div>

where:

- **W_t** represents a Wiener process.
- **σ_F** represents the magnitude of stochastic fluctuations in the modeled fatigue state.
- **α** represents the workload-to-fatigue accumulation coefficient.
- **β** represents the fatigue dissipation coefficient.
- **S(t)** represents the continuous academic stress signal.
- **H(t)** represents the rest-capacity function.

The stochastic term **σ_F dW_t** introduces random fluctuations into the deterministic fatigue dynamics, allowing the model to represent uncertainty or unobserved variation in the system.

---

## 4. Heterogeneous Student Models

A population-level extension could introduce student groups with different parameters:

$$
F_k(t)
$$

with group-specific:

$$
\alpha_k,\qquad\beta_k.
$$

This would allow investigation of heterogeneous responses to the same workload forcing function.

---

## 5. Multi-Objective Scheduling

Instead of minimizing only peak fatigue, multiple objectives could be optimized:

```text
Peak Fatigue
      +
Total Workload
      +
Assessment Clustering
      +
Schedule Constraints
```

---

## 6. Learning-Based Optimization

Classical grid search could be compared with:

- Bayesian optimization
- Evolutionary algorithms
- Reinforcement learning

This would provide a bridge between mathematical optimization and data-driven methods.

---

## 7. Statistical Validation

A future version could compare model outputs with appropriately collected and anonymized academic workload observations.

Such an extension would require:

- Empirical calibration
- Statistical validation
- Uncertainty quantification
- Independent evaluation

---

## 8. Coupled Course Dynamics

The model could be extended to account for:

- Course dependencies
- Prerequisites
- Shared assessments
- Project deadlines
- Cumulative workload

This could transform the current scalar model into a higher-dimensional dynamical system.

---

## 9. Semester-to-Semester Dynamics

A future extension of the model could allow the terminal state of one semester to influence the initial condition of the following semester.

The semester-to-semester relationship can be represented as:

$$
F_{k+1}(0) = \gamma F_k(T)
$$

where:

- **F_k(T)** represents the modeled fatigue state at the end of semester **k**.
- **F_(k+1)(0)** represents the initial modeled fatigue state of semester **k+1**.
- **γ** represents the carryover factor, where **0 ≤ γ ≤ 1**.

A value of **γ = 0** represents complete recovery between semesters, while larger values represent increasing persistence of the modeled state across academic terms.

---

# 🧠 Why This Project Is Research-Relevant

The project demonstrates a complete computational modeling workflow:

```text
Problem Formulation
        ↓
Mathematical Abstraction
        ↓
Model Construction
        ↓
Numerical Solution
        ↓
Parameter Sensitivity
        ↓
Computational Experiments
        ↓
Scenario Analysis
        ↓
Optimization
        ↓
Scientific Visualization
```

The important aspect is that the project does not treat the dashboard as the primary contribution.

The dashboard is an interface through which the underlying mathematical model can be experimentally investigated.

The research-oriented workflow is:

$$
\text{Problem}
\rightarrow
\text{Mathematical Model}
\rightarrow
\text{Numerical Method}
\rightarrow
\text{Experiment}
\rightarrow
\text{Analysis}
\rightarrow
\text{Extension}
$$

This makes the project relevant to computational mathematics, numerical analysis, scientific computing, and operations research.

---

# ⚠️ Model Scope & Limitations

This repository implements a **mathematical and computational simulation framework**, not a validated psychological or medical model.

The state variable \(F(t)\) is a modeled quantity derived from assumptions about:

- Academic workload
- Assessment timing
- Course weights
- Recovery intervals
- Model parameters

It does not directly measure:

- Clinical burnout
- Mental health
- Psychological well-being
- Sleep
- Individual behavior
- Personal circumstances

The current parameterization is not empirically calibrated.

Therefore:

> **Numerical results should be interpreted as properties of the mathematical model rather than validated claims about real students.**

Real-world institutional deployment would require:

- Appropriate data collection
- Ethical safeguards
- Empirical calibration
- Uncertainty analysis
- Independent validation

---

# 📌 Current Status

## ✅ Implemented

- Continuous academic stress model
- Fatigue differential equation
- Adaptive RK45 numerical integration
- 10-semester curriculum presets
- Dynamic course and credit editing
- Subject-wise stress decomposition
- What-if schedule analysis
- Grid-search schedule optimization
- Fatigue threshold analysis
- Weekly heatmap visualization
- CSV data export
- Streamlit deployment
- Docker support

## 🔭 Planned

- Empirical parameter estimation
- Uncertainty quantification
- Stochastic modeling
- Multi-objective optimization
- Population-level modeling
- Statistical validation
- Learning-based schedule optimization
- Course dependency modeling
- Semester-to-semester dynamics

---

# 🌐 Live Application

The interactive implementation is available here:

**https://academic-time-series-operations-analysis.streamlit.app/**

---

# 👤 Author

## Saonee Nandi

**Integrated M.Sc. Mathematics & Computing**  
**Birla Institute of Technology, Mesra**

GitHub:

**https://github.com/saoneenandi**

---

# ⭐ Research-Oriented Computational Project

This repository presents an open computational framework for experimenting with:

**ODE-based workload modeling · numerical simulation · time-series analysis · sensitivity analysis · and assessment-schedule optimization**

The current implementation serves as a computational baseline for future work involving empirical calibration, uncertainty quantification, stochastic dynamics, and advanced optimization.
