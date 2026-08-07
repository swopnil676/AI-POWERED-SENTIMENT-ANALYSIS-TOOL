import os
import json
from abc import ABC, abstractmethod
from typing import List

from models import AnalysisResult


class HistoryRepository(ABC):
    @abstractmethod
    def load_all(self) -> List[AnalysisResult]:
        raise NotImplementedError

    @abstractmethod
    def save_all(self, results: List[AnalysisResult]) -> None:
        raise NotImplementedError


class JSONHistoryRepository(HistoryRepository):
    def __init__(self, file_path: str = "sentiment_history.json"):
        self.file_path = file_path

    def load_all(self) -> List[AnalysisResult]:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [AnalysisResult.from_dict(item) for item in raw]

    def save_all(self, results: List[AnalysisResult]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in results], f, indent=2)