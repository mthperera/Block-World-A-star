from typing import List

from src.heuristics.bases import *


class HeuristicFactory:

    @staticmethod
    def create(heuristic_name: str, state: List[List[int]], goal: List[List[int]]):
        
        if heuristic_name == "rmse":
            return HeuristicRMSE(state, goal)
        elif heuristic_name == "blocking":
            return HeuristicBlocking(state, goal)
        elif heuristic_name == "nilsson":
            return HeuristicNilsson(state, goal)
        elif heuristic_name == "chamfer":
            return HeuristicChamfer(state, goal)
        elif heuristic_name == "hausdorff":
            return HeuristicHausdorff(state, goal)
        else:
            raise ValueError(f"Heurística '{heuristic_name}' não reconhecida")