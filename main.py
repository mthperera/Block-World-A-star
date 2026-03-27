from typing import List, Any

from aigyminsper.search.search_algorithms import AEstrela

from src.block_world_problem import BlockWorld


def main(
        initial_state: List[List[Any]], 
        goal_state: List[List[Any]], 
        heuristic: str,
        tracing: bool = True
    ):

    state = BlockWorld(
        name=str(initial_state),
        state=initial_state,
        goal=goal_state,
        heuristic=heuristic
    )

    algorithm = AEstrela()

    result = algorithm.search(state, pruning="general")

    if tracing:
        if result:
            print("Solution path:\n")
            print(result.show_path())
            print(f"\nCost: {result.g}")
        else:
            print("No solution found")
    
    return result


if __name__ == "__main__":
    main(
        initial_state = [[1, 2, 3, 5], [4], [], [], []], 
        goal_state = [[1], [], [], [5, 4, 2, 3], []], 
        heuristic="rmse"
    )