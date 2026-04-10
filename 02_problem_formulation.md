# Problem Formulation

## Traffic Network Representation
A traffic network is modeled as:

G = (N, A)

Where:
- N = set of nodes
- A = set of links

Each link has:
- Free flow travel time t₀
- Capacity c
- Flow x

## BPR Function

t(x) = t₀ (1 + α (x / c)^β)

Where:
- α = congestion sensitivity
- β = nonlinear growth factor

## Beckmann Formulation

The User Equilibrium is solved as:

min ∑ ∫₀ˣ t(w) dw

This transforms equilibrium into a convex optimization problem.

## Constraints
- Flow conservation: Ax = d
- Non-negativity: x ≥ 0
- Demand satisfaction: all OD demand is assigned