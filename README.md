# ⚡ Academic Time-Series Operational Analytics
### Student Fatigue Dynamics & Campus Stress Modeling

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SciPy](https://img.shields.io/badge/SciPy-RK45%20ODE-orange.svg)](https://scipy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Visualization-3F4F75.svg)](https://plotly.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://academic-time-series-operations-analysis.streamlit.app/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**A mathematical and computational framework for modeling academic workload as a continuous dynamical system and studying how assessment schedules influence modeled fatigue trajectories.**

> **Research-oriented project:** This repository explores the intersection of **ordinary differential equations, numerical analysis, time-series modeling, optimization, and scientific computing** through an operational model of academic workload.

🌐 **Live Application:**  
https://academic-time-series-operations-analysis.streamlit.app/

💻 **Repository:**  
https://github.com/saoneenandi/academic-time-series-operations-analysis

---

# 🔬 Project Overview

Academic workload is usually represented as a discrete collection of classes, assignments, quizzes, and examinations.

This project investigates a different representation:

> **Can a discrete academic calendar be transformed into a continuous workload signal and then analyzed as a dynamical system?**

The framework maps academic events into a continuous stress signal $S(t)$, which drives a fatigue state $F(t)$. The fatigue state evolves according to a differential equation incorporating workload accumulation and recovery.

The computational pipeline is:

```text
Academic Calendar
       ↓
Workload / Assessment Events
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
