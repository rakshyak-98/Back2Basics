1. **Manual Migrations**:
- Write scripts to update documents to the new schema.
- Use the MongoDB shell or a programming language driver to iterate over documents and apply changes.
- Example:
```js
db.collection.find().forEach(function(doc) {
    // Modify the document schema
    doc.newField = doc.oldField;
    delete doc.oldField;
    // Save the updated document
    db.collection.save(doc);
});
```

2. **Using a Migration Tool**:
   - Use tools like `migrate-mongo`, `MongoBee`, or `Mongock` to manage migrations.
   - These tools provide a structured way to define and apply migrations, similar to migration tools in SQL databases.