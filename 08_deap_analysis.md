# DEAP Analysis

## Method
Genetic Algorithm (evolutionary optimization)

## Representation
- Single variable flow split (2-route system)
- Implicit constraint: fA + fB = demand

## Evolution Process
- Selection (tournament)
- Crossover (blend / SBX)
- Mutation (Gaussian / polynomial)
- Fitness: Beckmann cost

## Strengths
- No gradient required
- Works on complex or unknown objective functions
- Flexible and robust

## Limitations
- Slower convergence
- Stochastic results
- Requires tuning

## Results
- Approximates Wardrop equilibrium
- Stable convergence (~100 generations)
- Good for non-convex extensions