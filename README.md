# Black Meridian Logon UI

A professional desktop login application built for Debian Linux using PyQt5. This application provides a secure and user-friendly interface for username/password authentication.

## Features

- Clean, modern login interface
- Username and password authentication
- Input validation
- Error handling and user feedback
- Cross-platform desktop compatibility (optimized for Linux)
- PyQt5 framework for robust GUI

## Requirements

- Python 3.8+
- PyQt5
- Debian Linux (or compatible)

## Installation

### 1. Install Python and Dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Install PyQt5

```bash
pip3 install PyQt5
```

### 3. Clone the Repository

```bash
git clone https://github.com/CipherCG/Black-Meridian-Logon-UI.git
cd Black-Meridian-Logon-UI
```

## Usage

Run the login application:

```bash
python3 main.py
```

## Project Structure

```
Black-Meridian-Logon-UI/
├── main.py              # Entry point
├── login_ui.py          # Login window UI
├── auth.py              # Authentication logic
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── assets/              # Images and resources
│   └── logo.png
└── README.md
```

## Configuration

Edit `config.py` to customize:
- Application title and styling
- Window dimensions
- Color scheme
- Authentication settings

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

CipherCG