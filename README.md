# suguru-solver

## What is this?

This project aims to solve Suguru puzzles (also known as Tectonic).

To define a puzzle, the following vocabulary is used:
- grid: Represents the entire puzzle board.
- form: Each grid is divided into different shapes (cages) containing one or more cells.
- cell: An individual square within the grid.

### Grid Definition
There are two ways to define a grid:
- Defining the forms: Explicitly listing each shape and its constituent cells.
- Pseudo-graphical definition: Defining the grid layout using a visual-like text representation.

In both cases, a cell is defined by its coordinates and its initial content.

## Example of grid definition:

The sample grid looks like this:
<pre>
# Novice / 61
┌───┬───┬───────┐
│   │ 2 │ 3 ·   │
│ - │ - └───┐ - │
│   │   · 4 │   │
│ - │ - + - ├───┤
│   │   ·   │   │
├───┴───────┘ - │
│   · 5 ·   ·   │
├───────┬───┐ - │
│ 1 ·   │   │   |
└───────┴───┴───┘
</pre>

### First way definition:
```python
from grid import Grid
d = {
	0: [(1, 1, 0), (2, 1, 0), (3, 1, 0)],
	1: [(1, 2, 2), (2, 2, 0), (2, 3, 4), (3, 2, 0), (3, 3, 0)],
	2: [(1, 3, 3), (1, 4, 0), (2, 4, 0)],
	3: [(3, 4, 0), (4, 1, 0), (4, 2, 5), (4, 3, 0), (4, 4, 2), (5, 4, 6)],
	4: [(5, 1, 1), (5, 2, 0)],
	5: [(5, 3, 0)]
}
```

The grid is defined as a dict:
- the key is the form name or index,
- the value is a tuple of 3 values:
  - the 2 first are the cell coordinate (row, column),
  - the last is the value: 0 or None if empty

### Second way definition:
```python
d = [
	[{1: 0}, {2: 2}, {3: 3}, {3: 0}],
	[{1: 0}, {2: 0}, {2: 4}, {3: 0}],
	[{1: 0}, {2: 0}, {2: 0}, {4: 0}],
	[{4: 0}, {4: 5}, {4: 0}, {4: 2}],
	[{5: 1}, {5: 0}, {6: 0}, {4: 6}]
]
```

The grid is defined as a 2-dimentional list to represent the grid. Every cell in this definition is represented with a dict:
- the key is the form index or name
- the value is the cell value, 0 or None if empty

## Other grids

```python
# Occasionnel / 130
d = {
	0: [(1, 1, 0), (1, 2, 0), (2, 1, 4), (2, 2, 0), (2, 3, 0)],
	1: [(1, 3, 0), (1, 4, 0), (1, 5, 4), (2, 4, 1), (2, 5, 0)],
	2: [(3, 1, 0), (3, 2, 0), (3, 3, 0), (3, 4, 0), (3, 5, 0)],
	3: [(4, 1, 0), (4, 2, 0), (4, 3, 0), (5, 1, 1), (5, 2, 0)],
	4: [(4, 4, 5), (4, 5, 0), (5, 3, 2), (5, 4, 4), (5, 5, 0)]
}
# Standard / 17
d = {
	0: [(1, 1, 0), (1, 2, 2), (1, 3, 0), (1, 4, 0), (2, 2, 0)],
	1: [(1, 5, 0), (2, 3, 0), (2, 4, 0), (2, 5, 0), (3, 4, 0)],
	2: [(2, 1, 0), (3, 1, 5), (3, 2, 0), (3, 3, 1), (4, 1, 0)],
	3: [(4, 2, 0), (5, 1, 0), (5, 2, 0), (6, 1, 2), (6, 2, 0)],
	4: [(3, 5, 2), (4, 3, 0), (4, 4, 0), (4, 5, 0), (5, 5, 0)],
	5: [(5, 3, 0), (5, 4, 0), (6, 3, 0), (6, 4, 3), (6, 5, 0)]
}
# Expert / 12
d = {
	0: [(1, 1, 1), (1, 2, 0), (2, 1, 5), (2, 2, 2), (3, 1, 0), (3, 2, 0)],
	1: [(1, 3, 0), (1, 4, 0), (2, 3, 0), (2, 4, 0), (2, 5, 3), (3, 5, 0)],
	2: [(1, 5, 0), (1, 6, 0), (1, 7, 5), (2, 6, 0), (2, 7, 0)],
	3: [(3, 3, 0), (3, 4, 0)],
	4: [(5, 1, 0)],
	5: [(3, 6, 0), (3, 7, 0)],
	6: [(4, 1, 0), (4, 2, 4), (4, 3, 0), (4, 4, 0), (5, 2, 0), (5, 3, 0)],
	7: [(4, 5, 0), (5, 4, 0), (5, 5, 0)],
	8: [(4, 6, 0), (4, 7, 0), (5, 6, 7), (5, 7, 0), (6, 7, 5), (7, 7, 0), (8, 7, 0)],
	9: [(6, 1, 0), (7, 1, 0), (8, 1, 0)],
	10: [(6, 2, 0), (7, 2, 0), (7, 3, 4), (7, 4, 0), (8, 2, 0), (8, 3, 0), (8, 4, 6)],
	11: [(6, 6, 0), (7, 6, 3), (8, 6, 0)],
	12: [(6, 3, 0), (6, 4, 0), (6, 5, 0), (7, 5, 0), (8, 5, 0)]
}

# Expert / 13
d= [
	[{1: 2}, {1: 0}, {1: 3}, {2: 0}, {2: 0}, {3: 0}],
	[{1: 0}, {2: 0}, {2: 0}, {2: 0}, {3: 0}, {3: 0}],
	[{4: 6}, {4: 0}, {4: 0}, {2: 0}, {5: 0}, {5: 0}],
	[{6: 2}, {4: 0}, {4: 5}, {8: 0}, {5: 0}, {5: 5}],
	[{6: 0}, {4: 0}, {7: 0}, {8: 0}, {8: 6}, {5: 0}],
	[{6: 0}, {6: 0}, {7: 0}, {8: 0}, {8: 3}, {8: 0}],
	[{6: 0}, {7: 0}, {7: 0}, {11: 0}, {11: 0}, {12: 0}],
	[{6: 0}, {7: 4}, {10: 0}, {10: 0}, {11: 0}, {12: 0}],
	[{9: 0}, {7: 0}, {10: 0}, {11: 4}, {11: 0}, {11: 0}]
]
```

## Solving the grid

```python
from grid import Grid
d = [
	[{1: 0}, {2: 2}, {3: 3}, {3: 0}],
	[{1: 0}, {2: 0}, {2: 4}, {3: 0}],
	[{1: 0}, {2: 0}, {2: 0}, {4: 0}],
	[{4: 0}, {4: 5}, {4: 0}, {4: 2}],
	[{5: 1}, {5: 0}, {6: 0}, {4: 6}]
]
grid = Grid(d)
grid.solve()
```

Just for fun or debug:
```python
for c in grid.cells:
  print(f"({c.row}, {c.col}, {c.value}) -- {c.denied_values} ++ {c.allowed_values}")

```
