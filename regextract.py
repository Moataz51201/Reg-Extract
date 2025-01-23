import argparse
import os
import sys
import json
import binascii
from Registry import Registry  # For offline hives (pip install python-registry)
import winreg  # For live registry

# Map registry hives to their respective constants in winreg
HIVES = {
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_USERS": winreg.HKEY_USERS,
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
}

def list_hives():
    """List all registry hives."""
    print("Available Registry Hives:")
    for idx, hive in enumerate(HIVES.keys(), 1):
        print(f"{idx}. {hive}")

def list_subkeys(base_key, sub_key):
    """List all subkeys of a given registry key."""
    try:
        with winreg.OpenKey(base_key, sub_key) as key:
            print(f"Subkeys under: {sub_key or 'Root'}")
            subkeys = []
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkeys.append(subkey_name)
                    print(f"  {i + 1}. {subkey_name}")
                    i += 1
                except OSError:
                    break  # No more subkeys
            return subkeys
    except PermissionError:
        print("Permission denied. Try running as Administrator.")
        return []

def list_values(base_key, sub_key):
    """List all values of a given registry key."""
    try:
        with winreg.OpenKey(base_key, sub_key) as key:
            print(f"Values under: {sub_key}")
            i = 0
            while True:
                try:
                    value = winreg.EnumValue(key, i)
                    print(f"  {value[0]}: {value[1]} ({value[2]})")
                    i += 1
                except OSError:
                    break  # No more values
    except PermissionError:
        print("Permission denied. Try running as Administrator.")

def traverse_registry_key(key):
    """Recursively traverse an offline registry key and collect its structure."""
    data = {
        "name": key.name(),
        "values": {},
        "subkeys": []
    }

    # Extract all values in the current key
    for value in key.values():
        try:
            if isinstance(value.value(), bytes):
                data["values"][value.name()] = binascii.hexlify(value.value()).decode("utf-8")
            else:
                data["values"][value.name()] = value.value()
        except Exception as e:
            data["values"][value.name()] = f"Error: {str(e)}"

    # Recursively process all subkeys
    for subkey in key.subkeys():
        data["subkeys"].append(traverse_registry_key(subkey))

    return data

def process_hive(hive_path, output_file):
    """Load and traverse an offline registry hive."""
    try:
        reg = Registry.Registry(hive_path)
        root_key = reg.root()
        result = traverse_registry_key(root_key)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
        print(f"Registry hive data saved to {output_file}")
    except Exception as e:
        print(f"Error processing hive: {e}")

def explore_live_registry():
        list_hives()
        hive_choice = input("Select a hive number to explore (or type 'exit' to quit): ").strip()
        if hive_choice.lower() == "exit":
            sys.exit()

        try:
            hive_choice = int(hive_choice)
            if hive_choice < 1 or hive_choice > len(HIVES):
                print("Invalid choice. Exiting.")
                sys.exit()
            hive_name = list(HIVES.keys())[hive_choice - 1]
            hive = HIVES[hive_name]
            print(f"\nYou selected: {hive_name}")
        except ValueError:
            print("Invalid input. Exiting.")
            sys.exit()

        current_path = ""
        while True:
            subkeys = list_subkeys(hive, current_path)
            if not subkeys:
                print("No more subkeys available.")
                break

            subkey_choice = input(
                "Enter a subkey number to explore, 'values <number>' to list values, 'back' to go up, or 'exit' to quit: "
            )
            if subkey_choice.lower() == "back":
                if "\\" in current_path:
                    current_path = "\\".join(current_path.split("\\")[:-1])
                else:
                    current_path = ""
                continue
            elif subkey_choice.lower().startswith("values"):
                try:
                    parts = subkey_choice.split()
                    if len(parts) != 2:
                        print("Invalid command. Use: values <number>")
                        continue
                    key_number = int(parts[1]) - 1
                    if 0 <= key_number < len(subkeys):
                        selected_subkey = f"{current_path}\\{subkeys[key_number]}" if current_path else subkeys[key_number]
                        list_values(hive, selected_subkey)
                    else:
                        print("Invalid key number. Try again.")
                except ValueError:
                    print("Invalid command. Use: values <number>")
                continue
            elif subkey_choice.lower() == "exit":
                print("Exiting.")
                break

            try:
                subkey_choice = int(subkey_choice) - 1
                if 0 <= subkey_choice < len(subkeys):
                    current_path = f"{current_path}\\{subkeys[subkey_choice]}" if current_path else subkeys[subkey_choice]
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Invalid input. Try again.")

def main():
    parser = argparse.ArgumentParser(description="Windows Registry Explorer Tool")
    parser.add_argument("-live", action="store_true", help="Explore the live system registry interactively.")
    parser.add_argument("-load", metavar="HIVE_PATH", type=str, help="Load an offline registry hive file.")
    parser.add_argument("-output", metavar="OUTPUT_FILE", type=str, default="registry_output.json",
                        help="Output file for the offline hive structure (default: registry_output.json).")

    args = parser.parse_args()

    if args.live:
        explore_live_registry()
    elif args.load:
        if not os.path.exists(args.load):
            print(f"Hive file not found: {args.load}")
            sys.exit()
        process_hive(args.load, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
