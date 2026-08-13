# Academic Time-Series Operational Analytics: Student Fatigue Dynamics & Campus Stress Modeling

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SciPy](https://img.shields.io/badge/SciPy-ODE%20Solver-green.svg)](https://scipy.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()

> An end-to-end mathematical modeling and time-series forecasting framework designed to quantitatively map campus operational velocity and predict student burnout dynamics across standard academic terms.

---

## 📌 Executive Summary

Traditional institutional scheduling tools treat academic calendars as static discrete events. This repository formulates campus stress and student fatigue as **continuous dynamical systems** governed by continuous heuristic functions and ordinary differential equations (ODEs).

By coupling numerical ODE integration ($\text{RK45}$) with machine learning forecasting pipelines ($\text{XGBoost} / \text{LSTM}$), this framework converts discrete structural parameters—such as exam windows, project deadlines, course weightings, and holiday recovery intervals—into actionable time-series analytics, fatigue heatmaps, and systemic overload anomaly triggers.

---

## 🧮 Mathematical Formulation

### 1. Continuous Campus Stress Index ($S(t)$)
Let $t \in [0, T]$ denote time in continuous academic days across a term. The instantaneous workload stress $S(t)$ is formulated as a continuous mapping $f: \mathbb{R}^n \to \mathbb{R}$:

$$S(t) = S_0 + \sum_{i \in \text{Exams}} w_i \cdot \mathcal{K}_{\sigma_i}(t - t_i) + \sum_{j \in \text{Projects}} w_j \cdot \mathcal{A}_{\lambda_j}(t - t_j)$$

Where:
* $S_0$: Baseline daily academic friction ($S_0 \approx 0.5$).
* $w_i, w_j$: Course credit weights (e.g., $w = 4.0$ for core lectures, $w = 2.0$ for electives).
* $\mathcal{K}_{\sigma}(\tau) = \exp\left(-\frac{\tau^2}{2\sigma^2}\right)$: Symmetric Gaussian kernel representing pre-exam preparation and post-exam review pressure around date $t_i$.
* $\mathcal{A}_{\lambda}(\tau) = \mathbb{I}(\tau \le 0) \cdot \exp\left(\frac{\tau}{\lambda}\right)$: Asymmetric exponential kernel modeling deadline pressure accumulation leading up to $t_j$.

### 2. Student Fatigue Ordinary Differential Equation (ODE)
Fatigue $F(t)$ represents the cumulative psychological and cognitive strain on the student body. The rate of change $\frac{dF(t)}{dt}$ is modeled via a non-linear ODE incorporating stress accumulation and calendar-governed recovery:

$$\frac{dF(t)}{dt} = \alpha \cdot S(t) - \beta \cdot F(t) \cdot \Big(1 - H(t)\Big)$$

Where:
* $\alpha > 0$: Stress vulnerability coefficient ($\text{day}^{-1}$).
* $\beta > 0$: Baseline dissipation/recovery rate ($\text{day}^{-1}$).
* $H(t) \in [0, 1]$: Calendar recovery function defining institutional rest capacity:
  $$H(t) = \begin{cases}    1.0 & \text{if } t \in \text{Full Break / Holiday} \\    0.5 & \text{if } t \in \text{Weekend} \\    0.0 & \text{if } t \in \text{Instructional Day}    \end{cases}$$

### 3. Numerical Integration Scheme
The continuous trajectory $F(t)$ is evaluated numerically over $t \in [0, T]$ using an explicit **Runge-Kutta 4th/5th Order (RK45)** adaptive step-size scheme:

$$F_{n+1} = F_n + h \sum_{i=1}^s b_i k_i, \quad k_i = f\left(t_n + c_i h, \, F_n + h \sum_{j=1}^{i-1} a_{ij} k_j\right)$$

---

## 🏗️ System Architecture

```text
                                  ACADEMIC CALENDAR DATASETS
                                (JSON / CSV / Course Catalogs)
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │       data_parser.py            │
                             │  • Event Extractor              │
                             │  • Weight Vector Normalization  │
                             └────────────────┬────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │       math_engine.py            │
                             │  • Stress Heuristic Kernel f(t) │
                             │  • RK45 ODE Numerical Solver    │
                             └────────────────┬────────────────┘
                                              │
                         ┌────────────────────┴────────────────────┐
                         ▼                                         ▼
        ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
        │       forecasting.py            │       │        visualizer.py            │
        │  • Feature Lag Engineering      │       │  • Operational Velocity Plots   │
        │  • XGBoost / LSTM Predictor     │       │  • Weekly Burnout Heatmaps      │
        │  • Anomaly Burnout Trigger      │       │  • Anomaly Highlights           │
        └────────────────┬────────────────┘       └────────────────┬────────────────┘
                         │                                         │
                         └────────────────────┬────────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │       streamlit_app.py          │
                             │   Interactive UI & Parameter    │
                             │        Sensitivity Tuning       │
                             └─────────────────────────────────┘
