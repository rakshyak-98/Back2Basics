static module -> built-in at compile time, cannot be disabled/enabled dynamically, always loaded in memory, even if unused, no dynamic linking at runtime.

shared module -> compiled separately, loaded at runtime via config `LoadModule`, can be enabled/disabled without recompiling, modular (reduces memory footprint).