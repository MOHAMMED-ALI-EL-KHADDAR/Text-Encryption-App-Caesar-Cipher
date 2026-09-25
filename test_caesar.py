#!/usr/bin/env python3
"""
Unit tests for Caesar Cipher implementation.
Tests encryption, decryption, brute-force, and edge cases.
"""

import sys
from main import CaesarCipher


class TestCaesarCipher:
    """Test suite for CaesarCipher class."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def assert_equal(self, actual, expected, test_name: str):
        """Helper: assert equality and track results."""
        if actual == expected:
            print(f"✓ {test_name}")
            self.passed += 1
        else:
            print(f"✗ {test_name}")
            print(f"  Expected: {expected}")
            print(f"  Actual:   {actual}")
            self.failed += 1
    
    def test_encrypt_simple(self):
        """Test basic encryption with shift 3."""
        cipher = CaesarCipher(shift=3)
        result = cipher.encrypt("Hello")
        self.assert_equal(result, "Khoor", "Encrypt 'Hello' with shift 3")
    
    def test_encrypt_full_alphabet(self):
        """Test encryption of all letters."""
        cipher = CaesarCipher(shift=1)
        result = cipher.encrypt("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        expected = "BCDEFGHIJKLMNOPQRSTUVWXYZA"
        self.assert_equal(result, expected, "Encrypt full uppercase alphabet (shift 1)")
        
        result = cipher.encrypt("abcdefghijklmnopqrstuvwxyz")
        expected = "bcdefghijklmnopqrstuvwxyza"
        self.assert_equal(result, expected, "Encrypt full lowercase alphabet (shift 1)")
    
    def test_encrypt_wraparound(self):
        """Test wraparound: Z→A with shift 1."""
        cipher = CaesarCipher(shift=1)
        result = cipher.encrypt("XYZ")
        self.assert_equal(result, "YZA", "Encrypt 'XYZ' with shift 1 (wraparound)")
        
        result = cipher.encrypt("xyz")
        self.assert_equal(result, "yza", "Encrypt 'xyz' with shift 1 (lowercase wraparound)")
    
    def test_encrypt_numbers_preserved(self):
        """Test that numbers are preserved."""
        cipher = CaesarCipher(shift=3)
        result = cipher.encrypt("Test123")
        self.assert_equal(result, "Whvw123", "Numbers preserved during encryption")
    
    def test_encrypt_special_chars_preserved(self):
        """Test that special characters and spaces are preserved."""
        cipher = CaesarCipher(shift=3)
        result = cipher.encrypt("Hello, World!")
        self.assert_equal(result, "Khoor, Zruog!", "Special chars preserved")
    
    def test_encrypt_mixed_content(self):
        """Test encryption with mixed alphanumeric and special content."""
        cipher = CaesarCipher(shift=5)
        result = cipher.encrypt("Test-123 Data!")
        self.assert_equal(result, "Yjxy-123 Ifyf!", "Mixed content preserved")
    
    def test_decrypt_simple(self):
        """Test basic decryption with shift 3."""
        cipher = CaesarCipher(shift=3)
        result = cipher.decrypt("Khoor")
        self.assert_equal(result, "Hello", "Decrypt 'Khoor' with shift 3")
    
    def test_decrypt_wraparound(self):
        """Test wraparound on decryption: A→Z with shift 1."""
        cipher = CaesarCipher(shift=1)
        result = cipher.decrypt("ABC")
        self.assert_equal(result, "ZAB", "Decrypt 'ABC' with shift 1 (wraparound)")
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypt then decrypt returns original."""
        plaintext = "The Quick Brown Fox Jumps Over The Lazy Dog 2024!"
        cipher = CaesarCipher(shift=7)
        encrypted = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(encrypted)
        self.assert_equal(decrypted, plaintext, "Roundtrip: encrypt → decrypt")
    
    def test_shift_normalization(self):
        """Test that shifts > 25 are normalized."""
        text = "Hello"
        
        # Shift 3 and shift 29 should produce same result (29 % 26 = 3)
        cipher3 = CaesarCipher(shift=3)
        cipher29 = CaesarCipher(shift=29)
        
        result3 = cipher3.encrypt(text)
        result29 = cipher29.encrypt(text)
        self.assert_equal(result29, result3, "Shift 29 normalized to shift 3")
    
    def test_shift_zero(self):
        """Test that shift 0 returns unchanged text."""
        cipher = CaesarCipher(shift=0)
        result = cipher.encrypt("Unchanged")
        self.assert_equal(result, "Unchanged", "Shift 0 returns original text")
    
    def test_shift_13_symmetry(self):
        """Test ROT-13: encrypting twice returns original."""
        text = "Hello"
        cipher = CaesarCipher(shift=13)
        encrypted_once = cipher.encrypt(text)
        encrypted_twice = cipher.encrypt(encrypted_once)
        self.assert_equal(encrypted_twice, text, "ROT-13 applied twice returns original")
    
    def test_brute_force_finds_all(self):
        """Test that brute-force generates all 26 shifts."""
        ciphertext = "Khoor"
        results = CaesarCipher.brute_force(ciphertext)
        
        # Should return 26 results
        self.assert_equal(len(results), 26, "Brute-force generates 26 results")
        
        # Results should include (3, "Hello")
        found = any(shift == 3 and plaintext == "Hello" for shift, plaintext in results)
        self.assert_equal(found, True, "Brute-force includes correct decryption (shift 3)")
    
    def test_brute_force_known_key(self):
        """Test brute-force finds the correct plaintext."""
        plaintext = "SecretMessage"
        cipher = CaesarCipher(shift=5)
        ciphertext = cipher.encrypt(plaintext)
        
        results = CaesarCipher.brute_force(ciphertext)
        
        # Find the result with shift 5
        for shift, decrypted in results:
            if shift == 5:
                self.assert_equal(decrypted, plaintext, "Brute-force identifies correct plaintext")
                break
    
    def test_empty_string(self):
        """Test encryption/decryption of empty string."""
        cipher = CaesarCipher(shift=3)
        result = cipher.encrypt("")
        self.assert_equal(result, "", "Encrypt empty string")
        
        result = cipher.decrypt("")
        self.assert_equal(result, "", "Decrypt empty string")
    
    def test_spaces_only(self):
        """Test encryption of string with only spaces."""
        cipher = CaesarCipher(shift=3)
        result = cipher.encrypt("   ")
        self.assert_equal(result, "   ", "Spaces preserved")
    
    def test_case_sensitivity(self):
        """Test that case is preserved."""
        cipher = CaesarCipher(shift=3)
        result = cipher.encrypt("HeLLo")
        self.assert_equal(result, "KhOOr", "Case sensitivity preserved")
    
    def test_long_text(self):
        """Test encryption of longer text."""
        plaintext = "The quick brown fox jumps over the lazy dog. " * 10
        cipher = CaesarCipher(shift=7)
        ciphertext = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(ciphertext)
        self.assert_equal(decrypted, plaintext, "Long text roundtrip")
    
    def run_all(self):
        """Run all tests and print summary."""
        print("\n" + "="*60)
        print("Caesar Cipher Test Suite")
        print("="*60 + "\n")
        
        print("[Basic Encryption]")
        self.test_encrypt_simple()
        self.test_encrypt_full_alphabet()
        self.test_encrypt_wraparound()
        
        print("\n[Character Handling]")
        self.test_encrypt_numbers_preserved()
        self.test_encrypt_special_chars_preserved()
        self.test_encrypt_mixed_content()
        self.test_case_sensitivity()
        
        print("\n[Decryption]")
        self.test_decrypt_simple()
        self.test_decrypt_wraparound()
        
        print("\n[Roundtrip & Validation]")
        self.test_encrypt_decrypt_roundtrip()
        self.test_shift_normalization()
        self.test_shift_zero()
        self.test_shift_13_symmetry()
        
        print("\n[Brute-Force]")
        self.test_brute_force_finds_all()
        self.test_brute_force_known_key()
        
        print("\n[Edge Cases]")
        self.test_empty_string()
        self.test_spaces_only()
        self.test_long_text()
        
        print("\n" + "="*60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("="*60 + "\n")
        
        return self.failed == 0


if __name__ == '__main__':
    tester = TestCaesarCipher()
    success = tester.run_all()
    sys.exit(0 if success else 1)
