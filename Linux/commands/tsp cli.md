
> [!NOTE]
> `tsp` does not read MP4 containers directly. Its input plugins expect transport stream input (file, IP, DVb tuner, etc.) not arbitrary container format.

```bash

tsp -I ip <mpts_ip>:<port> -P analyze # Output report listing each service in the MPTS with its service_id
tsp -I ip <mpts_ip>:<port> -P svinfo

```