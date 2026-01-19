"""
Data format definitions and constants for vocabulary seed scripts.

This module defines the standard format for vocabulary words and quality tiers.
"""

from typing import TypedDict, Optional, Literal


# TypedDict matching the Vocabulary database model
class VocabularyWord(TypedDict, total=False):
    """Standard format for vocabulary words matching database schema."""

    # Required fields
    word: str  # German word with article for nouns (e.g., "die Überweisung")
    translation_it: str  # Italian translation
    part_of_speech: str  # noun, verb, adjective, adverb, etc.
    difficulty: str  # CEFR level: A1, A2, B1, B2, C1, C2
    category: str  # finance, business, daily, technology, etc.
    example_de: str  # German example sentence
    example_it: str  # Italian example sentence translation

    # Optional enrichment fields
    pronunciation: Optional[str]  # IPA or simplified phonetic
    definition_de: Optional[str]  # German definition (1-2 sentences)
    synonyms: Optional[str]  # JSON array as string: '["word1", "word2"]'
    antonyms: Optional[str]  # JSON array as string: '["word1", "word2"]'
    usage_notes: Optional[str]  # Context, register, collocations

    # Noun-specific fields
    gender: Optional[str]  # masculine, feminine, neuter (for nouns)
    plural_form: Optional[str]  # Plural form (for nouns)

    # Linguistic flags (stored as 0/1 integers in database)
    is_idiom: Optional[int]  # 1 if idiomatic expression, 0 otherwise
    is_compound: Optional[int]  # 1 if compound word, 0 otherwise
    is_separable_verb: Optional[int]  # 1 if separable verb, 0 otherwise


# Quality tiers
QUALITY_TIERS = {
    "premium": {
        "description": "Business, C1-C2, Modal Particles - All 14 fields populated",
        "required_fields": [
            "word", "translation_it", "part_of_speech", "difficulty", "category",
            "example_de", "example_it", "pronunciation", "definition_de",
            "usage_notes", "synonyms"
        ],
        "completion_threshold": 11  # 11+ out of 14 fields
    },
    "standard": {
        "description": "B1-B2, Thematic - Core fields + pronunciation + usage notes",
        "required_fields": [
            "word", "translation_it", "part_of_speech", "difficulty", "category",
            "example_de", "example_it", "pronunciation"
        ],
        "completion_threshold": 8  # 8+ out of 14 fields
    },
    "basic": {
        "description": "A1-A2 - Required fields only",
        "required_fields": [
            "word", "translation_it", "part_of_speech", "difficulty", "category",
            "example_de", "example_it"
        ],
        "completion_threshold": 7  # 7 required fields
    }
}


# CEFR levels
CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


# Valid categories
VALID_CATEGORIES = [
    # Business & Finance
    "finance",
    "business",
    "legal",
    "technology",

    # Daily life
    "daily",
    "food",
    "travel",
    "health",
    "sports",
    "home",
    "education",
    "environment",
    "culture",
    "politics",

    # Linguistic
    "grammar",
    "idiom",
    "expression"
]


# Part of speech options
VALID_POS = [
    "noun",
    "verb",
    "adjective",
    "adverb",
    "preposition",
    "conjunction",
    "article",
    "pronoun",
    "particle",  # Modal particles: doch, halt, eben, mal, etc.
    "interjection",
    "idiom"
]


# Valid genders for nouns
VALID_GENDERS = ["masculine", "feminine", "neuter"]


# German articles for gender validation
ARTICLES = {
    "masculine": ["der"],
    "feminine": ["die"],
    "neuter": ["das"]
}


def get_quality_tier(word: VocabularyWord) -> str:
    """
    Determine the quality tier of a vocabulary word based on field completion.

    Args:
        word: Vocabulary word dictionary

    Returns:
        Quality tier: "premium", "standard", or "basic"
    """
    # Count populated optional fields
    optional_fields = [
        "pronunciation", "definition_de", "synonyms", "antonyms", "usage_notes",
        "gender", "plural_form"
    ]

    populated_count = sum(1 for field in optional_fields if word.get(field))
    total_fields = 7 + populated_count  # 7 required + optional

    if total_fields >= 11:
        return "premium"
    elif total_fields >= 8:
        return "standard"
    else:
        return "basic"


def validate_article_gender_match(word: str, gender: Optional[str]) -> bool:
    """
    Validate that the article in the word matches the specified gender.

    Args:
        word: German word with article (e.g., "die Überweisung")
        gender: Specified gender (masculine, feminine, neuter)

    Returns:
        True if article matches gender, False otherwise
    """
    if not gender or gender not in VALID_GENDERS:
        return False

    word_lower = word.lower().strip()

    # Check if word starts with the correct article
    for article in ARTICLES[gender]:
        if word_lower.startswith(article + " "):
            return True

    return False
