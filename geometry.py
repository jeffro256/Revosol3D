import math

class Vector2D(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		x = self.x + other.x
		y = self.y + other.y

		return type(self)(x, y)

	def __sub__(self, other):
		x = self.x - other.x
		y = self.y - other.y

		return type(self)(x, y)

	def __mul__(self, other):
		if type(other) == type(self):
			raise NotImplementedError("Can only scale by constants right now")

		x = self.x * other
		y = self.y * other

		return type(self)(x, y)

	def __truediv__(self, other):
		if type(other) == type(self):
			raise NotImplementedError("Can only scale by constants right now")

		x = self.x / other
		y = self.y / other

		return type(self)(x, y)

	def __neg__(self):
		return type(self)(-self.x, -self.y)

	def __pos__(self):
		return type(self)(self.x, self.y)

	def __abs__(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)

	def __str__(self):
		return "{}<{}, {}>".format(type(self).__name__, self.x, self.y)

	def normalized(self):
		return self / abs(self)

	def data_str(self):
		return "{}\t{}".format(self.x, self.y)

	def withx(self, x):
		return Vector3D(x, self.x, self.y)

	def withy(self, y):
		return Vector3D(self.x, y, self.y)

	def withz(self, z):
		return Vector3D(self.x, self.y, z)

class Vector3D(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other):
		x = self.x + other.x
		y = self.y + other.y
		z = self.z + other.z

		return type(self)(x, y, z)

	def __sub__(self, other):
		x = self.x - other.x
		y = self.y - other.y
		z = self.z - other.z

		return type(self)(x, y, z)

	def __mul__(self, other):
		if type(other) == type(self):
			raise NotImplementedError("Can only scale by constants right now")

		x = self.x * other
		y = self.y * other
		z = self.z * other

		return type(self)(x, y, z)

	def __truediv__(self, other):
		if type(other) == type(self):
			raise NotImplementedError("Can only scale by constants right now")

		x = self.x / other
		y = self.y / other
		z = self.z / other

		return type(self)(x, y, z)

	def __neg__(self):
		return type(self)(-self.x, -self.y, -self.z)

	def __pos__(self):
		return type(self)(self.x, self.y, self.z)

	def __abs__(self):
		return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z

	def __lt__(self, other):
		if self.x < other.x: return True
		if self.y < other.y: return True
		if self.z < other.z: return True

		return False

	def __str__(self):
		cls_name = type(self).__name__
		return "{}<{}, {}, {}>".format(cls_name, self.x, self.y, self.z)

	def __hash__(self):
		return hash((self.x, self.y, self.z))

	def cross(self, other):
		x = self.y * other.z - self.z * other.y
		y = self.z * other.x - self.x * other.z
		z = self.x * other.y - self.y * other.x

		return self(type)(x, y, z)

	def normalized(self):
		return self / abs(self)

	def data_str(self):
		return "{}\t{}\t{}".format(self.x, self.y, self.z)

class Triangle(object):
	def __init__(self, p1, p2, p3):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3

		if p1 == p2 or p2 == p3 or p3 == p1:
			raise ValueError("Triangle must contain three unique points")

	def normal(self):
		edge1 = self.p2 - self.p1
		edge2 = self.p3 - self.p1

		return edge1.cross(edge2).normalized()

	# Returns whether triangles share points and face in same direction
	def normal_equals(self, other):
		self_tup = ( self.p1,  self.p2,  self.p3)
		o1       = (other.p1, other.p2, other.p3)
		o2       = (other.p2, other.p3, other.p1)
		o3       = (other.p3, other.p1, other.p2)

		return self_tup == o1 or self_tup == o2 or self_tup == o3
