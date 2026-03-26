from typing import List

from aigyminsper.search.search_algorithms import AEstrela

from src.block_world_problem import BlockWorld


def main(
        initial_state: List[List[int]], 
        goal_state: List[List[int]], 
        heuristic: str
    ):

    state = BlockWorld(
        name=str(initial_state),
        state=initial_state,
        goal=goal_state,
        heuristic=heuristic
    )

    algorithm = AEstrela()

    result = algorithm.search(state)

    if result:
        print("Solution path:\n")
        print(result.show_path())
        print(f"\nCost: {result.g}")
    else:
        print("No solution found")


if __name__ == "__main__":
    main(
        initial_state = [[1, 2, 3], [4], [], []], 
        goal_state = [[1], [], [], [4, 2, 3]], 
        heuristic="rmse"
    )