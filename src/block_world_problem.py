from typing import List, Any

from aigyminsper.search.graph import State

from src.heuristics.factory import HeuristicFactory


class BlockWorld(State):
    
    def __init__(self,
        name: str,
        heuristic: str,
        state: List[List[Any]],
        goal: List[List[Any]],
    ) -> None:
        
        super().__init__(name)
        self.state = state
        self.goal = goal
        self.heuristic = heuristic
    
    def successors(self):
        successors = []

        for i, stack in enumerate(self.state):
            if len(stack) > 0:
                block = stack[-1]

                for j in range(len(self.state)):
                    new_state = [s.copy() for s in self.state]
                    if i == j:
                        continue
                    new_state[i].pop()
                    new_state[j].append(block)
                    successor = BlockWorld(
                        name = str(new_state),
                        heuristic = self.heuristic,
                        state = new_state,
                        goal = self.goal
                    )
                    successors.append(successor)

        return successors
    
    def is_goal(self):
        return self.state == self.goal

    def cost(self):
        return 1
    
    def h(self):
        heuristic = HeuristicFactory.create(self.heuristic, self.state, self.goal)
        return heuristic.calculate()
    
    def env(self):
        return self.state

    def description(self):
        return f"""
            Estado atual:
            {self.format_state(self.state)}

            Objetivo:
            {self.format_state(self.goal)}
        """
    
    ## ISSO AQ JÁ TAVA COMENTADO
    # @staticmethod
    # def format_state(state):

    #     max_height = max(len(stack) for stack in state)

    #     width = max(len(str(b)) for stack in state for b in stack)

    #     lines = []

    #     for h in range(max_height - 1, -1, -1):
    #         row = []
    #         for stack in state:
    #             if len(stack) > h:
    #                 value = str(stack[h])
    #             else:
    #                 value = ""
    #             row.append(value.center(width))
    #         lines.append(" | ".join(row))

    #     base = "-+-".join("-" * width for _ in state)

    #     return "\n".join(lines + [base])

    ## DAQUI PRA BAIXO EU N MEXI MAS JÁ TAVA COMENTADO
    # @staticmethod
    # def my_show_path(result):
    #     path = []
    #     node = result

    #     while node is not None:
    #         path.append(node)
    #         node = getattr(node, "parent", None) or getattr(node, "father", None)

    #     path.reverse()

    #     for i, node in enumerate(path):
    #         print(f"Step {i}:\n")
    #         print(BlockWorld.format_state(node.state.state))
    #         print()