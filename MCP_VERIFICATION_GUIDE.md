# MCP Server Verification Guide

## ✅ Code Verification Results

Both tools are **correctly defined** in `src/mood_reads_server.py`:
- ✓ `search_books_by_query` - Working (available as `mcp_mood-reads_search_books_by_query`)
- ✓ `get_book_details` - Defined but not currently available in Cursor

## Why `get_book_details` Isn't Showing Up

The tool is properly coded, but Cursor hasn't discovered it yet. This typically happens when:
1. The MCP server was started before `get_book_details` was added
2. Cursor needs to reload the MCP server connection
3. The server process needs to be restarted

## How to Fix It

### Step 1: Restart Cursor
1. **Completely close Cursor** (not just the window - fully quit the application)
2. **Reopen Cursor**
3. The MCP server should reconnect and discover both tools

### Step 2: Verify MCP Server Configuration

Cursor needs to know how to run your MCP server. Check your Cursor settings:

**Windows Location**: `%APPDATA%\Cursor\User\settings.json` or similar

Look for MCP server configuration that should include:
```json
{
  "mcpServers": {
    "mood-reads-server": {
      "command": "python",
      "args": ["-m", "src.mood_reads_server"],
      "env": {}
    }
  }
}
```

Or if using the entry point:
```json
{
  "mcpServers": {
    "mood-reads-server": {
      "command": "mood-reads-mcp"
    }
  }
}
```

### Step 3: Verify Dependencies Are Installed

Make sure the MCP dependencies are installed in the Python environment Cursor is using:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Step 4: Test the Server Manually

You can test if the server works by running it directly:

```bash
python -m src.mood_reads_server
```

The server should start and wait for stdio input (this is normal - MCP servers communicate via stdio).

## Expected Tool Names

When working, the tools should appear as:
- `mcp_mood-reads_search_books_by_query` ✅ (currently working)
- `mcp_mood-reads_get_book_details` ⏳ (should appear after restart)

## Troubleshooting

### If tools still don't appear after restart:

1. **Check Cursor logs** for MCP server errors
2. **Verify Python path** - ensure Cursor is using the correct Python interpreter
3. **Check server output** - look for any error messages when the server starts
4. **Verify imports** - ensure `mcp` package is installed in the active Python environment

### Test Scripts

Run these to verify your setup:

```bash
# Verify code structure
python verify_mcp_tools.py

# Test with dependencies (requires mcp package installed)
python test_mcp_server.py
```

## Current Status

- ✅ Code structure: **Correct** - Both tools properly defined
- ✅ Function definitions: **Correct** - Both async functions with @mcp.tool() decorator
- ⏳ Cursor discovery: **Pending** - Needs Cursor restart to discover `get_book_details`

## Next Steps

1. **Restart Cursor completely**
2. **Check if `mcp_mood-reads_get_book_details` appears** in available tools
3. **Test the tool** by calling it with a book ID like `/works/OL22082778W`

If it still doesn't work after restart, check the Cursor MCP server configuration and logs.

