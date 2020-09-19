# ------------------------------------------------------------------------------
# Copyright 2020 Rui LIU (@liurui39660)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# 	http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

from copy import deepcopy

from .CountMinSketch import CountMinSketch

class FilteringCore:
	def __init__(self, numRow: int, numColumn: int, threshold: float, factor: float = 0.5) -> None:
		super().__init__()
		self.timestamp = 1
		self.threshold = threshold
		self.factor = factor
		self.indexEdge = [0] * numRow
		self.indexSource = [0] * numRow
		self.indexDestination = [0] * numRow
		self.numCurrentEdge = CountMinSketch(numRow, numColumn)
		self.numTotalEdge = deepcopy(self.numCurrentEdge)
		self.scoreEdge = deepcopy(self.numCurrentEdge)
		self.numCurrentSource = CountMinSketch(numRow, numColumn)
		self.numTotalSource = deepcopy(self.numCurrentSource)
		self.scoreSource = deepcopy(self.numCurrentSource)
		self.numCurrentDestination = CountMinSketch(numRow, numColumn)
		self.numTotalDestination = deepcopy(self.numCurrentDestination)
		self.scoreDestination = deepcopy(self.numCurrentDestination)
		self.timestampReciprocal = 0

	@staticmethod
	def ComputeScore(a: float, s: float, t: float) -> float:
		return 0 if s == 0 else pow(a + s - a * t, 2) / (s * (t - 1))

	def __call__(self, source: int, destination: int, timestamp: int) -> float:
		if self.timestamp < timestamp:
			for i in range(self.numCurrentEdge.lenData):
				self.numTotalEdge.data[i] += self.numCurrentEdge.data[i] if self.scoreEdge.data[i] < self.threshold else self.numTotalEdge.data[i] * self.timestampReciprocal
			for i in range(self.numCurrentSource.lenData):
				self.numTotalSource.data[i] += self.numCurrentSource.data[i] if self.scoreSource.data[i] < self.threshold else self.numTotalSource.data[i] * self.timestampReciprocal
			for i in range(self.numCurrentDestination.lenData):
				self.numTotalDestination.data[i] += self.numCurrentDestination.data[i] if self.scoreDestination.data[i] < self.threshold else self.numTotalDestination.data[i] * self.timestampReciprocal
			self.numCurrentEdge.MultiplyAll(self.factor)
			self.numCurrentSource.MultiplyAll(self.factor)
			self.numCurrentDestination.MultiplyAll(self.factor)
			self.timestampReciprocal = 1 / (timestamp - 1)
			self.timestamp = timestamp
		self.numCurrentEdge.Hash(self.indexEdge, source, destination)
		self.numCurrentEdge.Add(self.indexEdge)
		self.numCurrentSource.Hash(self.indexSource, source)
		self.numCurrentSource.Add(self.indexSource)
		self.numCurrentDestination.Hash(self.indexDestination, destination)
		self.numCurrentDestination.Add(self.indexDestination)
		return max([
			self.scoreEdge.Assign(self.indexEdge, self.ComputeScore(self.numCurrentEdge(self.indexEdge), self.numTotalEdge(self.indexEdge), timestamp)),
			self.scoreSource.Assign(self.indexSource, self.ComputeScore(self.numCurrentSource(self.indexSource), self.numTotalSource(self.indexSource), timestamp)),
			self.scoreDestination.Assign(self.indexDestination, self.ComputeScore(self.numCurrentDestination(self.indexDestination), self.numTotalDestination(self.indexDestination), timestamp))
		])
