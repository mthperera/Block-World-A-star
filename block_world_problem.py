from typing import List

from aigyminsper.search.graph import State 


class BlockWorld(State):
    def __init__(self,
        name: str,
        heuristic: str,
        state: List[List[int]],
        goal: List[List[int]],
    ) -> None:
        
        super().__init__(name)
        self.state = state
        self.goal = goal
        self.heuristic = heuristic

    @staticmethod
    def format_state(state):
        altura_max = max(len(stack) for stack in state)
        linhas = []

        for h in range(altura_max - 1, -1, -1):
            linha = []
            for stack in state:
                if len(stack) > h:
                    linha.append(str(stack[h]))
                else:
                    linha.append(" ")
            linhas.append(" ".join(linha))

        return "\n".join(linhas)
    
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
                        name = self.format_state(new_state),
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
        if self.heuristic == "":
            return 0
    
    def env(self):
        return self.state

    def description(self):
        return f"""
            Estado atual:
            {self.format_state(self.state)}

            Objetivo:
            {self.format_state(self.goal)}
        """