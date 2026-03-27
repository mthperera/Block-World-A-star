from itertools import permutations
from math import comb, factorial
from pathlib import Path
import random
import sys
from typing import List, Any, Optional, Literal

sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import main


class Test():

    def __init__(self, 
            objects: List[Any], 
            heuristic: Literal["rmse", "blocking", "nilsson", "chamfer", "hausdorff"],
            max_tests: Optional[int] = None
        ):
        self.objects = objects
        self.heuristic = heuristic
        self.max_tests = max_tests

        n = len(self.objects)
        max_allowed = comb(2*n - 1, n) * factorial(n)

        if not self.max_tests:
            self.max_tests = max_allowed

        if self.max_tests > max_allowed:
            raise ValueError(
                f"'max_tests' ({self.max_tests}) excede o máximo permitido ({max_allowed}) para n={n}"
            )

    def _initial_block_world_states(self) -> List[List[Any]]:
        states = []
        n = len(self.objects)

        def split(lst, k):
            if k == 1:
                return [[lst]]

            result = []
            for i in range(len(lst) + 1):
                first = lst[:i]
                for rest in split(lst[i:], k - 1):
                    result.append([first] + rest)
            return result

        for perm in permutations(self.objects):
            states += split(list(perm), n)

        return states

    def run(self) -> List[int]:
        all_states = self._initial_block_world_states()

        initial_states_tests = random.sample(all_states, self.max_tests)
        goal_states_tests = random.sample(all_states, self.max_tests)

        results =[]

        for i in range(self.max_tests):

            print(f"Teste {i+1}")
            print(initial_states_tests[i])
            print(goal_states_tests[i])

            result = main(
                initial_state=initial_states_tests[i], 
                goal_state=goal_states_tests[i], 
                heuristic=self.heuristic,
                tracing=False
            )

            results.append(result.g)

            print(f"Custo: {result.g}", end="\n\n")
    
        return results


if __name__ == "__main__":
    results = Test([1, 2, 3], "rmse").run()
    print(results)