#!/bin/bash
# Black Meridian Installation Script

echo "Installing Black Meridian..."

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Update desktop file with correct path
sed -i "s|/path/to/Black-Meridian-Logon-UI|$SCRIPT_DIR|g" "$SCRIPT_DIR/black_meridian.desktop"

# Install desktop entry
sudo cp "$SCRIPT_DIR/black_meridian.desktop" /usr/share/applications/black_meridian.desktop

# Make main.py executable
chmod +x "$SCRIPT_DIR/main.py"

echo "Installation complete!"
echo "You can now launch 'Black Meridian' from your application menu."
