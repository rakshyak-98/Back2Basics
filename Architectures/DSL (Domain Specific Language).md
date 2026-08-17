[[Descriptive/Mermaid (DSL)]] [[Terraform/variable file]] [[Nginx/Configuration]] [[Architectures/Orchestration layer]]

# DSL (Domain Specific Language)

> Language tuned to one problem domain — expressive for experts, useless elsewhere — **contrast with general-purpose languages**.

```txt
        DSL (Domain Specif ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** DSL questions separate internal vs external DSLs and when a constrained langu…

## Sources
- [Martin Fowler — Domain-Specific Languages](https://martinfowler.com/books/dsl.html) — deep-dive
- [Wikipedia — Domain-specific language](https://en.wikipedia.org/wiki/Domain-specific_language) — overview

## Key Concepts
- **Note:** A **DSL** trades generality for **domain fit**: SQL for relations, Regex for …

```
- **Note:** General-purpose (Java, Python) DSL (SQL, Makefile, GraphQL schema)
        │                                    │
- **Note:** Turing-complete, broad Narrow vocabulary, high signal
- **Note:** more boilerplate wrong tool outside domain
```

| Type | Example | Hosted in |
|------|---------|-----------|
| **External DSL** | SQL, Regex | Own parser |
| **Internal DSL** | Fluent API in Ruby | Host language syntax |
| **Declarative config** | [[Terraform/variable file]] HCL, K8s YAML | Engine interprets |

## Technical Details
### When to introduce a DSL

```text
☐ Domain rules repeat across code (policy, routing, workflow)
☐ Non-dev stakeholders must edit safely (ops, analysts)
☐ Errors should be domain-specific ("invalid CIDR" not stack trace)
☐ Alternative is 500-line if/else — DSL + interpreter cleaner
```

### External DSL example — policy (conceptual)

```rego
# Open Policy Agent — Rego DSL
allow {
  input.user.role == "admin"
}
```

### Internal DSL — builder pattern

```javascript
const query = db.select('id', 'name')
  .from('users')
  .where('active', true)
  .limit(10);
```

### Infra DSL — Terraform HCL

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = "t3.micro"
  tags = { Env = var.environment }
}
```

### Diagram DSL — Mermaid (this vault)

```mermaid
flowchart LR
  Client --> API --> DB
```

- See [[Descriptive/Mermaid (DSL)]].

### Anti-pattern — accidental DSL

```javascript
// Stringly "DSL" in JSON without schema validation
{ "action": "doThing", "arg": 1 }  // prefer protobuf/OpenAPI/JSON Schema
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Users hate syntax | Wrong abstraction level | Narrow vocabulary; better errors |
| DSL bugs opaque | No source locations in errors | ANTLR/pest with line numbers |
| Security hole in interpreter | Turing-complete user scripts | Sandbox; cap loops; no file IO |
| Two DSLs for same domain | Org drift | Consolidate; version schema |
| Hard to test | No golden files | Snapshot parse → AST → eval |

## Mistakes to Avoid
- **Mistake:** Every DSL becomes a maintenance product
- **Mistake:** **YAML as DSL**
- **Mistake:** **Internal DSL** inherits host complexity
- **Mistake:** **Version DSL files** in git

## Pros/Cons or Trade-offs
- **Trade-off:** One-off 10-line configuration — JSON/YAML enough.
- **Trade-off:** Team lacks parser expertise and domain rules change weekly — use data-driven tables in code.
