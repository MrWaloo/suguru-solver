
from cell import Cell

class Shape:
	def __init__(self, id: int):
		self.id = id
		self.cells: list[Cell] = []

	def add_cell(self, cell: Cell) -> Cell:
		self.cells.append(cell)
		return cell
	
	@property
	def size(self) -> int:
		return len(self.cells)
	
	def has_value(self, value: int) -> bool:
		for cell in self.cells:
			if cell.value == value:
				return True
		return False
	
	def found_values(self) -> set:
		values = set()
		for cell in self.cells:
			if cell.value is not None:
				values.add(cell.value)
		return values