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
        if self.heuristic == "rmse":
            return self.heuristica_rmse()
        
        elif self.heuristic == "distancia_logica":
            return self.heuristica_distancia_logica()
        
        elif self.heuristic == "nilsson":
            return self.heuristica_nilsson()
        
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
    


    def to_matrix(self, state): # função auxiliar p heurística rmse
        n = sum(len(stack) for stack in self.state)

        matriz = [[0] * n for _ in range(n)]
        for j, stack in enumerate(state):
            for i, _ in enumerate(stack):
                if j < n:
                    matriz[i][j] = 1
        return matriz
    
    def heuristica_rmse(self): # admissivel e não produtiva        
        n = sum(len(stack) for stack in self.state)

        mat_atual = self.to_matrix(self.state)
        mat_goal  = self.to_matrix(self.goal)

        erros = []
        for i in range(n):
            for j in range(n):
                erros.append((mat_atual[i][j] - mat_goal[i][j]) ** 2)

        return (sum(erros) / n**2) ** 0.5 
    
    
    # ========================= HEURÍSTICA 2 =========================
    
    def get_posicoes(self, state): # função auxiliar p heurística dist lógica
            positions = {}
            for i, stack in enumerate(state):
                for j, block in enumerate(stack):
                    positions[block] = (i, j)
            return positions
    
    def heuristica_distancia_logica(self): # admissivel ()

        pos_atual = self.get_posicoes(self.state)
        pos_goal  = self.get_posicoes(self.goal)

        custo = 0
        for i, stack in enumerate(self.state):
            for j, block in enumerate(stack):
                if pos_atual[block] != pos_goal.get(block):
                    custo += 1  # bloco no lugar errado
                    custo += len(stack) - j - 1  # blocos em cima dele
        return custo    
    
    
    # ========================= HEURÍSTICA 3 =========================
    
    def heuristica_nilsson(self): # nao admissível (do pdf q mandei no grpo)
        
        pos_atual = self.get_posicoes(self.state)
        pos_goal  = self.get_posicoes(self.goal)
        custo = 0
        
        for i, stack in enumerate(self.state):
            for j, block in enumerate(stack):
                # se o bloco n esta na coordenada do objetivo
                if pos_atual[block] != pos_goal.get(block):
                    custo += 3 
                    # se esse bloco ta errado terá q ser movido, portanto TODOS os blocos acima dele estão obstruindo o caminho
                    blocos_acima = len(stack) - j - 1
                    custo += 2 * blocos_acima

        return custo
    
    
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