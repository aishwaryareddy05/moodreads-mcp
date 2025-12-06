"""
Test script to verify the MCP server exposes both tools correctly.
This simulates what Cursor should see when connecting to the server.
"""
import sys
import asyncio
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from mood_reads_server import mcp, search_books_by_query, get_book_details
    
    print("=" * 60)
    print("MCP Server Verification Test")
    print("=" * 60)
    
    # Check server name
    print(f"\n✓ Server Name: {mcp.name}")
    
    # Check if tools are registered
    print("\n" + "-" * 60)
    print("Checking Registered Tools:")
    print("-" * 60)
    
    # FastMCP stores tools internally - let's check the object
    if hasattr(mcp, '_tools'):
        tools = mcp._tools
        print(f"\nFound {len(tools)} registered tool(s):")
        for tool_name, tool_info in tools.items():
            print(f"  ✓ {tool_name}")
            if hasattr(tool_info, '__name__'):
                print(f"    Function: {tool_info.__name__}")
    else:
        print("\n⚠ Could not access _tools attribute directly")
        print("   Checking function definitions instead...")
        
        # Check if functions exist
        if 'search_books_by_query' in globals():
            print("  ✓ search_books_by_query function found")
        if 'get_book_details' in globals():
            print("  ✓ get_book_details function found")
    
    # Try to test the functions directly
    print("\n" + "-" * 60)
    print("Testing Tool Functions:")
    print("-" * 60)
    
    async def test_tools():
        print("\n1. Testing search_books_by_query...")
        try:
            result = await search_books_by_query("cozy fantasy", limit=2)
            print(f"   ✓ search_books_by_query works!")
            print(f"   Found {result.get('total_found', 0)} books")
            print(f"   Returned {len(result.get('books', []))} results")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print("\n2. Testing get_book_details...")
        try:
            result = await get_book_details("/works/OL22082778W")
            print(f"   ✓ get_book_details works!")
            print(f"   Book: {result.get('title', 'Unknown')}")
            print(f"   ID: {result.get('id', 'Unknown')}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    # Run async tests
    asyncio.run(test_tools())
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print("Both tools are defined in the code.")
    print("If Cursor doesn't see get_book_details, the MCP server")
    print("needs to be restarted in Cursor to discover the new tool.")
    print("=" * 60)
    
except ImportError as e:
    print(f"✗ Import Error: {e}")
    print("\nMake sure dependencies are installed:")
    print("  uv sync  # or: pip install -e .")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

