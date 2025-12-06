# 📚 MoodReads — MCP-Powered Mood-Based Book Recommender

> _"Tell me how you feel, and I'll find the story that matches your heart."_

MoodReads is an **MCP-based AI agent** that recommends books based on your **current mood and vibes**, not just genre keywords.

You say things like:

> _"I feel emotionally tired and want a soft hopeful fantasy with found family."_

The system:

1. Interprets your mood,
2. Builds a smart search query,
3. Calls MCP tools to the **Open Library API**,
4. Ranks and explains recommendations,
5. Optionally fetches detailed info for any book you pick.

---

## 🧭 High-Level Project Overview

- **Interface**: You chat from an MCP-enabled client (e.g. Cursor).
- **Brain**: An LLM acting as a "Mood Librarian".
- **Tools** (MCP):
  - `search_books_by_query(query, limit)` → finds candidate books from Open Library.
  - `get_book_details(book_id)` → fetches rich metadata, description, subjects, etc.
- **Source of Truth**: Open Library's free, public book catalog API.
- **Goal**: Map **emotions + vibes → story suggestions** in a transparent, tool-driven, reproducible way.

---

## 🧩 System Architecture

```mermaid
graph TD
    U[User: Mood Input] --> C[MCP Client]
    C --> LLM[LLM: Mood Librarian]
    LLM --> S[MCP Server]
    
    subgraph "MCP Layer"
        S --> T1[Tool: Search Books]
        S --> T2[Tool: Get Details]
    end
    
    T1 --> OL[Open Library API]
    T2 --> OL
    
    OL --> T1
    OL --> T2
    
    T1 --> S
    T2 --> S
    S --> LLM
    LLM --> C
    C --> U[Recommendations]
```
## 🔁 End-to-End Request Flow

```mermaid
sequenceDiagram
    participant User
    participant Client as MCP Client
    participant LLM
    participant Server as MCP Server
    participant SearchTool
    participant DetailsTool
    participant OpenLib as Open Library API

    User->>Client: "I feel emotionally tired, want soft hopeful fantasy"
    Client->>LLM: Forward message + tools
    LLM->>LLM: Parse mood → extract tone, genre, vibes
    LLM->>Server: call search_books_by_query
    Server->>SearchTool: Invoke tool
    SearchTool->>OpenLib: GET /search.json
    OpenLib-->>SearchTool: Book list
    SearchTool-->>Server: Results
    Server-->>LLM: Tool result
    LLM->>LLM: Rank books by mood fit
    LLM->>Client: Recommendations + explanations
    Client->>User: Show recommendations
    
    Note over User,LLM: User requests more details
    User->>Client: "Tell me more about book #1"
    Client->>LLM: Forward request
    LLM->>Server: call get_book_details
    Server->>DetailsTool: Invoke tool
    DetailsTool->>OpenLib: GET /works/{id}.json
    OpenLib-->>DetailsTool: Metadata
    DetailsTool-->>Server: Details
    Server-->>LLM: Book info
    LLM->>Client: Summary with emotional themes
    Client->>User: Human-friendly explanation
```

## 🔍 Internal Flow: Mood → Query → Tools

```mermaid
flowchart TD
    A["User mood input<br>tired, need soft hopeful fantasy"] --> B[LLM: Parse Mood]
    B --> C[Extract Features<br>mood, genre, trope, pacing]
    C --> D[Build Query<br>cozy fantasy found family hopeful gentle]
    D --> E[Call Search Tool]
    E --> F[Receive Book List]
    F --> G[Rank by Vibe Match]
    G --> H[Return Top Recommendations]
    H --> I{User Wants Details?}
    I -->|Yes| J[Call Details Tool]
    I -->|No| K[Continue Conversation]
```
## 🧠 Tools Overview
🔎 search_books_by_query
Signature:

```python
async def search_books_by_query(query: str, limit: int = 5) -> Dict[str, Any]
Used by the LLM to search Open Library using a mood/genre/trope-rich string.
```
Example return:

```json
{
  "query": "cozy fantasy found family hopeful",
  "total_found": 123,
  "books": [
    {
      "id": "/works/OL22082778W",
      "title": "Heartsong",
      "author": "T.J. Klune",
      "first_publish_year": 2019,
      "subjects": ["Fantasy", "Romance", "LGBTQ+", "Found family"],
      "edition_count": 12
    }
  ]
}
```
📖 get_book_details
Signature:

```python
async def get_book_details(book_id: str) -> Dict[str, Any]
Takes the id returned by search_books_by_query (e.g. /works/OL22082778W) and fetches rich metadata from the Open Library works API.
```
Example return:

```json
{
  "id": "/works/OL22082778W",
  "title": "Heartsong",
  "description": "A cozy, found-family fantasy...",
  "subjects": ["Fantasy", "Queer", "Friendship", "Found family"],
  "first_publish_date": "2019",
  "covers": [1234567],
  "links": [],
  "raw": { "full Open Library payload" }
}
```
## 🧱 Component Architecture

```mermaid
flowchart LR
    subgraph ClientSide[Client Side]
        U[User]
        CUR[Cursor / MCP Client]
        MODEL[LLM: Mood Librarian]
    end

    subgraph ServerSide[Server Side]
        subgraph MCPServer[MCP Server]
            SFILE[Python Server]
            TSEARCH[Search Tool]
            TDETAILS[Details Tool]
            HTTPX[HTTP Client]
        end
        ENV[uv + venv]
    end

    subgraph External[External Services]
        OL[Open Library API]
    end

    U --> CUR
    CUR --> MODEL
    MODEL <--> MCPServer
    
    SFILE --> TSEARCH
    SFILE --> TDETAILS
    TSEARCH --> HTTPX
    TDETAILS --> HTTPX
    HTTPX --> OL
    
    ENV --- MCPServer
```
## ⚙️ Runtime View

```mermaid
graph LR
    subgraph Runtime
        A[Start MCP Client] --> B[Load Config]
        B --> C[Spawn MCP Server]
        C --> D[Register Tools]
        D --> E[Start Chat Session]
        E --> F[LLM Receives Tools]
        F --> G[Tool Calls]
        G --> H[Final Recommendations]
    end
```

## 🛠 Tech Stack
```markdown

| Layer              | Technology                           |
|--------------------|--------------------------------------|
| AI Orchestration   | MCP (Model Context Protocol)         |
| Agent Client       | Cursor (MCP-enabled IDE)             |
| Backend            | Python, FastMCP                      |
| HTTP Client        | httpx                                |
| Book Catalog       | Open Library API                     |
| Environment        | uv + virtualenv (.venv)              |


```

## 🚀 Quick Start
1. Clone & Install
```bash
git clone https://github.com/your-username/moodreads-mcp.git
cd moodreads-mcp
```
2. Run MCP Server (for dev / inspector)
```bash
uv run mcp dev src/mood_reads_server.py
# Opens MCP Inspector where you can test both tools
```
3. Configure in Cursor (MCP)
In Cursor MCP settings:
```json
{
  "mcpServers": {
    "mood-reads": {
      "command": "C:/path/to/.venv/Scripts/python.exe",
      "args": [
        "C:/path/to/repo/src/mood_reads_server.py"
      ]
    }
  }
}
```
## 💡 Example Prompts
```
"I feel drained and need something gentle, soft, and warm with found family."

"Give me dark academia with mystery and slow-burn romance."

"Tell me more about the first book you recommended; fetch detailed info."
```

## 🗺 Roadmap
```
User preference learning (remember what you liked)

Scoring & ranking model for better match quality

Web UI or Streamlit app

Integration with other book APIs (Goodreads/StoryGraph style)
```

## 📝 License
```
MIT — free to use, modify, and extend.
```

## ❤️ Credits
```
Open Library for book metadata.

MCP ecosystem for tool-based AI patterns.
```

