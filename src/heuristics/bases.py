from abc import ABC, abstractmethod


class Heuristic(ABC):
    def __init__(self, state, goal):
        self.state = state
        self.goal = goal

    @abstractmethod
    def calculate(self):
        pass


class HeuristicRMSE(Heuristic):

    def to_matrix(self, state):
        n = sum(len(stack) for stack in state)
        matriz = [[0] * n for _ in range(n)]

        for j, stack in enumerate(state):
            for i, _ in enumerate(stack):
                if j < n:
                    matriz[i][j] = 1
        return matriz

    def calculate(self):
        n = sum(len(stack) for stack in self.state)

        mat_atual = self.to_matrix(self.state)
        mat_goal  = self.to_matrix(self.goal)

        erros = []
        for i in range(n):
            for j in range(n):
                erros.append((mat_atual[i][j] - mat_goal[i][j]) ** 2)

        return (sum(erros) / n**2) ** 0.5


class HeuristicDistance(Heuristic):

    def get_positions(self, state):
        positions = {}
        for i, stack in enumerate(state):
            for j, block in enumerate(stack):
                positions[block] = (i, j)
        return positions

    def calculate(self):
        pos_atual = self.get_positions(self.state)
        pos_goal  = self.get_positions(self.goal)

        cost = 0
        for i, stack in enumerate(self.state):
            for j, block in enumerate(stack):
                if pos_atual[block] != pos_goal.get(block):
                    cost += 1
                    cost += len(stack) - j - 1
        return cost


class HeuristicNilsson(Heuristic):

    def get_positions(self, state):
        positions = {}
        for i, stack in enumerate(state):
            for j, block in enumerate(stack):
                positions[block] = (i, j)
        return positions

    def calculate(self):
        pos_atual = self.get_positions(self.state)
        pos_goal  = self.get_positions(self.goal)

        cost = 0
        for i, stack in enumerate(self.state):
            for j, block in enumerate(stack):
                if pos_atual[block] != pos_goal.get(block):
                    cost += 3
                    blocos_acima = len(stack) - j - 1
                    cost += 2 * blocos_acima
        return cost