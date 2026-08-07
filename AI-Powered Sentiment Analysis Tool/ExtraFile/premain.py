import os
import json
import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List

import nltk

for pkg, path in [("vader_lexicon", "sentiment/vader_lexicon.zip")]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(pkg, quiet=True)

from nltk.sentiment import SentimentIntensityAnalyzer


class Sentiment(Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


@dataclass
class AnalysisResult:
    id: int
    text: str
    sentiment: Sentiment
    positive_score: float
    negative_score: float
    neutral_score: float
    compound_score: float
    analyzed_at: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    def to_dict(self) -> dict:
        data = asdict(self)
        data["sentiment"] = self.sentiment.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisResult":
        return cls(
            id=data["id"],
            text=data["text"],
            sentiment=Sentiment(data["sentiment"]),
            positive_score=data["positive_score"],
            negative_score=data["negative_score"],
            neutral_score=data["neutral_score"],
            compound_score=data["compound_score"],
            analyzed_at=data["analyzed_at"],
        )

    def __str__(self):
        preview = self.text if len(self.text) <= 60 else self.text[:57] + "..."
        return (
            f"ID: {self.id:<4} | {self.sentiment.value:<9} | "
            f"compound: {self.compound_score:>6.3f} | \"{preview}\""
        )


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


class SentimentService:
    """Wraps the VADER analyzer and manages analysis history."""

    def __init__(self, repository: HistoryRepository):
        self.repository = repository
        self.analyzer = SentimentIntensityAnalyzer()
        self.history: List[AnalysisResult] = self.repository.load_all()

    def _next_id(self) -> int:
        if not self.history:
            return 1
        return max(r.id for r in self.history) + 1

    @staticmethod
    def _classify(compound: float) -> Sentiment:
        if compound >= 0.05:
            return Sentiment.POSITIVE
        elif compound <= -0.05:
            return Sentiment.NEGATIVE
        return Sentiment.NEUTRAL

    def analyze(self, text: str, save: bool = True) -> AnalysisResult:
        scores = self.analyzer.polarity_scores(text)
        result = AnalysisResult(
            id=self._next_id(),
            text=text,
            sentiment=self._classify(scores["compound"]),
            positive_score=scores["pos"],
            negative_score=scores["neg"],
            neutral_score=scores["neu"],
            compound_score=scores["compound"],
        )
        if save:
            self.history.append(result)
            self.repository.save_all(self.history)
        return result

    def analyze_batch(self, texts: List[str]) -> List[AnalysisResult]:
        results = []
        for text in texts:
            text = text.strip()
            if text:
                results.append(self.analyze(text))
        return results

    def get_history(self) -> List[AnalysisResult]:
        return self.history

    def statistics(self) -> dict:
        total = len(self.history)
        by_sentiment = {
            sentiment: len([r for r in self.history if r.sentiment == sentiment])
            for sentiment in Sentiment
        }
        avg_compound = round(sum(r.compound_score for r in self.history) / total, 3) if total else 0
        return {"total": total, "by_sentiment": by_sentiment, "avg_compound": avg_compound}

    def clear_history(self):
        self.history = []
        self.repository.save_all(self.history)


class SentimentAnalysisCLI:
    def __init__(self, service: SentimentService):
        self.service = service

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    def run(self):
        self.clear_screen()
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()
            handler = self.get_handler(choice)

            if handler is None:
                print("Invalid choice, try again.")
            elif handler == "exit":
                print("Goodbye")
                break
            else:
                handler()

            input("\nPress enter to continue...")
            self.clear_screen()

    def get_handler(self, choice: str):
        handlers = {
            "1": self.analyze_single,
            "2": self.analyze_from_file,
            "3": self.view_history,
            "4": self.show_statistics,
            "5": self.clear_history,
            "6": lambda: self.clear_screen(),
            "7": "exit",
        }
        return handlers.get(choice)

    def show_menu(self):
        print("=" * 60)
        print("SENTIMENT ANALYSIS TOOL (VADER, offline, no API)")
        print("=" * 60)
        print("1. Analyze a single sentence")
        print("2. Analyze sentences from a text file")
        print("3. View analysis history")
        print("4. View statistics")
        print("5. Clear history")
        print("6. Clear screen")
        print("7. Exit")
        print("=" * 60)

    def analyze_single(self):
        print("\n--- Analyze Text ---")
        text = input("Enter a sentence or short paragraph: ").strip()
        if not text:
            print("Text cannot be empty.")
            return

        result = self.service.analyze(text)
        self.print_result(result)

    def analyze_from_file(self):
        print("\n--- Analyze From File ---")
        print("The file should have one sentence per line.")
        path = input("Enter file path: ").strip()

        if not os.path.exists(path):
            print("File not found.")
            return

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        results = self.service.analyze_batch(lines)
        print(f"\nAnalyzed {len(results)} line(s):")
        for r in results:
            print(r)

    def print_result(self, result):
        print(f"\nSentiment: {result.sentiment.value}")
        print(f"Compound score: {result.compound_score}")
        print(f"Positive: {result.positive_score}  Negative: {result.negative_score}  Neutral: {result.neutral_score}")

    def view_history(self):
        print("\n--- Analysis History ---")
        history = self.service.get_history()
        if not history:
            print("No analysis history yet.")
            return
        for r in history:
            print(r)

    def show_statistics(self):
        print("\n--- Statistics ---")
        stats = self.service.statistics()
        print(f"Total analyzed: {stats['total']}")
        if stats["total"] == 0:
            return
        for sentiment, count in stats["by_sentiment"].items():
            percent = round((count / stats["total"]) * 100, 1)
            print(f"{sentiment.value}: {count} ({percent}%)")
        print(f"Average compound score: {stats['avg_compound']}")

    def clear_history(self):
        confirm = input("Are you sure you want to clear all history? (y/n): ").strip().lower()
        if confirm == "y":
            self.service.clear_history()
            print("History cleared.")
        else:
            print("Cancelled.")


def main():
    repository = JSONHistoryRepository("sentiment_history.json")
    service = SentimentService(repository)
    app = SentimentAnalysisCLI(service)
    app.run()


if __name__ == "__main__":
    main()