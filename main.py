#!/usr/bin/env python3
"""
Text Encryption App - Caesar Cipher Implementation
A production-ready Caesar Cipher with CLI interface, encryption/decryption,
and cryptanalysis (brute-force) mode.

WARNING: For educational purposes only. Caesar Cipher is cryptographically weak
and should NOT be used for real security. Use AES-256, ChaCha20, or modern
cryptographic algorithms for actual data protection.
"""

import sys
import argparse
from typing import Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from rich.align import Align


class CaesarCipher:
    """
    Caesar Cipher implementation with support for uppercase, lowercase,
    numbers, and special characters (preserved as-is).
    
    Modulo arithmetic ensures wrapping: (char_index + shift) % 26
    """
    
    UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
    DIGITS = '0123456789'
    
    def __init__(self, shift: int = 0):
        """
        Initialize with a shift key (0-25).
        
        Args:
            shift: Integer shift value (0-25). Values > 25 are normalized via modulo.
        """
        self.shift = shift % 26  # Normalize to 0-25 range
    
    def encrypt(self, text: str) -> str:
        """
        Encrypt text using Caesar Cipher with current shift key.
        
        Algorithm:
        1. For each character in text:
           - If uppercase letter: (char_index + shift) % 26 → new char
           - If lowercase letter: (char_index + shift) % 26 → new char
           - If digit or special char: preserve unchanged
        2. Return encrypted text
        
        Args:
            text: Plain text string to encrypt
            
        Returns:
            Encrypted text with same case sensitivity
        """
        result = []
        for char in text:
            if char in self.UPPERCASE:
                # Encrypt uppercase: A=0, B=1, ..., Z=25
                idx = self.UPPERCASE.index(char)
                new_idx = (idx + self.shift) % 26
                result.append(self.UPPERCASE[new_idx])
            elif char in self.LOWERCASE:
                # Encrypt lowercase: a=0, b=1, ..., z=25
                idx = self.LOWERCASE.index(char)
                new_idx = (idx + self.shift) % 26
                result.append(self.LOWERCASE[new_idx])
            else:
                # Preserve digits, spaces, punctuation
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, text: str) -> str:
        """
        Decrypt text using Caesar Cipher (reverse shift).
        
        Decryption uses negative shift: (char_index - shift) % 26
        
        Args:
            text: Encrypted text string to decrypt
            
        Returns:
            Decrypted (original) text
        """
        # Decryption is encryption with negative shift
        result = []
        for char in text:
            if char in self.UPPERCASE:
                idx = self.UPPERCASE.index(char)
                new_idx = (idx - self.shift) % 26
                result.append(self.UPPERCASE[new_idx])
            elif char in self.LOWERCASE:
                idx = self.LOWERCASE.index(char)
                new_idx = (idx - self.shift) % 26
                result.append(self.LOWERCASE[new_idx])
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def brute_force(ciphertext: str) -> list[Tuple[int, str]]:
        """
        Attempt all 25 possible shifts to crack the cipher without key.
        
        Returns all possible decryptions—useful for frequency analysis
        or when the key is unknown.
        
        Args:
            ciphertext: Encrypted text to crack
            
        Returns:
            List of tuples: (shift_key, decrypted_text)
        """
        results = []
        for shift in range(26):
            cipher = CaesarCipher(shift)
            plaintext = cipher.decrypt(ciphertext)
            results.append((shift, plaintext))
        return results


class CaesarCipherCLI:
    """
    Rich CLI interface for Caesar Cipher operations.
    Provides formatted tables, status indicators, and security warnings.
    """
    
    def __init__(self):
        self.console = Console()
    
    def print_header(self):
        """Print application header with security warning."""
        title = Text("🔐 Caesar Cipher Text Encryption App", style="bold cyan")
        header_panel = Panel(
            Align.center(title),
            border_style="cyan",
            expand=False
        )
        self.console.print(header_panel)
        
        warning_text = Text(
            "⚠️  SECURITY WARNING: Caesar Cipher is cryptographically WEAK.\n"
            "For educational use only. Use AES-256/ChaCha20 for real security.",
            style="bold yellow"
        )
        warning_panel = Panel(
            warning_text,
            border_style="red",
            style="on #2b2b2b"
        )
        self.console.print(warning_panel)
    
    def print_encrypt_result(self, plaintext: str, ciphertext: str, shift: int):
        """Display encryption result in formatted table."""
        table = Table(title="[bold cyan]Encryption Result[/bold cyan]", show_header=True)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Operation", "[bold]Encryption[/bold]")
        table.add_row("Shift Key", f"[bold yellow]{shift}[/bold yellow]")
        table.add_row("Plain Text", plaintext)
        table.add_row("Cipher Text", f"[bold green]{ciphertext}[/bold green]")
        table.add_row("Text Length", str(len(plaintext)))
        
        self.console.print(table)
    
    def print_decrypt_result(self, ciphertext: str, plaintext: str, shift: int):
        """Display decryption result in formatted table."""
        table = Table(title="[bold cyan]Decryption Result[/bold cyan]", show_header=True)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Operation", "[bold]Decryption[/bold]")
        table.add_row("Shift Key", f"[bold yellow]{shift}[/bold yellow]")
        table.add_row("Cipher Text", ciphertext)
        table.add_row("Plain Text", f"[bold green]{plaintext}[/bold green]")
        table.add_row("Text Length", str(len(ciphertext)))
        
        self.console.print(table)
    
    def print_brute_force_results(self, ciphertext: str, results: list[Tuple[int, str]]):
        """Display all 26 brute-force decryption attempts."""
        table = Table(
            title="[bold cyan]Brute-Force Cryptanalysis[/bold cyan]",
            show_header=True
        )
        table.add_column("Shift Key", style="yellow", width=12)
        table.add_column("Decrypted Text", style="green")
        
        for shift, plaintext in results:
            # Truncate long results for readability
            display_text = plaintext[:80] + "..." if len(plaintext) > 80 else plaintext
            table.add_row(str(shift), display_text)
        
        self.console.print(table)
        
        info_text = Text(
            "💡 Review results above and identify readable text. "
            "This brute-force is feasible because Caesar Cipher has only 26 possible keys.",
            style="dim italic"
        )
        self.console.print(Panel(info_text, border_style="blue"))
    
    def print_success(self, message: str):
        """Print success message with checkmark badge."""
        self.console.print(f"[bold green]✓ {message}[/bold green]")
    
    def print_error(self, message: str):
        """Print error message with X badge."""
        self.console.print(f"[bold red]✗ {message}[/bold red]")
    
    def print_info(self, message: str):
        """Print info message with info badge."""
        self.console.print(f"[bold blue]ℹ {message}[/bold blue]")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Caesar Cipher Text Encryption App (Educational Purpose Only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encrypt "Hello World" --shift 3
  %(prog)s decrypt "Khoor Zruog" --shift 3
  %(prog)s crack "Khoor Zruog"
  %(prog)s encrypt "Secret Message" --shift 13 --copy
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Operation to perform')
    
    # Encrypt subcommand
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt text')
    encrypt_parser.add_argument('text', help='Plain text to encrypt')
    encrypt_parser.add_argument(
        '--shift', type=int, default=3, choices=range(26),
        help='Shift key (0-25, default: 3)'
    )
    encrypt_parser.add_argument(
        '--copy', action='store_true',
        help='Copy result to clipboard (requires pyperclip)'
    )
    
    # Decrypt subcommand
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt text')
    decrypt_parser.add_argument('text', help='Cipher text to decrypt')
    decrypt_parser.add_argument(
        '--shift', type=int, default=3, choices=range(26),
        help='Shift key (0-25, default: 3)'
    )
    decrypt_parser.add_argument(
        '--copy', action='store_true',
        help='Copy result to clipboard (requires pyperclip)'
    )
    
    # Crack/Brute-force subcommand
    crack_parser = subparsers.add_parser(
        'crack',
        help='Attempt all 26 shifts (brute-force cryptanalysis)'
    )
    crack_parser.add_argument('text', help='Cipher text to crack')
    
    args = parser.parse_args()
    
    cli = CaesarCipherCLI()
    cli.print_header()
    
    try:
        if args.command == 'encrypt':
            cipher = CaesarCipher(args.shift)
            ciphertext = cipher.encrypt(args.text)
            cli.print_encrypt_result(args.text, ciphertext, args.shift)
            
            if args.copy:
                try:
                    import pyperclip
                    pyperclip.copy(ciphertext)
                    cli.print_success("Cipher text copied to clipboard!")
                except ImportError:
                    cli.print_error("pyperclip not installed. Install with: pip install pyperclip")
        
        elif args.command == 'decrypt':
            cipher = CaesarCipher(args.shift)
            plaintext = cipher.decrypt(args.text)
            cli.print_decrypt_result(args.text, plaintext, args.shift)
            
            if args.copy:
                try:
                    import pyperclip
                    pyperclip.copy(plaintext)
                    cli.print_success("Plain text copied to clipboard!")
                except ImportError:
                    cli.print_error("pyperclip not installed. Install with: pip install pyperclip")
        
        elif args.command == 'crack':
            results = CaesarCipher.brute_force(args.text)
            cli.print_brute_force_results(args.text, results)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        cli.print_error(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
