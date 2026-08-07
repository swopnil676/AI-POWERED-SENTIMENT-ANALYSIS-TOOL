import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum


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