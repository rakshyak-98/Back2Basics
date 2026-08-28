
**Application Layer**

```go
type VideoGenerator interface {
    Generate(prompt string) (string, error)
}
```

Application Layer service (The Application Layer doesn't Know Evator exists)
- it only know "I have a `VideoGenerator` capability"

```go
type VideoService struct {
    generator VideoGenerator
}

func NewVideoService(generator VideoGenerator) *VideoService {
    return &VideoService{
        generator: generator,
    }
}

func (s *VideoService) GenerateVideo(prompt string) (string, error) {
    if prompt == "" {
        return "", errors.New("prompt cannot be empty")
    }

    videoURL, err := s.generator.Generate(prompt)
    if err != nil {
        return "", err
    }

    return videoURL, nil
}
```


**Infrastructure Layer**
"I'll provide the capability using Evator"

```go
type EvatorVideoGenerator struct {
    client *EvatorClient
}

func NewEvatorVideoGenerator(client *EvatorClient) *EvatorVideoGenerator {
    return &EvatorVideoGenerator{
        client: client,
    }
}

func (e *EvatorVideoGenerator) Generate(prompt string) (string, error) {
    videoURL, err := e.client.GenerateVideo(prompt)
    if err != nil {
        return "", err
    }

    return videoURL, nil
}
```

**Presentation Layer**

```go
type GenerateVideoRequest struct {
    Prompt string `json:"prompt"`
}

type VideoHandler struct {
    service *VideoService
}

func NewVideoHandler(service *VideoService) *VideoHandler {
    return &VideoHandler{
        service: service,
    }
}
```

```go
func (h *VideoHandler) GenerateVideo(
    w http.ResponseWriter,
    r *http.Request,
) {
    var req GenerateVideoRequest

    err := json.NewDecoder(r.Body).Decode(&req)
    if err != nil {
        http.Error(w, "invalid request", http.StatusBadRequest)
        return
    }

    videoURL, err := h.service.GenerateVideo(req.Prompt)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    response := map[string]string{
        "video_url": videoURL,
    }

    w.Header().Set("Content-Type", "application/json")

    json.NewEncoder(w).Encode(response)
}

```

**At application startup, we construct the object**

```go
func main() {

    // Infrastructure
    evatorClient := NewEvatorClient(...)
    videoGenerator := NewEvatorVideoGenerator(evatorClient)

    // Application
    videoService := NewVideoService(videoGenerator)

    // Presentation
    videoHandler := NewVideoHandler(videoService)

    http.HandleFunc(
        "/videos",
        videoHandler.GenerateVideo,
    )

    http.ListenAndServe(":8080", nil)
}
```