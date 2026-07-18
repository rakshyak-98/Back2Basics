Even if you load the manifest via:
`http://localhost:3000/flussonic/STREAM/index.mpd` the manifest content itself can contain absolute URLs .e.g.,
- IN MPD: `<Location>http://127.0.0.1/...` or `http://FLUSSONIC_ORIGIN/...`
- In HLS playlists: absolute `http://...` URLs for nested playlist/segments

Many players (include Shaka) will then use those absolute URLs for:
- MPD refreshes (re-fetching the MPD periodically)
- segment/playlist requests

so the browser starts requesting direction from `http://127.0.0.1/...` or `http://FLUSSONIC_ORIGIN/...` instead of `http://localhost:3000/flussonic/...`

**Why is that bad?** 
Because your Node server is doing important proxy work (and in DRM setups, often also controls headers/CORS/origin consistency). If the player switches away from the Node origin:
- your proxy logic is bypassed.
- you can hit CORS issues (different origin than the page).
- Requests may go to an address that is only valid on the server machine (e.g., `127.0.0.1`) inside Flussonic's containr/host, not the user's browser).
- Behavior becomes inconsistent: initial load via proxy, refreshes/segements via upstream.

**Why rewriting fixes it?**
When Node proxies a manifest, it rewrites occurrences like:
- `${FLUSSONIC_ORIGIN}/...` -> `/flussonic/...`
That forces the player to keep making subsequent requests back to: `http://localhost:3000/flussonic/...`


 SO MPD refreshes and related fetches stay on the Node origin. Prevent Shaka from switching away during MPD refreshes.


> [!INFO]
> No the manifest file on Flussonic is not changed.

The rewrite happens in memory, on the fly, when your Node server proxies the request:
1. Node fetches the manifest from Flussonic (`FLUSSONIC_ORIGIN`)
2. It reads the response text
3. It replaces 1. `${FLUSSONIC_ORIGIN}/...` with `/flussonic/...`
4. It sends that modified copy to the browser.

> [!NOTE]
> What the player receives that is rewritten version.

A translator in the middle, the source document stays the same, but the player only sees the translated version.