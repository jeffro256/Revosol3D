#!/usr/local/bin/python3

from datetime import datetime
from pathlib import Path

from mathparse import MathParser
import pipeline

version = (1, 1, 2)
ver_str = "{}.{}.{}".format(*version)

def main():
	f1, f2, xparse = MathParser(), MathParser(), MathParser()
	# 2.1 is a random num I thought of
	guaranteed_input("f(x) = ", lambda s: (f1.feed(s), f1.eval(2.1)))
	guaranteed_input("g(x) = ", lambda s: (f2.feed(s), f2.eval(2.1)))
	x1 = guaranteed_input("x1 = ", lambda s: (xparse.feed(s), xparse.eval())[-1])
	x2 = guaranteed_input("x2 = ", lambda s: (xparse.feed(s), xparse.eval())[-1])
	qual = guaranteed_input("Quality (5-12 recommended): ", float)
	fname = input("File name: ")
	fullfname = str(Path.home()) + "/Documents/" + fname
	f = open(fullfname, 'w')
	print()

	a = 10
	b = 1.5
	c = 3
	xn = int(a * b ** qual)
	thetan = int(c * b ** qual)

	print("x samples: {}, θ samples: {}".format(xn, thetan))

	xsection = pipeline.create_xsection(f1, f2, x1, x2, xn)

	print("Created cross section.")

	volume = pipeline.get_volume_from_xsection(xsection)
	vol_str = "%.2f" % volume

	print("Volume:", vol_str)

	xsection, epsilon = pipeline.remove_holes_from_xsection(xsection)

	epsilon_str = "%.4f" % epsilon

	print("Removed holes from cross section. Epsilon:", epsilon_str)

	vertmap = pipeline.rotate_xsection(xsection, thetan)

	print("Created vertex map.")

	triangles = pipeline.get_triangles_from_vmap(vertmap)

	print("Created {} triangles.".format(len(triangles)))

	metadata = {
		'Date Created'        : datetime.now().isoformat(),
		'Revosol3D Version'   : ver_str,
		'Function 1'          : f1.parse_string(),
		'Function 2'          : f2.parse_string(),
		'Left Bound'          : x1,
		'Right Bound'         : x2,
		'# of x samples'      : xn,
		'# of theta samples'  : thetan,
		'# of triangles'      : len(triangles),
		'Volume'              : volume,
		'Quality coefficient' : qual,
		'Original save path'  : fullfname
	}

	pipeline.write_mesh(f, triangles, metadata=metadata, showProgress=True)

	print("Wrote mesh to file {}.".format(fullfname))

	input("Done. Press Enter to Quit.\n")

def guaranteed_input(prompt, func, err_handler=None):
	while True:
		in_str = input(prompt)

		try:
			return func(in_str)
		except Exception as e:
			if err_handler:
				err_handler(in_str, e)
			else:
				print("Sorry, that couldn't be parsed.")
				print("Try again")

if __name__ == '__main__':
	main()
