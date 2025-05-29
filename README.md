# 🔥 Greedy-fire-simulator

A modular simulator for the Firefighter Problem in trees  using a greedy strategy. 

This package models the fire spread. At each time step, the fire spreads to its neighbors that have not been protected by a firefighter.

For its part, the firefighter protects one or more nodes at each time step depending on its speed. 

Node selection is done using a greedy strategy that consists of selecting the node with the largest subtree (as long as it can reach it before the fire). In case of ties, the node that is reached the fastest is chosen. In case of ties at this point, the node to be protected is chosen arbitrarily.

### What this simulator does?

- Models fire spreading on trees.
- Simulates fire spread step by step.
- At each time step, selects the best node to protect using a greedy policy.
- Returns the results in a directory.
