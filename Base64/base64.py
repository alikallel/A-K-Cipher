import base64

def base_64():
    while True:
        print("\nBase64 Tool")
        print("\u2554" + "\u2550" * 27 + "\u2557")
        print("\u2551 1. Encode to Base64       \u2551")
        print("\u2551 2. Decode from Base64     \u2551")
        print("\u2551 0. Return to Main Menu    \u2551")
        print("\u255a" + "\u2550" * 27 + "\u255d")
        
        choice = input("Enter your choice (0-2): ")
        
        if choice == "1":
            text = input("Enter the text to encode: ")
            encoded = base64.b64encode(text.encode()).decode()
            print(f"Encoded Base64: {encoded}")
        
        elif choice == "2":
            text = input("Enter the Base64 to decode: ")
            try:
                decoded = base64.b64decode(text).decode()
                print(f"Decoded Text: {decoded}")
            except base64.binascii.Error:
                print("Invalid Base64 input. Please try again.")
        
        elif choice == "0":
            print("Returning to the main menu...")
            break
        
        else:
            print("\nInvalid choice. Please select 0-2.")
