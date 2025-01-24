def rot_bruteforce(text):
    results = []
    for shift in range(26):
        decrypted = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decrypted += chr((ord(char) - base - shift) % 26 + base)
            else:
                decrypted += char
        results.append((shift, decrypted))
    return results

def rot():
    while True:
        print("\nROT Cipher Tool")
        print("\u2554" + "\u2550" * 27+ "\u2557")
        print("\u2551 1. Encrypt with ROT       \u2551")
        print("\u2551 2. Decrypt with ROT       \u2551")
        print("\u2551 3. Bruteforce Decrypt     \u2551")
        print("\u2551 0. Return to Main Menu    \u2551")
        print("\u255a" + "\u2550" * 27 + "\u255d")

        choice = input("Enter your choice (0-3): ")

        if choice == "1":
            text = input("Enter the text: ")
            try:
                rot_value = int(input("Enter the ROT value (0-25): "))
                if not 0 <= rot_value <= 25:
                    raise ValueError

                result = ""
                for char in text:
                    if char.isalpha():
                        base = ord('A') if char.isupper() else ord('a')
                        result += chr((ord(char) - base + rot_value) % 26 + base)
                    else:
                        result += char

                print(f"Encrypted Text: {result}")
            except ValueError:
                print("Invalid ROT value. Please enter a number between 0 and 25.")

        elif choice == "2":
            text = input("Enter the text: ")
            try:
                rot_value = int(input("Enter the ROT value (0-25): "))
                if not 0 <= rot_value <= 25:
                    raise ValueError

                result = ""
                for char in text:
                    if char.isalpha():
                        base = ord('A') if char.isupper() else ord('a')
                        result += chr((ord(char) - base - rot_value) % 26 + base)
                    else:
                        result += char

                print(f"Decrypted Text: {result}")
            except ValueError:
                print("Invalid ROT value. Please enter a number between 0 and 25.")

        elif choice == "3":
            text = input("Enter the encrypted text to bruteforce: ")
            print("\nPossible Decryptions:")
            results = rot_bruteforce(text)
            for shift, decrypted in results:
                print(f"ROT-{shift}: {decrypted}")

        elif choice == "0":
            print("Returning to the main menu...")
            break
        else:
            print("\nInvalid choice. Please select 0-3.")