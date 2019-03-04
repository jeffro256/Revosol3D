from bisect import bisect_left

from geometry import *
from mathparse import MathParser
from vmap import VertexMap, VertexRing

def create_math_functions(*strs):
	parsers = [MathParser() for _ in range(len(strs))]

	for i, s in enumerate(strs):
		parsers[i].feed(s)

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

			try:
				t1 = Triangle(v1, v2, v3)

				triangles.append(t1)
			except:
				pass
			
			try:
				#t2 = Triangle(v2, v3, v4)
				t2 = Triangle(v4, v3, v2)

				triangles.append(t2)
			except:
				pass ################################################# FIIIIIIXXXXX

			if not t1.normal_equals(t2): # To catch when one ring's radius is 0
				triangles.extend((t1, t2))
			else:
				triangles.append(t1)

	# outer
	for i in range(num_rings - 1):
		this_ring = vertex_map.outer[i]
		next_ring = vertex_map.outer[i+1]

		for j in range(-num_ring_pts, 0):
			v1 = this_ring[j]
			v2 = this_ring[j+1]
			v3 = next_ring[j]
			v4 = next_ring[j+1]

			try:
				t1 = Triangle(v1, v2, v3)

				triangles.append(t1)
			except:
				pass
			
			try:
				#t2 = Triangle(v2, v3, v4)
				t2 = Triangle(v4, v3, v2)

				triangles.append(t2)
			except:
				pass ################################################# FIIIIIIXXXXX

	# left cap
	left_iring = vertex_map.inner[0]
	left_oring = vertex_map.outer[0]
	for i in range(num_ring_pts):
		v1 = left_iring[i]
		v2 = left_oring[i]
		v3 = left_oring[i-1]
		v4 = left_iring[i-1]

		t1 = Triangle(v1, v2, v3)
		#t2 = Triangle(v2, v3, v4)
		t2 = Triangle(v4, v3, v2)

		if left_iring.radius != 0:
			triangles.extend((t1, t2))
		else:
			triangles.append(t1)

	# right cap
	right_iring = vertex_map.inner[-1]
	right_oring = vertex_map.outer[-1]
	for i in range(-num_ring_pts, 0):
		v1 = right_iring[i]
		v2 = right_oring[i]
		v3 = right_oring[i+1]
		v4 = right_iring[i+1]

		t1 = Triangle(v1, v2, v3)
		#t2 = Triangle(v2, v3, v4)
		t2 = Triangle(v4, v3, v2)

		if right_iring.radius != 0:
			triangles.extend((t1, t2))
		else:
			triangles.append(t1)

	return triangles

def write_mesh(f, triangles):
	vertices = set()

	for triangle in triangles:
		vertices.update((triangle.p1, triangle.p2, triangle.p3))

	print("m1")

	#vertices = sorted(list(vertices))
	vertices = list(vertices)

	for vertex in vertices:
		f.write("v {} {} {}\n".format(vertex.x, vertex.y, vertex.z))

	print("m2")

	l = len(triangles)
	for i, triangle in enumerate(triangles):
		print("{}%".format(i / l * 100))

		vert_index1 = vertices.index(triangle.p1) + 1
		vert_index2 = vertices.index(triangle.p2) + 1
		vert_index3 = vertices.index(triangle.p3) + 1

		f.write("f {} {} {}\n".format(vert_index1, vert_index2, vert_index3))

	print("m3")

	f.close()








