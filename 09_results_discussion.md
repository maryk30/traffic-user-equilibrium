# Results and Discussion

## Braess Paradox
All frameworks correctly identified:

- Adding a shortcut increased total system travel time
- Confirms non-intuitive nature of user equilibrium

## Performance Comparison

### SciPy
- Fast and stable
- Best numerical precision
- Strong baseline method

### CVXPY
- Best modeling simplicity
- Requires scaling for stability
- Good medium-to-large performance

### Pyomo
- Most flexible modeling framework
- Solver dependency is a limitation

### Python-MIP
- Excellent for discrete optimization
- Not suitable for nonlinear traffic models

### DEAP
- Most flexible in objective type
- Slowest but most general
- Good for simulation-based systems

## Key Insight
- Deterministic solvers (SciPy, CVXPY) outperform heuristics in precision
- Evolutionary methods are useful when structure is unknown
- Scaling is critical for nonlinear congestion models

## Final Conclusion
No single library dominates all metrics:
- SciPy → best numerical baseline
- CVXPY → best modeling abstraction
- DEAP → best flexibility
- Pyomo → best structural modeling
- MIP → best discrete optimization