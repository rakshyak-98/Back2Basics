```bash

ffprobe -show_streams input.mp4; # Show stream information

```

```txt
Stream #0:0 Video: h264
    start_time=0.000000

Stream #0:1 Audio: aac
    start_time=0.000000
```

pts_time -> (Presentation Timestamp Time) is the time (in seconds) at which a frame (video) re-sample (audio) should be presented (played) to the user.

### Output formats

| Format  | Option        | Best For                  |
| ------- | ------------- | ------------------------- |
| Default | _(none)_      | Human-readable            |
| JSON    | `-of json`    | APIs, scripts             |
| XML     | `-of xml`     | XML tools                 |
| CSV     | `-of csv`     | Excel, spreadsheets       |
| Compact | `-of compact` | Terminal                  |
| Flat    | `-of flat`    | Shell scripting           |
| INI     | `-of ini`     | Configuration-like output |

```bash

ffprobe \
-show_frames \
-select_streams v \
-of json \
input.mp4

```
