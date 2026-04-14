# Bill of Materials (BOM)

Everything you need to build your own MARPY robot. Total cost is approximately **$40-55 USD** depending on what you already have.

## Electronics

| # | Component | Qty | Est. Price | Link |
|---|-----------|-----|-----------|------|
| 1 | ESP32 DevKit V1 (30-pin) with Screw Terminal Breakout Board | 1 | ~$10 | [Amazon](https://www.amazon.com/dp/B0BNQ8VQDX) |
| 2 | L298N Dual H-Bridge Motor Driver | 1 | ~$3 | [Amazon](https://a.co/d/04wIWBpv) |
| 3 | TT Encoder Motor (6V DC Gear Motor with Hall Encoder) | 2 | ~$12 | [Amazon](https://www.amazon.com/dp/B0GS97898M) |
| 4 | 65mm TT Motor Wheels | 2 | ~$3 | [Amazon](https://www.amazon.com/dp/B0CG1C7T8J) |
| 5 | Low Profile Plastic Caster Wheel (1") | 1 | ~$3 | [Amazon](https://a.co/d/03JeFDlU) |
| 6 | 18650 Li-Ion Battery (3.7V, 2600mAh+) | 2 | ~$5 | [Amazon](https://www.amazon.com/dp/B0FP2DPJK7) |
| 7 | 2S 18650 Battery Holder with Switch | 1 | ~$3 | [Amazon](https://www.amazon.com/dp/B09ZPCX9VD) |
| 8 | LM2596S Adjustable DC-DC Buck Converter (7-28V to 5V) | 1 | ~$2 | [Amazon](https://a.co/d/05IxwOWH) |
| 9 | MPU6050 IMU (6-axis accelerometer + gyroscope) | 1 | ~$2 | [Amazon](https://www.amazon.com/dp/B00LP25V1A) |
| 10 | Jumper Wires | 1 kit | ~$3 | [Amazon](https://www.amazon.com/dp/B077NH83CJ) |
| 11 | Micro-USB Cable (for flashing ESP32) | 1 | ~$2 | [Amazon](https://www.amazon.com/dp/B013G4EAEI) |
| (optional) | ESP32-CAM with OV2640 Camera | 1 | ~$9 | [AliExpress](https://www.aliexpress.com/item/1005006341099716.html) |

## Hardware / Fasteners

| # | Component | Qty | Est. Price | Link |
|---|-----------|-----|-----------|------|
| 13 | M3x24 screws | 4 | ~$2 | See note below |
| 14 | M3x20 screws | 2 | ~$1 | See note below |
| 15 | M3x16 screws | 2 | ~$1 | See note below |
| 16 | M3x12 screws | 8 | ~$1 | See note below |
| 17 | M3x8 screws | 14 | ~$1 | See note below |
| 18 | M3x6 flat head screws | 2 | ~$1 | See note below |
| 19 | M3 nuts | 10 | ~$1 | See note below |
| 20 | M3 shims | 4 | ~$1 | See note below |
| 21 | M3x12 standoffs (female-male) | 4 | ~$2 | See note below |
| 22 | M3x40 standoffs (female-female) | 4 | ~$2 | [Amazon](https://a.co/d/03zlcVNa) |

> **Note:** Instead of buying each screw size individually, consider getting an **M3 hardware kit** that includes screws, nuts, standoffs, and washers in various sizes.

## 3D Printed Parts

| # | Part | File | Qty | Material |
|---|------|------|-----|----------|
| 23 | Base Plate (bottom deck) | `Marpy_base_plate.STL` | 1 | PLA/PETG |
| 24 | Top Plate (electronics deck) | `Marpy_top_plate.STL` | 1 | PLA/PETG |
| 25 | Left Motor Mount | `Marpy_left_TT_motor_mount.STL` | 1 | PLA/PETG |
| 26 | Right Motor Mount | `Marpy_right_TT_motor_mount.STL` | 1 | PLA/PETG |
| 27 | On/Off Switch Mount | `Marpy_on_off_switch_mount.STL` | 1 | PLA/PETG |
| 28 | Camera Mount | `Marpy_cam_mount.STL` | 1 | PLA/PETG |
| 29 | ESP32-CAM Case | `ESP32_cam_case.stl` | 1 | PLA/PETG |
| 30 *(optional)* | ESP32-CAM Case (GoPro mount) | [Printables](https://www.printables.com/model/837615-esp32-cam-case-with-gopro-mount) | 1 | PLA/PETG |

> **Note:** STL files for all printed parts are available on [MakerWorld](https://makerworld.com/en/models/2655868-marpy#profileId-2936800). The optional [ESP32-CAM GoPro case](https://www.printables.com/model/837615-esp32-cam-case-with-gopro-mount) can be used with the camera mount adapter included in the MakerWorld files. Print at 0.2mm layer height, 20%+ infill. PLA works fine for indoor use.
