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

class RelationalCore:
	def __init__(self, numRow: int, numColumn: int, factor: float = 0.5) -> None:
		super().__init__()
		self.timestamp = 1
		self.factor = factor
		self.indexEdge = [0] * numRow
		self.indexSource = [0] * numRow
		self.indexDestination = [0] * numRow
		self.numCurrentEdge = CountMinSketch(numRow, numColumn)
		self.numTotalEdge = deepcopy(self.numCurrentEdge)
		self.numCurrentSource = CountMinSketch(numRow, numColumn)
		self.numTotalSource = deepcopy(self.numCurrentSource)
		self.numCurrentDestination = CountMinSketch(numRow, numColumn)
		self.numTotalDestination = deepcopy(self.numCurrentDestination)

	@staticmethod
	def ComputeScore(a: float, s: float, t: float) -> float:
		return 0 if s == 0 or t - 1 == 0 else pow((a - s / t) * t, 2) / (s * (t - 1))

	def __call__(self, source: int, destination: int, timestamp: int) -> float:
		if self.timestamp < timestamp:
			self.numCurrentEdge.MultiplyAll(self.factor)
			self.numCurrentSource.MultiplyAll(self.factor)
			self.numCurrentDestination.MultiplyAll(self.factor)
			self.timestamp = timestamp
		self.numCurrentEdge.Hash(self.indexEdge, source, destination)
		self.numCurrentEdge.Add(self.indexEdge)
		self.numTotalEdge.Add(self.indexEdge)
		self.numCurrentSource.Hash(self.indexSource, source)
		self.numCurrentSource.Add(self.indexSource)
		self.numTotalSource.Add(self.indexSource)
		self.numCurrentDestination.Hash(self.indexDestination, destination)
		self.numCurrentDestination.Add(self.indexDestination)
		self.numTotalDestination.Add(self.indexDestination)
		return max([
			self.ComputeScore(self.numCurrentEdge(self.indexEdge), self.numTotalEdge(self.indexEdge), timestamp),
			self.ComputeScore(self.numCurrentSource(self.indexSource), self.numTotalSource(self.indexSource), timestamp),
			self.ComputeScore(self.numCurrentDestination(self.indexDestination), self.numTotalDestination(self.indexDestination), timestamp),
		])
