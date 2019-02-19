def crosssection(f1, f2, x1, x2, n):
	dx = (x2 - x1) / n

	bounds = []

	for i in range(n+1):
		x = x1 + dx * i

		y1 = f1(x)
		y2 = f2(x)

		inner, outer = (y1, y2) if abs(y1) < abs(y2) else (y2, y1)

		bounds.append((x, inner, outer))

	return bounds

def rotatex(xsection, n):
	pass