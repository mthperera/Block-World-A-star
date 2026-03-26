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
            return self._heuristica_rmse()
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
    
    def _heuristica_rmse(self):
        # '''
        # Heurística 1: RMSE -> VERSAO 1

        # Cada bloco tem uma posição (coluna, altura) no estado atual e no objetivo.
        # Calcula o erro quadrático entre as posições de cada bloco e tira a média,
        # aplicando raiz quadrada no final:
        # RMSE = sqrt( (1/n) * sum( (delta_coluna)^2 + (delta_altura)^2 ) )
        # Blocos ausentes em um dos estados recebem posição padrão (0, 0).
        # '''
        
        # def get_posicoes(state):
        #     # dicionário pra armazenar as posições dos blocos
        #     positions = {}
        #     for i, stack in enumerate(state):
        #         for j, block in enumerate(stack):
        #             positions[block] = (i, j)
        #     return positions
        
        # pos_atual = get_posicoes(self.state)
        # pos_goal = get_posicoes(self.goal)
        
        # total_blocos = set(pos_atual.keys()) | set(pos_goal.keys()) # união dos blocos do estado atual + objetivo
        # n = len(total_blocos)
        
        # if n == 0:
        #     return 0
        # erros = []
        # for block in total_blocos:
        #     pos_i, pos_j = pos_atual.get(block, (0,0))
        #     meta_i, meta_j = pos_goal.get(block, (0,0))
        #     erros.append((pos_i - meta_i)**2 + (pos_j - meta_j)**2)
        
        # return (sum(erros)/n)**0.5
        
        
        '''
        Heurística 1: RMSE -> VERSAO 2
        
        Representa o estado atual e o objetivo como matrizes nXn, onde n = número de blocos e cada coluna é uma pilha. Daí
        RMSE = sqrt((1/n^2) * sum((atual[i][j] - goal[i][j])^2))
        '''
        
        n = sum(len(stack) for stack in self.state)

        mat_atual = self.to_matrix(self.state)
        mat_goal  = self.to_matrix(self.goal)

        erros = []
        for i in range(n):
            for j in range(n):
                erros.append((mat_atual[i][j] - mat_goal[i][j]) ** 2)

        return (sum(erros) / n**2) ** 0.5 
                
    
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