# Introduction

This study evaluates Python-based optimization tools for solving the Traffic Assignment Problem (TAP).

The focus is on **User Equilibrium (Wardrop’s Principle)**, where no driver can reduce travel time by switching routes.

Traffic congestion is modeled using the **BPR function**, making the problem nonlinear and convex.

We compare:
- Numerical solvers (SciPy)
- Convex modeling frameworks (CVXPY, Pyomo)
- Integer optimization (Python-MIP)
- Heuristic search (DEAP)

The goal is to evaluate:
- Accuracy
- Scalability
- Numerical stability
- Ease of implementation