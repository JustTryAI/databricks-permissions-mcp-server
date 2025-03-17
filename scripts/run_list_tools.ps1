#!/usr/bin/env pwsh
# Script to run the Databricks Permissions MCP server and list available tools

param(
    [switch]$SkipPrompt
)

# Get the directory of this script
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path $scriptPath -Parent
$projectRoot = Split-Path $scriptDir -Parent

# Change to the project root directory
Set-Location $projectRoot

# Check if the virtual environment exists
if (-not (Test-Path -Path ".venv")) {
    Write-Host "Virtual environment not found. Creating it now..."
    python -m venv .venv
}

# Activate virtual environment
. .\.venv\Scripts\Activate.ps1

# Check if environment variables are set
if (-not (Get-Item -Path Env:DATABRICKS_HOST -ErrorAction SilentlyContinue) -or 
    -not (Get-Item -Path Env:DATABRICKS_TOKEN -ErrorAction SilentlyContinue)) {
    Write-Host "Warning: DATABRICKS_HOST and/or DATABRICKS_TOKEN environment variables are not set."
    Write-Host "You can set them now or the server will look for them in other sources."
    
    # Skip prompt when called from tests
    if ($SkipPrompt) {
        Write-Host "Auto-continuing due to SkipPrompt flag..."
    } else {
        $continue = Read-Host "Do you want to continue? (y/n)"
        if ($continue -ne "y") {
            exit 1
        }
    }
}

# Start the server and list tools
Write-Host "Starting Databricks Permissions MCP server and listing tools..."

# Run the server in a background job
$job = Start-Job -ScriptBlock {
    param($projectRoot)
    Set-Location $projectRoot
    python -m src.server.databricks_permissions_mcp_server
} -ArgumentList $projectRoot

# Wait a moment for the server to start
Start-Sleep -Seconds 2

# Use MCP CLI to list tools
Write-Host "Available tools for managing Databricks permissions and credentials:"
Write-Host "=============================================================="

# Run the Python script to list tools
python -c @"
import asyncio
import json
import subprocess
import sys

async def list_tools():
    # Start the MCP server in a separate process
    server_process = subprocess.Popen(
        [sys.executable, '-m', 'src.server.databricks_permissions_mcp_server'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Wait a moment for the server to start
        await asyncio.sleep(2)
        
        # Initialize the MCP protocol
        init_message = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'initialize',
            'params': {
                'protocolVersion': '2024-11-05',
                'capabilities': {}
            }
        }
        server_process.stdin.write(json.dumps(init_message) + '\n')
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline())
        
        # List available tools
        list_tools_message = {
            'jsonrpc': '2.0',
            'id': 2,
            'method': 'listTools',
            'params': {}
        }
        server_process.stdin.write(json.dumps(list_tools_message) + '\n')
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline())
        
        # Print the tools
        if 'result' in response and 'tools' in response['result']:
            tools = response['result']['tools']
            
            # Group tools by category
            categories = {}
            for tool in tools:
                name = tool['name']
                description = tool['description']
                
                # Determine category based on name
                if 'permission' in name.lower():
                    category = 'Permissions Management'
                elif 'service_principal' in name.lower():
                    category = 'Service Principals'
                elif 'git_credential' in name.lower():
                    category = 'Git Credentials'
                elif 'unity_catalog' in name.lower() or 'catalog' in name.lower() or 'schema' in name.lower() or 'table' in name.lower():
                    category = 'Unity Catalog'
                elif 'share' in name.lower():
                    category = 'Delta Sharing'
                else:
                    category = 'Other'
                
                if category not in categories:
                    categories[category] = []
                
                categories[category].append((name, description))
            
            # Print tools by category
            for category, tools in categories.items():
                print(f"\n{category}:")
                print("-" * len(category) + "---")
                for name, description in tools:
                    print(f"  - {name}: {description}")
        else:
            print("No tools found or error in response")
    
    finally:
        # Shutdown the server
        shutdown_message = {
            'jsonrpc': '2.0',
            'id': 3,
            'method': 'shutdown',
            'params': {}
        }
        server_process.stdin.write(json.dumps(shutdown_message) + '\n')
        server_process.stdin.flush()
        
        # Wait for the server to shut down
        server_process.wait(timeout=5)

asyncio.run(list_tools())
"@

# Stop the background job
Stop-Job -Job $job
Remove-Job -Job $job

Write-Host "`nDone!" 