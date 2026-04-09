# Firmware Setup (ESP32)

This guide walks you through flashing the micro-ROS firmware onto the ESP32.

## What is PlatformIO?

[PlatformIO](https://platformio.org/) is a development platform for embedded systems. Think of it as a smarter replacement for the Arduino IDE - it handles board definitions, libraries, and build toolchains automatically. We use it to compile the micro-ROS firmware and flash it onto the ESP32.

The easiest way to use it is through the **VS Code extension**:

1. Open VS Code
2. Go to the Extensions tab (Ctrl+Shift+X)
3. Search for **"PlatformIO IDE"** and install it
4. Wait for it to finish setting up (it downloads toolchains in the background, this can take a few minutes the first time)
5. You'll see a new PlatformIO icon (alien head) in the left sidebar when it's ready

## Prerequisites

- [PlatformIO IDE](https://platformio.org/install/ide?install=vscode) extension in VS Code
- USB cable connected to the ESP32
- Your WiFi network name and password

## 1. Clone the Firmware

```bash
git clone https://github.com/LevinTamir/marpy_firmware.git
cd marpy_firmware
```

## 2. Configure WiFi and Agent IP

Create your private config file from the template:

```bash
cp include/wifi_config.h.example include/wifi_config.h
```

Edit `include/wifi_config.h` with your network details:

```cpp
static char WIFI_SSID[] = "YOUR_WIFI_SSID";        // your Wi-Fi network name
static char WIFI_PSK[]  = "YOUR_WIFI_PASSWORD";     // your Wi-Fi password
IPAddress AGENT_IP(192, 168, 1, 100);               // your PC's IP address
uint16_t AGENT_PORT = 8888;                         // micro-ROS agent port
```

### Finding your network details

**WiFi SSID** - the name of the network your PC is connected to:
```bash
nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2
```

**PC IP address** - this is what the ESP32 will connect to:
```bash
hostname -I | awk '{print $1}'
```

You can also find both from the network settings GUI: Settings > Wi-Fi > click the gear icon on your connected network. The IPv4 address is your `AGENT_IP`.

**WiFi password** - if you forgot it, you can retrieve the saved password:
```bash
nmcli -s -g 802-11-wireless-security.psk connection show "YOUR_SSID"
```

**Quick check** - verify everything in one command:
```bash
echo "SSID: $(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2)"
echo "IP:   $(hostname -I | awk '{print $1}')"
```

> **Important:** The ESP32 and your PC must be on the **same WiFi network** (2.4 GHz). The ESP32 does not support 5 GHz networks.
>
> `wifi_config.h` is git-ignored - your credentials never get pushed to GitHub.

## 3. Build and Flash

### Using VS Code (recommended)

1. Open the `marpy_firmware` folder in VS Code (`File > Open Folder`)
2. PlatformIO will detect the `platformio.ini` file and configure the project automatically
3. Connect the ESP32 via USB
4. Click the **Upload** button (right arrow icon ➜) in the bottom status bar

   You can also find it in the PlatformIO sidebar: `PROJECT TASKS > esp32dev > Upload`

5. Wait for it to compile and flash. You'll see `SUCCESS` in the terminal when done

### Using the CLI

If you prefer the terminal:
```bash
pio run --target upload
```

## 4. Monitor Serial Output

```bash
pio device monitor -b 115200
```

You should see:
```
WiFi connected
Waiting for micro-ROS agent...
micro-ROS agent connected!
```

If it stays on "Waiting for micro-ROS agent..." - make sure the agent is running on your PC (see [ROS2 Setup](ros2-setup.md)).

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Upload fails | Hold the **BOOT** button on ESP32 while uploading |
| WiFi won't connect | Double-check SSID/password in `include/wifi_config.h`, ensure 2.4GHz network (ESP32 doesn't support 5GHz) |
| Agent not found | Verify PC IP address, check firewall (`sudo ufw allow 8888/udp`) |
| Motors don't spin | Check wiring, verify L298N ENA/ENB jumpers are **removed** |
