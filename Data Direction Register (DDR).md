- crucial component in micro-controller architecture, particularly in AVR and ARM systems.
- used to configure the input/output direction of the pins on a micro-controller's port
## Functionality of Data Direction Register
1. **Input/Output Configuration**: The DDR determines whether each pin on a port operates as an **input** or an **output**. Each bit in the DDR corresponds to a specific pin; setting a bit to `1` configures the respective pin as an output, while setting it to `0` configures it as an input.
2. **Byte-Wide Register**: The DDR is typically an 8-bit register, allowing control over eight pins simultaneously. For example, in the ATmega328 microcontroller, the DDR for Port B is referred to as **DDRB**
3. **Bit Manipulation**: Users can manipulate individual bits of the DDR using bitwise operations. For instance, to set pin 2 of Port B as an output, you would execute:
```c
DDRB |= (1 << DDB2);
```
- this operation shifts `1` left by the number of bits specified by `DDB2` effectively setting that particular bit