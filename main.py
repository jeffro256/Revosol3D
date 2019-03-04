#!/usr/local/bin/python3

from pathlib import Path

import pipeline

if __name__ == '__main__':
	f1str = input("f(x) = ")
	f2str = input("g(x) = ")
	x1str = input("x1 = ")
	x2str = input("x2 = ")
	qual = float(input("Quality (1-12 recommended): "))
	fname = input("File name: ")
	fullfname = str(Path.home()) + "/Documents/" + fname
	f = open(fullfname, 'w')
	print()

	print(Path.home())

	a = 10
	b = 1.5
	c = 3
	xn = int(a * b ** qual)
	thetan = int(c * b ** qual)

	print("x samples: {}, θ samples: {}".format(xn, thetan))

	f1, f2, x1, x2 = pipeline.create_math_functions(f1str, f2str, x1str, x2str)
	x1, x2 = x1.eval(), x2.eval()

	xsection = pipeline.create_xsection(f1, f2, x1, x2, xn)

	print("Created cross section.")

	volume = pipeline.get_volume_from_xsection(xsection)

	print("Volume:", volume)

	vertmap = pipeline.rotate_xsection(xsection, thetan)

	print("Created vertex map.")

	triangles = pipeline.get_triangles_from_vmap(vertmap)

	print("Created {} triangles.".format(len(triangles)))

	pipeline.write_mesh(f, triangles, showProgress=True)

	print("Wrote mesh to file {}.".format(fullfname))

	input("Done. Press Enter to Quit.\n")
