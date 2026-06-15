"""
Shared utilities for smart romanization.
Extracted from nepali-romanization project.
"""
import re

# Predefined word mappings from romanize.py
LOAN_WORDS = {
    'रेडियो': 'radio',
    'कोट': 'coat',
    'डाक्टर': 'doctor',
    'स्कुल': 'school',
    'क्यान्सर': 'cancer',
    'ब्याग': 'bag',
    'टिकट': 'ticket',
    'सिनेमा': 'cinema',
    'फोटो': 'photo',
    'टेलिफोन': 'telephone',
    'फोन': 'phone',
    'क्यामेरा': 'camera',
    'कम्प्युटर': 'computer',
    'मोटर': 'motor',
    'मोबाइल': 'mobile',
    'क्यालेन्डर': 'calendar',
    'क्याम्पस': 'campus',
    'स्टुडियो': 'studio',
    'कलेज': 'college',
    'पुलिस': 'police',
    'इन्जिनियर': 'engineer',
    'टुरिस्ट': 'tourist',
    'कफी': 'coffee',
    'कर्फ्यु': 'curfew'
}

HARD_CODED = {
    'काठमाडौं': 'Kathmandu',
    'गीत': 'geet',
    'तर': 'tara',
    'मञ्च': 'manch',
    'तँ': 'ta',
    'संयोजक': 'samyojak',
    'प्रशंसा': 'prasamsha',
    'संलग्न': 'samlagna',
    'वर्ष': 'barsha',
    'नम्बर': 'number',
    'न.': 'No.',
    'नाम': 'naam',
    'छैन': 'chhaina',
    'दिन': 'din',
    'तल': 'tala',
    'बाट': 'bata'
}

PREDEFINED = LOAN_WORDS.copy()
PREDEFINED.update(HARD_CODED)

KARS = ['ा', 'ि', 'ी', 'ु', 'ू', 'े', 'ै', 'ो', 'ौ', 'ं', 'ँ', '्', 'ृ', 'ः']
CONSONANTS = ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण',
              'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व',
              'श', 'ष', 'स', 'ह', 'क्ष', 'त्र', 'ज्ञ']
VOWELS = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ']
BINDUS = ['ँ', 'ं', 'ः']


def simplify_vowels(text: str) -> str:
    """
    Simplify vowel representation: ee→i, oo→u
    Makes output closer to how people naturally type.
    """
    return text.replace('ee', 'i').replace('oo', 'u')


def should_drop_trailing_a(nepali_word: str, char_idx: int, current_roman: str) -> bool:
    """
    Decide if trailing 'a' should be dropped from consonant.
    Based on romanize.py's pronouce_inherent logic (inverted).

    Returns True if 'a' should be dropped (i.e., inherent vowel NOT pronounced).
    """
    if char_idx == 0:
        return False  # Don't drop from first char if it's standalone

    nepali_char = nepali_word[char_idx]
    prev_char = nepali_word[char_idx - 1]

    # Keep 'a' if: छ, य, ह (these always pronounce inherent)
    if nepali_char in ['छ', 'य', 'ह']:
        return False

    # Keep 'a' if followed by dead consonant or bindus
    if prev_char == '्' or prev_char in BINDUS:
        return False

    # Keep 'a' for garera, parera pattern (े + र)
    if prev_char == 'े' and nepali_char == 'र' and len(nepali_word) > 3:
        return False

    # Keep 'a' for न (bhanana, ganana pattern)
    if nepali_char == 'न':
        return False

    # Keep 'a' if consonant after vowel
    if prev_char in VOWELS:
        return False

    # Drop 'a' in all other cases (most common: word-final consonants)
    return True


def apply_smart_rules(nepali_text: str, roman_text: str) -> str:
    """
    Apply smart romanization rules:
    1. Check predefined dictionary
    2. Simplify vowels (ee→i, oo→u)
    3. Drop trailing 'a' from word-final consonants contextually
    4. Handle bindus at word end (drop the 'n' sound)

    Args:
        nepali_text: Original Nepali text
        roman_text: Roman text from character-by-character conversion

    Returns:
        Smart-processed roman text
    """
    # Check predefined words first
    if nepali_text in PREDEFINED:
        return PREDEFINED[nepali_text]

    # Simplify vowels
    result = simplify_vowels(roman_text)

    # Drop trailing 'a' from consonants at word end
    # This handles cases like: दिन → din (not dina), फल → phal (not phala)
    if len(nepali_text) > 1:
        last_char = nepali_text[-1]

        # If last char is a consonant, check if we should drop trailing 'a'
        if last_char in CONSONANTS:
            if should_drop_trailing_a(nepali_text, len(nepali_text) - 1, result):
                if result.endswith('a'):
                    result = result[:-1]

        # Handle ङ at end → 'ng' (special case)
        if last_char == 'ङ' and result.endswith('na'):
            result = result[:-2] + 'ng'

    # Handle bindus at end: गरें → gare (not gareM)
    if len(nepali_text) > 0 and nepali_text[-1] in BINDUS:
        # Remove the trailing 'n' or 'M' or 'NN'
        if result.endswith('M'):
            result = result[:-1]
        elif result.endswith('NN'):
            result = result[:-2]
        elif result.endswith('an'):
            result = result[:-2]

    return result


def convert_word_only(converter_instance, text: str) -> str:
    """
    Convert a single Nepali word to Roman without word splitting.
    Used internally by smart mode.

    Args:
        converter_instance: ReverseConverter or ReverseConverterV2 instance
        text: Single Nepali word

    Returns:
        Roman conversion of the word
    """
    from nepali_unicode_converter.mappings import halanta

    result = []
    i = 0

    while i < len(text):
        matched = False

        # Try word mappings first
        for nepali_word, roman_word in converter_instance.reverse_word_maps.items():
            if text[i:].startswith(nepali_word):
                result.append(roman_word)
                i += len(nepali_word)
                matched = True
                break

        if matched:
            continue

        # Try character mappings
        for nepali_char, roman_char in converter_instance.reverse_mappings.items():
            if text[i:].startswith(nepali_char):
                if i + len(nepali_char) < len(text) and text[i + len(nepali_char)] == halanta:
                    if roman_char.endswith('a'):
                        result.append(roman_char[:-1])
                    else:
                        result.append(roman_char)
                    i += len(nepali_char) + 1
                else:
                    result.append(roman_char)
                    i += len(nepali_char)
                matched = True
                break

        if not matched:
            result.append(text[i])
            i += 1

    return ''.join(result)


def convert_with_smart(converter_instance, text: str) -> str:
    """
    Generic smart conversion that works with any converter instance.
    Splits text into words, applies regular conversion, then smart rules.

    Args:
        converter_instance: Instance with reverse_mappings and reverse_word_maps
        text: Nepali Unicode text

    Returns:
        Smart-processed roman text
    """
    if not text:
        return text

    # Split into words (preserve spaces and punctuation)
    pattern = r'[^\s,!\?\[\]\(\)।]+'

    def convert_word(match):
        nepali_word = match.group()
        # Regular conversion first
        roman_word = convert_word_only(converter_instance, nepali_word)
        # Apply smart rules
        return apply_smart_rules(nepali_word, roman_word)

    return re.sub(pattern, convert_word, text)
