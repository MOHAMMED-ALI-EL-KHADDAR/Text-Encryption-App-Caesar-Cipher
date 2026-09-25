# Caesar Cipher App - Quick Start Guide

## Installation (First Time Only)

```bash
# 1. Navigate to the project directory
cd caesar_cipher_app

# 2. Create a Python virtual environment
python3 -m venv venv

# 3. Activate the environment
# On Linux/macOS:
source venv/bin/activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## Basic Usage

### 1. Encrypt Text

**Command:**
```bash
python main.py encrypt "Your text here" --shift 5
```

**Example:**
```bash
python main.py encrypt "Secret Message" --shift 7

# Output:
# Plain Text:  Secret Message
# Cipher Text: Zljyld Tlzzhnl
# Shift Key:   7
```

---

### 2. Decrypt Text

**Command:**
```bash
python main.py decrypt "Your encrypted text" --shift 5
```

**Example:**
```bash
python main.py decrypt "Zljyld Tlzzhnl" --shift 7

# Output:
# Cipher Text: Zljyld Tlzzhnl
# Plain Text:  Secret Message
# Shift Key:   7
```

---

### 3. Crack Ciphertext (Brute-Force)

**Command:**
```bash
python main.py crack "Your encrypted text"
```

**Example:**
```bash
python main.py crack "Zljyld Tlzzhnl"

# Output shows all 26 possible shifts:
# Shift 0: Zljyld Tlzzhnl
# Shift 1: Yvkxkc Skyygml
# Shift 2: Xujwjb Rjxxflk
# ...
# Shift 7: Secret Message  ← This one is readable!
# ...
```

**How to identify the key:**
1. Scroll through all 26 results
2. Find the one that reads like English
3. Note the shift number (in this case: 7)

---

## Advanced Options

### Copy to Clipboard

After encryption or decryption, automatically copy the result:

```bash
python main.py encrypt "Hello" --shift 3 --copy
# Cipher text copied to clipboard!

python main.py decrypt "Khoor" --shift 3 --copy
# Plain text copied to clipboard!
```

---

### Use Different Shift Keys

The shift key must be between 0–25:

```bash
# Shift by 1
python main.py encrypt "Hello" --shift 1  # Ifmmp

# Shift by 13 (ROT-13)
python main.py encrypt "Hello" --shift 13  # Uryyb

# Shift by 25 (equivalent to -1)
python main.py encrypt "Hello" --shift 25  # Gdkkn
```

---

### Test with Special Characters & Numbers

The cipher preserves digits, punctuation, and spaces:

```bash
python main.py encrypt "Test123! 2024-09-25" --shift 3

# Output:
# Plain:  Test123! 2024-09-25
# Cipher: Whvw123! 2024-09-25

# Notice: T→W, e→h, s→v, t→w (letters shifted)
#         123, !, spaces, hyphens (preserved)
```

---

## Common Workflows

### Workflow 1: Encrypt a Secret & Share

```bash
# Step 1: Encrypt your message
python main.py encrypt "Meet me at the park" --shift 9 --copy

# Step 2: Send encrypted text to recipient via email/chat
# (Automatically copied to clipboard)

# Step 3: Recipient decrypts with the known shift key
python main.py decrypt "<encrypted text>" --shift 9
```

---

### Workflow 2: Intercept & Crack an Unknown Cipher

```bash
# You intercepted: "Gssjf iye xs bsf iye"

# Step 1: Run brute-force
python main.py crack "Gssjf iye xs bsf iye"

# Step 2: Scan results manually
# Shift 3: "Depot fur at fur fur"  (gibberish)
# Shift 4: "Delno etq zs etq etq"  (gibberish)
# Shift 5: "Hello due to due due"  (partial sense)
# ...
# Shift 9: "Bread was at way was"  (not right)
# Shift 10: "Azqjy vtz zs vzx vtz"  (gibberish)

# Step 3: Most readable shift ≈ shift 5
python main.py decrypt "Gssjf iye xs bsf iye" --shift 5
```

---

### Workflow 3: Test Multiple Shifts

```bash
# Encrypt the same message with different shift keys
python main.py encrypt "Test Message" --shift 1
python main.py encrypt "Test Message" --shift 5
python main.py encrypt "Test Message" --shift 10
python main.py encrypt "Test Message" --shift 25

# Compare the outputs to see the pattern
```

---

## Troubleshooting

### Issue: `No module named 'rich'`

**Solution:** Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install rich==13.7.0 pyperclip==1.8.2
```

---

### Issue: `command not found: python`

**Solution:** Use `python3` instead:
```bash
python3 main.py encrypt "Hello" --shift 3
```

---

### Issue: `--copy` flag doesn't work

**Solution:** The app requires `pyperclip`. It's listed in `requirements.txt`, but if not installed:
```bash
pip install pyperclip==1.8.2
```

The app will display a helpful error if pyperclip is missing.

---

### Issue: Non-English text or special alphabets

**Current limitation:** The app only handles A–Z (uppercase/lowercase). To extend to other languages:
1. Modify the `UPPERCASE`, `LOWERCASE` character sets in `CaesarCipher` class
2. Define alphabet for your language (e.g., Cyrillic, Arabic)
3. Adjust the modulo operations accordingly

---

## Educational Notes

### Why Only 26 Shifts?

The English alphabet has 26 letters. Caesar Cipher shifts letters by a fixed number in a circular pattern:

```
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
          ↓ (shift 3)
D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
```

Since there are only 26 unique starting positions, there can only be 26 unique shifts (0–25). This tiny key space makes brute-force trivial.

---

### Frequency Analysis Weakness

In English text, the letter 'E' appears ~12% of the time. After encryption, the most common letter in the ciphertext should map to 'E'. By analyzing character frequency, you can guess the shift without brute-force.

**Example:**
- Original: "the elephant eats eggs everywhere"
  - 'e' appears 10 times
- Encrypted (shift 3): "wkh hohskdqw hdwv hjjv hyhuazkhuh"
  - 'h' appears 10 times
- Frequency analysis: 'h' ≈ 'e', so shift ≈ 3

---

### Security Implications

| Attack | Effort | Feasibility |
|---|---|---|
| Brute-Force (26 keys) | Milliseconds | ✅ Easy |
| Frequency Analysis | Minutes | ✅ Easy |
| Known-Plaintext | Instant (1 char) | ✅ Easy |

Modern encryption (AES-256) has 2^256 possible keys—brute-force would take longer than the age of the universe. Never use Caesar Cipher for real security.

---

## Help & Options

View all available commands:
```bash
python main.py --help
```

View subcommand help:
```bash
python main.py encrypt --help
python main.py decrypt --help
python main.py crack --help
```

---

## Next Steps

- Experiment with different messages and shift keys
- Try the `crack` command on encrypted text
- Analyze character frequency in results
- Read the full `README.md` for technical details
- Modify the code to add features (file I/O, Vigenère cipher, etc.)

---

**Enjoy exploring classical cryptography! 🔐**
