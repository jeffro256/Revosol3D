class CrossSection(object):
	def __init__(self, x1, x2):
		self.x1 = x1
		self.x2 = x2

		self._samples = []

	def addSample(self, x, inner, outer):
		if not x1 <= x <= x2:
			raise ValueError("x value not in bounds [{}, {}]".format(x, x1, x2))

		ins_index = 0
		for i in reversed(range(len(self._samples))):
			if x > self._samples[i][0]:
				ins_index = i + 1
				break

		sample = (x, inner, outer)
		self._samples.insert(ins_index, sample)

	def __getitem__(self, index):
		return self._samples[index]

	def __iter__(self):
		return iter(self._samples)

	def __len__(self):
		return len(self._samples)
