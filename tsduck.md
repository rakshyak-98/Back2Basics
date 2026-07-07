[[MPTS]] [[SPTS]] [[PAT/PMT]] [[PSI Table]] [[demux]]

```bash
tsp -I ip <multicast_ip>:<port> \
    -P zap <service_id> \
    -O ip <output_ip>:<output_port>
```

`service_id` -> identifies which service (channel) within the MPTS to extract.
What it is -> The numeric service ID from the PAT/PMT of the source MPTS, unique per service within that transport stream.

`zap` -> is a TSDuck plugin that extracts a single service from a transport stream and rebuilds valid PAT/PMT for it, producing a proper SPTS

### PAT (Program Association Table)

PSI table listing all service in a transport stream, mapping each service_id to the PID of its corresponding PMT.

### PMT (Program Map Table)

PSI table for a single server, listening the PIDs for its components (video, audio, PCR, and other elementary streams).

> [!NOTE]
> Relevance to `zap`: When extracting one service into as SPTS, the original PAT (which lists all MPTS service) is invalid. `zap` regenerates a new PAT containing only the target service, and adjusts the PMT accordingly, so the output stream is self-consistent.

> [!INFO]
> An MPTS carries multiple TV channels (services) multiplexed together over one UDP/multicast stream. Each channel is identified by a service_id, with the PAT mapping service_ids to PMT PIDs, and each PMT listing that channel's video/audio/PCR PIDs.
- to distribute channels individually, this tool splits the MPTS into separate SPTS streams, one per channel:

```bash
tsp -I ip <mpts_ip>:<port> -P zap <service_id> -O ip <output_ip>:<output_port>

# `-I ip` joins the MPTS source. `zap` filters to the specified service_id's PIDs and rebuilds a clean PAT/PMT scoped to that one channel. `-O ip` sends the resulting SPTS to its own multicast address/port.
```

for multiple channels, one `tsp` process runs per service_id, each mapped to a distinct output port:

```bash

SRC="239.1.1.1:5000"
SERVICES=(101 102 103 104)
BASE_PORT=6001

for i in "${!SERVICES[@]}"; do
	PORT=$((BASE_PORT + i))
	tsp -I ip "$SRC" -P zap "${SERVICES[$i]}" -O ip "239.2.2.$((i + 2)):PORT" &
done
wait

```
Result: Each downstream receiver/decoder gets a single-channel stream (SPTS) on its own address/port, instead of having to demux the full MPTS itself