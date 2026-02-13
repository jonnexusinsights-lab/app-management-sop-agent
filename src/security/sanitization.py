from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PIISanitizer:
    """Handles PII detection and masking using Microsoft Presidio."""

    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def sanitize(self, text: str) -> str:
        """
        Detects and masks PII in the given text.

        Args:
            text: The input text to sanitize.

        Returns:
            The text with PII entities masked.
        """
        results = self.analyzer.analyze(text=text, entities=[], language='en')
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        return anonymized_result.text
