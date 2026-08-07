from typing import List

import nltk

for pkg, path in [("vader_lexicon", "sentiment/vader_lexicon.zip")]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(pkg, quiet=True)

from nltk.sentiment import SentimentIntensityAnalyzer

from models import Sentiment, AnalysisResult
from repository import HistoryRepository


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