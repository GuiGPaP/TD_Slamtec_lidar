#!/usr/bin/env python3
'''
LIDAR data acquisition with CLI and OSC output
'''
from rplidar import RPLidar
import argparse
import time
from pythonosc import udp_client
import signal
import sys

class LidarController:
    def __init__(self, com_port, osc_ip, osc_port):
        self.com_port = com_port
        self.running = False
        self.lidar = None
        self.iterator = None
        
        # Initialize OSC client
        try:
            self.osc_client = udp_client.SimpleUDPClient(osc_ip, osc_port)
            print(f"OSC client initialized - sending to {osc_ip}:{osc_port}")
        except Exception as e:
            print(f"Error setting up OSC client: {e}")
            sys.exit(1)

    def start_scan(self):
        """Start LIDAR scanning"""
        try:
            print(f"Connecting to LIDAR on {self.com_port}...")
            self.lidar = RPLidar(self.com_port)
            self.iterator = self.lidar.iter_scans()
            self.running = True
            
            print("Starting LIDAR scan...")
            while self.running:
                try:
                    scan = next(self.iterator)
                    for meas in scan:
                        quality, angle, distance = meas
                        # Send all values in a single OSC message
                        self.osc_client.send_message("/lidar/data", [
                            True,           # new_scan
                            int(quality),   # quality
                            float(angle),   # angle
                            float(distance) # distance
                        ])
                except Exception as e:
                    print(f"Error during scan: {e}")
                    break

        except Exception as e:
            print(f"Error starting scan: {e}")
            self.stop_scan()
            sys.exit(1)

    def stop_scan(self):
        """Stop LIDAR scanning"""
        self.running = False
        if self.lidar:
            print("\nStopping LIDAR...")
            self.lidar.stop()
            self.lidar.disconnect()
            self.lidar = None
        print("LIDAR stopped")

def signal_handler(sig, frame):
    print("\nSignal received, stopping...")
    if hasattr(signal_handler, 'controller'):
        signal_handler.controller.stop_scan()
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='LIDAR data acquisition with OSC output')
    parser.add_argument('--osc_serverip', type=str, default='127.0.0.1',
                        help='OSC server IP address (default: 127.0.0.1)')
    parser.add_argument('--osc_serverport', type=int, default=8000,
                        help='OSC server port (default: 8000)')
    parser.add_argument('--com_port', type=str, required=True,
                        help='COM port for LIDAR connection (e.g., COM5)')

    args = parser.parse_args()

    # Create controller and store it in signal handler for cleanup
    controller = LidarController(args.com_port, args.osc_serverip, args.osc_serverport)
    signal_handler.controller = controller

    # Setup signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        controller.start_scan()
    except KeyboardInterrupt:
        controller.stop_scan()

if __name__ == '__main__':
    main()