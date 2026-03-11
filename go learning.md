Here is a detailed series of **copy-paste ready prompts** you can feed sequentially to any AI agent (like me, Claude, or ChatGPT) over the next 6 months. Each prompt is self-contained, builds on prior ones, and turns the AI into your personal Go interview coach.

**Instructions for use:**

- Run prompts in order, one session per topic/project/mock.
    
- After each AI response, paste your code/answers back with: _"Here is my attempt. Review it line-by-line, score 1-10, suggest idiomatic improvements, and give me the next exercise."_
    
- Aim for 7-10 hours/week: 60% coding, 30% Q&A drills, 10% review.
    
- Track progress in a GitHub repo with weekly commits.
    

---

## 🎯 **PHASE 1: FOUNDATIONS (Months 1-2)**

## **Prompt 1.1: Create your personalized Go roadmap**

text

`I have 6 months to prepare for Go backend developer interviews. I have a frontend JS background and 7-10 hours/week to study. I'm in Bengaluru, India. Create a detailed 24-week Go learning roadmap covering: - Go syntax, types, control flow (weeks 1-2)   - Structs, methods, interfaces, errors (weeks 3-4) - Concurrency (goroutines, channels, context) (weeks 5-6) - HTTP servers, JSON, middleware (weeks 7-8) - Databases (PostgreSQL/SQLite), ORM (GORM/sqlc) (weeks 9-10) - Testing, benchmarking, Docker (weeks 11-12) For each week, provide: 1. Learning objectives (3-5 key concepts) 2. 3-5 coding exercises (small, testable) 3. 5 interview questions to drill 4. Recommended free resources (Go Tour, Effective Go, videos) Make it realistic for someone transitioning from JS. Start with Week 1 now.`

## **Prompt 1.2: Daily Go concept drill (repeat weekly)**

text

`Teach me [TOPIC: e.g., "Go slices vs arrays"] for Go backend interviews. Provide: 1. 60-second explanation (differences from JS arrays) 2. 3 code examples (basic usage, gotchas, performance) 3. 5 interview questions (conceptual + coding) 4. 3 small exercises (write functions using this concept) Ask me questions one-by-one. Wait for my answer before moving to next. After each answer, score me 1-10 and show model answer + improvements. Start with question 1.`

## **Prompt 1.3: Weekly coding challenge**

text

`Give me a Week [X] Go coding challenge: [paste current week's topic, e.g., "build a CLI todo app using slices/maps/structs"]. Requirements: - 50-100 lines max, production-ready - Include comprehensive tests (table-driven) - Follow Go idioms (error handling, zero values) - README with "why I made these decisions" After I submit my code, review it for: - Idiomatic Go (naming, structure, simplicity) - Error handling patterns - Test coverage and quality - Performance considerations - Interview talking points Provide refactored "senior engineer" version + explanation.`

---

## 🚀 **PHASE 2: BACKEND + CONCURRENCY (Months 3-4)**

## **Prompt 2.1: API project kickoff**

text

`Help me build Project 1: REST API for hotel room booking (ties to my frontend experience). Tech stack: Go 1.23+, Gin/Echo, PostgreSQL (dockerized), GORM, JWT auth. Phase 1 spec: 1. POST /rooms (create room: name, price, available) 2. GET /rooms?available=true&price_lt=5000 (filter/paginate) 3. PUT /rooms/:id/book (idempotent booking) 4. Middleware: rate limiting, logging, CORS Scaffold the complete project structure first: - folder layout - go.mod with minimal deps - main.go with graceful shutdown - database connection + migrations - basic handlers Generate the skeleton code. I'll implement handlers next.`

## **Prompt 2.2: Concurrency masterclass**

text

`Run a concurrency bootcamp for Go interviews. My level: [beginner/intermediate]. Cover these patterns one-by-one (ask my solution first, then reveal best practice): 1. Fan-out/fan-in worker pool (process 1000 items with 10 workers) 2. Pipeline (read→process→write with channels) 3. Rate limiter (token bucket) 4. Context cancellation (timeout graceful shutdown) 5. Mutex vs Channels (when to use each) For each: - Problem statement + expected benchmark - Write the solution together (I'll code, you review) - 3 interview variations - Common bugs + pprof analysis Start with worker pool.`

## **Prompt 2.3: Code review simulator**

text

`[PASTE YOUR CODE HERE] Act as a senior Go engineer doing interview code review. Score this production code: Categories (1-10 each): 1. Go idioms and simplicity 2. Error handling and context propagation   3. Concurrency safety (race conditions) 4. Testability and test coverage 5. Performance (allocations, escapes) 6. Production readiness (logging, config, graceful shutdown) Provide: - Line-by-line feedback - "Nit", "Suggestion", "Blocker" labels - Refactored version (if <7/10) - 5 questions interviewer would ask about this code`

---

## 🎤 **PHASE 3: INTERVIEW SIMULATION (Months 5-6)**

## **Prompt 3.1: Full 60-minute mock interview**

text

`Run a realistic 60-minute Go Backend Developer interview. I'm interviewing at [FAANG/Fintech/Startup]. Structure: [ ] 5 min: "Tell me about your Go projects" [ ] 15 min: Live coding (you provide problem, I solve on pastebin) [ ] 20 min: System design ("Design URL shortener at Twitter scale") [ ] 15 min: Go deep dive ("Explain Go scheduler + gotchas") [ ] 5 min: Behavioral + questions for us Rules: - One question at a time, realistic timing - Think silently for 30s after my answer (simulate thinking) - Give specific, constructive feedback - Track my score across rounds Ready? Start with "Tell me about yourself and your Go experience."`

## **Prompt 3.2: System design practice**

text

`System design round: "Design a distributed URL shortener that handles 1B redirects/day." Guide me through 45 minutes: 1. Requirements gathering (functional + non-functional) 2. High-level design (components, APIs, data model) 3. Deep dives (sharding, caching, rate limiting, monitoring) 4. Trade-offs and scale stories 5. Go-specific implementation details After each step, critique my answer and ask clarifying questions an interviewer would. Start with: "Walk me through your approach."`

## **Prompt 3.3: Tricky Go questions drill**

text

`Quiz me on 20 advanced Go interview questions (hide answers until I respond). Focus on trickiest topics: - init() order, package init cycles - Interface{} gotchas, type assertions - Escape analysis, stack vs heap - Context vs timeout vs cancel - Race conditions, sync.Pool patterns - Defer semantics, panic/recover Format: Question → My answer → Score + explanation → Next question. Make it brutal - these are FAANG-level questions. Question 1: What happens in this code and why? [paste tricky code snippet]`

---

## 🔄 **WEEKLY REVIEW & PROJECT DEMO**

## **Prompt 4.1: Weekly progress review**

text

`Week [X] complete! Here's my GitHub: [REPO LINK] Review my progress against the roadmap: 1. Code quality evolution (show before/after) 2. Which concepts clicked vs still shaky 3. Interview readiness % (honest assessment) 4. Next week's focus areas + resources 5. One celebration win Updated roadmap for Week [X+1].`

## **Prompt 4.2: Portfolio storytelling**

text

`I have these 3 Go projects: [list them]. Turn each into 2-minute interview talking points: For each project: 1. "Problem → Solution → Results" story (STAR format) 2. 3 technical challenges + how I solved 3. 3 metrics (RPS, latency, saved engineer months) 4. 3 decisions I'd make differently 5. Follow-up questions interviewer might ask Practice round: Ask me to explain Project 1, then critique delivery.`

---

## 🚀 **FINAL PREP (Last 2 weeks)**

## **Prompt 5.1: War games - hardest questions**

text

`Give me the 10 hardest Go questions you've seen in real interviews. Sources: LeetCode Go contests, FAANG offers, senior promotions. For each: - Question + expected time to solve - 3 solution approaches (optimal first) - Space/time complexity - Go-specific optimizations I'll solve live. Be ruthless.`

**Start with Prompt 1.1 today.** Copy-paste it to me now, and we'll generate your complete 24-week schedule!

This system will get you interview-ready. Commit to it daily. 💪linkedin+2