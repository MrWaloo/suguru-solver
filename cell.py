
class Cell:
	def __init__(self, row: int, col: int, value: int|None=None):
		self.row = row
		self.col = col
		self.value = value
		self._allowed_values = set()
		self._denied_values = set()
		self.prev_allowed = set()
		self.prev_denied = set()

	@property
	def allowed_values(self) -> set:
		return self._allowed_values

	@property
	def denied_values(self) -> set:
		return self._denied_values
	
	@property
	def neighbors(self) -> list[tuple[int, int]]:
		neighbors = []
		for dr in [-1, 0, 1]:
			for dc in [-1, 0, 1]:
				if dr == 0 and dc == 0:
					continue
				if self.row + dr > 0 and self.col + dc > 0:
					neighbors.append((self.row + dr, self.col + dc))
		return neighbors
	
	def allow_values(self, values: set):
		self._allowed_values |= values
		self._denied_values -= values
	
	def allow_value(self, value: int):
		allow = set([value])
		self.allow_values(allow)

	def deny_values(self, values: set):
		self._denied_values |= values
		self._allowed_values -= values

	def deny_value(self, value: int):
		deny = set([value])
		self.deny_values(deny)