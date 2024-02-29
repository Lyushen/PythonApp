import subprocess
import os

def launch_main_app_with_mode():
    main_directory = os.path.dirname(os.path.abspath(__file__)) # Automatically determine the directory of this script
    # Prompt the user for their choice of interface
    print("Launcher: Please choose the interface mode:")
    print("1. [CLI] Command Line Iterface (Assignment)")
    print("2. [GUI] Graphical User Interface (Experimental)")
    print("3. Exit from the Launcher")
    choice = input("Enter your choice (1/2/3): ")
    if choice=="3":
        return
    mode = 'cli' if choice == '1' else 'gui' if choice == '2' else None # Determine the mode based on user input
    main_app_path = os.path.join(main_directory, "ONAssignment_OOP.py") # Construct the path to the main application script
    # Launch the main application with the chosen mode
    if mode:
        subprocess.call(["python", main_app_path, mode])
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    launch_main_app_with_mode()