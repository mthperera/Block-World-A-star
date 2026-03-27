from typing import List, Any, Optional, Literal

from aigyminsper.search.graph import State

from src.heuristics.factory import HeuristicFactory


class BlockWorld(State):
    
    def __init__(self,
        name: str,
        heuristic: Literal["rmse", "blocking", "nilsson", "chamfer", "hausdorff"],
        state: List[List[Any]],
        goal: List[List[Any]],
        goal_set: Optional[set] = None
    ) -> None:
        
        super().__init__(name)
        self.state = state
        self.goal = goal
        self.heuristic = heuristic
        self.goal_set = goal_set
        if not self.goal_set:
            self.goal_set = set(map(tuple, self.goal))
    
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
                        goal = self.goal,
                        goal_set=self.goal_set
                    )
                    successors.append(successor)

        return successors
    
    def is_goal(self):
        return set(map(tuple, self.state)) == self.goal_set

    def cost(self):
        return 1
    
    def h(self):
        heuristic = HeuristicFactory.create(self.heuristic, self.state, self.goal)
        return heuristic.calculate()
    
    def env(self):
        return tuple(tuple(row) for row in self.state)

    def description(self):
        return f"""
            Estado atual:
            {self.format_state(self.state)}

            Objetivo:
            {self.format_state(self.goal)}
        """