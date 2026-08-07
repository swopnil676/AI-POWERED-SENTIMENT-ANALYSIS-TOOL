from repository import JSONHistoryRepository
from service import SentimentService
from cli import SentimentAnalysisCLI


def main():
    repository = JSONHistoryRepository("sentiment_history.json")
    service = SentimentService(repository)
    app = SentimentAnalysisCLI(service)
    app.run()


if __name__ == "__main__":
    main()