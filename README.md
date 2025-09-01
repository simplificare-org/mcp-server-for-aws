# AWS MCP Server - SyntropAI Ecosystem

**Part of the [SyntropAI MCP Ecosystem](https://github.com/paihari/documentation-syntropai)** - A unified multi-cloud abstraction framework.

This MCP (Model Context Protocol) server provides secure, dynamic access to AWS services through the innovative SyntropAI abstraction layer. Unlike traditional hardcoded service catalogs, this server supports **any AWS service** through dynamic SDK access with built-in security sandboxing.

## 🚀 Key Features

- **Universal AWS Access**: Dynamic access to all AWS services without hardcoded limitations
- **Secure Code Execution**: AST-based validation and sandboxed execution environment
- **Provider-Agnostic Design**: Built on SyntropAI's unified abstraction pattern
- **Future-Proof Architecture**: Automatically supports new AWS services without updates
- **Docker Containerization**: Production-ready deployment

## 🏗️ Architecture

This server implements the SyntropAI abstraction pattern:

```
Claude Desktop → MCP Protocol → AWS MCP Server → SyntropAIBox → boto3 → AWS Services
```

### Core Components:
- **AWSSession**: Unified AWS credential management using `BaseSession`
- **AWSResourceQuerier**: Secure query execution extending `BaseQuerier`  
- **AST Sandbox**: Safe code execution with timeout protection
- **Dynamic Schema**: Runtime API documentation generation

## 📋 Prerequisites

- Python 3.10 or higher
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM roles)
- Docker (recommended)
- [SyntropAIBox](https://test.pypi.org/project/syntropaibox/) core library

## 🐳 Docker Installation (Recommended)

### Build and Run
```bash
# Build the image
docker build -t mcp-server-aws-resources .

# Run with AWS profile
docker run -i --rm \
  -e AWS_PROFILE=default \
  -v ~/.aws:/root/.aws \
  mcp-server-aws-resources:latest

# Run with environment variables
docker run -i --rm \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_DEFAULT_REGION=us-east-1 \
  mcp-server-aws-resources:latest
```

## ⚙️ Claude Desktop Integration

Add to your `claude_config.json`:

```json
{
  "mcpServers": {
    "aws-resources": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "AWS_PROFILE=default", 
        "-v", "/Users/yourusername/.aws:/root/.aws",
        "mcp-server-aws-resources:latest"
      ]
    }
  }
}
```

## 🛡️ Security Features

### AST-Based Validation
- Prevents malicious code injection
- Whitelisted imports and functions
- Controlled execution environment

### Safe Execution
- Timeout protection (2-second default)
- Isolated namespace
- JSON-serialized responses

### Example Safe Query
```python
# User provides this code snippet:
import boto3
ec2 = session.client('ec2')
result = ec2.describe_instances()
```

The system:
1. ✅ Validates AST syntax
2. ✅ Checks allowed imports (`boto3` approved)  
3. ✅ Executes in sandbox with timeout
4. ✅ Returns JSON-serialized results

## 🔧 Usage Examples

### List EC2 Instances
```python
import boto3
ec2 = session.client('ec2')
result = ec2.describe_instances()
```

### Create S3 Bucket
```python  
import boto3
s3 = session.client('s3')
result = s3.create_bucket(Bucket='my-unique-bucket-name')
```

### Lambda Functions
```python
import boto3
lambda_client = session.client('lambda')
result = lambda_client.list_functions()
```

## 🌟 SyntropAI Ecosystem Benefits

### Unified Multi-Cloud
- Same patterns work across AWS, Azure, OCI
- Consistent authentication and error handling
- Provider-agnostic abstractions

### Non-Hardcoded Services
- Supports **any** AWS service automatically
- No service catalog limitations
- Future services work immediately

### Enterprise Ready
- Security-first design
- Docker containerization
- Comprehensive logging

## 🔗 Related Projects

- **[Main Documentation](https://github.com/paihari/documentation-syntropai)**: Complete ecosystem overview and architecture
- **[SyntropAIBox Core](https://test.pypi.org/project/syntropaibox/)**: Shared abstraction library
- **[Azure MCP Server](../mcp-server-azure)**: Azure implementation  
- **[OCI MCP Server](../mcp-server-oci)**: Oracle Cloud implementation
- **[Finviz MCP Server](../mcp_finviz)**: Financial data server

## 🏆 Technical Highlights

This implementation showcases:
- **Advanced Abstraction Patterns**: Clean separation of concerns
- **Security Engineering**: AST validation and sandboxed execution  
- **Cloud Architecture**: Scalable, maintainable multi-cloud design
- **DevOps Excellence**: Containerized, configurable deployment

## 📞 Support

For questions about the SyntropAI MCP ecosystem:
- **Documentation**: [SyntropAI Documentation Project](https://github.com/paihari/documentation-syntropai)
- **Author**: Hari Bantwal (hpai.bantwal@gmail.com)

---

*This server demonstrates cutting-edge cloud abstraction technology, providing secure, unified access to AWS services through innovative architectural patterns.*