- where your system absorbs the most load: storage versus compute.

## The Static file Approach

- In this model, the media file (e.g., `.mp3` `.mp4`) are entirely pre-processed, encoded, and saved to a storage system before the user ever hits "play".
- When a user requests the media, the server simply reads the file from the disk and sends it over the network.

**How it works in Practice** 
- You upload a raw video, a background worker processes it into various resolutions, and the final assests are stored in an object store (like AWS S3). A content delivery Network (CDN) sites in front of this storage to cache and server the files globally.

> [!INFO]
> CDNs are built exactly for this. Once a file is cached at an edge location, your backend infrastructure does zero work to server subsequent requests.
> - Low compute cost -> serving the file require almost no CPU power.