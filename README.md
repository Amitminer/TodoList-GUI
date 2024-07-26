# Todolist-GUI Application

## Overview

This is a simple Todo List application built with Python using Tkinter for the graphical user interface and SQLite for data storage. The application allows users to add, view, mark as done, and remove tasks.

## Features

- Add new tasks.
- Mark tasks as done or not done.
- Remove tasks from the list.
- View tasks with details such as status and date.

## Requirements

- Python 3.7 or higher
- `tkinter` (included with Python)
- `aiodatabase` (for asynchronous database operations)

## Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/Amitminer/TodoList-GUI
    cd TodoList-GUI
    ```

2. **Install the Required Packages:**
    - Ensure you have Python installed and added to your system PATH.
    - Create a virtual environment (optional but recommended):
      ```sh
      python -m venv venv
      venv\Scripts\activate
      ```
    - Install the required packages:
      ```sh
      pip install -r requirements.txt
      ```

## Building the Executable

1. **Run the Build Script:**
    - On Windows, use the provided `build.bat` file to automate the build process:
      ```sh
      build.bat
      ```

   This script will:
   - Check if Python is installed.
   - Install required packages.
   - Build the executable using PyInstaller.
   - Inform you of the location of the built executable.

2. **Locate the Executable:**
    - After running the build script, the executable will be located in the `dist` directory:
      ```
      dist\main.exe
      ```

## Usage

1. **Run the Application:**
    - You can run the executable directly:
      ```sh
      dist\main.exe
      ```

2. **Usage Instructions:**
    - The application window will open. You can start adding tasks by typing in the input field and pressing "Add" or hitting Enter.

## Configuration

Configuration settings can be adjusted in the `config.py` file. This file contains settings such as the application title, window size, and colors.

## Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This application uses Tkinter for the GUI and `aiodatabase` for asynchronous database operations.

---