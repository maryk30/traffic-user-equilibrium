import numpy as np

import matplotlib.pyplot as plt
from scipy.optimize import minimize
from traffic_optimisation import run_all_models

# =========================
# BPR Model
# =========================

def bpr(t0, x, c, alpha=0.15, beta=4):
    return t0 * (1 + alpha * (x / c) ** beta)


def beckmann_integral(t0, x, c, alpha=0.15, beta=4):
    return t0 * (x + alpha * c * (x / c) ** (beta + 1) / (beta + 1))


# =========================
# SciPy UE
# =========================

def scipy_ue(t0, c, demand):
    n = len(t0)

    def obj(x):
        return np.sum([beckmann_integral(t0[i], x[i], c[i]) for i in range(n)])

    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - demand})
    bounds = [(0, None)] * n
    x0 = np.ones(n) * demand / n

    res = minimize(obj, x0, method="SLSQP", bounds=bounds, constraints=cons)
    return res.x


# =========================
# CVXPY UE
# =========================

def cvxpy_ue():
    import cvxpy as cp

    n = 3
    demand = 100

    t0 = np.array([1.0, 1.5, 2.0])
    c = np.array([100, 120, 150])
    alpha, beta = 0.15, 4

    x = cp.Variable(n)

    cost = cp.sum([
        t0[i] * (x[i] + alpha * c[i] * cp.power(x[i] / c[i], beta + 1) / (beta + 1))
        for i in range(n)
    ])

    prob = cp.Problem(cp.Minimize(cost), [cp.sum(x) == demand, x >= 0])
    prob.solve(solver=cp.SCS)

    return x.value


# =========================
# MIP (toy)
# =========================

def mip_model():
    from mip import Model, xsum, INTEGER

    m = Model()

    x = [m.add_var(var_type=INTEGER, lb=0, ub=100) for _ in range(3)]

    m.objective = xsum([2 * x[i] for i in range(3)])
    m.sense = "MAX"

    m += xsum(x) <= 100

    m.optimize()

    return np.array([v.x for v in x])


# =========================
# DEAP GA
# =========================

def deap_model():
    from deap import base, creator, tools, algorithms
    import random

    demand = 100
    n = 3

    def fitness(ind):
        x = np.array(ind)
        x = np.clip(x, 0, demand)
        x = x / np.sum(x) * demand
        return (np.sum(x**2),)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr", random.uniform, 0, demand)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr, n=n)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", fitness)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=50, sigma=15, indpb=0.3)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=40)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=40, verbose=False)

    best = tools.selBest(pop, 1)[0]
    x = np.array(best)
    x = x / np.sum(x) * demand
    return x


# =========================
# Metrics
# =========================

def compute_times(x, t0, c):
    return t0 * (1 + 0.15 * (x / c) ** 4)


def TSTT(x, t):
    return np.sum(x * t)


# =========================
# Run all models
# =========================

def run_all_models():
    t0 = np.array([1.0, 1.5, 2.0])
    c = np.array([100, 120, 150])
    demand = 100

    results = {}

    results["SciPy"] = scipy_ue(t0, c, demand)
    results["CVXPY"] = cvxpy_ue()
    results["MIP"] = mip_model()
    results["DEAP"] = deap_model()

    return results, t0, c


# =========================
# VISUALISATION
# =========================

def plot_results(results, t0, c):
    models = list(results.keys())

    # -------- Flow Plot --------
    plt.figure()
    for m in models:
        plt.plot(results[m], marker='o', label=m)

    plt.title("Route Flow Comparison")
    plt.xlabel("Route")
    plt.ylabel("Flow")
    plt.legend()
    plt.grid()
    plt.show()

    # -------- Travel Time Plot --------
    plt.figure()
    for m in models:
        t = compute_times(results[m], t0, c)
        plt.plot(t, marker='o', label=m)

    plt.title("Travel Time Comparison")
    plt.xlabel("Route")
    plt.ylabel("Travel Time")
    plt.legend()
    plt.grid()
    plt.show()

    # -------- TSTT Bar Chart --------
    plt.figure()

    tstt_values = []
    for m in models:
        t = compute_times(results[m], t0, c)
        tstt_values.append(TSTT(results[m], t))

    plt.bar(models, tstt_values)

    plt.title("Total System Travel Time (TSTT)")
    plt.ylabel("TSTT")
    plt.grid(axis='y')
    plt.show()


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    results, t0, c = run_all_models()
    plot_results(results, t0, c)