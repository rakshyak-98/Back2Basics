SMT -> Simultaneous Multi-threading. SMT is the technology that lets one physical CPU core run two (or more) threads at the same time. Intel calls it **Hyper-Threading (HT)**, AMD calls it SMT.

**How it actually works**
One physical core has these execution units
- ALU
- FPU (floating point)
- Load/Store units
- Branch predictor etc.
in normal single-threads use, many of these units sit idle every clock cycle waiting for the current thread.

**With SMT**
- Core pretends to be two logical cores (threads).
- When thread A is waiting for memory -> Thread B uses the ALU.
- When thread B stalls on a branch mispredict -> Thread A keeps going.