# Assembly Instructions

Step-by-step guide to physically build your MARPY robot. Once assembled, continue to the [Wiring Guide](wiring.md) to connect everything electrically.

## What You'll Need

- All parts from the [Bill of Materials](bom.md)
- 3D printed parts (Download the STLs from [MakerWorld](https://makerworld.com/en/models/2655868-marpy#profileId-2936800))
- Basic tools: screwdriver, hex key (Allen wrench)

<img src="images/marpy_parts.jpeg" height="350" alt="All parts laid out"/>

## Step 1: Attach Motors to Motor Mounts

| Hardware | Qty |
|----------|-----|
| Motor mounts (3D printed) | 2 |
| M3x24 screws | 4 |
| M3 nuts | 4 |

1. Slide each DC motor into its 3D-printed motor mount bracket.
2. Secure each motor with 2 screws and nuts.

<p>
<img src="images/motor_mounts_assembly1.jpeg" height="250" alt="Motor mount parts"/>
<img src="images/motor_mounts_assembly3.jpeg" height="250" alt="Motor secured in mount"/>
<img src="images/motor_mounts_assembly2.jpeg" height="250" alt="Both motors with mounts"/>
</p>

## Step 2: Assemble the On/Off Switch

| Hardware | Qty |
|----------|-----|
| On/off switch | 1 |
| Switch mount (3D printed) | 1 |

1. Press-fit the on/off switch into the 3D-printed switch mount.

<img src="images/on_off_switch_assembly.jpeg" height="250" alt="On/off switch in mount"/>

## Step 3: Assemble the Caster Wheel

| Hardware | Qty |
|----------|-----|
| Caster wheel | 1 |
| M3x12 standoffs (female-male) | 4 |
| M3 shims | 4 |
| M3 nuts | 4 |

1. Attach the caster wheel to its mounting plate using screws and nuts.
2. Screw the standoffs into the caster plate, these will later connect to the base plate.

<p>
<img src="images/caster_wheel_aseembly1.jpeg" height="250" alt="Caster wheel assembled"/>
<img src="images/caster_wheel_aseembly2.jpeg" height="250" alt="Caster wheel with standoffs"/>
</p>

## Step 4: Assemble the Lower Chassis

<img src="images/lower_chassis_parts.jpeg" height="350" alt="Lower chassis parts laid out"/>

### Step 4.1: Mount Motors to Base Plate

| Hardware | Qty |
|----------|-----|
| M3x20 screws | 2 |
| M3x16 screws | 2 |
| M3 nuts | 2 |

1. Slide the motor mount brackets into the base plate slots from the bottom.
2. Secure each motor mount with the M3x16 screws and nuts.
3. Insert the M3x20 screws facing **upwards** through the base plate - no nuts needed, these will thread into the standoffs later.

<p>
<img src="images/motors_to_bottom_assembly1.jpeg" height="250" alt="Motor mounted to base plate"/>
<img src="images/motors_to_bottom_assembly2.jpeg" height="250" alt="Both motors mounted"/>
</p>

### Step 4.2: Attach Caster and Switch to Base Plate

| Hardware | Qty |
|----------|-----|
| M3x12 screws | 4 |

1. Screw the caster assembly and on/off switch to the base plate using the M3x12 screws.

<p>
<img src="images/lower_chassis_assembly_bottom_view.jpeg" height="250" alt="Lower chassis bottom view"/>
<img src="images/lower_chassis_assembly_upper_view.jpeg" height="250" alt="Lower chassis top view"/>
</p>

## Step 5: Mount the Electronics

| Hardware | Qty |
|----------|-----|
| L298N motor driver | 1 |
| Battery holder (2S 18650) | 1 |
| Buck converter | 1 |
| M3x8 screws | 8 |
| M3x6 flat head screws (optional) | 2 |

Mount the electronic components onto the base plate. Wiring is covered in the [Wiring Guide](wiring.md) later.

1. Mount the **L298N motor driver** and **LM2596S buck converter** to the base plate using M3x8 screws. Match the orientation shown in the photos.
2. Attach the **battery holder** using M3x6 flat head screws (glue/double-sided tape is also possible)

<p>
<img src="images/lower_chassis_electric_components.jpeg" height="250" alt="Electronics components before mounting"/>
<img src="images/lower_chassis_electric_assembled.jpeg" height="250" alt="Electronics mounted on base plate"/>
</p>

## Step 6: Attach the Wheels

| Hardware | Qty |
|----------|-----|
| TT motor wheels | 2 |

1. Press the yellow TT wheels onto the motor shafts.

<p>
<img src="images/wheels_assembly1.jpeg" height="250" alt="Wheels attached top view"/>
<img src="images/wheels_assembly2.jpeg" height="250" alt="Wheels attached side view"/>
</p>

## Step 7: Install Standoffs and Top Deck

| Hardware | Qty |
|----------|-----|
| Top plate (3D printed) | 1 |
| M3x40 standoffs | 4 |
| M3x16 screws | 2 |

1. Screw the 4 standoff posts into the base plate corners.
2. Place the top deck on the standoffs and secure with M3 screws.

<p>
<img src="images/standoffs_assembly1.jpeg" height="250" alt="Standoffs and screws"/>
<img src="images/standoffs_assembly2.jpeg" height="250" alt="Standoffs installed"/>
</p>

## Step 8: Mount the ESP32

| Hardware | Qty |
|----------|-----|
| ESP32 DevKit V1 | 1 |
| Pin headers / breadboard | 1 |

1. Mount the ESP32 DevKit on the top deck using pin headers or a breadboard for easy access.
2. Keep the USB port accessible for flashing and debugging.

## Done!

Your MARPY robot is now physically assembled. Next steps:

1. **[Wiring Guide](wiring.md)** - Connect all the electrical components
2. **[Firmware Setup](firmware-setup.md)** - Flash micro-ROS onto the ESP32
3. **[ROS2 Setup](ros2-setup.md)** - Start driving!
