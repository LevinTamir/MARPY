# Wiring Guide

This guide covers all electrical connections for the MARPY robot. Make sure you've completed the [Assembly](assembly.md) first - all components should be physically mounted before wiring.

## Wiring Diagram

<img src="images/wiring_diagram.png" width="800" alt="MARPY Wiring Diagram"/>

## Full Schematic

<img src="images/marpy_schematic.png" width="800" alt="MARPY Schematic"/>

## Step 1: Power Distribution

1. **Battery Pack** (2S 18650, ~7.4V) connects through the on/off switch to:
   - L298N `+12V` input (powers the motors directly)
   - Buck converter input

2. **Buck Converter** (7.4V -> 5V) connects to:
   - ESP32 `VIN` pin (5V)
   - Encoder VCC lines (5V)

3. **Ground:** All GND connections must be **common** - ESP32 GND, L298N GND, buck converter GND, encoder GND all tied together.

> **Tip:** Set the buck converter output to **5V** using a multimeter before connecting the ESP32.

## Step 2: Motor Control Wiring (ESP32 to L298N)

| ESP32 GPIO | L298N Pin | Function |
|-----------|-----------|----------|
| GPIO 25 | ENA | Right motor speed (PWM) |
| GPIO 26 | IN1 | Right motor direction A |
| GPIO 27 | IN2 | Right motor direction B |
| GPIO 32 | IN3 | Left motor direction A |
| GPIO 33 | IN4 | Left motor direction B |
| GPIO 14 | ENB | Left motor speed (PWM) |

> **Important:** Remove the ENA and ENB jumpers on the L298N board. These pins must be driven by the ESP32 PWM, not tied to 5V.

## Step 3: Motor Wiring (L298N to Motors)

Each DC gear motor has 6 wires:

| Wire | Connection |
|------|-----------|
| Motor + (red) | L298N OUT1/OUT3 |
| Motor - (black) | L298N OUT2/OUT4 |
| Encoder VCC (red) | 5V |
| Encoder GND (black) | GND |
| Encoder A (yellow/green) | ESP32 GPIO (see table below) |
| Encoder B (white/blue) | ESP32 GPIO (see table below) |

> **Tip:** If a motor spins the wrong direction, swap its two motor wires (+ and -) at the L298N output. If an encoder counts in the wrong direction, swap its A and B channels.

## Step 4: Encoder Wiring

| ESP32 GPIO | Function |
|-----------|----------|
| GPIO 18 | Right encoder - Channel A |
| GPIO 19 | Right encoder - Channel B |
| GPIO 21 | Left encoder - Channel A |
| GPIO 22 | Left encoder - Channel B |

Each encoder also needs **5V** and **GND** from the buck converter output.

## Pre-Flight Checklist

Before powering on, verify:

- [ ] L298N ENA/ENB jumpers **removed**
- [ ] All grounds connected together
- [ ] Buck converter output reads ~5V with a multimeter
- [ ] ESP32 powers on when battery is connected
- [ ] Motors are free to spin (wheels off the ground for first test)

## Next Step

With all wiring complete, proceed to the [Firmware Setup](firmware-setup.md) to flash micro-ROS onto the ESP32.
