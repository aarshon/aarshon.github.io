# Toward Hardware Design V 2.0 — targeted refinements for a stronger, safer, and more extensible HMI board

A full semester of bench time—and five public demo sessions—has revealed a handful of friction points that Version 1.0 masked. Below is a “wish‑list” for Version 2.0, grouped by schematic block. Taken together, these changes would streamline manufacturing, raise robustness for long‑term classroom deployment, and open headroom for the next round of features.

1. Power‑input & regulation

**What we learned:** the AP63203WU‑7 buck operates comfortably at 200 mA load, but the in‑rush spike from the OLED charge‑pump and Wi‑Fi TX bursts still nudges the 1 .5 A resettable fuse. Why improve: repeated fuse trips annoy teachers and worry students who think they “broke it.”

- Upgrade path:
    - Replace the polyfuse + buck pair with a pre‑regulated 5 V → 3 .3 V DC barrel supply and add a low‑IQ LDO locally for the OLED (isolates surge).

    - Integrate a load‑switch with soft‑start (e.g., TPS22918) on the 3 .3 V rail: slope‑limited turn‑on caps the in‑rush at ~80 mA, giving the upstream wall‑wart relaxed specs.

    - Move the large 100 µF electrolytic closer to the barrel jack (sheet: Power) to satisfy ripple spec before it splashes into the board.

2. Spare I/O and feature headroom

**What we learned:** teachers asked for a buzzer alert and students wanted a “next‑page” capacitive swipe. We currently have only two spare GPIOs broken out.

- Upgrade path:

    - Replace the one‑row debug header with a 12‑pin header exposing six strappable GPIOs plus 3 .3 V and GND. Costs peanuts, grants future sensor or haptic‑motor add‑ons.
    Pre‑route a PWM trace to a no‑load pad footprint. If unpopulated, adds zero BOM and negligible capacitance.

## Conclusion

None of these changes overhaul the architecture—they polish it. They convert the “good enough for a semester” V 1.0 board into a deploy‑and‑forget instructional tool that can survive many school years, accept new lesson modules, and stand up to the real‑world rough‑and‑tumble of science fairs. Version 2.0 would markedly raise reliability, maintainability, and pedagogical flexibility—turning a successful prototype into a product‑grade teaching asset. 