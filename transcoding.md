[[ffmpeg]]

**Transcoding** is the direct digital-to-digital conversion of one media file format (audio or video) into another.

At its core, it is the process of taking an existing media file, decoding it to an uncompressed state, and then re-encoding it into a new format, size, or quality.

### How It Works

The transcoding process typically involves a two-step pipeline:

1. **Decoding:** The original compressed file (e.g., an MKV video file) is unpacked and converted into an uncompressed format.
    
2. **Encoding:** That uncompressed data is then compressed again into the target format (e.g., an MP4 file) using a specific codec.
    

### Why It Is Used

Transcoding is essential for modern digital media delivery for several reasons:

- **Device Compatibility:** Not all devices support the same media formats. Transcoding ensures that a video recorded on a specialized camera can be played on a standard smartphone or web browser.
    
- **Adaptive Bitrate Streaming:** Streaming platforms like YouTube and Netflix use transcoding to create multiple versions of the same video at different resolutions (e.g., 4K, 1080p, 720p, 480p). The platform then dynamically delivers the best version based on the user's internet speed.
    
- **File Size Reduction:** High-quality raw video files are enormous. Transcoding allows these files to be compressed into smaller, more manageable sizes for storage or internet transmission without an unacceptable loss in quality.
    
- **Editing Workflows:** Video editors often transcode highly compressed footage from consumer cameras into "mezzanine" or intermediate formats (like Apple ProRes) that are easier for editing software to process smoothly.