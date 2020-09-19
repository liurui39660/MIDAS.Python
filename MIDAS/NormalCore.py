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

class NormalCore:
	def __init__(self, numRow: int, numColumn: int) -> None:
		super().__init__()
		self.timestamp: int = 1
		self.index = [0] * numRow
		self.numCurrent = CountMinSketch(numRow, numColumn)
		self.numTotal = deepcopy(self.numCurrent)

	@staticmethod
	def ComputeScore(a: float, s: float, t: float) -> float:
		return 0 if s == 0 or t - 1 == 0 else pow((a - s / t) * t, 2) / (s * (t - 1))

	def __call__(self, source: int, destination: int, timestamp: int) -> float:
		if self.timestamp < timestamp:
			self.numCurrent.ClearAll()
			self.timestamp = timestamp
		self.numCurrent.Hash(self.index, source, destination)
		self.numCurrent.Add(self.index)
		self.numTotal.Add(self.index)
		return self.ComputeScore(self.numCurrent(self.index), self.numTotal(self.index), timestamp)
