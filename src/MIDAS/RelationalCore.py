from numba import f4, i4
from numba.core.types import string
from numba.experimental import jitclass
from numpy import inf, zeros
from numpy.random import randint

# region @jitclass
@jitclass({
	'current': f4[:],
	'total': f4[:],
})
# endregion
class CMSGroup:
	def __init__(self, length: int):
		self.current = zeros(length, f4)
		self.total = zeros(length, f4)

# region @jitclass
@jitclass({
	'nameAlg': string,
	'ts': i4,
	'row': i4,
	'col': i4,
	'factor': f4,
	'param': i4[:],
	'edge': CMSGroup.class_type.instance_type,
	'source': CMSGroup.class_type.instance_type,
	'destination': CMSGroup.class_type.instance_type,
})
# endregion
class RelationalCore:
	def __init__(self, row: int, col: int, factor: float = 0.5):
		self.nameAlg = 'MIDAS-R'
		self.ts = 1
		self.row = row
		self.col = col
		self.factor = factor
		self.param = randint(1, 1 << 16, 2 * row).astype(i4)
		self.edge = CMSGroup(row * col)
		self.source = CMSGroup(row * col)
		self.destination = CMSGroup(row * col)

	@staticmethod
	def ChiSquaredTest(a: float, s: float, t: float) -> float:
		return 0 if s == 0 or t - 1 == 0 else pow((a - s / t) * t, 2) / (s * (t - 1))

	def Update(self, a: int, b: int, cms: CMSGroup) -> float:
		minCurrent = minTotal = inf
		for i in range(self.row):
			i = i * self.col + ((a + 347 * b) * self.param[i] + self.param[i + self.row]) % self.col
			cms.current[i] += 1
			cms.total[i] += 1
			minCurrent = min(minCurrent, cms.current[i])
			minTotal = min(minTotal, cms.total[i])
		return self.ChiSquaredTest(minCurrent, minTotal, self.ts)

	def Call(self, src: int, dst: int, ts: int) -> float:
		if self.ts < ts:
			for cms in [self.edge, self.source, self.destination]:
				cms.current *= self.factor
			self.ts = ts
		return max(
			self.Update(src, dst, self.edge),
			self.Update(src, 0, self.source),
			self.Update(dst, 0, self.destination),
		)
