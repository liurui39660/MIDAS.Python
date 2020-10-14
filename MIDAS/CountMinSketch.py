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

from random import randint
from typing import List

class CountMinSketch:
	def __init__(self, numRow: int, numColumn: int) -> None:
		super().__init__()
		self.r: int = numRow
		self.c: int = numColumn
		self.m: int = 104729  # The same magic number in C++ implementation
		self.lenData: int = self.r * self.c
		self.param1 = [randint(0, 0x7fff) + 1 for _ in range(self.r)]
		self.param2 = [randint(0, 0x7fff) for _ in range(self.r)]
		self.data = [0.] * self.lenData

	def ClearAll(self, with_: float = 0) -> None:
		self.data = [with_] * self.lenData  # Faster than for loop

	def MultiplyAll(self, by: float) -> None:
		for i in range(self.lenData):  # Faster than list(map(...))
			self.data[i] *= by

	def Hash(self, indexOut: List[int], a: int, b: int = 0) -> None:
		for i in range(self.r):  # Faster than using two maps
			indexOut[i] = ((a + self.m * b) * self.param1[i] + self.param2[i]) % self.c
			indexOut[i] += i * self.c + (self.c if indexOut[i] < 0 else 0)

	def __call__(self, index: List[int]) -> float:
		return min(map(lambda i: self.data[i], index))  # Faster than for loop

	def Assign(self, index: List[int], with_: float) -> float:
		for i in index:
			self.data[i] = with_
		return with_

	def Add(self, index: List[int], by: float = 1) -> None:
		for i in index:
			self.data[i] += by
