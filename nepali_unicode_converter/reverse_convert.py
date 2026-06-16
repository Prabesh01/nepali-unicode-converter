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


class ReverseConverter:
    """
    Converts Nepali Unicode text to Roman (English letters).

    Args:
        smart: If True, applies smart romanization rules:
               - Simplifies vowels (ee→i, oo→u)
               - Drops trailing 'a' contextually (din vs dina)
               - Uses predefined word dictionary
               Default: False (strict character mapping)
        custom_mappings: Dict of additional roman->nepali mappings (e.g. {'ba': 'व'})

    Note: This is a best-effort conversion. Some Nepali characters can be
    represented by multiple roman equivalents, so the output may not exactly
    match the original roman input that was used to generate the Nepali text.
    """

    def __init__(self, smart: bool = False, custom_mappings: Mappings = None):
        self.smart = smart
        self.custom_mappings = self._expand_custom_mappings(custom_mappings) if custom_mappings else None
        self.reverse_mappings = self._build_reverse_mappings()
        word_maps = get_word_maps()
        self.reverse_word_maps = dict(
            sorted({v: k for k, v in word_maps.items()}.items(),
                   key=lambda x: len(x[0]),
                   reverse=True)
        )

    def _expand_custom_mappings(self, custom: Mappings) -> Mappings:
        """Expand custom consonants to include halanta and kaar forms."""
        expanded = dict(custom)

        for roman, nepali in custom.items():
            if roman.endswith('a') and len(roman) > 1:
                base = roman[:-1]
                # Add halanta
                expanded[base] = nepali + halanta
                # Add kaar variants
                for kaar_rom, kaar_sym in consonant_kaars.items():
                    expanded[base + kaar_rom] = nepali + kaar_sym

        return expanded

    def _build_reverse_mappings(self) -> Dict[str, str]:
        """Build reverse mappings from Nepali to Roman."""
        forward_maps = get_mappings()
        if self.custom_mappings:
            forward_maps.update(self.custom_mappings)
        reverse = {}

        # Invert the mappings, preferring shorter/simpler roman equivalents
        for roman, nepali in forward_maps.items():
            if nepali not in reverse:
                reverse[nepali] = roman
            else:
                # Prefer shorter roman representation
                if len(roman) < len(reverse[nepali]):
                    reverse[nepali] = roman

        # Add special characters
        reverse[amkaar] = 'M'
        reverse[aNNkaar] = 'NN'
        reverse[Ri] = 'Ri'

        # Sort by length (longest first) for greedy matching
        return dict(sorted(reverse.items(), key=lambda x: len(x[0]), reverse=True))

    def convert(self, text: str) -> str:
        """
        Convert Nepali Unicode text to Roman.

        Args:
            text: Nepali Unicode text

        Returns:
            Roman (English letter) representation
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
