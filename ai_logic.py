import numpy as np
import logic
import constants as c
import copy

class GameAI:
    def __init__(self, search_depth=3):
        self.search_depth = search_depth
    
    def evaluate_board(self, matrix):

        total_score = sum(sum(row) for row in matrix)
        
        empty_cells = sum(row.count(0) for row in matrix)               

        smoothness = self.calculate_smoothness(matrix)                 # how close adjacent tiles are
        
        monotonicity = self.calculate_monotonicity(matrix)             # preference for tiles increasing in a direction
        
        corner_weight = self.calculate_corner_weight(matrix)
        # weighted evaluation
        return (
            total_score * 0.2 +     # score matters
            empty_cells * 60 +      # more empty cells are good
            smoothness * 30 +       # smooth board preferred
            monotonicity * 40 +     # monotonic arrangement is good
            corner_weight * 50      # keep larger tiles in corner
        )
    
    def calculate_corner_weight(self, matrix):
        corners = [
            matrix[0][0], matrix[0][-1],
            matrix[-1][0], matrix[-1][-1]
        ]
        return max(corners)

    def calculate_smoothness(self, matrix):
        smoothness = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != 0:
                    # horizontal smoothness
                    if j < len(matrix[0]) - 1 and matrix[i][j+1] != 0:
                        smoothness -= abs(np.log2(matrix[i][j]) - np.log2(matrix[i][j+1]))
                    
                    # vertical smoothness
                    if i < len(matrix) - 1 and matrix[i+1][j] != 0:
                        smoothness -= abs(np.log2(matrix[i][j]) - np.log2(matrix[i+1][j]))
        return smoothness
    
    def calculate_monotonicity(self, matrix):
        def calculate_monotonicity_single_line(line):
            # remove zeros and calculate monotonicity
            line = [x for x in line if x != 0]
            if len(line) <= 1:
                return 0
            
            # check if the line is sorted in ascending or descending order
            return max(
                sum(line[i] <= line[i+1] for i in range(len(line)-1)),  # increasing
                sum(line[i] >= line[i+1] for i in range(len(line)-1))   # decreasing
            ) / (len(line) - 1)
        
        # check monotonicity for rows and columns
        monotonicity = 0
        
        for row in matrix:
            monotonicity += calculate_monotonicity_single_line(row)
        
        for col in zip(*matrix):
            monotonicity += calculate_monotonicity_single_line(col)
        
        return monotonicity
    
    def minimax_with_alpha_beta(self, matrix, depth, alpha, beta, is_maximizing):
        # Check game state
        game_state = logic.game_state(matrix)
        if game_state == 'win':
            return float('inf')
        if game_state == 'lose':
            return float('-inf')
        
        # Reached search depth
        if depth == 0:
            return self.evaluate_board(matrix)
        
        # Maximizer (AI's turn)
        if is_maximizing:
            max_eval = float('-inf')
            moves = [
                ('up', logic.up),
                ('down', logic.down),
                ('left', logic.left),
                ('right', logic.right)
            ]
            
            for move_name, move_func in moves:
                new_matrix, done = move_func(copy.deepcopy(matrix))
                
                if done:
                    new_matrix = logic.add_random_tile(new_matrix)
                    
                    # Recursively evaluate
                    eval_score = self.minimax_with_alpha_beta(
                        new_matrix, depth - 1, alpha, beta, False
                    )
                    
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    
                    # Pruning
                    if beta <= alpha:
                        break
            
            return max_eval
        
        # Minimizer (random tile placement)
        else:
            min_eval = float('inf')
            empty_tiles = [
                (i, j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] == 0
            ]
            
            for i, j in empty_tiles:
                # Try placing 2 (90% probability)
                new_matrix_2 = copy.deepcopy(matrix)
                new_matrix_2[i][j] = 2
                eval_score_2 = self.minimax_with_alpha_beta(
                    new_matrix_2, depth - 1, alpha, beta, True
                )
                
                # Try placing 4 (10% probability)
                new_matrix_4 = copy.deepcopy(matrix)
                new_matrix_4[i][j] = 4
                eval_score_4 = self.minimax_with_alpha_beta(
                    new_matrix_4, depth - 1, alpha, beta, True
                )
                
                # Weighted average
                eval_score = 0.9 * eval_score_2 + 0.1 * eval_score_4
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                # Pruning
                if beta <= alpha:
                    break
            
            return min_eval


    def get_num_empty_tiles(self, matrix):
        return sum(row.count(0) for row in matrix)

    
    def get_best_move(self, matrix):

        moves = [
            ('up', logic.up),
            ('down', logic.down),
            ('left', logic.left),
            ('right', logic.right)
        ]
        
        best_move = None
        best_score = float('-inf')
        
        for move_name, move_func in moves:
            
            new_matrix, done = move_func(copy.deepcopy(matrix))
            
            empty_tiles = self.get_num_empty_tiles(matrix)
            if empty_tiles > 6:
                depth = 4
            elif empty_tiles > 3:
                depth = 3
            else:
                depth = 2

            if done:
                # Score this move
                new_matrix = logic.add_random_tile(new_matrix)
                move_score = self.minimax_with_alpha_beta(
                    new_matrix, depth, float('-inf'), float('inf'), False
                )
                
                # Update best move
                if move_score > best_score:
                    best_score = move_score
                    best_move = move_name
        
        return best_move