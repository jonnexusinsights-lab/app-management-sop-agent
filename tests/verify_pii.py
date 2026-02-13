import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.security.sanitization import PIISanitizer

def test_pii_sanitization():
    sanitizer = PIISanitizer()

    test_cases = [
        (
            "My name is John Doe and my email is john.doe@example.com.",
            ["<PERSON>", "<EMAIL_ADDRESS>"]
        ),
        (
            "Call me at 555-123-4567 regarding the incident.",
            ["<PHONE_NUMBER>"]
        ),
        (
            "The keys are in the safe.",
            [] # No PII
        )
    ]

    failed = False
    print("Running PII Sanitization Tests...")

    for text, expected_entities in test_cases:
        sanitized = sanitizer.sanitize(text)
        print(f"\nOriginal: {text}")
        print(f"Sanitized: {sanitized}")

        # Basic check: masked entities should appear
        for entity in expected_entities:
            if entity not in sanitized:
                print(f"FAILED: Expected entity marker {entity} not found.")
                failed = True

        # Basic check: original PII should NOT appear (naive check for this test)
        if "John Doe" in sanitized or "john.doe@example.com" in sanitized or "555-123-4567" in sanitized:
             print("FAILED: PII leaked in sanitized text.")
             failed = True

    if failed:
        print("\n❌ Tests FAILED")
        sys.exit(1)
    else:
        print("\n✅ Tests PASSED")

if __name__ == "__main__":
    test_pii_sanitization()
