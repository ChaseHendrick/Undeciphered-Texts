"""RFC 8439 ChaCha20 vectors and supplied-key byte recovery.

Source: https://www.rfc-editor.org/rfc/rfc8439.html
Independent published vectors are in sections 2.3.2 and 2.4.2.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.chacha20 import (
    chacha20_block,
    chacha20_decrypt,
    chacha20_encrypt,
    chacha20_xor,
    solve_chacha20,
)


_KEY = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
    "101112131415161718191a1b1c1d1e1f"
)
_BLOCK_NONCE = bytes.fromhex("000000090000004a00000000")
_CIPHER_NONCE = bytes.fromhex("000000000000004a00000000")
_BLOCK = bytes.fromhex(
    "10f1e7e4d13b5915500fdd1fa32071c4"
    "c7d1f4c733c068030422aa9ac3d46c4e"
    "d2826446079faa0914c2d705d98b02a2"
    "b5129cd1de164eb9cbd083e8a2503c4e"
)
_PLAIN = (
    b"Ladies and Gentlemen of the class of '99: If I could offer you only "
    b"one tip for the future, sunscreen would be it."
)
_CIPHER = bytes.fromhex(
    "6e2e359a2568f98041ba0728dd0d6981"
    "e97e7aec1d4360c20a27afccfd9fae0b"
    "f91b65c5524733ab8f593dabcd62b357"
    "1639d624e65152ab8f530c359f0861d8"
    "07ca0dbf500d6a6156a38e088a22b65e"
    "52bc514d16ccf806818ce91ab7793736"
    "5af90bbf74a35be6b40b8eedf2785e42"
    "874d"
)
_MAX_COUNTER = (1 << 32) - 1
_CERT_PATH = Path(__file__).resolve().parents[1] / "engine/data/chacha20_certificate.json"


class ChaCha20PublishedVectorTest(unittest.TestCase):
    def test_rfc_8439_section_2_3_2_block(self) -> None:
        self.assertEqual(chacha20_block(key=_KEY, nonce=_BLOCK_NONCE, counter=1), _BLOCK)

    def test_rfc_8439_section_2_4_2_encryption_and_decryption(self) -> None:
        self.assertEqual(len(_PLAIN), 114)
        self.assertEqual(
            chacha20_encrypt(_PLAIN, key=_KEY, nonce=_CIPHER_NONCE, counter=1), _CIPHER
        )
        self.assertEqual(
            chacha20_decrypt(_CIPHER, key=_KEY, nonce=_CIPHER_NONCE, counter=1), _PLAIN
        )

    def test_partial_and_exact_blocks_match_published_prefixes(self) -> None:
        for length in (0, 1, 15, 63, 64, 65, 113, 114):
            with self.subTest(length=length):
                self.assertEqual(
                    chacha20_xor(_PLAIN[:length], key=_KEY, nonce=_CIPHER_NONCE, counter=1),
                    _CIPHER[:length],
                )

    def test_long_binary_message_roundtrips_without_text_conversion(self) -> None:
        plain = bytes(range(256)) * 2 + b"\x00\xff"
        cipher = chacha20_encrypt(plain, key=b"\x80" * 32, nonce=b"\x7f" * 12, counter=7)
        self.assertEqual(len(cipher), len(plain))
        self.assertNotEqual(cipher, plain)
        self.assertEqual(
            chacha20_decrypt(cipher, key=b"\x80" * 32, nonce=b"\x7f" * 12, counter=7),
            plain,
        )

    def test_supplied_key_result_is_explicitly_hex_encoded(self) -> None:
        result = solve_chacha20(_CIPHER, key=_KEY, nonce=_CIPHER_NONCE, counter=1)
        self.assertEqual(result.method, "chacha20")
        self.assertEqual(result.plaintext, _PLAIN.hex())
        self.assertEqual(result.details["plaintext_encoding"], "hex")
        self.assertEqual(result.details["input_encoding"], "bytes")
        self.assertEqual(result.details["mode"], "known_key")
        self.assertEqual(result.details["authentication"], "none")
        self.assertEqual(result.details["bytes"], 114)
        self.assertEqual(result.details["counter"], 1)
        self.assertEqual(result.details["nonce_hex"], _CIPHER_NONCE.hex())
        self.assertEqual(result.details["plaintext_sha256"], hashlib.sha256(_PLAIN).hexdigest())


class ChaCha20ValidationTest(unittest.TestCase):
    def test_key_and_nonce_lengths(self) -> None:
        for key in (b"", b"A" * 31, b"A" * 33):
            with self.subTest(key_length=len(key)):
                with self.assertRaises(ValueError):
                    chacha20_block(key=key, nonce=_CIPHER_NONCE, counter=0)
        for nonce in (b"", b"A" * 8, b"A" * 11, b"A" * 13):
            with self.subTest(nonce_length=len(nonce)):
                with self.assertRaises(ValueError):
                    chacha20_block(key=_KEY, nonce=nonce, counter=0)

    def test_parameters_require_bytes_and_integer_counter(self) -> None:
        for invalid in (None, "a" * 32, bytearray(32), [0] * 32):
            with self.subTest(key_type=type(invalid).__name__):
                with self.assertRaises(TypeError):
                    chacha20_block(key=invalid, nonce=_CIPHER_NONCE, counter=0)
        with self.assertRaises(TypeError):
            chacha20_block(key=_KEY, nonce="0" * 12, counter=0)
        for data in (None, "plaintext", bytearray(b"message")):
            with self.subTest(data_type=type(data).__name__):
                with self.assertRaises(TypeError):
                    chacha20_xor(data, key=_KEY, nonce=_CIPHER_NONCE, counter=1)
        for counter in (None, True, False, 1.0, "1"):
            with self.subTest(counter=counter):
                with self.assertRaises(TypeError):
                    chacha20_block(key=_KEY, nonce=_CIPHER_NONCE, counter=counter)

    def test_counter_range_and_stream_overflow(self) -> None:
        for counter in (-1, 1 << 32):
            with self.subTest(counter=counter):
                with self.assertRaises(ValueError):
                    chacha20_block(key=_KEY, nonce=_CIPHER_NONCE, counter=counter)
        last = chacha20_block(key=_KEY, nonce=_CIPHER_NONCE, counter=_MAX_COUNTER)
        self.assertEqual(
            chacha20_xor(b"\x00" * 64, key=_KEY, nonce=_CIPHER_NONCE, counter=_MAX_COUNTER),
            last,
        )
        self.assertEqual(
            chacha20_xor(b"", key=_KEY, nonce=_CIPHER_NONCE, counter=_MAX_COUNTER), b""
        )
        for data, counter in ((b"\x00" * 65, _MAX_COUNTER), (b"\x00" * 129, _MAX_COUNTER - 1)):
            with self.subTest(length=len(data), counter=counter):
                with self.assertRaisesRegex(ValueError, "overflow"):
                    chacha20_xor(data, key=_KEY, nonce=_CIPHER_NONCE, counter=counter)


class ChaCha20CertificateTest(unittest.TestCase):
    def test_certificate_recovers_and_hashes_raw_plaintext_bytes(self) -> None:
        cert = json.loads(_CERT_PATH.read_text(encoding="utf-8"))
        keys = cert["keys"]
        recovered = chacha20_decrypt(
            bytes.fromhex(cert["ciphertext_hex"]),
            key=bytes.fromhex(keys["key_hex"]),
            nonce=bytes.fromhex(keys["nonce_hex"]),
            counter=keys["counter"],
        )
        self.assertEqual(cert["cipher_name"], "chacha20")
        self.assertEqual(cert["source_url"], "https://www.rfc-editor.org/rfc/rfc8439.html#section-2.4.2")
        self.assertEqual(recovered, _PLAIN)
        self.assertEqual(recovered.hex(), cert["plaintext_hex"])
        self.assertEqual(hashlib.sha256(recovered).hexdigest(), cert["plaintext_sha256"])
        self.assertEqual(cert["hash_encoding"], "raw_bytes")
        self.assertEqual(bytes.fromhex(cert["ciphertext_hex"]), _CIPHER)
        self.assertNotIn("plaintext", cert)
        self.assertNotIn("ciphertext", cert)
        self.assertNotIn("key", cert)
        block = cert["block_vector"]
        self.assertEqual(
            chacha20_block(
                key=bytes.fromhex(block["key_hex"]),
                nonce=bytes.fromhex(block["nonce_hex"]),
                counter=block["counter"],
            ).hex(),
            block["output_hex"],
        )
        self.assertEqual(bytes.fromhex(block["output_hex"]), _BLOCK)


if __name__ == "__main__":
    unittest.main()
