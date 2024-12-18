```js
use admin;
db.getRoles({showBuiltinRoles: true, showPrivileges: true});
db.runCommand({ connectionStatus: 1 }); // details about the authenticated user for the current session
db.createUser({
  user: "myUser",
  pwd: "myPassword",
  roles: [
    { role: "readWrite", db: "myDatabase" },
    { role: "dbAdmin", db: "myDatabase" }
  ]
});
```

```js
db.getUsers(); // view users;
db.updateUser("myUser", {
	roles: [{role: "dbAdmin", db: "testDB"}]
})
db.deleteUser("myUser"); // remove user from current database;
db.changeUserPassword("myUser", "newPassword");
db.grantRolesToUser("myUser", [{role: "read", db: "testDB"}])
db.revokeRolesFromUser("myUser", [{role: "read", db: "testDB" }])
db.auth("myUser", "password");
```

### **Default Roles Overview**

1. **Database-Specific Roles**:
   - `read`: Read-only access to a database.
   - `readWrite`: Read and write access to a database.
2. **Administrative Roles**:
   - `dbAdmin`: Administrative tasks like indexing and stats.
   - `userAdmin`: User management for the database.
3. **Cluster Roles**:
   - `clusterAdmin`: Full control of the cluster.
   - `clusterMonitor`: Read-only access to cluster monitoring.
4. **Backup and Restore Roles**:
   - `backup`: Permissions for backups.
   - `restore`: Permissions for restoring data.

```js
db.runCommand({ listCommands: 1 }); // list all available commands (actions correspond to commands)
db.createRole({
  role: "<role_name>",
  privileges: [
    {
      resource: { db: "<database>", collection: "<collection>" },
      actions: ["<action1>", "<action2>"]
    }
  ],
  roles: ["<existing_role1>", "<existing_role2>"]
});
```
### **Common Default Actions**
#### **CRUD Actions**:
- `find`: Read documents.
- `insert`: Add new documents.
- `update`: Modify existing documents.
- `remove`: Delete documents.

#### **Administrative Actions**:
- `createCollection`: Create new collections.
- `dropCollection`: Drop collections.
- `createIndex`: Create indexes.
- `dropIndex`: Drop indexes.
- `compact`: Defragment data on storage.

#### **Database Management Actions**:
- `listCollections`: List collections in a database.
- `listIndexes`: List indexes on a collection.
- `collStats`: Retrieve collection statistics.
- `dbStats`: Retrieve database statistics.

#### **User and Role Management Actions**:
- `createUser`: Create users.
- `dropUser`: Remove users.
- `grantRole`: Grant roles to a user.
- `revokeRole`: Revoke roles from a user.

#### **Backup and Restore Actions**:
- `backup`: Take database backups.
- `restore`: Restore databases from backups.

#### **Cluster-Level Actions**:
- `addShard`: Add shards to a cluster.
- `removeShard`: Remove shards from a cluster.
- `shardCollection`: Shard a collection.