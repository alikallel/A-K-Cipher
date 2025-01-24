# A-K Cipher Tool

The A-K Cipher Tool is a cryptographic toolkit designed for Capture The Flag (CTF) challenges and general cryptographic operations. This tool supports multiple cipher techniques, including RSA, XOR, Caesar, AES, Diffie-Hellman, Base Encoding/Decoding, and ROT ciphers. It also includes advanced mathematical operations for cryptanalysis and number theory transformations.

## Features

### RSA Operations:
- **Encryption**: Encrypt messages using the RSA algorithm.
- **Decryption**: Multiple decryption methods including: Known prime factors (p, q), Known private exponent (d), Common modulus attack.
- **Factorization**: Use various methods, including Fermat’s factorization.

### AES Operations:
- **Supported Modes**: Electronic Codebook (ECB), Cipher Block Chaining (CBC).
- **Features**: 16-byte key requirement, Support encryption and decryption

### Diffie-Hellman
- **Features**: Modular exponentiation calculator, Shared secret computation, Message decryption, Support for AES-CBC encrypted messages.

### XOR Cipher:
- **Encryption**: Encrypt messages using the XOR cipher with a custom key, with support for flag formatting (e.g., `CTF{message}`).
- **Decryption**: Decrypt XOR-encrypted messages.

### Caesar Cipher:
- **Encryption**: Encrypt messages using the Caesar cipher with a specified shift value (1-25).
- **Decryption**: Decrypt messages using a known shift value or brute-force all possible shifts to recover the original message.

### ROT Cipher:
- **Encryption**: Encrypt messages using the ROT cipher with a specified shift value (0-25).
- **Decryption**: Decrypt messages using a known shift value or brute-force all possible shifts to recover the original message.

### Base Encoding/Decoding:
- **Base64**: Encode and decode messages using Base64.
- **Base32**: Encode and decode messages using Base32.
- **Base16**: Encode and decode messages using Base16.

### Mathematical Operations:
- **Quadratic Residues**: Find quadratic residues modulo a prime.
- **Modular Square Root**: Compute modular square roots using the Tonelli-Shanks algorithm.
- **Chinese Remainder Theorem**: Solve systems of congruences using the Chinese Remainder Theorem.
- **Lattice Reduction**: Perform Gaussian reduction on lattice vectors.
- **Legendre Symbol**: Compute the Legendre symbol.
- **Number Theory Transformations**: Binary to decimal, decimal to binary, and modular exponentiation.
- **Tonelli-Shanks Algorithm**: Compute modular square roots using the Tonelli-Shanks algorithm.

### Additional Features: 
- FactorDB integration

## Requirements

- Python 3.x
- Required Python libraries:
  - `pwn`
  - `pycryptodome`
  - `hashlib`
  - `sympy`
  - `numpy`
  - `requests`

## Usage

To use the A-K Cipher Tool, run the `main.py` script:

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.