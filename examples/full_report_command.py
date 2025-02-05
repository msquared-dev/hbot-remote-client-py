#!/usr/bin/env python3

import asyncio
from hbotrc import BotListener, BotCommands


async def run_commands(client):
    resp = client.full_report()
    print(f'Full Report Command Response: {resp}')
    await asyncio.sleep(1)



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Give instance_id argument')
    _id = sys.argv[1]
    client = BotCommands(
        host='localhost',
        port=1883,
        username='',
        password='',
        bot_id=_id,
    )
    asyncio.new_event_loop().run_until_complete(run_commands(client))
