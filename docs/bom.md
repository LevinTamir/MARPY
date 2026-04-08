# Bill of Materials (BOM)

Everything you need to build your own MERPY robot. Total cost is approximately **$40-55 USD** depending on what you already have.

## Electronics

| # | Component | Qty | Est. Price | Link |
|---|-----------|-----|-----------|------|
| 1 | ESP32 DevKit V1 (30-pin) | 1 | ~$7 | [Amazon](https://www.amazon.com/dp/B08D5ZD528) |
| 2 | L298N Dual H-Bridge Motor Driver | 1 | ~$3 | [Amazon](https://www.amazon.com/dp/B07BK1QL5T) |
| 3 | DC Gear Motor with Encoder (6V, 11 PPR, 48:1 gear ratio) | 2 | ~$12 | [Amazon](https://www.amazon.com/dp/B07Y2SVNCT) |
| 4 | 65mm Yellow TT Motor Wheels | 2 | ~$3 | [Amazon](https://www.amazon.com/dp/B07VQ2N1F3) |
| 5 | Caster Wheel (0.75" - 1" ball or swivel) | 1 | ~$3 | [Amazon](https://www.amazon.com/dp/B06Y49V4TJ) |
| 6 | 18650 Li-Ion Battery (3.7V, 2600mAh+) | 2 | ~$5 | [Amazon](https://www.amazon.com/dp/B0B7N1K2CC) |
| 7 | 2S 18650 Battery Holder with Switch | 1 | ~$3 | [Amazon](https://www.amazon.com/dp/B09MDV4Y2S) |
| 8 | Mini Buck Converter (7-28V to 5V, 3A) | 1 | ~$2 | [Amazon](https://www.amazon.com/dp/B01MQGMOKI) |
| 9 | Jumper Wires (M-F and M-M assorted) | 1 kit | ~$3 | [Amazon](https://www.amazon.com/dp/B077NH83CJ) |
| 10 | Micro-USB Cable (for flashing ESP32) | 1 | ~$2 | [Amazon](https://www.amazon.com/dp/B013G4EAEI) |

## Hardware / Fasteners

| # | Component | Qty | Est. Price | Link |
|---|-----------|-----|-----------|------|
| 11 | M3 x 10mm Screws + Nuts | ~12 | ~$3 | [Amazon](https://www.amazon.com/dp/B014OO5KQG) |
| 12 | M3 Standoffs (30-40mm, for deck spacing) | 4 | ~$3 | [Amazon](https://www.amazon.com/dp/B07B9X1KY6) |

## 3D Printed Parts

| # | Part | Qty | Material | Notes |
|---|------|-----|----------|-------|
| 13 | Bottom Deck (chassis plate) | 1 | PLA/PETG | Motor mounts integrated |
| 14 | Top Deck (electronics plate) | 1 | PLA/PETG | ESP32 + accessory mounting |
| 15 | Caster Wheel Mount | 1 | PLA/PETG | Rear caster bracket |
| 16 | Motor Clamps (optional) | 2 | PLA/PETG | If not using integrated mounts |

> **Note:** STL files for all printed parts are in the [`CAD/`](../CAD/) folder. Print at 0.2mm layer height, 20%+ infill. PLA works fine for indoor use.

## Tools Needed (not included in BOM)

- 3D Printer (or use a printing service)
- Soldering iron + solder (for motor/encoder wires)
- Small Phillips screwdriver
- Wire strippers
- Computer running Ubuntu 24.04 with WiFi

## Power Notes

- The 2S 18650 pack provides ~7.4V which feeds the L298N motor input directly
- The buck converter steps 7.4V down to 5V for the ESP32
- Expected runtime: **2-3 hours** of intermittent driving on 2600mAh cells
