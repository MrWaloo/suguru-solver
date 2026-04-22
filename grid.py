"""
This module defines the Grid class, which represents the entire puzzle grid.
It manages the forms and cells, and contains the logic for solving the puzzle by applying constraints and deducing values based
on the relationships between cells and forms.
"""

from form import Form
from cell import Cell

class Grid:
	def __init__(self, config: dict[int, list[tuple[int, int, int|None]]]|list[list[dict[int, int]]]):
		self.forms: list[Form] = []
		self.cells: list[Cell] = []
		if isinstance(config, dict):
			for form_id, cell_data in config.items():
				form = self.add_form(form_id)
				for row, col, value in cell_data:
					value = None if value == 0 else value
					cell = self.add_cell(row, col, value)
					form.add_cell(cell)
		elif isinstance(config, list):
			for row, row_data in enumerate(config):
				for col, cell_data in enumerate(row_data):
					row_idx = row + 1
					col_idx = col + 1
					for form_id, value in cell_data.items():
						if not self.form_exists(form_id):
							form = self.add_form(form_id)
						else:
							form = next(f for f in self.forms if f.id == form_id)
						value = None if value == 0 else value
						cell = self.add_cell(row_idx, col_idx, value)
						form.add_cell(cell)
	
	@property
	def total_forms(self) -> int:
		return len(self.forms)
	
	@property
	def rows(self) -> int:
		max_row = 0
		for form in self.forms:
			for cell in form.cells:
				if cell.row > max_row:
					max_row = cell.row
		return max_row

	@property
	def cols(self) -> int:
		max_col = 0
		for form in self.forms:
			for cell in form.cells:
				if cell.col > max_col:
					max_col = cell.col
		return max_col

	def add_form(self, form_id: int) -> Form:
		form = Form(form_id)
		self.forms.append(form)
		return form

	def form_exists(self, form_id: int) -> bool:
		return any(form.id == form_id for form in self.forms)

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
					for form in self.forms:
						if neighbor in form.cells and cell not in form.cells:
							for form_cell in form.cells:
								if form_cell == cell:
									continue
								if form_cell.value is None and allowed_value in form_cell.allowed_values and allowed_value not in form_cell.denied_values:
									if f.get(form.id) is None:
										f[form.id] = []
									f[form.id].append(form_cell)
			for form_id, form_cells in f.items():
				if set(form_cells) <= set(neighbors):
					cell.deny_value(allowed_value)
					print("PLOP", cell.row, cell.col, allowed_value, form_id)

	def solve(self) -> bool:
		stay = True
		solved = False
		loops = 0
		while stay and not solved:
			loops += 1
			stay = False
			for form in self.forms:
				for cell in form.cells:
					if cell.value is not None:
						continue
					possible_values = set(range(1, form.size + 1))
					# Remove found values in the same form
					possible_values -= form.found_values()
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
				
				for form in self.forms:
					for cell in form.cells:
						if cell.value is not None:
							continue
						# Check for unique allowed values in the form
						for value in cell.allowed_values:
							unique = True
							for other_cell in form.cells:
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
					# Check if allowed values changed
					if cell.prev_allowed != cell.allowed_values or cell.prev_denied != cell.denied_values:
						stay = True
			
			# Check if all cells are filled
			solved = all(cell.value is not None for cell in self.cells)

			for f in self.forms:
				print(f"**** form id: {f.id}")
				for c in f.cells:
					print(f"({c.row}, {c.col}, {c.value}) -- {c.denied_values} ++ {c.allowed_values}")
			print("---- Loop", loops, "Stay:", stay, "Solved:", solved, "----")

		if solved:
			print("Puzzle solved in", loops, "loops!")
			self.show()
		
		return stay or solved
	
	def set_cell_value(self, cell: Cell, value: int):
		cell.value = value
		for form in self.forms:
			if cell in form.cells:
				for form_cell in form.cells:
					if form_cell != cell:
						form_cell.deny_value(value)
				break
	
	def show(self):
		grid = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
		for cell in self.cells:
			if cell.value is not None:
				grid[cell.row - 1][cell.col - 1] = str(cell.value)
		for row in grid:
			print(" ".join(row))