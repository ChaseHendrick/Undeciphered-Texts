"""Known-key keyed Vigenère, pinned to the published Kryptos K1 and K2 readings.

K1's expected plaintext is the letter-by-letter decrypt in the NSA FOIA paper
(DOCID 4051151), which Wikipedia's "Solution of passage 1" also prints with
spaces. The prose line in that memo that says ILLUSION is a respacing, not
the letter groups. That test fails if those groups are "corrected".

K2's expected plaintext is Wikipedia's "Solution of passage 2", which Sanborn
confirmed in 2006. The same NSA memo reads the panel as cut and ends
IDBYROWS. That ending is not the published K2 plaintext.

K4 is out of scope. Nothing here is a K4 claim.
"""

from __future__ import annotations

import unittest
import hashlib
import json
from pathlib import Path

from engine.alphabet import letters_only
from engine.ciphers import vigenere_decrypt, vigenere_encrypt
from engine.solvers import SOLVERS
from engine.solvers.keyed_vigenere import (
    cipher_alphabet,
    keyed_vigenere_decrypt,
    keyed_vigenere_encrypt,
    keyword_mixed_alphabet,
    solve_keyed_vigenere,
)

# Sculpture K1, first two lines, as printed by Wikipedia and the NSA cipher sheet.
PUBLISHED_K1_CIPHERTEXT = (
    "EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD"
)
# NSA letter groups: BETWE ENSUB TLESH ADING ANDTH ABSCE NCEOF LIGHT /
# LIEST HENUA NCEOF IQLUS ION. Wikipedia spaces the same letters.
PUBLISHED_K1_PLAINTEXT = (
    "BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION"
)
PUBLISHED_K1_SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION"
)
PUBLISHED_ALPHABET = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
# Cipher rows for PALIMPSEST under index letter K, from the same NSA tableau.
PUBLISHED_ROWS = {
    "P": "PTOSABCDEFGHIJLMNQUVWXZKRY",
    "A": "ABCDEFGHIJLMNQUVWXZKRYPTOS",
    "L": "LMNQUVWXZKRYPTOSABCDEFGHIJ",
    "I": "IJLMNQUVWXZKRYPTOSABCDEFGH",
    "M": "MNQUVWXZKRYPTOSABCDEFGHIJL",
    "S": "SABCDEFGHIJLMNQUVWXZKRYPTO",
    "E": "EFGHIJLMNQUVWXZKRYPTOSABCD",
    "T": "TOSABCDEFGHIJLMNQUVWXZKRYP",
}


class KeyedAlphabetTest(unittest.TestCase):
    def test_kryptos_alphabet_is_keyword_then_remaining_letters(self) -> None:
        mixed = keyword_mixed_alphabet("KRYPTOS")
        self.assertEqual(mixed, PUBLISHED_ALPHABET)
        self.assertEqual(len(mixed), 26)
        self.assertIn("C", mixed)
        self.assertEqual(keyword_mixed_alphabet("kryptos kryptos"), mixed)

    def test_published_tableau_rows(self) -> None:
        alphabet = keyword_mixed_alphabet("KRYPTOS")
        for key_letter, row in PUBLISHED_ROWS.items():
            self.assertEqual(cipher_alphabet(alphabet, key_letter, "K"), row)


class KryptosK1Test(unittest.TestCase):
    def test_recovers_published_k1_plaintext_exactly(self) -> None:
        result = solve_keyed_vigenere(
            PUBLISHED_K1_CIPHERTEXT,
            key="PALIMPSEST",
            alphabet_keyword="KRYPTOS",
            index_letter="K",
        )
        self.assertEqual(result.plaintext, PUBLISHED_K1_PLAINTEXT)
        self.assertEqual(letters_only(result.plaintext), letters_only(PUBLISHED_K1_SPACED))
        self.assertIn("IQLUSION", result.plaintext)
        self.assertNotIn("ILLUSION", result.plaintext)
        self.assertEqual(result.key, "PALIMPSEST")
        self.assertEqual(result.details["alphabet"], PUBLISHED_ALPHABET)
        self.assertEqual(result.details["index_letter"], "K")
        self.assertEqual(result.details["period"], 10)
        self.assertNotIn("k4 plaintext", result.details["scope"].lower())

    def test_encrypt_published_plaintext_reproduces_ciphertext(self) -> None:
        cipher = keyed_vigenere_encrypt(
            PUBLISHED_K1_PLAINTEXT,
            key="PALIMPSEST",
            alphabet_keyword="KRYPTOS",
            index_letter="K",
        )
        self.assertEqual(cipher, PUBLISHED_K1_CIPHERTEXT)
        again = keyed_vigenere_decrypt(
            cipher,
            key="palimpsest",
            alphabet_keyword="Kryptos",
            index_letter="k",
        )
        self.assertEqual(again, PUBLISHED_K1_PLAINTEXT)

    def test_not_registered_as_a_blind_solver(self) -> None:
        self.assertNotIn("keyed-vigenere", SOLVERS)


# Sculpture K2 (Wikipedia note, the twelve lines after K1) plus the one
# ciphertext S Sanborn said was left off the panel. That S is the ninth
# character from the end, between E and W of ...PLGEWJLLAETG. Wikipedia,
# "Solution of passage 2" (fetched 2026-10-02), and the 2006 Sanborn
# confirmation print the plaintext this insertion recovers. The 1992 NSA
# FOIA memo (DOCID 4051151) uses the same key ABSCISSA, the same KRYPTOS
# alphabet, and index letter K, but it reads the panel as cut, so its
# letter groups end IDBYROWS and its prose prints UNDERGROUND,
# TRANSMISSION, and SEVENTY-SEVEN MINUTES. Those are not this plaintext.
PUBLISHED_K2_PANEL = (
    "VFPJUDEEHZWETZYVGWHKKQETGFQJNCE"
    "GGWHKK?DQMCPFQZDQMMIAGPFXHQRLG"
    "TIMVMZJANQLVKQEDAGDVFRPJUNGEUNA"
    "QZGZLECGYUXUEENJTBJLBQCRTBJDFHRR"
    "YIZETKZEMVDUFKSJHKFWHKUWQLSZFTI"
    "HHDDDUVH?DWKBFUFPWNTDFIYCUQZERE"
    "EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDX"
    "FLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF"
    "FHQNTGPUAECNUVPDJMQCLQUMUNEDFQ"
    "ELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE"
    "DNQFMPNZGLFLPMRJQYALMGNUVPDXVKP"
    "DQUMEBEDMHDAFMJGZNUPLGEWJLLAETG"
)
PUBLISHED_K2_CIPHERTEXT = PUBLISHED_K2_PANEL.replace("PLGEWJLLAETG", "PLGESWJLLAETG", 1)
PUBLISHED_K2_PLAINTEXT = (
    "ITWASTOTALLYINVISIBLEHOWSTHATPOSSIBLE?THEYUSEDTHEEARTHSMAGNETICFIELDX"
    "THEINFORMATIONWASGATHEREDANDTRANSMITTEDUNDERGRUUNDTOANUNKNOWNLOCATIONX"
    "DOESLANGLEYKNOWABOUTTHIS?THEYSHOULDITSBURIEDOUTTHERESOMEWHEREX"
    "WHOKNOWSTHEEXACTLOCATION?ONLYWWTHISWASHISLASTMESSAGEX"
    "THIRTYEIGHTDEGREESFIFTYSEVENMINUTESSIXPOINTFIVESECONDSNORTH"
    "SEVENTYSEVENDEGREESEIGHTMINUTESFORTYFOURSECONDSWESTXLAYERTWO"
)
PUBLISHED_K2_SPACED = (
    "IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE ? THEY USED THE EARTHS "
    "MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND TRANSMITTED "
    "UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS ? "
    "THEY SHOULD ITS BURIED OUT THERE SOMEWHERE X WHO KNOWS THE EXACT "
    "LOCATION ? ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES "
    "FIFTY SEVEN MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES "
    "EIGHT MINUTES FORTY FOUR SECONDS WEST X LAYER TWO"
)


class KryptosK2Test(unittest.TestCase):
    def test_recovers_published_k2_plaintext_exactly(self) -> None:
        result = solve_keyed_vigenere(
            PUBLISHED_K2_CIPHERTEXT,
            key="ABSCISSA",
            alphabet_keyword="KRYPTOS",
            index_letter="K",
        )
        self.assertEqual(result.plaintext, PUBLISHED_K2_PLAINTEXT)
        self.assertEqual(letters_only(result.plaintext), letters_only(PUBLISHED_K2_SPACED))
        self.assertIn("UNDERGRUUND", result.plaintext)
        self.assertNotIn("UNDERGROUND", result.plaintext)
        self.assertTrue(result.plaintext.endswith("WESTXLAYERTWO"))
        self.assertNotIn("IDBYROWS", result.plaintext)
        self.assertEqual(result.plaintext.count("?"), 3)
        self.assertEqual(result.key, "ABSCISSA")
        self.assertEqual(result.details["alphabet"], PUBLISHED_ALPHABET)
        self.assertEqual(result.details["index_letter"], "K")
        self.assertEqual(result.details["period"], 8)
        self.assertNotIn("k4 plaintext", result.details["scope"].lower())
        panel = solve_keyed_vigenere(
            PUBLISHED_K2_PANEL,
            key="ABSCISSA",
            alphabet_keyword="KRYPTOS",
            index_letter="K",
        )
        self.assertNotEqual(panel.plaintext, PUBLISHED_K2_PLAINTEXT)
        self.assertTrue(panel.plaintext.endswith("WESTIDBYROWS"))

    def test_encrypt_published_plaintext_reproduces_ciphertext(self) -> None:
        cipher = keyed_vigenere_encrypt(
            PUBLISHED_K2_PLAINTEXT,
            key="ABSCISSA",
            alphabet_keyword="KRYPTOS",
            index_letter="K",
        )
        self.assertEqual(cipher, PUBLISHED_K2_CIPHERTEXT)
        again = keyed_vigenere_decrypt(
            cipher,
            key="abscissa",
            alphabet_keyword="Kryptos",
            index_letter="k",
        )
        self.assertEqual(again, PUBLISHED_K2_PLAINTEXT)


class KeyedVigenereGeneralTest(unittest.TestCase):
    def test_plain_alphabet_matches_standard_vigenere(self) -> None:
        plain = "The harbor bell rang at dusk."
        key = "SECRET"
        cipher = vigenere_encrypt(plain, key)
        self.assertEqual(
            keyed_vigenere_decrypt(cipher, key, alphabet_keyword="", index_letter="A"),
            vigenere_decrypt(cipher, key),
        )
        self.assertEqual(keyword_mixed_alphabet(""), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_punctuation_does_not_advance_the_key(self) -> None:
        plain = "AB, CD."
        cipher = keyed_vigenere_encrypt(plain, "K", "KRYPTOS", "K")
        self.assertEqual(cipher[2], ",")
        self.assertEqual(cipher[-1], ".")
        self.assertEqual(keyed_vigenere_decrypt(cipher, "K", "KRYPTOS", "K"), plain)



K1_CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "kryptos_k1_certificate.json"
K2_CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "kryptos_k2_certificate.json"


class KryptosCertificateTest(unittest.TestCase):
    """Certificates check published K1/K2 plaintexts, not K4 or an unknown script."""

    def test_k1_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        cert = json.loads(K1_CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["cipher_name"], "keyed-vigenere")
        self.assertEqual(cert["passage"], "K1")
        plaintext = cert["plaintext"]
        ciphertext = cert["ciphertext"]
        keys = cert["keys"]
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["plaintext_sha256"])
        result = solve_keyed_vigenere(
            ciphertext,
            key=keys["key"],
            alphabet_keyword=keys["alphabet_keyword"],
            index_letter=keys["index_letter"],
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertIn("not an unknown script", cert["note"].lower())

    def test_k2_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        cert = json.loads(K2_CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["cipher_name"], "keyed-vigenere")
        self.assertEqual(cert["passage"], "K2")
        plaintext = cert["plaintext"]
        ciphertext = cert["ciphertext"]
        keys = cert["keys"]
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["plaintext_sha256"])
        result = solve_keyed_vigenere(
            ciphertext,
            key=keys["key"],
            alphabet_keyword=keys["alphabet_keyword"],
            index_letter=keys["index_letter"],
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
