import pipeline

if __name__ == '__main__':
	f1str = input("f(x) = ")
	f2str = input("g(x) = ")
	x1 = float(input("x1 = "))
	x2 = float(input("x2 = "))
	n = 400

	f1, f2 = pipeline.create_math_functions(f1str, f2str)

	xsection = pipeline.create_xsection(f1, f2, x1, x2, n)

	for x, i, o in xsection:
		print(x, i, o, sep="\t")