import os
import subprocess
from pystray import MenuItem as item
from pystray import Icon
from PIL import Image, ImageDraw

main_directory:str = os.path.dirname(os.path.abspath(__file__))
print(main_directory)

def create_image():
    """Create an image for the tray icon."""
    # Create an image with single color
    image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.rectangle([16, 16, 48, 48], fill=(255, 0, 0))
    return image

def start_flask(icon):
    """Function to start Flask server."""
    # Specify the full path to the Python executable inside the virtual environment
    python_exec_path = os.path.join(main_directory,r"bookclub-webapp\venv\Scripts\python.exe")
    print(python_exec_path)
    # Flask application entry point, adjust if your Flask app is started differently
    flask_app_path = os.path.join(main_directory,r"bookclub-webapp\bookclub.py")
    print(flask_app_path)
    # Use the Python executable to run the Flask app
    command = f"{python_exec_path} {flask_app_path}"
    print(command)
    subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    



def quit_app(icon):
    """Stop the icon."""
    icon.stop()

# Define the menu for the tray icon
menu = (item('Quit', quit_app),)
# Create an icon
icon = Icon('test_icon', create_image(), menu=menu)
icon.run_detached(start_flask)