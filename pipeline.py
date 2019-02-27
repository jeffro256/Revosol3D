def sign(x):
    return -1 if x < 0 else 1

def createxsection(f1, f2, x1, x2, num_samples):
    dx = (x2 - x1) / num_samples

    xsection = CrossSection()

    for i in range(num_samples+1):
        x = x1 + dx * i

        y1 = f1(x)
        y2 = f2(x)

        if sign(y1) != sign(y2):
            inner = 0
            outer = max(abs(y1), abs(y2))
        else:
            inner, outer = sorted((abs(y1), abs(y2)))

        sample = (x, inner, outer)
        xsection.addSample(sample)

    return xsection

def rotatex(xsection, num_samples):
    if num_samples < 3:
        raise ValueError(str(num_samples) + " samples? Are you kidding me?")

    unit_circle = []
    for i in range(num_samples):
        angle = (i / num_samples) * 2 * math.pi
        y, z = math.cos(angle), math.sin(angle)

        pt = Point2D(y, z)
        unit_circle.append(pt)

    scale = lambda a: (lambda x: x * a)

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