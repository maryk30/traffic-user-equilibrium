# SciPy Analysis

## Method
Uses `scipy.optimize.minimize` with SLSQP.

## Key Features
- Gradient-based optimization
- Handles constraints explicitly
- Requires manual model formulation

## Formulation Steps
- Build incidence matrix A
- Define demand vector d
- Solve:
  min Beckmann(x)
  subject to Ax = d

## Strengths
- Fast convergence
- High numerical stability
- Transparent implementation

## Limitations
- Manual modeling required
- Sensitive to formulation errors

## Results Summary
- Correct Braess paradox detection
- Low residuals (~1e-10)
- Efficient runtime (< seconds for medium networks)
- Scales reasonably to Sioux Falls