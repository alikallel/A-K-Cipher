# A-K Cipher Tool

A centralized cryptographic toolkit designed for Capture The Flag (CTF) challenges, providing easy-to-use interfaces for multiple cipher techniques. This tool supports RSA, XOR, and Caesar ciphers, enabling encryption and decryption operations, as well as advanced cryptanalysis features.

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

### Additional Features: 
- FactorDB integration

## Requirements

- Python 3.x
- Required Python libraries:
  - `pwn`
  - `pycryptodome`
  - `hashlib`

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.