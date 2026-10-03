"""AES block known-answer checks from NIST FIPS 197 Appendix C.

Official printed vectors:
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf
These tests require the published key and do not crack an unknown AES key.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.aes import (
    FIPS197_URL,
    aes_decrypt_block,
    aes_encrypt_block,
    aes_expand_key,
    solve_aes,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "aes_certificate.json"
PLAINTEXT = bytes.fromhex("00112233445566778899aabbccddeeff")
# Independent literal ciphertexts from Appendix C, not generated at test time.
VECTORS = (
    (128, "000102030405060708090a0b0c0d0e0f", "69c4e0d86a7b0430d8cdb78070b4c55a"),
    (
        192,
        "000102030405060708090a0b0c0d0e0f1011121314151617",
        "dda97ca4864cdfe06eaf70a0ec0d7191",
    ),
    (
        256,
        "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
        "8ea2b7ca516745bfeafc49904b496089",
    ),
)


class AesPublishedVectorTest(unittest.TestCase):
    def test_encrypts_all_three_published_vectors(self) -> None:
        for bits, key_hex, ciphertext_hex in VECTORS:
            with self.subTest(bits=bits):
                self.assertEqual(
                    aes_encrypt_block(PLAINTEXT, bytes.fromhex(key_hex)),
                    bytes.fromhex(ciphertext_hex),
                )

    def test_decrypts_all_three_published_vectors(self) -> None:
        for bits, key_hex, ciphertext_hex in VECTORS:
            with self.subTest(bits=bits):
                self.assertEqual(
                    aes_decrypt_block(bytes.fromhex(ciphertext_hex), bytes.fromhex(key_hex)),
                    PLAINTEXT,
                )

    def test_key_schedule_matches_published_round_keys(self) -> None:
        # Appendix C prints these final round keys for each sequential-byte key.
        finals = {
            128: "13111d7fe3944a17f307a78b4d2b30c5",
            192: "a4970a331a78dc09c418c271e3a41d5d",
            256: "24fc79ccbf0979e9371ac23c6d68de36",
        }
        for bits, key_hex, _ciphertext_hex in VECTORS:
            with self.subTest(bits=bits):
                keys = aes_expand_key(bytes.fromhex(key_hex))
                self.assertEqual(len(keys), {128: 11, 192: 13, 256: 15}[bits])
                self.assertEqual(keys[0].hex(), "000102030405060708090a0b0c0d0e0f")
                self.assertEqual(keys[-1].hex(), finals[bits])
                self.assertTrue(all(len(key) == 16 for key in keys))

    def test_solver_returns_hex_with_explicit_binary_metadata(self) -> None:
        for bits, key_hex, ciphertext_hex in VECTORS:
            with self.subTest(bits=bits):
                result = solve_aes(bytes.fromhex(ciphertext_hex), key=bytes.fromhex(key_hex))
                self.assertEqual(result.method, "aes")
                self.assertEqual(result.plaintext, PLAINTEXT.hex())
                self.assertEqual(result.key, key_hex)
                self.assertEqual(result.details["mode"], "known_key")
                self.assertEqual(result.details["encoding"], "hex")
                self.assertEqual(result.details["key_bits"], bits)
                self.assertEqual(result.details["block_bytes"], 16)
                self.assertEqual(result.details["source_url"], FIPS197_URL)
                self.assertEqual(
                    result.details["plaintext_sha256"], hashlib.sha256(PLAINTEXT).hexdigest()
                )
                self.assertEqual(result.details["hash_encoding"], "raw_bytes")

    def test_roundtrips_arbitrary_binary_without_padding(self) -> None:
        blocks = (bytes(16), bytes([255] * 16), b"\x00\xff\x80\x01" * 4, bytes(range(16)))
        for key_length in (16, 24, 32):
            key = bytes((i * 37 + 11) % 256 for i in range(key_length))
            for block in blocks:
                with self.subTest(key_length=key_length, block=block.hex()):
                    ciphertext = aes_encrypt_block(block, key)
                    self.assertEqual(len(ciphertext), 16)
                    self.assertEqual(aes_decrypt_block(ciphertext, key), block)


class AesInvalidInputTest(unittest.TestCase):
    def test_rejects_block_lengths_other_than_sixteen(self) -> None:
        for transform in (aes_encrypt_block, aes_decrypt_block):
            for length in (0, 1, 15, 17, 32):
                with self.subTest(transform=transform.__name__, length=length):
                    with self.assertRaises(ValueError):
                        transform(bytes(length), bytes(16))
        with self.assertRaises(ValueError):
            solve_aes(bytes(32), key=bytes(16))

    def test_rejects_unsupported_key_lengths(self) -> None:
        for length in (0, 15, 17, 23, 25, 31, 33):
            key = bytes(length)
            with self.subTest(length=length):
                with self.assertRaises(ValueError):
                    aes_expand_key(key)
                with self.assertRaises(ValueError):
                    aes_encrypt_block(bytes(16), key)
                with self.assertRaises(ValueError):
                    aes_decrypt_block(bytes(16), key)
                with self.assertRaises(ValueError):
                    solve_aes(bytes(16), key=key)

    def test_rejects_text_and_other_non_bytes_inputs(self) -> None:
        for value in ("00" * 16, 16, None, [0] * 16, bytearray(16)):
            with self.subTest(value_type=type(value).__name__):
                with self.assertRaises(TypeError):
                    aes_encrypt_block(value, bytes(16))
                with self.assertRaises(TypeError):
                    aes_decrypt_block(value, bytes(16))
                with self.assertRaises(TypeError):
                    aes_encrypt_block(bytes(16), value)
                with self.assertRaises(TypeError):
                    aes_expand_key(value)

    def test_wrapper_requires_an_explicit_key(self) -> None:
        with self.assertRaises(TypeError):
            solve_aes(bytes(16))


class AesCertificateTest(unittest.TestCase):
    def test_binary_certificate_decrypts_and_hashes_raw_bytes(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["cipher_name"], "aes")
        self.assertEqual(cert["name"], "aes")
        self.assertEqual(cert["encoding"], "hex")
        self.assertEqual(cert["hash_encoding"], "raw_bytes")
        self.assertNotIn("plaintext", cert)
        self.assertNotIn("ciphertext", cert)
        self.assertEqual(cert["source_url"], FIPS197_URL)
        self.assertEqual(len(cert["vectors"]), 3)
        self.assertEqual(cert["plaintext_hex"], PLAINTEXT.hex())
        self.assertEqual(cert["ciphertext_hex"], VECTORS[0][2])
        for vector, (bits, key_hex, ciphertext_hex) in zip(cert["vectors"], VECTORS):
            with self.subTest(bits=bits):
                self.assertEqual(vector["key_bits"], bits)
                self.assertEqual(vector["key_hex"], key_hex)
                self.assertEqual(vector["ciphertext_hex"], ciphertext_hex)
                self.assertEqual(vector["plaintext_hex"], PLAINTEXT.hex())
                recovered = aes_decrypt_block(
                    bytes.fromhex(vector["ciphertext_hex"]),
                    bytes.fromhex(vector["key_hex"]),
                )
                self.assertEqual(recovered, PLAINTEXT)
                self.assertEqual(
                    hashlib.sha256(recovered).hexdigest(), vector["plaintext_sha256"]
                )
                self.assertEqual(vector["plaintext_sha256"], cert["plaintext_sha256"])
        self.assertNotEqual(
            cert["plaintext_sha256"], hashlib.sha256(cert["plaintext_hex"].encode()).hexdigest()
        )


if __name__ == "__main__":
    unittest.main()
