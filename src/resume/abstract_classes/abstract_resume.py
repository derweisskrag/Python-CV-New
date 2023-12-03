from abc import (
	ABC,
	abstractmethod
)

from typing import (
	Dict
)

class CV(ABC):
	def __init__(self, data: Dict, name: str) -> None:
		self._data = data
		self._name = name

	@abstractmethod
	def generate_cv(self) -> str:
		pass