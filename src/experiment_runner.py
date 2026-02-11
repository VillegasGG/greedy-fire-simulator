"""
Run experiments: rollout and parallel rollout, for k = [1,2,3]
"""

from execute_rollout import run_rollout
from execute_parallel import run_parallel

if __name__ == "__main__":
    k = [1, 2, 3]

    for k_i in k:
        print(f"Running rollout for k={k_i}")
        run_rollout(k_i)

        print(f"Running parallel rollout for k={k_i}")
        run_parallel(k_i)