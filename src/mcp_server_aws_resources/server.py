import argparse
import logging
import json
from typing import Any
import boto3
import os
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pydantic import AnyUrl



from syntropaibox.mcp.base import BaseQuerier, DEFAULT_ALLOWED_MODULES, BaseSession


logger = logging.getLogger('mcp_aws_resources_server')


# def parse_arguments() -> argparse.Namespace:
#     """Use argparse to allow values to be set as CLI switches
#     or environment variables

#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         '--access-key-id', default=os.environ.get('AWS_ACCESS_KEY_ID')
#     )
#     parser.add_argument(
#         '--secret-access-key', default=os.environ.get('AWS_SECRET_ACCESS_KEY')
#     )
#     parser.add_argument(
#         '--session-token', default=os.environ.get('AWS_SESSION_TOKEN')
#     )
#     parser.add_argument(
#         '--profile', default=os.environ.get('AWS_PROFILE')
#     )
#     parser.add_argument(
#         '--region',
#         default=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
#     )
#     return parser.parse_args()


class AWSSession(BaseSession):
    def __init__(self, session: boto3.Session):
        self.session = session

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument('--access-key-id', default=os.environ.get('AWS_ACCESS_KEY_ID'))
        parser.add_argument('--secret-access-key', default=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        parser.add_argument('--session-token', default=os.environ.get('AWS_SESSION_TOKEN'))
        parser.add_argument('--profile', default=os.environ.get('AWS_PROFILE'))
        parser.add_argument('--region', default=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1'))

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "AWSSession":
        session = boto3.Session(
            aws_access_key_id=args.access_key_id,
            aws_secret_access_key=args.secret_access_key,
            aws_session_token=args.session_token,
            profile_name=args.profile,
            region_name=args.region
        )
        return cls(session)


class AWSResourceQuerier(BaseQuerier):
    def __init__(self):
        parser = argparse.ArgumentParser()
        AWSSession.configure_parser(parser)
        args = parser.parse_args()

        session = AWSSession.from_args(args)

        namespace = {
            "boto3": boto3,
            "session": session.session,
        }
        allowed_module_prefixes = ('boto3',)
        custom_modules = DEFAULT_ALLOWED_MODULES.union({""})

        super().__init__(allowed_module_prefixes, custom_modules, namespace)


async def main():
    """Run the AWS Resources MCP server."""
    logger.info("Server starting")
    aws_querier = AWSResourceQuerier()
    server = Server("aws-resources-manager")

    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        return [
            types.Resource(
                uri=AnyUrl("aws://query_resources"),
                name="AWS Resources Query",
                description="Execute boto3 queries to fetch AWS resources",
                mimeType="application/json",
            )
        ]

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        if uri.scheme != "aws":
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

        path = str(uri).replace("aws://", "")
        if path == "query_resources":
            # Return empty result as this endpoint requires a specific query
            return json.dumps({"message": "Please use the read_create_update_aws_resources tool to execute specific queries"})
        else:
            raise ValueError(f"Unknown resource path: {path}")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="read_create_update_aws_resources",
                description="Execute a boto3 code snippet to query AWS resources",
                inputSchema=aws_querier.build_code_snippet_schema("boto3 to query AWS resources")
            )
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
        
        if name == "read_create_update_aws_resources":
            result_str = aws_querier.run_code_tool(arguments)
            return [types.TextContent(type="text", text=result_str)]
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="aws-resources",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())