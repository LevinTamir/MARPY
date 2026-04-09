# Wiring Guide

This guide covers all electrical connections for the MARPY robot.

## Wiring Diagram

<img src="images/wiring_diagram.png" width="800" alt="MARPY Wiring Diagram"/>

## Full Schematic

<img src="images/marpy_schematic.png" width="800" alt="MARPY Schematic"/>

## ESP32 to L298N - Motor Control

| ESP32 GPIO | L298N Pin | Function |
|-----------|-----------|----------|
| GPIO 25 | ENA | Right motor speed (PWM) |
| GPIO 26 | IN1 | Right motor direction A |
| GPIO 27 | IN2 | Right motor direction B |
| GPIO 32 | IN3 | Left motor direction A |
| GPIO 33 | IN4 | Left motor direction B |
| GPIO 14 | ENB | Left motor speed (PWM) |

> **Important:** Remove the ENA and ENB jumpers on the L298N board. These pins must be driven by the ESP32 PWM, not tied to 5V.

## Encoder Connections

| ESP32 GPIO | Function |
|-----------|----------|
| GPIO 18 | Right encoder - Channel A |
| GPIO 19 | Right encoder - Channel B |
| GPIO 21 | Left encoder - Channel A |
| GPIO 22 | Left encoder - Channel B |

Each encoder also needs **5V** and **GND** from the ESP32 (or buck converter output).

## Power Distribution

1. **Battery Pack** (2S 18650, ~7.4V) connects to:
   - L298N `+12V` input (powers the motors directly)
   - Buck converter input

2. **Buck Converter** (7.4V → 5V) connects to:
   - ESP32 `VIN` pin (5V)
   - Encoder VCC lines (5V)

3. **Ground:** All GND connections must be **common** - ESP32 GND, L298N GND, buck converter GND, encoder GND all tied together.

## Motor Wiring

Each DC gear motor has 6 wires:

| Wire | Connection |
|------|-----------|
| Motor + (red) | L298N OUT1/OUT3 |
| Motor - (black) | L298N OUT2/OUT4 |
| Encoder VCC (red) | 5V |
| Encoder GND (black) | GND |
| Encoder A (yellow/green) | ESP32 GPIO (see table above) |
| Encoder B (white/blue) | ESP32 GPIO (see table above) |

> **Tip:** If a motor spins the wrong direction, swap its two motor wires (+ and -) at the L298N output. If an encoder counts in the wrong direction, swap its A and B channels.

## Pre-Flight Checklist

- [ ] L298N ENA/ENB jumpers **removed**
- [ ] All grounds connected together
- [ ] Buck converter output reads ~5V with a multimeter
- [ ] ESP32 powers on when battery is connected
- [ ] Motors are free to spin (wheels off the ground for first test)
