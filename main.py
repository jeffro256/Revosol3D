import pipeline

if __name__ == '__main__':
	f1str = input("f(x) = ")
	f2str = input("g(x) = ")
	x1str = input("x1 = ")
	x2str = input("x2 = ")
	f = open(input("filename: "), 'w')
	print()

	xn = 51
	thetan = 30

	f1, f2, x1, x2 = pipeline.create_math_functions(f1str, f2str, x1str, x2str)
	x1, x2 = x1.eval(), x2.eval()

	xsection = pipeline.create_xsection(f1, f2, x1, x2, xn)

	print("created xsection")

	vertmap = pipeline.rotate_xsection(xsection, thetan)

	print("created vertmap")

	triangles = pipeline.get_triangles_from_vmap(vertmap)

	print("created triangles")

	pipeline.write_mesh(f, triangles)

	print("wrote mesh")