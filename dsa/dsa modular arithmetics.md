- modular arithmetic is often called "Clock Arithmetic". Think of a clock: if it 10:00 and you add 5 hours, it becomes 3:00, not 15:00. This is because a clock works in Modulo 12.

- The cycle -> imagine a circle with 5 points (0, 1, 2, 3, 4) if you take 17 steps around that circle, you land on 2.
	- in DSA we use this to keep numbers within a certain range (like hash tables) or to check for patterns without dealing with massive integers.

> [!INFO]
> Every number greater than 1 is either a prime or can be made by multiplying primes together (e.g., 12 = 2 x 2 x 3).

## Euclid's Algorithm 

- Instead of subtracting 18 from 28 repeatedly (which is slow), the modulo operator `%` jumps to the reminder, performing multiple "subtractions" in one step.

> [!NOTE]
> Forgetting that `GCD(0, 0)` is mathematically undefined. Most implementations return 0 or throw an error, but failing to check for "Division of Zero" during the modulo step can crash a program.


> [!WARNING]
> GCD is an integer theory concept; passing `4.5` will lead to infinite loops or logic errors.