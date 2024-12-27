# Slamtec LIDAR TouchDesigner Integration

A TouchDesigner extension for integrating Slamtec LIDAR A1/A2 devices, providing real-time point cloud data visualization and OSC data streaming capabilities.

## Features

- Real-time LIDAR data acquisition via serial port
- OSC data streaming to any compatible software
- Coordinate system conversion (Polar/Cartesian)
- Automatic Python environment management
- Integrated process control (Start/Stop)
- Configurable connection parameters:
  - COM port selection
  - OSC server IP and port
- Graceful process handling and cleanup
- Automatic Python executable detection

## Requirements

### Hardware
- Slamtec LIDAR device (tested with RPLidar A1)
- USB to Serial connection
- Windows-compatible system

### Software
- TouchDesigner (tested with 2023.11760)
- Python 3.x
- Required Python packages (automatically installed):
  - rplidar-roboticia
  - python-osc
  - pyserial

## Installation

1. Clone this repository into your TouchDesigner project folder:
   ```
   git clone [repository-url]
   ```

2. In TouchDesigner:
   - Create a new container COMP
   - Drag and drop the `Slamtec_lidar.tox` into your project
   - Set the Base Folder parameter to point to your installation directory

3. First-time setup:
   - Click the "Install Dependencies" button to create a Python virtual environment and install required packages
   - Wait for the installation to complete (a command prompt window will show the progress)

4. Configure your device:
   - Set the COM port number in the LIDAR COM Port parameter
   - Configure OSC server IP and port if needed (defaults to 127.0.0.1:7000)

5. Start using:
   - Click "Start" to begin LIDAR data acquisition
   - LIDAR data will be streamed via OSC messages
   - Use "Stop" to gracefully terminate the process

## OSC Message Format

Data is streamed using the following OSC message format:
```
/lidar/data [new_scan, quality, angle, distance]
```
- new_scan: boolean (true/false)
- quality: integer (0-255)
- angle: float (degrees)
- distance: float (millimeters)

## TODO

### Planned Features and Improvements
- Create a direct C++/Python binding using RPLidar SDK for:
  - Broader device compatibility
  - Enhanced performance
  - Access to advanced features
  - Support for more LIDAR models
  - Lower-level device control
  - Better error handling and diagnostics