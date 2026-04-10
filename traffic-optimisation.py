import numpy as np
from scipy.optimize import minimize

# =========================
# Traffic Network (Basic)
# =========================

def bpr(t0, x, c, alpha=0.15, beta=4):
    return t0 * (1 + alpha * (x / c) ** beta)

def beckmann_integral(t0, x, c, alpha=0.15, beta=4):
    return t0 * (x + alpha * c * (x / c) ** (beta + 1) / (beta + 1))

# =========================
# SciPy (User Equilibrium)
# =========================

def scipy_user_equilibrium(t0, c, demand):
    n = len(t0)

    def objective(x):
        return np.sum([
            beckmann_integral(t0[i], x[i], c[i]) for i in range(n)
        ])

    constraints = ({
        "type": "eq",
        "fun": lambda x: np.sum(x) - demand
    })

    bounds = [(0, None) for _ in range(n)]
    x0 = np.ones(n) * demand / n

    res = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=constraints)
    return res.x


# =========================
# CVXPY (Convex Form)
# =========================

def cvxpy_user_equilibrium():
    import cvxpy as cp

    n = 3
    demand = 100

    x = cp.Variable(n)

    t0 = np.array([1.0, 1.2, 1.5])
    c = np.array([100, 100, 100])

    alpha, beta = 0.15, 4

    cost = cp.sum([
        t0[i] * (x[i] + alpha * c[i] * cp.power(x[i] / c[i], beta + 1) / (beta + 1))
        for i in range(n)
    ])

    prob = cp.Problem(
        cp.Minimize(cost),
        [cp.sum(x) == demand, x >= 0]
    )

    prob.solve(solver=cp.SCS)
    return x.value


# =========================
# Python-MIP (Linear Approx)
# =========================

def mip_example():
    from mip import Model, xsum, MAXIMIZE, INTEGER

    m = Model()

    x = [m.add_var(var_type=INTEGER, lb=0, ub=100) for _ in range(3)]

    m.objective = xsum([3 * x[i] for i in range(3)])
    m.sense = MAXIMIZE

    m += xsum(x) <= 100

    m.optimize()

    return [v.x for v in x]


# =========================
# DEAP Genetic Algorithm
# =========================

def deap_ga():
    from deap import base, creator, tools, algorithms
    import random
    import numpy as np

    demand = 100
    n_routes = 3

    def fitness(ind):
        x = np.array(ind)
        x = np.clip(x, 0, demand)

        # force feasibility
        x = x / np.sum(x) * demand

        cost = np.sum(x**2)
        return (cost,)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, 0, demand)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=n_routes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", fitness)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=50, sigma=20, indpb=0.3)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=40)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=50, verbose=False)

    best = tools.selBest(pop, 1)[0]
    x = np.array(best)

    # normalize to demand
    x = x / np.sum(x) * demand
    return x

def print_results(title, x, t0, c):
    x = np.array(x)
    n = len(x)

    # truncate or extend safely
    t0 = np.array(t0[:n])
    c = np.array(c[:n])

    times = t0 * (1 + 0.15 * (x / c) ** 4)
    tstt = np.sum(x * times)

    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)

    for i in range(n):
        print(f"Route {i+1}:")
        print(f"  Flow = {x[i]:.4f}")
        print(f"  Travel time = {times[i]:.4f}")

    print(f"\nTotal System Travel Time (TSTT): {tstt:.4f}")

# =========================
# Run Example
# =========================

if __name__ == "__main__":
    t0 = np.array([1.0, 1.5, 2.0])
    c = np.array([100, 120, 150])
    demand = 100

    scipy_sol = scipy_user_equilibrium(t0, c, demand)
    cvxpy_sol = cvxpy_user_equilibrium()
    mip_sol = mip_example()
    deap_sol = deap_ga()

    print_results("SciPy (User Equilibrium)", scipy_sol, t0, c)
    print_results("CVXPY (Convex Optimization)", cvxpy_sol, t0, c)
    print_results("MIP (Discrete Approximation)", mip_sol, t0, c)
    print_results("DEAP (Genetic Algorithm)", [deap_sol[0], demand - deap_sol[0]], t0, c)