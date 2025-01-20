from DiffieHellman.dh_analysis import run_dh_analysis
from DiffieHellman.dh import diffiehellman
from utils.menu_utils import display_table_menu

def dh_menu():
    while True:
        display_table_menu("Diffie-Hellman Menu", ["Run Analysis", "Key Exchange"])
        choice = input("Enter your choice (0-2): ")

        if choice == "1":
            print("\nDiffie-Hellman Key Analysis")
            run_dh_analysis()
        elif choice == "2":
            print("\nDiffie-Hellman Key Exchange")
            diffiehellman()
        elif choice == "0":
            print("Returning to the main menu...")
            break
        else:
            print("\nInvalid choice. Please select 0-2.")