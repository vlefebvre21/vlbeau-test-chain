def reverse(s):
    return s[::-1]

def capitalize_words(s):
    return ' '.join(word.capitalize() for word in s.split())

def count_vowels(s):
    return sum(1 for c in s.lower() if c in 'aeiouy')