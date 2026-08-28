import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd

class CampusMathEngine:
    def __init__(self, semester_days=120, alpha=0.18, beta=0.07):
        self.T = semester_days
        self.alpha = alpha
        self.beta = beta

    def continuous_stress_heuristic(self, t, exams, projects):
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
        S_t = self.continuous_stress_heuristic(t, exams, projects)
        return [self.alpha * S_t - self.beta * F[0] * (1.0 - H_t)]

    def solve(self, events, holiday_mask):
        t_eval = np.linspace(0, self.T, self.T * 5)
        sol = solve_ivp(
            fun=self.fatigue_ode,
            t_span=(0, self.T),
            y0=[0.0],
            t_eval=t_eval,
            args=(events.get('exams', []), events.get('projects', []), holiday_mask),
            method='RK45'
        )
        stress_vals = [self.continuous_stress_heuristic(t, events.get('exams', []), events.get('projects', [])) for t in sol.t]
        return pd.DataFrame({'time_day': sol.t, 'stress_index': stress_vals, 'fatigue_level': sol.y[0]})
