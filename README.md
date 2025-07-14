# DMX Tester Program

The DMX Tester program is a Python application that allows users to test DMX lighting controls. It provides a user-friendly interface for controlling DMX output through various protocols such as Serial, Art-Net, and sACN.

## Features

- Supports sending DMX signals over Serial, Art-Net, and sACN protocols
- Adjustable sliders for setting DMX channel values (1-512)
- Real-time log of DMX stream status
- Auto-detects COM ports and prefers COM5 if available

## How to Use

1. **Connect your USB DMX dongle** to your computer
2. **Select "Serial"** protocol from the drop-down menu
3. **Choose the correct COM port** (COM5 or whatever port your dongle uses)
4. **Click "Connect"** to establish the connection
5. **Use the sliders** to set values for each DMX channel (1-512)
6. **Monitor the log box** for connection status and DMX stream information

## Installation Instructions

### Windows

1. Install Python: Download and install Python from the official [Python website](https://www.python.org/).
2. Install required libraries: Open Command Prompt and run the following commands:
   ```
   pip install tk
   pip install pyserial
   ```
3. Download the DMX Tester program code.
4. Run the program by executing the `main.py` script.

### macOS

1. Install Homebrew: Open Terminal and run the following command to install Homebrew:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python and required libraries: Run the following commands in Terminal:
   ```
   brew install python-tk
   pip install pyserial
   ```
3. Download the DMX Tester program code.
4. Run the program by executing the `main.py` script.

### Linux

1. Install Python and Tkinter:
   - Ubuntu/Debian: `sudo apt-get install python3-tk`
   - CentOS/RHEL: `sudo yum install python3-tkinter`
2. Install required libraries: Open terminal and run the following command:
   ```
   pip install pyserial
   ```
3. Download the DMX Tester program code.
4. Run the program by executing the `main.py` script.

## Troubleshooting

### Connection Issues
- Make sure your USB DMX dongle is properly connected
- Check Device Manager to confirm the COM port assignment
- Ensure no other DMX software is running simultaneously
- Try selecting a different COM port if available

## Credits

This DMX Tester program was created by Kaiman Walker.
