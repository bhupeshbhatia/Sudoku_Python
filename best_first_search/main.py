from pathlib import Path
import sudoku_solver
import numpy as np


f = open('../puzzles/hardsudoku-3.txt', 'r')
lines = f.read()
f.close()
sudoku = [[character for character in line if not character==" "] for line in lines.split("\n")]

def change_to_zero(sudoku):
  
  for r in range(9):
    for c in range(9):
      if sudoku[r][c] == "_":
        sudoku[r][c] = '0'

    sudoku[r] = list(map(int, sudoku[r]))
  return sudoku


result = np.array(change_to_zero(sudoku))
print(result)
sudoku_solver.solve_sudoku(result)
print(result)
print('Solved?: ', sudoku_solver.is_board_solved(result))
