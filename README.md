# DMX Tester Program

The DMX Tester program is a Python application that allows users to test DMX lighting controls. It provides a user-friendly interface for controlling DMX output through various protocols such as Serial, Art-Net, and sACN.

## Features

- Supports sending DMX signals over Serial, Art-Net, and sACN protocols.
- Adjustable sliders for setting DMX channel values.
- Real-time log of DMX stream status.

## How to Use

1. Select the desired output protocol (Serial, Art-Net, sACN) from the drop-down menu.
2. Based on the selected protocol, provide the necessary configuration details such as the COM port for Serial, Node IP for Art-Net, or Universe for sACN.
3. Adjust the sliders to set the values for each DMX channel (1-512).
4. Click the "Connect" button to establish the connection and start sending DMX signals.
5. The log box displays the current DMX stream status, including any errors.

## Installation Instructions

### Windows

1. Install Python: Download and install Python from the official [Python website](https://www.python.org/).
2. Install required libraries: Open Command Prompt and run the following commands:
   ```
   pip install tk
   pip install pyserial
   ```
3. Download the DMX Tester program code.
4. Run the program by executing the `DMX_Tester.py` script.

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
4. Run the program by executing the `DMX_Tester.py` script.

### Linux

1. Install Python and Tkinter:
   - Ubuntu/Debian: `sudo apt-get install python3-tk`
   - CentOS/RHEL: `sudo yum install python3-tkinter`
2. Install required libraries: Open terminal and run the following command:
   ```
   pip install pyserial
   ```
3. Download the DMX Tester program code.
4. Run the program by executing the `DMX_Tester.py` script.

## Credits

This DMX Tester program was created by Kaiman Walker.
