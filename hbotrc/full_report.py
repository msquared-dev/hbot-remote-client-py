import asyncio
import json
import sys
from hbotrc import BotCommands

async def run_full_report(client):
    """Generate and return the full report from the bot."""
    resp = client.full_report()
    return resp.report  # Expecting JSON-compatible structure

def get_client(host, port, username, password, bot_id):
    """Create and return a BotCommands client."""
    return BotCommands(
        host=host,
        port=int(port),
        username='',
        password='',
        bot_id=bot_id,
    )

def main():
    """Main entry point for script execution."""
    if len(sys.argv) < 6:
        print(json.dumps({"error": "Usage: python -m hbotrc.full_report <host> <port> <username> <password> <bot_id>"}))
        sys.exit(1)

    host, port, username, password, bot_id = sys.argv[1:6]

    try:
        client = get_client(host, port, username, password, bot_id)
        result = asyncio.new_event_loop().run_until_complete(run_full_report(client))
        print(result)  # Print JSON result to stdout
    except Exception as e:
        print({"error": f"Error getting full report: {str(e)}"})

if __name__ == "__main__":
    main()
