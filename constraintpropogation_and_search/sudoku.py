
#!/usr/bin/python
import time, random

# Rules for constraint propogation and search based sudoku solver
# row = r = A
# column = c = 1
# square = s = A1 - each square in the grid has 3 unites and 20 peers
# digit = d = 6
# unit = u = 3 x 3 matrix = ['A1','B1','C1','D1','E1','F1','G1','H1','I1'] = row, column and the box it appears in
# grid = 81 squares = .18...7
# values = map or dict of possible values = A1: 12345, A2: 789

# All units for each square are created using cross function
def cross(A, B):
  "Cross product of elements in A and elements in B."
  return [a+b for a in A for b in B]

# Squares = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']
  # squares = []
  # for a in rows:
  #   for b in cols:
  #     squares.append(a+b)
  # return squares


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] + [cross(r, cols) for r in rows] + [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])

# Dictionaries created that use square names as keys and three units or 20 peers as values
units = dict((s, [u for u in unitlist if s in u]) for s in squares)

peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares) # peers of a square = all other squares in the units

# Now, the 3 units of ‘C2’ can be accessed with units['C2'] and will give the following result:
# [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]

# def test():
#     "A set of unit tests."
#     assert len(squares) == 81
#     assert len(unitlist) == 27
#     assert all(len(units[s]) == 3 for s in squares)
#     assert all(len(peers[s]) == 20 for s in squares)
#     assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
#                            ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
#                            ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
#     assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
#                                'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
#                                'A1', 'A3', 'B1', 'B3'])
#     print('All tests pass.')


# test()

# Grid - needs to be parsed

# squares have names like 'A1'. Therefore, values will be a dict with squares as keys. 
# The value of each key will be the possible digits for that square: a single digit if it 
# was given as part of the puzzle definition or if we have figured out what it must be, and a 
# collection of several digits if we are still uncertain. We can use a set or list but we are using string of digits
# as its easier to eliminate. a grid where A1 is 7 and C7 is empty would be represented 
# as {'A1': '7', 'C7': '123456789', ...}. 

def parse_grid(grid):
  # Convert grid to a dict of possible values, {square: digits}, or
  # return False if a contradiction is detected."""

  #First for every square we have all digits - then assign values from grid
  # Another representation of the grid - to internally describe the current state of a puzzle. 
  # It will keep track of all remaining possible values for each square and be named values.
  values = dict((s, digits) for s in squares)
  for s,d in grid_values(grid).items():
      if d in digits and not assign(values, s, d):
          return False ## (Fail if we can't assign d to square s.)
  return values

def grid_values(grid):
    # Convert grid into dict of {square: character with 0 or . for empties}
    chars = [c for c in grid if c in digits or c in '0.']
    assert(len(chars) == 81)
    return dict(zip(squares, chars))

# The initial values for the squares will be either specific digits (1-9) or an empty value.
# apply constraints to each square and eliminate values that are impossible. 

# Two strategies:
# If a square has only one possible value, then eliminate that value from the square's peers. = A1 has a value of 5, then 5 can be removed from all 20 of its peers. 

# If a unit has only one possible place for a value, then put the value there. = none of A1 through A8 contains 9 as a possible value, then we can be sure that A9 has a value of 9 since 9 must occur somewhere in the unit
# Every time a square is updated, it will cause possible updates to all its peers.

# Assign function = called inside parse_grid function.
# values = dictionary of each square with all possible values for that square
# s = square 
# d = digit
# Eliminate all the other values (except d) from values[s] and propagate.
# Return values, except return False if a contradiction is detected.
def assign(values, s, d):
  other_values = values[s].replace(d, '')
  if all(eliminate(values, s, d2) for d2 in other_values):
    return values
  else:
    return False

# Eliminate function - removes values that can't be the solution using the 2 strategies
# Eliminate d from values[s]; propagate when values or places <= 2.
# Return values, except return False if a contradiction is detected.
def eliminate(values, s, d):
  #Return already eliminated values
  if d not in values[s]:
    return values
  
  values[s] = values[s].replace(d, '')

  # First constraints - if a square has only one value d2, then remove d2 from peers
  if len(values[s]) == 0:
    # Contradiction: removed last value
    return False
  elif len(values[s]) == 1:
    d2 = values[s]
    # recursion
    if not all(eliminate(values, s2, d2) for s2 in peers[s]):
      return False

  # Second constraint - if a unit has only possible value d, then place it there
  for u in units[s]:
    dplaces = [s for s in u if d in values[s]]
    if len(dplaces) == 0:
      # Contradiction: no place for this value
      return False
    elif len(dplaces) == 1:
      # d can only be in one place in units; assign it there
      if not assign(values, dplaces[0], d):
        return False
  return values

# display function calls parse_grid and shows result with possible values in 2D grid
def display(values):
  "Display these values as a 2-D grid."
  width = 1+max(len(values[s]) for s in squares)
  line = '+'.join(['-'*(width*3)]*3)
  for r in rows:
      print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
      if r in 'CF': 
          print(line)
  print()


# Search algorithm to solve hard puzzles 
# no solution has already been found. Then, choose an unfilled square 
# and considers all values that are still possible. Finally, one at a time, try to
# assign the square each value, and search from the resulting position.

# Variable ordering: to choose which square to start exploring
# common heuristic called minimum remaining values, which means to choose the (or one of the) square with the minimum number of possible values. 
# because of probabilitiy: 
# If square B3 has 7 possibilities (1256789), so we’d expect to guess wrong with probability 6/7. 
# If instead we chose G2, which only has 2 possibilities (89), we’d expect to be wrong with probability only 1/2.
# So choose the square with the fewest possibilities and the best chance of guessing right.

def solve(grid):
  return search(parse_grid(grid))

# "Using depth-first search and propagation, try all possible values."
# search for a value d such that we can successfully search for a solution 
# from the result of assigning square s to d. If the search leads to an failed position,
# go back and consider another value of d.

# create a new copy of values for each recursive call to search. 
# This way each branch of the search tree is independent, and doesn't confuse another branch. 
# This is the reason to implement the set of possible values for a square as a string: 
# We can copy values with values.copy() which is simple and efficient.
# Otherwise we would need to use backtracking search - which becomes complicated when each assignment can lead to many other changes via constraint propogation.
def search(values):
  if values is False:
    return False # Failed
  
  if all(len(values[s]) == 1 for s in squares):
    #This is solved as there is only 1 value
    return values
  
  # Choose square that is not filled with least number of possibilities
  n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
  # The search function is called recursively until the puzzle is solved. values is copied to avoid complexity.
  return some(search(assign(values.copy(), s, d)) for d in values[s])

# check if an attempt succeeds to solve the puzzle.
# Return some element of seq that is true.
def some(seq):
  for e in seq:
    if e: return e
  return False


def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    f = open('test-puzzles-1.txt', 'r')
    # file = f.read()
    return f.read().strip().split(sep)


def solve_all(grids, name='', showif=1.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.perf_counter()
        values = solve(grid)
        t = time.perf_counter()-start
        ## Display puzzles that take long enough

        display(grid_values(grid))
        if values: display(values)
        timeSolved = "{timeSeconds} seconds\n"
        print(timeSolved.format(timeSeconds = t))
        # if showif is not None:
        #     display(grid_values(grid))
        #     if values: display(values)
        #     timeSolved = "{timeSeconds} seconds\n"
        #     print(timeSolved.format(timeSeconds = t))
        
        # elif showif is not None:
        #   display(grid_values(grid))
        
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
      
      result = "Solved {res} of {iter} {name} puzzles (avg {avg} secs ({hz} Hz), max {max} secs)."
      print(result.format(res=sum(results), iter = N, name =name, avg=sum(times)/N, hz=N/sum(times), max=max(times)))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)


# def readSudoku():
#   f = open('puzzle-2.txt', 'r')
#   grid = f.read()
#   f.close()
#   values = solve(grid)
#   display(grid_values(grid))
#   solved(values)
#   # display(parse_grid(grid))
#   # solve(problem)
#   # display(problem)
#   # return display(parse_grid(problem))
  

# readSudoku()


solve_all(from_file("test-puzzles-1.txt", '========'), "puzzles", None)