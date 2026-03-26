from typing import List

from src.heuristics.bases import *


class HeuristicFactory:

    @staticmethod
    def create(heuristic_name: str, state: List[List[int]], goal: List[List[int]]):
        
        if heuristic_name == "rmse":
            return HeuristicRMSE(state, goal)
        elif heuristic_name == "distance":
            return HeuristicDistance(state, goal)
        elif heuristic_name == "nilsson":
            return HeuristicNilsson(state, goal)
        else:
            raise ValueError(f"Heurística '{heuristic_name}' não reconhecida")