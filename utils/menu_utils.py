def display_table_menu(title, options):
    print("\n" + "╔" + "═" * 39 + "╗")
    print(f"║ {title.center(37)} ║")
    print("╠" + "═" * 39 + "╣")

    for idx, option in enumerate(options, start=1):
        print(f"║ {idx}. {option.ljust(34)} ║")

    print("║ 0. Quit".ljust(39) + " ║")
    print("╚" + "═" * 39 + "╝")