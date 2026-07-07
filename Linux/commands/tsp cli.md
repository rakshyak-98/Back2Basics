
> [!NOTE]
> `tsp` does not read MP4 containers directly. Its input plugins expect transport stream input (file, IP, DVb tuner, etc.) not arbitrary container format.

```bash

tsp -I ip <mpts_ip>:<port> -P analyze # Output report listing each service in the MPTS with its service_id
tsp -I ip <mpts_ip>:<port> -P svinfo

```


```bash

tstables <output.ts>;

```
- Output represents the core **Program Specific Information (PSI/SI)**  tables for a single-program transport stream, confirming the multiplex structure and content mapping.

```txt

* SDT Actual, TID 0x42 (66), PID 0x0011 (17)
  Version: 0, sections: 1, total size: 40 bytes
  - Section 0:
    Transport Stream Id: 0x0001 (1)
    Original Network Id: 0xFF01 (65281)
    Service Id: 0x0001 (1), EITs: no, EITp/f: no, CA mode: free
    Running status: running
    - Descriptor 0: Service (0x48, 72), 18 bytes
      Service type: 0x01 (Digital television service)
      Service: "Service01", Provider: "FFmpeg"

* PAT, TID 0x00 (0), PID 0x0000 (0)
  Version: 0, sections: 1, total size: 16 bytes
  - Section 0:
    TS id:       1 (0x0001)
    Program:     1 (0x0001)  PID: 4096 (0x1000)

* PMT, TID 0x02 (2), PID 0x1000 (4096)
  Version: 0, sections: 1, total size: 32 bytes
  - Section 0:
    Program: 0x0001 (1), PCR PID: 0x0100 (256)
    Elementary stream: type 0x1B (AVC video), PID: 0x0100 (256)
    Elementary stream: type 0x0F (MPEG-2 AAC Audio), PID: 0x0101 (257)
    - Descriptor 0: ISO-639 Language (0x0A, 10), 4 bytes
      Language: und, Type: 0x00 (undefined)

```
