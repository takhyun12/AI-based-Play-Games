from tetris.Tetromino import Tetromino
from tetris.ai.TetrisWeight import TetrisWeight


class TetrisAI:

    def __init__(self, settings, tetris_model):
        self._base_weight = TetrisWeight()
        self._opt_weight = TetrisWeight()
        self._weight = TetrisWeight()

        self.board_height = settings.GRID_HEIGHT
        self.board_width = settings.GRID_WIDTH

        self._opt_weight.WEIGHT_FULL = 50
        self._opt_weight.WEIGHT_POST_FLOOR = 5
        self._opt_weight.WEIGHT_HEIGHT = -10
        self._opt_weight.WEIGHT_DEEP_HOLE = -0.1
        self._opt_weight.WEIGHT_ROOF = -0.1

        self.i_tetris_model = tetris_model

    def get_evaluated_states(self):
        max_score = -999999999
        max_state = None

        low_score = 999999999
        low_state = None

        _, d_height, d_deep_hole, d_roof = self.i_tetris_model.analysis_board(self.i_tetris_model.board)

        states = self.get_state_list()
        for index in range(len(states)):
            board, _, _, _, post_side, post_floor = states[index]
            full, height, deep_hole, roof = self.i_tetris_model.analysis_board(board)

            score = 0

            score += full * self._weight.WEIGHT_FULL
            score += post_side * self._weight.WEIGHT_POST_SIDE
            score += post_floor * self._weight.WEIGHT_POST_FLOOR

            score += (height - d_height) * self._weight.WEIGHT_HEIGHT
            score += deep_hole * self._weight.WEIGHT_DEEP_HOLE
            score += roof * self._weight.WEIGHT_ROOF

            if height == self.board_height:
                score += -999999999

            if score > max_score:
                max_score = score
                max_state = states[index]

            if score < low_score:
                low_score = score
                low_state = states[index]

        return max_state, low_state

    def get_state_list(self):
        states = dict()

        num_index = 0
        rotate_count = Tetromino.get_rotate_count(self.i_tetris_model.current_shape_code) + 1
        for rotate_rate in range(rotate_count):
            for x in range(self.board_width):
                if self.i_tetris_model.rotate_block_rate(0, x, rotate_rate):
                    dy = 0
                    while self.i_tetris_model.can_move_block(dy + 1, x):
                        dy += 1

                    def check_pos(fy, fx):
                        return fy >= self.board_height or fx >= self.board_width or fx < 0 or self.i_tetris_model.get_board(fy, fx) == 1

                    post_floor = 0
                    post_side = 0
                    for col in range(len(self.i_tetris_model.current_tetromino)):
                        for row in range(len(self.i_tetris_model.current_tetromino[0])):
                            if self.i_tetris_model.current_tetromino[col][row] == 1:
                                if check_pos(dy + col, x + row - 1):
                                    post_side += 1
                                if check_pos(dy + col, x + row + 1):
                                    post_side += 1
                                if check_pos(dy + col + 1, x + row):
                                    post_floor += 1

                    states[num_index] = self.i_tetris_model.get_sum_tetromino_board(dy, x), dy, x, rotate_rate, post_side, post_floor
                    num_index += 1
        return states
