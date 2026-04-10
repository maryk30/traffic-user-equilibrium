# Python Optimization Platforms for Traffic Flow Analysis

## Overview
This project compares multiple Python optimization libraries applied to the Traffic Assignment Problem (TAP) under the User Equilibrium (Wardrop’s First Principle).

The problem is formulated using the Beckmann transformation and the BPR congestion model.

## Libraries Compared
- SciPy (gradient-based nonlinear optimization)
- CVXPY (convex optimization DSL)
- Pyomo (algebraic modeling + external solvers)
- Python-MIP (integer linear optimization)
- DEAP (genetic algorithms)

## Problem Summary
We solve traffic flow allocation across networks where:

- Travel time increases with congestion (BPR function)
- Total demand must be satisfied
- Users act selfishly (User Equilibrium)

## Networks Used
- Braess Paradox network (validation)
- Grid networks (scalability stress test)
- Chain networks (baseline scaling)
- Sioux Falls network (real-world benchmark)

## Key Output Metrics
- Total System Travel Time (TSTT)
- Beckmann objective value
- Runtime (CPU + wall time)
- Memory usage
- Constraint feasibility