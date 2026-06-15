from typing import Dict
from nepali_unicode_converter.mappings import (
    get_mappings,
    consonant_kaars,
    get_word_maps,
    Mappings,
    amkaar,
    aNNkaar,
    Ri,
    halanta,
    numbers,
    basic_vowels,
    akaars,
)
from nepali_unicode_converter.smart_utils import convert_with_smart


class ReverseConverterV2:
    """
    Converts Nepali Unicode text to Roman (English letters).

    V2: Prefers linguistically accurate romanization over shortest forms.
    - Uses 'pha' instead of 'fa' for फ
    - Uses 'bha' instead of 'va' for भ
    - Uses 'Ree' instead of 'Ri' for ॠ when appropriate

    Args:
        smart: If True, applies smart romanization rules:
               - Simplifies vowels (ee→i, oo→u)
               - Drops trailing 'a' contextually (din vs dina)
               - Uses predefined word dictionary
               Default: False (strict character mapping)

    Note: This is still a best-effort conversion. Some Nepali characters can be
    represented by multiple roman equivalents.
    """

    def __init__(self, smart: bool = False):
        self.smart = smart
        self.reverse_mappings = self._build_reverse_mappings()
        word_maps = get_word_maps()
        self.reverse_word_maps = dict(
            sorted({v: k for k, v in word_maps.items()}.items(),
                   key=lambda x: len(x[0]),
                   reverse=True)
        )

    def _build_reverse_mappings(self) -> Dict[str, str]:
        """Build reverse mappings from Nepali to Roman with linguistic preferences."""
        forward_maps = get_mappings()
        reverse = {}

        # Base consonant preferences - prefer these over shorter alternatives
        base_preferences = {
            'फ': 'pha',   # prefer pha over fa
            'भ': 'bha',   # prefer bha over va
            'ॠ': 'Ree',   # prefer Ree over Ri
        }

        # Invert the mappings
        for roman, nepali in forward_maps.items():
            if nepali not in reverse:
                reverse[nepali] = roman
            else:
                # Prefer shorter if no specific preference
                if len(roman) < len(reverse[nepali]):
                    reverse[nepali] = roman

        # Apply base preferences to consonant and all its forms
        # This catches फ, फ्, फा, फि, etc. and their roman equivalents
        for nepali_base, preferred_roman_base in base_preferences.items():
            for nepali, roman in list(reverse.items()):
                if nepali.startswith(nepali_base):
                    # Find what forward mapping created this
                    for fwd_roman, fwd_nepali in forward_maps.items():
                        if fwd_nepali == nepali and fwd_roman.startswith(preferred_roman_base.rstrip('a')):
                            reverse[nepali] = fwd_roman
                            break

        # Add special characters
        reverse[amkaar] = 'M'
        reverse[aNNkaar] = 'NN'
        reverse[Ri] = 'Ri'  # This is the kaar form (ृ), different from ॠ

        # Sort by length (longest first) for greedy matching
        return dict(sorted(reverse.items(), key=lambda x: len(x[0]), reverse=True))

    def convert(self, text: str) -> str:
        """
        Convert Nepali Unicode text to Roman.

        Args:
            text: Nepali Unicode text

        Returns:
            Roman (English letter) representation with linguistic preferences
        """
        if not text:
            return text

        if self.smart:
            return convert_with_smart(self, text)

        result = []
        i = 0

        while i < len(text):
            matched = False

            # Try word mappings first (longest match)
            for nepali_word, roman_word in self.reverse_word_maps.items():
                if text[i:].startswith(nepali_word):
                    result.append(roman_word)
                    i += len(nepali_word)
                    matched = True
                    break

            if matched:
                continue

            # Try character mappings (longest match)
            for nepali_char, roman_char in self.reverse_mappings.items():
                if text[i:].startswith(nepali_char):
                    # Check if next char is halanta - if so, remove 'a' suffix
                    if i + len(nepali_char) < len(text) and text[i + len(nepali_char)] == halanta:
                        # Remove trailing 'a' from roman_char if present
                        if roman_char.endswith('a'):
                            result.append(roman_char[:-1])
                        else:
                            result.append(roman_char)
                        i += len(nepali_char) + 1  # skip halanta
                    else:
                        result.append(roman_char)
                        i += len(nepali_char)
                    matched = True
                    break

            if not matched:
                # Keep character as-is if no mapping found
                result.append(text[i])
                i += 1

        return ''.join(result)
        i = 0

        while i < len(text):
            matched = False

            # Try word mappings first
            for nepali_word, roman_word in self.reverse_word_maps.items():
                if text[i:].startswith(nepali_word):
                    result.append(roman_word)
                    i += len(nepali_word)
                    matched = True
                    break

            if matched:
                continue

            # Try character mappings
            for nepali_char, roman_char in self.reverse_mappings.items():
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
