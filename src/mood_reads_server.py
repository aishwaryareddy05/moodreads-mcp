from typing import Any, Dict
import httpx
from mcp.server.fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("mood-reads-server", json_response=True)


@mcp.tool()
async def search_books_by_query(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Search Open Library for books based on a free-text query.

    Example query: "cozy fantasy found family"
    """
    url = "https://openlibrary.org/search.json"

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url,
            params={"q": query, "limit": limit},
            headers={"User-Agent": "mood-reads-mcp/0.1.0"},
            timeout=15.0,
        )

    if resp.status_code != 200:
        return {
            "error": f"Open Library returned {resp.status_code}: {resp.text[:200]}"
        }

    data = resp.json()
    docs = data.get("docs", [])

    books = []
    for b in docs:
        books.append(
            {
                "id": b.get("key"),  # e.g. "/works/OL12345W"
                "title": b.get("title"),
                "author": (b.get("author_name") or [None])[0],
                "first_publish_year": b.get("first_publish_year"),
                "subjects": b.get("subject", []),
                "edition_count": b.get("edition_count"),
            }
        )

    return {
        "query": query,
        "total_found": data.get("numFound"),
        "books": books,
    }

@mcp.tool()
async def get_book_details(book_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a book/work from Open Library.

    book_id should usually be the `id` field returned by search_books_by_query,
    e.g. "/works/OL42561374W".
    """

    # Normalize the ID: if it doesn't start with "/", assume it's a works ID
    # like "OL42561374W" and build "/works/OL42561374W"
    if not book_id.startswith("/"):
        book_id = f"/works/{book_id}"

    # Build the URL: https://openlibrary.org/works/OLxxxx.json
    url = f"https://openlibrary.org{book_id}.json"

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url,
            headers={"User-Agent": "mood-reads-mcp/0.1.0"},
            timeout=15.0,
        )

    if resp.status_code != 200:
        return {
            "error": f"Open Library returned {resp.status_code}: {resp.text[:200]}",
            "book_id": book_id,
        }

    data = resp.json()

    # description can be a string OR a dict with "value"
    raw_desc = data.get("description")
    if isinstance(raw_desc, dict):
        description = raw_desc.get("value")
    else:
        description = raw_desc

    # subjects might be called "subjects" or "subject_places" etc.
    subjects = data.get("subjects") or []

    result = {
        "id": book_id,
        "title": data.get("title"),
        "description": description,
        "subjects": subjects,
        "first_publish_date": data.get("first_publish_date"),
        "covers": data.get("covers", []),
        "links": data.get("links", []),
        "raw": data,  # keep full raw payload if you want to inspect more
    }

    return result



def main() -> None:
    # Run the MCP server over stdio (what MCP clients expect)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
