def calculate_credits(text: str) -> float:
    base_cost = 1.0
    char_count = len(text)
    word_cost = sum(0.1 if len(word) <= 3 else 0.2 if len(word) <= 7 else 0.3 for word in text.split())
    third_vowels = sum(1 for i, char in enumerate(text) if (i + 1) % 3 == 0 and char in "aeiouAEIOU")

    total_credits = base_cost + (char_count * 0.05) + word_cost + (third_vowels * 0.3)

    if char_count > 100:
        total_credits += 5
    if len(set(text.split())) == len(text.split()):
        total_credits -= 2
    if ''.join(filter(str.isalnum, text)).lower() == ''.join(filter(str.isalnum, text)).lower()[::-1]:
        total_credits *= 2

    return max(total_credits, 1.0)
