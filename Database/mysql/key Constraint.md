[[mysql]] [[mysql table]] [[Database design]]

# key Constraint

> UNIQUE / FK / PK constraints stop bad rows at write time — the database enforces relationships, not just the app.

---

## Mental model

**Say it in one breath:** Primary key identifies the row; UNIQUE blocks duplicates (including composites); FOREIGN KEY requires a matching parent — InnoDB also indexes FK columns.

```txt
HotelSections
  PK id
  FK hotel_template_id → HotelTemplates(id)
  FK template_section_id → TemplateSections(id)
  UNIQUE (hotel_template_id, template_section_id)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **PRIMARY KEY** | Unique row id, NOT NULL | “One PK; InnoDB clusters on it.” |
| **UNIQUE** | No duplicate key values | “Composite UNIQUE = pair must be unique.” |
| **FOREIGN KEY** | Must exist in parent | “Prevents orphan children.” |
| **Constraint name** | Label for ALTER/DROP | “Name it so errors are readable.” |

---

## Standard config / commands

```sql
CREATE TABLE HotelSections (
  id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_template_id INT NOT NULL,
  template_section_id INT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (hotel_template_id) REFERENCES HotelTemplates(id),
  FOREIGN KEY (template_section_id) REFERENCES TemplateSections(id),
  UNIQUE (hotel_template_id, template_section_id)
);

ALTER TABLE HotelSections
  ADD CONSTRAINT unique_hotel_template_section
  UNIQUE (hotel_template_id, template_section_id);
```

| Knob | Why it matters |
|------|----------------|
| Composite UNIQUE | Business rule: one section per template pair |
| FK + index | InnoDB auto-indexes FK; check `INFORMATION_SCHEMA` |
| `ON DELETE CASCADE` | Parent delete removes children — intentional only |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate entry for key | Existing row / UNIQUE | Dedupe data; then ADD CONSTRAINT |
| Cannot add FK | Child orphans / type mismatch | Clean data; match types/signedness/charset |
| Error 1452 | Missing parent id | Insert parent first or fix id |
| Constraint already exists | `SHOW CREATE TABLE` | DROP CONSTRAINT then recreate |

---

## Gotchas

> [!WARNING]
> **FK requires matching types** — `INT` vs `BIGINT`, signed vs unsigned, charset/collation on string keys.

> [!WARNING]
> **MyISAM ignores FKs** — use InnoDB ([[mysql engine]]).

---

## When NOT to use

- **Soft uniqueness only in application** — race conditions will duplicate; prefer UNIQUE in DB.
- **Cross-database FKs** — MySQL won’t enforce; redesign or application checks.

---

## Related

[[mysql table]] [[mysql index]] [[Database design]] [[SQL normalization]]
