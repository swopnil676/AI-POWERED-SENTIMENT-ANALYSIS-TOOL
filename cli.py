import os

from service import SentimentService


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