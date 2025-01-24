from Base.base64ed import encode_base64, decode_base64
from Base.base32ed import encode_base32, decode_base32
from Base.base16ed import encode_base16, decode_base16

def display_menu():
    print("\nBase Encoding/Decoding")
    print("\u2554" + "\u2550" * 30 + "\u2557")
    print("\u2551 1. Base64 Encode             \u2551")
    print("\u2551 2. Base64 Decode             \u2551")
    print("\u2551 3. Base32 Encode             \u2551")
    print("\u2551 4. Base32 Decode             \u2551")
    print("\u2551 5. Base16 Encode             \u2551")
    print("\u2551 6. Base16 Decode             \u2551")
    print("\u2551 0. Exit                      \u2551")
    print("\u255a" + "\u2550" * 30 + "\u255d")

def base():
    while True:
        display_menu()
        choice = input("Enter your choice (0-6): ")
        
        if choice == "1":
            text = input("Enter text to Base64 encode: ")
            print(f"Encoded: {encode_base64(text)}")
        elif choice == "2":
            text = input("Enter Base64 to decode: ")
            print(f"Decoded: {decode_base64(text)}")
        elif choice == "3":
            text = input("Enter text to Base32 encode: ")
            print(f"Encoded: {encode_base32(text)}")
        elif choice == "4":
            text = input("Enter Base32 to decode: ")
            print(f"Decoded: {decode_base32(text)}")
        elif choice == "5":
            text = input("Enter text to Base16 encode: ")
            print(f"Encoded: {encode_base16(text)}")
        elif choice == "6":
            text = input("Enter Base16 to decode: ")
            print(f"Decoded: {decode_base16(text)}")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

