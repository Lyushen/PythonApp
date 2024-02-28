import subprocess
import os

def launch_main_app_with_mode():
    # Automatically determine the directory of this script
    main_directory = os.path.dirname(os.path.abspath(__file__))
    # Prompt the user for their choice of interface
    print("Choose the interface mode:")
    print("1. CLI Interface (Assignment)")
    print("2. GUI Interface (Experimental)")
    choice = input("Enter your choice (1/2): ")
    # Determine the mode based on user input
    mode = 'cli' if choice == '1' else 'gui' if choice == '2' else None
    # Construct the path to the main application script
    main_app_path = os.path.join(main_directory, "ONAssignment_OOP.py")
    # Launch the main application with the chosen mode
    if mode:
        subprocess.call(["python", main_app_path, mode])
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    launch_main_app_with_mode()