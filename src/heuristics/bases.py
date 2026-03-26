from abc import ABC, abstractmethod
from typing import List

import numpy as np
from scipy.spatial import KDTree
from scipy.spatial.distance import cdist


class Heuristic(ABC):
    
    def __init__(self, state: List[List[int]], goal: List[List[int]]):
        self.state = state
        self.goal = goal

    @abstractmethod
    def calculate(self):
        pass


class HeuristicRMSE(Heuristic):

    def _to_matrix(self, state: List[List[int]]):
        n = sum(len(stack) for stack in state)
        matriz = [[0] * n for _ in range(n)]

        for j, stack in enumerate(state):
            for i, _ in enumerate(stack):
                if j < n:
                    matriz[i][j] = 1
        return matriz

    def calculate(self):
        n = sum(len(stack) for stack in self.state)

        mat_atual = self._to_matrix(self.state)
        mat_goal  = self._to_matrix(self.goal)

        erros = []
        for i in range(n):
            for j in range(n):
                erros.append((mat_atual[i][j] - mat_goal[i][j]) ** 2)

        return (sum(erros) / n**2) ** 0.5


class HeuristicBlocking(Heuristic):

    def _get_positions(self, state: List[List[int]]):
        positions = {}
        for i, stack in enumerate(state):
            for j, block in enumerate(stack):
                positions[block] = (i, j)
        return positions

    def calculate(self):
        pos_atual = self._get_positions(self.state)
        pos_goal  = self._get_positions(self.goal)

        cost = 0
        for _, stack in enumerate(self.state):
            for j, block in enumerate(stack):
                if pos_atual[block] != pos_goal.get(block):
                    cost += 1
                    cost += len(stack) - j - 1
        return cost


class HeuristicNilsson(Heuristic):

    def _get_positions(self, state: List[List[int]]):
        positions = {}
        for i, stack in enumerate(state):
            for j, block in enumerate(stack):
                positions[block] = (i, j)
        return positions

    def calculate(self):
        pos_atual = self._get_positions(self.state)
        pos_goal  = self._get_positions(self.goal)

        cost = 0
        for _, stack in enumerate(self.state):
            for j, block in enumerate(stack):
                if pos_atual[block] != pos_goal.get(block):
                    cost += 3
                    blocos_acima = len(stack) - j - 1
                    cost += 2 * blocos_acima
        return cost


class HeuristicChamfer(Heuristic):

    def _get_points(self, state: List[List[int]]) -> np.ndarray:

        points = []
        for i, stack in enumerate(state):
            for j, _ in enumerate(stack):
                points.append((i, j))
        return np.array(points, dtype=float)

    def calculate(self):
        points_atual = self._get_points(self.state)
        points_goal = self._get_points(self.goal)

        if len(points_atual) == 0 or len(points_goal) == 0:
            return 0

        tree_goal = KDTree(points_goal)
        dist_atual = tree_goal.query(points_atual)[0]

        tree_atual = KDTree(points_atual)
        dist_goal = tree_atual.query(points_goal)[0]

        cost = np.mean(dist_atual) + np.mean(dist_goal)
        return cost
    

class HeuristicHausdorff(Heuristic):

    def _get_points(self, state: List[List[int]]) -> np.ndarray:
        points = []
        for i, stack in enumerate(state):
            for j, _ in enumerate(stack):
                points.append((i, j))
        return np.array(points, dtype=float)

    def calculate(self):
        points_atual = self._get_points(self.state)
        points_goal  = self._get_points(self.goal)

        if len(points_atual) == 0 or len(points_goal) == 0:
            return 0

        D = cdist(points_atual, points_goal)

        min_dist_A = np.min(D, axis=1)
        min_dist_B = np.min(D, axis=0)

        cost = max(np.max(min_dist_A), np.max(min_dist_B))
        return cost