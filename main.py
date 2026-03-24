from block_world_problem import BlockWorld

from aigyminsper.search.search_algorithms import AEstrela


def main(initial_state, goal_state):

    # create initial node
    state = BlockWorld(
        name=str(initial_state),
        state=initial_state,
        goal=goal_state,
        heuristic="" # Aqui tem que alterar
    )

    # A* algorithm
    algorithm = AEstrela()

    # run search
    result = algorithm.search(state)

    # output
    if result:
        print("Solution path:\n")
        print(result.show_path())
        print(f"\nCost: {result.g}")
    else:
        print("No solution found")


if __name__ == "__main__":
    main(initial_state = [[1, 2, 3], [4]], goal_state = [[1], [4, 3, 2]])