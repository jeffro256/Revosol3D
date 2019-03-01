# Specialized!
class VertexMap(object):
	def __init__(self):
		self.inner = []
		self.outer = []

class VertexRing(list):
	def __init__(self, x, unit_circle, radius):
		super().__init__()

		self.extend([(radius * pt).withx(x) for pt in unit_circle])

		self.x = x
