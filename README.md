# OctoPrint-Mglcd

An OctoPrint plugin for controlling a USB-serial LCD; currently configured for a Nextion NX4832K035_011 display.

## Compatibility

- **Python 3.x** - Fully compatible (migrated from Python 2)
- **OctoPrint** - Latest versions supported
- **Hardware** - Nextion NX4832K035_011 display via USB-serial

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/ouchinou/OctoPrint-Mglcd/archive/master.zip

### Requirements

- Python 3.x
- pyserial 3.5+
- OctoPrint
- Nextion display connected via USB-serial

### Features

- Real-time temperature monitoring (bed, tool0, tool1)
- Print progress display with time estimates
- File browser with folder navigation
- WiFi network configuration
- Manual printer controls (movement, homing, extrusion)
- Nextion firmware flashing capability
- System controls (restart, shutdown, reset)

## Technical Details

Uses the Pynextion Python library (https://github.com/raffmont/pynextion) and the Nextion firmware flasher from (https://github.com/g4klx/MMDVMHost/blob/master/Nextion_G4KLX/nextion.py).

### Recent Updates

- **Python 3 Migration**: Complete migration from Python 2 to Python 3
- **Code Quality**: Fixed Pylance warnings, improved exception handling
- **Nextion Protocol**: Corrected `picq` command format (x, y, w, h, picid)
- **Bug Fixes**: Removed duplicate methods, unused variables, and improved type safety
