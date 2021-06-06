from numba import float_, int_, types
from numba.experimental import jitclass
from numpy import inf, zeros
from numpy.random import randint

# region @jitclass
@jitclass({
	'index': int_[:],
	'current': float_[:],
	'total': float_[:],
	'score': float_[:],
})
# endregion
class CMSGroup:
	def __init__(self, length: int):
		self.index = zeros(length, int_)
		self.current = zeros(length, float_)
		self.total = zeros(length, float_)
		self.score = zeros(length, float_)

# region @jitclass
@jitclass({
	'nameAlg': types.string,
	'ts': int_,
	'row': int_,
	'col': int_,
	'threshold': float_,
	'factor': float_,
	'param': int_[:],
	'edge': CMSGroup.class_type.instance_type,
	'source': CMSGroup.class_type.instance_type,
	'destination': CMSGroup.class_type.instance_type,
	'tsReciprocal': float_,
})
# endregion
class FilteringCore:
	def __init__(self, row: int, col: int, threshold: float, factor: float = 0.5):
		self.nameAlg = 'MIDAS-F'
		self.ts = 1
		self.row = row
		self.col = col
		self.threshold = threshold
		self.factor = factor
		self.param = randint(1, 1 << 16, 2 * row).astype(int_)
		self.edge = CMSGroup(row * col)
		self.source = CMSGroup(row * col)
		self.destination = CMSGroup(row * col)
		self.tsReciprocal = 0

	@staticmethod
	def ChiSquaredTest(a: float, s: float, t: float) -> float:
		return 0 if s == 0 else pow(a + s - a * t, 2) / (s * (t - 1))

	def Update(self, a: int, b: int, ts: int, cms: CMSGroup) -> float:
		minCurrent = minTotal = inf
		for i in range(self.row):
			cms.index[i] = i * self.col + ((a + 347 * b) * self.param[i] + self.param[i + self.row]) % self.col
			i = cms.index[i]
			cms.current[i] += 1
			minCurrent = min(minCurrent, cms.current[i])
			minTotal = min(minTotal, cms.total[i])
		score = self.ChiSquaredTest(minCurrent, minTotal, ts)
		for i in cms.index:
			cms.score[i] = score
		return score

	def Call(self, src: int, dst: int, ts: int) -> float:
		if self.ts < ts:
			for cms in [self.edge, self.source, self.destination]:
				for i in range(self.row * self.col):
					cms.total[i] += cms.current[i] if cms.score[i] < self.threshold else cms.total[i] * self.tsReciprocal
				cms.current *= self.factor
			self.tsReciprocal = 1 / (ts - 1)
			self.ts = ts
		return max(
			self.Update(src, dst, ts, self.edge),
			self.Update(src, 0, ts, self.source),
			self.Update(dst, 0, ts, self.destination),
		)
