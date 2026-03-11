# Go Backend Projects: Brief Specifications

## **Beginner (Syntax, Structs, Testing)**

## **1. CLI Todo App**

text

`- Add/list/delete/complete todos   - Persist to JSON file - Flag parsing (go flags) - Input validation, pretty table output - 100% unit tests`

**Files**: `main.go`, `todo.go`, `store.go`, `cmd/*.go`

## **2. URL Shortener CLI**

text

`- Shorten/expand URLs (base62 encoding) - In-memory LRU cache (100 entries) - Validate URLs, collision handling - Stats: total short/expand calls - Benchmark encoding`

**Files**: `main.go`, `shortener.go`, `lru.go`

## **3. File Stats Analyzer**

text

`- Scan directory recursively - Concurrent file scanning (10 goroutines) - Stats: files by type/size/age - JSON/CSV output - Graceful shutdown (SIGINT)`

**Files**: `main.go`, `scanner.go`, `stats.go`

## **Intermediate (APIs, DB, Concurrency)**

## **4. REST Task API** (Gin + PostgreSQL)

text

`Endpoints: - POST/GET/PUT/DELETE /tasks - GET /tasks?user_id=123&status=done&limit=20 - POST /auth/login (JWT)`

**Tech**: Gin, GORM, PostgreSQL, JWT middleware, Docker  
**Tests**: Integration + unit (80% coverage)

## **5. Chat Server** (WebSockets)

text

`- Join/leave rooms - Send/receive messages (broadcast) - Message history (100 latest) - Rate limiting per user`

**Tech**: gorilla/websocket, channels + mutex, Redis (optional)

## **6. Rate Limited API Gateway**

text

`- Proxy to backend services - Token bucket (100 req/min per IP) - Metrics endpoint (/metrics) - Graceful shutdown`

**Tech**: http.Client, Redis, Prometheus metrics

## **Advanced (Distributed Systems)**

## **7. Distributed KV Store** (gRPC)

text

`- Put/Get/Delete keys (TTL support) - Leader election (Raft/etcd) - 3-node cluster (Docker Compose) - List keys, consistent reads`

**Tech**: gRPC, Raft, boltdb

## **8. Hotel Booking Service** (Microservices)

text

`Services: rooms, bookings, notifications - Saga pattern for distributed transactions - Kafka events - PostgreSQL + Redis cache`

**Tech**: Docker Compose, Kafka, gRPC/REST

## **9. Log Aggregator**

text

`- Tail multiple log files - Parse JSON logs, extract metrics - Buffer → HTTP sink (batch upload) - Retry failed uploads`

**Tech**: fsnotify, buffered channels, gzip compression

---

## **Production Checklist** (All Projects)

text

`✅ Docker + docker-compose ✅ 80%+ test coverage (go test ./...) ✅ Graceful shutdown (context) ✅ Config via env vars ✅ README: build/run/benchmark ✅ GitHub Actions CI ✅ Architecture diagram (mermaid)`

**Start order**: 1→9. Each takes 4-12 hours. Deploy to Fly.io. Perfect interview portfolio!