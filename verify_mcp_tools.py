"""
Simple verification script to check that both tools are defined in the code.
This doesn't require dependencies - it just checks the code structure.
"""
import ast
import sys
from pathlib import Path

def check_mcp_tools():
    """Parse the MCP server file and verify both tools are defined."""
    server_file = Path(__file__).parent / "src" / "mood_reads_server.py"
    
    if not server_file.exists():
        print(f"✗ Server file not found: {server_file}")
        return False
    
    print("=" * 60)
    print("MCP Server Code Verification")
    print("=" * 60)
    
    # Read the file
    with open(server_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for tool decorators and function definitions
    tools_found = []
    
    # Check for search_books_by_query
    if '@mcp.tool()' in content and 'async def search_books_by_query' in content:
        tools_found.append('search_books_by_query')
        print("✓ search_books_by_query tool found")
    else:
        print("✗ search_books_by_query tool NOT found")
    
    # Check for get_book_details
    if '@mcp.tool()' in content and 'async def get_book_details' in content:
        tools_found.append('get_book_details')
        print("✓ get_book_details tool found")
    else:
        print("✗ get_book_details tool NOT found")
    
    # Count @mcp.tool() decorators
    tool_count = content.count('@mcp.tool()')
    print(f"\nTotal @mcp.tool() decorators found: {tool_count}")
    
    print("\n" + "=" * 60)
    print("Code Structure Check:")
    print("=" * 60)
    
    # Parse the AST to verify structure
    try:
        tree = ast.parse(content)
        
        # Find all async function definitions with @mcp.tool() decorator
        mcp_tools = []
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                # Check if it has @mcp.tool() decorator
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call):
                        if isinstance(decorator.func, ast.Attribute):
                            if (isinstance(decorator.func.value, ast.Name) and 
                                decorator.func.value.id == 'mcp' and
                                decorator.func.attr == 'tool'):
                                mcp_tools.append(node.name)
        
        print(f"\nFound {len(mcp_tools)} MCP tool function(s):")
        for tool_name in mcp_tools:
            print(f"  ✓ {tool_name}")
        
        if len(mcp_tools) == 2:
            print("\n✓ Both tools are properly defined!")
            return True
        else:
            print(f"\n⚠ Expected 2 tools, found {len(mcp_tools)}")
            return False
            
    except SyntaxError as e:
        print(f"✗ Syntax error in server file: {e}")
        return False

if __name__ == "__main__":
    success = check_mcp_tools()
    sys.exit(0 if success else 1)

