# 🛠️ DMX Diagnostic Tool (Serial / Art-Net / sACN)

This tool is a desktop GUI application for testing and debugging DMX output across **USB Serial**, **Art-Net**, and **sACN (E1.31)** protocols. It allows you to control all 512 DMX channels using sliders and visualize output in real-time with logging.

---

## 🔧 Features

- ✅ 512 DMX sliders with real-time value updates
- ✅ Output via:
  - **USB Serial** (DMX over FTDI adapters, Teensy, etc.)
  - **Art-Net** (UDP broadcast or unicast to a node)
  - **sACN (E1.31)** (multicast streaming or optional unicast)
- ✅ Fixed-width, scrollable GUI optimized for quick hands-on testing
- ✅ Live logging of DMX output (first 16 channels previewed per frame)
- ✅ Protocol-specific fields auto-show/hide
- ✅ 30 FPS DMX transmission (adjustable in code)

---

## 📦 Installation

### 🔁 Dependencies

Install Python 3.8+ and the following packages:

```bash
pip install pyserial

sACN and Art-Net use only standard Python libraries (socket, struct)

🚀 How to Run
python dmx_tester.py

🖥️ GUI Overview
Section	Description
Protocol Dropdown	Choose Serial, Art-Net, or sACN
COM Port / IP Fields	Auto-filled or user-input depending on protocol
Universe Selector	For Art-Net and sACN (0–255 supported)
512 Channel Sliders	Drag to control each DMX value
Live Console	Displays outgoing DMX values (1–16) every second

🧪 Common Use Cases
🔌 1. Verifying USB-to-DMX Adapters
Use the Serial option:

Select COM port for your FTDI/RS485 device

Adjust sliders

Confirm fixture responds or observe DMX LED

🌐 2. Testing Art-Net Nodes
Use the Art-Net option:

Enter node IP address

Set correct universe

Confirm light responds

Useful for:

LED controllers

Media servers

GrandMA/Onyx/Resolume previsualization

🛰️ 3. Validating sACN Fixtures (E1.31)
Use the sACN option:

Enter universe

Multicast to 239.255.0.X automatically

For architectural lighting and theatrical installs

Works with:

Pathway nodes

ETC/Obsidian/ColorSource gear

LED pixel controllers

🧠 Pro Tips
You don’t need to enter an IP for sACN — it auto-sends to the correct multicast address

If your fixture isn’t responding:

Double check universe

Verify DMX mode and start address

Use the console window to confirm values being sent

If using Serial, ensure no other app (like Unity or QLC+) is holding the COM port

🚨 Known Limitations
Only supports 1 universe at a time

No ArtPoll/ArtSync (advanced Art-Net commands)

sACN is sender-only (no receiver/debug listener yet)

🧰 Built With
Python 3

Tkinter (GUI)

pyserial (USB COM)

socket + struct (for Art-Net and sACN)

💡 Created For
This tool was designed to support:

Lighting professionals testing installs on-site

Developers debugging DMX output

Engineers integrating microcontrollers with DMX fixtures

Artists prototyping interactive DMX behaviors
```
