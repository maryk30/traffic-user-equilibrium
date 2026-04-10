# CVXPY Analysis

## Method
Convex optimization using Disciplined Convex Programming (DCP)

## Solver
- SCS (primary)
- Clarabel (attempted but unstable in large cases)

## Key Idea
Automatically transforms problem into conic form.

## Strengths
- Very easy model formulation
- Handles convex nonlinear problems cleanly
- Good scalability with scaling applied

## Challenges
- Numerical instability due to x⁵ growth in BPR integral
- Requires scaling for large networks
- Some solver failures in dense grids

## Scaling Fix
- Demand and capacity scaled by factor 100
- Restored numerical stability
- Improved convergence significantly

## Results
- Accurate equilibrium flows
- Stable on Sioux Falls after scaling
- Sensitive to unscaled nonlinear terms