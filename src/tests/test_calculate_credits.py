import pytest
from utils import calculate_credits

def test_calculate_credits_basic():
    message = "Test message with more words"
    result = calculate_credits(message)
    assert result > 1.0, f"Base credits should include base cost + char/word costs. Got {result}"

def test_calculate_credits_palindrome():
    palindrome = "A man a plan a canal Panama"
    expected_result = 7.3

    palindrome_result = calculate_credits(palindrome)

    assert palindrome_result > 1.0, "Credits should be greater than 1.0"
    assert palindrome_result == expected_result, f"Palindrome should match expected result. Got {palindrome_result}"

def test_calculate_credits_unique_words():
    message = "Every word here is unique"
    result = calculate_credits(message)
    assert result > 0, "Credit calculation should consider unique word bonuses."
