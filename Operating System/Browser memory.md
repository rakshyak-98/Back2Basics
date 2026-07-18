## Keeping files/data in browser memory (not on disk)

- You upload an image in the browser -> it stays in RAM, never touches your hard drive.

```js
<input type="file" id="fileInput" />
<script>
  document.getElementById('fileInput').onchange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    
    reader.onload = (event) => {
      const buffer = event.target.result; // ← in browser memory!
      console.log('File is now in RAM:', buffer.byteLength, 'bytes');
      // You can send it to server, show preview, etc.
    };
    
    reader.readAsArrayBuffer(file); // keeps it in memory
  };
</script>
```
- The file never saves to disk.
- Lives only in **browser RAM**.
- Perfect for privacy or temporary previews.

## In-memory browser database like (SQLite in browser)

- Tools like `SQL.js` or `IndexedDB` let you run full database inside the browser, stored only in RAM.

```js
// SQL.js = SQLite running in browser memory
const db = new SQL.Database(); // ← 100% in RAM
db.run("CREATE TABLE users (name TEXT);");
db.run("INSERT INTO users VALUES ('Alice');");
```
- Lost when you close/refresh the page
- Super fast, No files on disk