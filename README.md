# MCP Server for AWS Resources

This repository contains the implementation of the MCP (Model Context Protocol) server for managing AWS resources. It provides a Python-based server to interact with AWS services using the `boto3` library.

## Features

- Create, delete, and manage AWS resources.
- Built with Python and leverages `boto3` for AWS SDK integration.
- Includes Pydantic for data validation and serialization.
- Designed for extensibility and ease of use.

## Prerequisites

- Python 3.10 or higher
- AWS credentials configured in your environment (e.g., via `~/.aws/credentials` or environment variables)
- Docker 

## Installation

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t mcp-server-aws-resources .
   ```

2. Run the container:
   ```bash
   docker run -i --rm \
     -e AWS_PROFILE=default \
     -v /path/to/.aws:/root/.aws \
     mcp-server-aws-resources:latest
   ```

## Usage

The server exposes endpoints to create and delete AWS resources. Refer to the MCP documentation.

To integrate this server with your system, add the following configuration to your `claude_config.json` file (or a similar configuration file for other LLM host applications):

```json
{
  "mcpServers": {
    "aws-resources": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "AWS_PROFILE=default",
        "-v",
        "/Users/bantwal/.aws:/root/.aws",
        "mcp-server-aws-resources:latest"
      ]
    }
  }
}
```

