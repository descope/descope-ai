# Basic Usage Example

This example demonstrates basic usage of the MCP Descope SDK for fetching user and tenant tokens.

## Prerequisites

- Python 3.8 or higher
- Descope project with outbound applications configured

## Setup

### Option 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to this directory
cd examples/basic_usage

# Install dependencies
uv sync

# Run the example
uv run python basic_usage.py
```

### Option 2: Using pip

```bash
# Navigate to this directory
cd examples/basic_usage

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the SDK in development mode from the root directory
cd ../..
pip install -e .
cd examples/basic_usage

# Run the example
python basic_usage.py
```

## Configuration

Set the following environment variables before running:

```bash
export DESCOPE_PROJECT_ID="your-project-id"
export DESCOPE_MANAGEMENT_KEY="your-management-key"
```

Or create a `.env` file in this directory:

```
DESCOPE_PROJECT_ID=your-project-id
DESCOPE_MANAGEMENT_KEY=your-management-key
```

## What This Example Shows

- Fetching user tokens with specific scopes
- Fetching user tokens without scopes
- Fetching tenant tokens with specific scopes
- Fetching tenant tokens without scopes
- Error handling

## Running

```bash
python basic_usage.py
```
