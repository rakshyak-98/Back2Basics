- Media Presentation Description (MPD)


> [!NOTE]
> **Client-Side Adaptation** The video player in your browser/app (e.g., dash.js, Shaka Player, Bitmovin, Video.js with plugins) downloads the MPD first. Then it:
> - Monitors bandwidth, buffer level, CPU usage
> - Requests the most suitable segment from the next quality level
> - Switches seamlessly when conditions change (e.g., you move from Wi-Fi to mobile data)