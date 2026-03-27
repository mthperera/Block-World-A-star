from typing import List, Literal, Any

from src.heuristics.bases import *


class HeuristicFactory:

    @staticmethod
    def create(
            heuristic_name: Literal["rmse", "blocking", "nilsson", "chamfer", "hausdorff"], 
            state: List[List[Any]], 
            goal: List[List[Any]]
        ):
        
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