from bisect import bisect_left
from math import *

from geometry import *
from mathparse import MathParser
from pyparsing import ParseException
from vmap import VertexMap, VertexRing

def create_math_functions(*strs):
	parsers = [MathParser() for _ in range(len(strs))]

	for i, s in enumerate(strs):
		try:
			parsers[i].feed(s)
		except ParseException as pe:
			print("Bad string: ", s)
			raise pe

	return parsers

def create_xsection(f1, f2, x1, x2, num_samples):
	dx = (x2 - x1) / num_samples

	xsection = []

	sign = lambda x: (x > 0) - (x < 0)

	for i in range(num_samples + 1):
		x = x1 + dx * i

		y1 = f1(x)
		y2 = f2(x)

		if sign(y1) != sign(y2):
			inner = 0
			outer = max(abs(y1), abs(y2))
		else:
			inner, outer = sorted((abs(y1), abs(y2)))

		xsection.append((x, (inner, outer)))

	return xsection

def get_volume_from_xsection(xsection):
	vol_sum = 0

	for i in range(len(xsection) - 1):
		this_samp = xsection[i]
		next_samp = xsection[i+1]

		dx = next_samp[0] - this_samp[0]
		y1 = this_samp[1][1]
		y2 = next_samp[1][1]
		y3 = this_samp[1][0]
		y4 = next_samp[1][0]

		#dy1 = y2 - y1
		#dy2 = y4 - y3

		#slice_vol = pi * dx * (dy1**2 / 3 - dy2**2 / 3 + y1 * dy1 - y3 * dy2 + y1**2 - y3**2)
		slice_vol = pi * dx / 3 * (y1 ** 2 + y2 ** 2 - y3 ** 2 - y4 ** 2 + y1*y2 + y3*y4)
		# slice_vol = pi * dx * y1**2 - y3**2

		vol_sum += slice_vol

	return vol_sum

def remove_holes_from_xsection(xsection, epsilon=None):
	if epsilon is None:
		epsilon = max([x[1][1] for x in xsection]) / 1000

	is_small_list = [s[1][0] <= epsilon for s in xsection]

	if is_small_list.count(True) >= 2:
		first_small = is_small_list.index(True)
		last_small = len(xsection) - list(reversed(is_small_list)).index(True) - 1

		new_xsection = []

		new_xsection.extend(xsection[:first_small])
		new_xsection.extend([(s[0], (0.0, s[1][1])) for s in xsection[first_small:last_small+1]])
		new_xsection.extend(xsection[last_small+1:])

		return (new_xsection, epsilon)
	else:
		return (xsection, epsilon)

def rotate_xsection(xsection, num_samples):
	if num_samples < 3:
		raise ValueError(str(num_samples) + " samples? Are you kidding me?")

	vmap = VertexMap()

	unit_circle = []
	for i in range(num_samples):
		angle = (i / num_samples) * 2 * math.pi
		y, z = math.cos(angle), math.sin(angle)

		pt = Vector2D(y, z)
		unit_circle.append(pt)

	for sample in xsection:
		x = sample[0]
		inner_rad = sample[1][0]
		outer_rad = sample[1][1]

		inner_ring = VertexRing(x, unit_circle, inner_rad)
		outer_ring = VertexRing(x, unit_circle, outer_rad)

		vmap.inner.append(inner_ring)
		vmap.outer.append(outer_ring)

	return vmap

def get_triangles_from_vmap(vertex_map):
	triangles = []

	num_rings = len(vertex_map.inner)
	num_ring_pts = len(vertex_map.inner[0]) # Should be the same for all rings 

	# inner
	for i in range(num_rings - 1):
		this_ring = vertex_map.inner[i]
		next_ring = vertex_map.inner[i+1]

		if this_ring.radius == next_ring.radius == 0:
			continue # To avoid making triangles that are just lines
		
		for j in range(num_ring_pts):
			v1 = this_ring[j]
			v2 = this_ring[j-1]
			v3 = next_ring[j]
			v4 = next_ring[j-1]

			t1 = t2 = None

			if v1 != v2:
				t1 = Triangle(v1, v2, v3)

			if v3 != v4:
				t2 = Triangle(v4, v3, v2)
			
			if t1 is None and t2 is None:
				print("Warning, no inner triangles made b/t {} & {}".format(this_ring.x, next_ring.x))

			if t1:
				triangles.append(t1)

			if t2:
				triangles.append(t2)

	# outer
	for i in range(num_rings - 1):
		this_ring = vertex_map.outer[i]
		next_ring = vertex_map.outer[i+1]

		for j in range(-num_ring_pts, 0):
			v1 = this_ring[j]
			v2 = this_ring[j+1]
			v3 = next_ring[j]
			v4 = next_ring[j+1]

			t1 = t2 = None

			if v1 != v2:
				t1 = Triangle(v1, v2, v3)

			if v3 != v4:
				t2 = Triangle(v4, v3, v2)
			
			if t1 is None and t2 is None:
				print("Warning, no outer triangles made b/t {} & {}".format(this_ring.x, next_ring.x))

			if t1:
				triangles.append(t1)

			if t2:
				triangles.append(t2)

	# left cap
	left_iring = vertex_map.inner[0]
	left_oring = vertex_map.outer[0]
	for i in range(num_ring_pts):
		v1 = left_iring[i]
		v2 = left_oring[i]
		v3 = left_oring[i-1]
		v4 = left_iring[i-1]

		t1 = Triangle(v1, v2, v3)
		triangles.append(t1)

		if v1 != v4:
			t2 = Triangle(v1, v3, v4)
			triangles.append(t2)

	# right cap
	right_iring = vertex_map.inner[-1]
	right_oring = vertex_map.outer[-1]
	for i in range(-num_ring_pts, 0):
		v1 = right_iring[i]
		v2 = right_oring[i]
		v3 = right_oring[i+1]
		v4 = right_iring[i+1]

		t1 = Triangle(v1, v2, v3)
		triangles.append(t1)

		if v1 != v4:
			t2 = Triangle(v1, v3, v4)
			triangles.append(t2)

	#flag
	#triangles.append(Triangle(Vector3D(0, 2, 0), Vector3D(1, 3, 0), Vector3D(0, 4, 0)))

	return triangles

def write_mesh(f, triangles, metadata={}, showProgress=False):
	vertices = {}
	vert_index = 1

	faces = []

	l = len(triangles)
	for i, triangle in enumerate(triangles):
		if i % 10 == 0:
			print("Creating mesh: {}%    ".format(int(i / l * 1000) / 10), end="\r", flush=True)

		p1 = triangle.p1
		p2 = triangle.p2
		p3 = triangle.p3

		try:
			p1index = vertices[p1]
		except KeyError:
			vertices[p1] = p1index = vert_index
			vert_index += 1

		try:
			p2index = vertices[p2]
		except KeyError:
			vertices[p2] = p2index = vert_index
			vert_index += 1

		try:
			p3index = vertices[p3]
		except KeyError:
			vertices[p3] = p3index = vert_index
			vert_index += 1

		faces.append((p1index, p2index, p3index))

	vertices = [y[1] for y in sorted([(vertices[x], x) for x in vertices])]

	f.write("# Jeffrey Ryan greets you from early 2019!\n")
	f.write("# This file was created by Revosol3D :)\n\n")

	if metadata:
		f.write("# Metadata:\n")

		for key in metadata:
			f.write("#     {}: {}\n".format(key, metadata[key]))
	else:
		f.write("# No Metadata :(\n")

	f.write("\n\n\n\n\n# Okay, let's get to business!\n\n")

	f.write("\n# VERTICES\n")
	for vertex in vertices:
		f.write("v {} {} {}\n".format(vertex.x, vertex.y, vertex.z))

	f.write("\n# FACES\n")
	for face in faces:
		f.write("f {} {} {}\n".format(*face))

	f.write("\n# Goodbye ;)\n")

	f.close()

