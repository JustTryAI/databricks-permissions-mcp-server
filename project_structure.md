databricks-permissions-mcp-server/
├── src/                             # Source code
│   ├── __init__.py                  # Makes src a package
│   ├── __main__.py                  # Main entry point for the package
│   ├── main.py                      # Entry point for the MCP server
│   ├── api/                         # Databricks API clients
│   │   ├── __init__.py              # Makes api a package
│   │   ├── service_principals.py    # Service Principals API
│   │   ├── unity_catalog.py         # Unity Catalog API
│   │   ├── permissions.py           # Permissions API
│   │   ├── shares.py                # Delta Sharing API
│   │   └── git_credentials.py       # Git Credentials API
│   ├── core/                        # Core functionality
│   │   ├── __init__.py              # Makes core a package
│   │   ├── auth.py                  # Authentication utilities
│   │   ├── config.py                # Configuration management
│   │   └── utils.py                 # Utility functions
│   ├── server/                      # Server implementation
│   │   ├── __init__.py              # Makes server a package
│   │   ├── __main__.py              # Run server module directly
│   │   ├── app.py                   # FastAPI app for tests
│   │   └── databricks_permissions_mcp_server.py # Main MCP server
│   └── cli/                         # Command-line interface
│       ├── __init__.py              # Makes cli a package 
│       └── commands.py              # CLI commands
├── tests/                           # Test directory
│   ├── __init__.py                  # Makes tests a package
│   ├── test_direct.py               # Direct server tests
│   ├── test_mcp_client.py           # MCP client tests
│   ├── test_mcp_server.py           # MCP server tests
│   └── test_tools.py                # Individual tool tests
├── scripts/                         # Scripts directory
│   ├── start_mcp_server.ps1         # Server startup script (Windows)
│   ├── start_mcp_server.sh          # Server startup script (Linux/Mac)
│   ├── run_tests.ps1                # Test runner script
│   └── run_list_tools.ps1           # Tool listing script (Windows)
│   └── run_list_tools.sh            # Tool listing script (Linux/Mac)
├── examples/                        # Example usage
│   ├── direct_usage.py              # Direct server usage for permissions and credentials
│   ├── mcp_client_usage.py          # Client example for permissions and credentials
│   └── README.md                    # Examples documentation
├── docs/                            # Documentation
│   ├── api.md                       # API documentation
│   ├── tools.md                     # Tool documentation
│   ├── setup.md                     # Setup instructions
│   └── architecture.md              # Architecture overview
├── .venv/                           # Virtual environment
├── .env                             # Environment variables
├── .env.example                     # Example environment file
├── .gitignore                       # Git ignore file
├── start_mcp_server.ps1             # Wrapper for server startup script
├── start_mcp_server.sh              # Wrapper for server startup script (Linux/Mac)
├── README.md                        # Main README
├── LICENSE                          # License file
├── pyproject.toml                   # Modern Python packaging
└── uv.lock                          # UV package manager lock file
``` 