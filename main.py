import math

def crosssection(f1, f2, x1, x2, num_samples):
	dx = (x2 - x1) / num_samples

	bounds = []

	for i in range(num_samples+1):
		x = x1 + dx * i

		y1 = f1(x)
		y2 = f2(x)

		inner, outer = (y1, y2) if abs(y1) < abs(y2) else (y2, y1)

		bounds.append((x, (inner, outer)))

	return bounds

def rotatex(xsection, num_samples):
	if num_samples < 3:
		raise ValueError(str(num_samples) + " sample" + ("s" if num_samples != 1 else "") + "? Are you kidding me?")

	unit_circle = []
	for i in range(num_samples):
		angle = (i / num_samples) * 2 * math.pi
		y, z = math.cos(angle), math.sin(angle)

		unit_circle.append((y, z))

	scale = lambda a: (lambda x: (x[0] * a, x[1] * a))

	vertices = []
	for sample in xsection:
		x = sample[0]
		innerRad = sample[1][0]
		outerRad = sample[1][1]

		innerPoints = list(map(scale(innerRad), unit_circle))
		outerPoints = list(map(scale(outerRad), unit_circle))

		data = (x, innerPoints, outerPoints)

		vertices.append(data)

	return vertices

if __name__ == '__main__':
	def test1():
		f1 = lambda x: math.sin(x)
		f2 = lambda x: x / 3
		x1 = -math.pi
		x2 = math.pi
		n = 100

		xsection = crosssection(f1, f2, x1, x2, n)
		print(xsection)

		for sample in xsection:
			print(sample[0], sample[1][0], sample[1][1], sep="\t")

	def test2():
		xsection = [(0.0, (1.0, 2.5))]
		n = 10

		res = rotatex(xsection, n)
		print(res[0][0])
		print(res[0][1])
		print(res[0][2])

		print("****")
		x, inner, outer = res[0]
		print("->", x)
		for y, z in inner:
			print(y, z, sep="\t")
		print("----")
		for y, z in outer:
			print(y, z, sep="\t")
		print("****")


	test1()
	print("###################################################################")
	test2()


