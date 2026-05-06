"""
This module defines the Grid class, which represents the entire puzzle grid.
It manages the shapes and cells, and contains the logic for solving the puzzle by applying constraints and deducing values based
on the relationships between cells and shapes.
"""

from shape import Shape
from cell import Cell

class Grid:
	def __init__(self, config: dict[int, list[tuple[int, int, int|None]]]|list[list[dict[int, int]]]):
		self.shapes: list[Shape] = []
		self.cells: list[Cell] = []
		if isinstance(config, dict):
			for shape_id, cell_data in config.items():
				shape = self.add_shape(shape_id)
				for row, col, value in cell_data:
					value = None if value == 0 else value
					cell = self.add_cell(row, col, value)
					shape.add_cell(cell)
		elif isinstance(config, list):
			for row, row_data in enumerate(config):
				for col, cell_data in enumerate(row_data):
					row_idx = row + 1
					col_idx = col + 1
					for shape_id, value in cell_data.items():
						if not self.shape_exists(shape_id):
							shape = self.add_shape(shape_id)
						else:
							shape = next(s for s in self.shapes if s.id == shape_id)
						value = None if value == 0 else value
						cell = self.add_cell(row_idx, col_idx, value)
						shape.add_cell(cell)
	
	@property
	def total_shapes(self) -> int:
		return len(self.shapes)
	
	@property
	def rows(self) -> int:
		max_row = 0
		for shape in self.shapes:
			for cell in shape.cells:
				if cell.row > max_row:
					max_row = cell.row
		return max_row

	@property
	def cols(self) -> int:
		max_col = 0
		for shape in self.shapes:
			for cell in shape.cells:
				if cell.col > max_col:
					max_col = cell.col
		return max_col

	def add_shape(self, shape_id: int) -> Shape:
		shape = Shape(shape_id)
		self.shapes.append(shape)
		return shape

	def shape_exists(self, shape_id: int) -> bool:
		return any(shape.id == shape_id for shape in self.shapes)

	def add_cell(self, row: int, col: int, value: int|None) -> Cell:
		cell = Cell(row, col, value)
		self.cells.append(cell)
		return cell
	
	def neighbors_of(self, cell: Cell) -> list[Cell]:
		neighbors = []
		for row, col in cell.neighbors:
			if row > self.rows or col > self.cols:
				continue
			for c in self.cells:
				if c.row == row and c.col == col:
					neighbors.append(c)
					break
		return neighbors
	
	def check_denied_values(self, cell: Cell):
		neighbors = self.neighbors_of(cell)
		for allowed_value in cell.allowed_values.copy():
			f = {}
			for neighbor in neighbors:
				if neighbor.value is None and allowed_value in neighbor.allowed_values and allowed_value not in neighbor.denied_values:
					for shape in self.shapes:
						if neighbor in shape.cells and cell not in shape.cells:
							for shape_cell in shape.cells:
								if shape_cell == cell:
									continue
								if shape_cell.value is None and allowed_value in shape_cell.allowed_values and allowed_value not in shape_cell.denied_values:
									if f.get(shape.id) is None:
										f[shape.id] = []
									f[shape.id].append(shape_cell)
			for shape_id, shape_cells in f.items():
				if set(shape_cells) <= set(neighbors):
					cell.deny_value(allowed_value)
					#print("PLOP", cell.row, cell.col, allowed_value, shape_id)

	def solve(self) -> bool:
		stay = True
		solved = False
		loops = 0
		while stay and not solved:
			loops += 1
			stay = False
			for shape in self.shapes:
				for cell in shape.cells:
					if cell.value is not None:
						continue
					possible_values = set(range(1, shape.size + 1))
					# Remove found values in the same shape
					possible_values -= shape.found_values()
					# Remove denied values
					possible_values -= cell.denied_values
					# Update allowed and denied values
					cell.prev_allowed = cell.allowed_values.copy()
					cell.prev_denied = cell.denied_values.copy()
					cell.allow_values(possible_values)

					neighbors = self.neighbors_of(cell)
					# Deny values found in neighbors
					for neighbor in neighbors:
						if neighbor.value in possible_values:
							cell.deny_value(neighbor.value)
				
				for shape in self.shapes:
					for cell in shape.cells:
						if cell.value is not None:
							continue
						# Check for unique allowed values in the shape
						for value in cell.allowed_values:
							unique = True
							for other_cell in shape.cells:
								if other_cell == cell or other_cell.value is not None:
									continue
								if value in other_cell.allowed_values or other_cell.value == value:
									unique = False
									break
							if unique:
								self.set_cell_value(cell, value)
								stay = True
								break
						
						if cell.value is None:
							self.check_denied_values(cell)

				for cell in self.cells:
					if cell.value is not None:
						continue
					# If only one possible value, assign it
					if len(cell.allowed_values) == 1:
						self.set_cell_value(cell, cell.allowed_values.pop())
						stay = True
					# Check if allowed or denied values changed
					if cell.prev_allowed != cell.allowed_values or cell.prev_denied != cell.denied_values:
						stay = True
			
			# Check if all cells are filled
			solved = all(cell.value is not None for cell in self.cells)

			#for s in self.shapes:
			#	print(f"**** shape id: {s.id}")
			#	for c in s.cells:
			#		print(f"({c.row}, {c.col}, {c.value}) -- {c.denied_values} ++ {c.allowed_values}")
			#print("---- Loop", loops, "Stay:", stay, "Solved:", solved, "----")

		if solved:
			print("Puzzle solved in", loops, "loops!")
			self.show()
		
		return stay or solved
	
	def set_cell_value(self, cell: Cell, value: int):
		cell.value = value
		for shape in self.shapes:
			if cell in shape.cells:
				for shape_cell in shape.cells:
					if shape_cell != cell:
						shape_cell.deny_value(value)
				break
	
	def show(self):
		grid = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
		for cell in self.cells:
			if cell.value is not None:
				grid[cell.row - 1][cell.col - 1] = str(cell.value)
		for row in grid:
			print(" ".join(row))

	def show_graphical(self):
		rows = self.rows
		cols = self.cols
		# Create grid of values and shapes
		grid = [[' ' for _ in range(cols)] for _ in range(rows)]
		shape_grid = [[None for _ in range(cols)] for _ in range(rows)]
		for cell in self.cells:
			grid[cell.row - 1][cell.col - 1] = str(cell.value) if cell.value else ' '
			for shape in self.shapes:
				if cell in shape.cells:
					shape_grid[cell.row - 1][cell.col - 1] = shape.id # pyright: ignore[reportArgumentType, reportCallIssue]
					break
		
		# Top border
		top = '┌' + '┬'.join('───' for _ in range(cols)) + '┐'
		print(top)
		
		for r in range(rows):
			# Row content
			row_str = '│'
			for c in range(cols):
				val = grid[r][c]
				row_str += f' {val} '
				if c < cols - 1:
					if shape_grid[r][c] == shape_grid[r][c+1]:
						row_str += '·'
					else:
						row_str += '│'
			row_str += '│'
			print(row_str)
			
			# Horizontal line below, if not last
			if r < rows - 1:
				line = '├'
				for c in range(cols):
					if shape_grid[r][c] == shape_grid[r+1][c]:
						line += ' - '
					else:
						line += '───'
					if c < cols - 1:
						# Junction
						up_diff = shape_grid[r][c] != shape_grid[r][c+1]
						down_diff = shape_grid[r+1][c] != shape_grid[r+1][c+1]
						left_diff = shape_grid[r][c] != shape_grid[r+1][c]
						right_diff = shape_grid[r][c+1] != shape_grid[r+1][c+1]
						if not left_diff and not right_diff and not up_diff and not down_diff:
							line += '┼'
						elif not left_diff and not right_diff and not up_diff:
							line += '┴'
						elif not left_diff and not right_diff and not down_diff:
							line += '┬'
						elif not left_diff and not up_diff and not down_diff:
							line += '┤'
						elif not right_diff and not up_diff and not down_diff:
							line += '├'
						elif not left_diff and not right_diff:
							line += '─'
						elif not up_diff and not down_diff:
							line += '│'
						else:
							line += ' '
				line += '┤'
				print(line)
		
		# Bottom border
		bottom = '└' + '┴'.join('───' for _ in range(cols)) + '┘'
		print(bottom)