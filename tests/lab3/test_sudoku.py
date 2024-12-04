import unittest
from src.lab3.sudoku import (create_grid, group, get_row, get_col, get_block, find_empty_positions,
                             find_possible_values, solve, generate_sudoku, check_solution)

class MyTestCase(unittest.TestCase):
    def test_group(self):
        self.assertEqual(group([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(group([], 3), [])
        self.assertEqual(group([1, 2, 3], 1), [[1], [2], [3]])
        self.assertEqual(group([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_create_grid(self):
        puzzle = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
        grid = create_grid(puzzle)
        self.assertEqual(len(grid), 9)
        self.assertEqual(len(grid[0]), 9)
        self.assertEqual(grid[0], ["5", "3", ".", ".", "7", ".", ".", ".", "."])
        self.assertEqual(grid[1], ["6", ".", ".", "1", "9", "5", ".", ".", "."])

    def test_get_row(self):
        grid = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["6", "7", "8", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        self.assertEqual(get_row(grid, (0, 0)), ["5", "3", "4", "6", "7", "8", "9", "1", "2"])
        self.assertEqual(get_row(grid, (7, 7)), ["6", "7", "8", "4", "1", "9", "6", "3", "5"])
        self.assertEqual(get_row(grid, (8, 8)), ["3", "4", "5", "2", "8", "6", "1", "7", "9"])

    def test_find_empty_postions(self):
        grid = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.assertIsNone(find_empty_positions(grid))

        grid = [["1", "2", "3"], ["4", "5", "."], ["7", "8", "9"]]
        self.assertEqual(find_empty_positions(grid), (1, 2))

        grid = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        self.assertEqual(find_empty_positions(grid), (0, 0))

    def test_find_possible_values(self):
        grid = [
            ["1", "2", ".", ".", "5", ".", ".", ".", "."],
            ["3", ".", ".", "4", "6", "7", ".", ".", "."],
            [".", "5", "6", ".", ".", ".", ".", "8", "."],
            ["9", ".", ".", ".", "2", ".", ".", ".", "4"],
            ["7", ".", ".", "1", ".", "8", ".", ".", "3"],
            ["2", ".", ".", ".", "3", ".", ".", ".", "5"],
            [".", "4", ".", ".", ".", ".", "1", "9", "."],
            [".", ".", ".", "7", "8", "2", ".", ".", "6"],
            [".", ".", ".", ".", "4", ".", ".", "3", "1"],
        ]

        # Позиция (0, 2) - пустая клетка
        self.assertEqual(find_possible_values(grid, (0, 2)), {"9", "4", "7", "8"})

        # Позиция (4, 7) - пустая клетка
        self.assertEqual(find_possible_values(grid, (4, 7)), {"2", "6"})

        # Позиция (8, 0) - пустая клетка
        self.assertEqual(find_possible_values(grid, (8, 0)), {"6", "5", "8"})

    def test_solve(self):
        grid = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
        ]
        expected_solution = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertEqual(solution, expected_solution)
        self.assertTrue(check_solution(solution))

    def test_check_solution(self):
        solution = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        self.assertTrue(check_solution(solution))

        incorrect_solution_row = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "2", "3", "5"], #две двойки в строке
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        self.assertFalse(check_solution(incorrect_solution_row))

        incorrect_solution_col = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        incorrect_solution_col[5][0] = "5"
        self.assertFalse(check_solution(incorrect_solution_col))

        incorrect_solution_block = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        incorrect_solution_block[4][0] = "1"
        self.assertFalse(check_solution(incorrect_solution_block))

    def test_generate_sudoku(self):
        #whole empty
        grid = generate_sudoku(0)
        num_filled = sum(1 for row in grid for e in row if e != ".")
        self.assertEqual(num_filled, 0)
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))

        grid = generate_sudoku(50)
        num_filled = sum(1 for row in grid for e in row if e != ".")
        self.assertEqual(num_filled, 50)
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))

        grid = generate_sudoku(81)
        num_filled = sum(1 for row in grid for e in row if e != ".")
        self.assertEqual(num_filled, 81)
        self.assertTrue(check_solution(grid))

if __name__ == "__main__":
    unittest.main()



























if __name__ == '__main__':
    unittest.main()

