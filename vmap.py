__all__ = ['VertexMap', 'VertexRing']

# Specialized!
class VertexMap(object):
	def __init__(self):
		self.inner = []
		self.outer = []

class VertexRing(list):
	def __init__(self, x, unit_circle, radius):
		super().__init__()

		self.extend([(pt * radius).withx(x) for pt in unit_circle])

		self.x = x
		self.radius = radius

	def __eq__(self, other):
		return self.x == other.x and self.radius == other.radius and len(self) == len(other)

	def __lt__(self, other):
		return self.x < other.x