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

	def __str__(self):
		cls_name = type(self).__name__
		return "{}<{}, {}, {}>".format(cls_name, self.x, self.y, self.z)

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

	def normal(self):
		edge1 = self.p2 - self.p1
		edge2 = self.p3 - self.p1

		return edge1.cross(edge2).normalized()
