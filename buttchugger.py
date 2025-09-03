import asyncio
import os
import json
import random
from telethon import TelegramClient, errors
from datetime import datetime

# files to track progress because apparently i'm responsible sometimes
PROGRESS_FILE = "buttchugger_progress.json"
# logs to remind myself that i did something today
LOG_FILE = "buttchugger_log.json"

# cursed captions, like my brain on a monday
TROLL_CAPTIONS = [
    "uwu",  # cute but sad
    ":thinking:",  # contemplating existence
    ">:3",  # chaotic energy, unlike me
    "chaos gremlin detected",  # yes, that gremlin is me
    "[auto forwarded]",  # pretend this means something
    "lolol",  # laughter to mask tears
    "poggers",  # a fleeting moment of joy
    "this is cursed",  # just like my life
    "what even is this?",  # existential dread
    "never forget",  # not sure what, maybe my sanity
]

async def main():
    print("=== Buttchugger ===")
    # we begin the descent into digital degeneracy

    # login stuff, aka me giving away my soul to Telegram
    api_id = int(input("API ID: ").strip())
    api_hash = input("API Hash: ").strip()
    phone = input("Phone (+countrycode): ").strip()
    session_name = "buttchugger_session"
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start(phone)
    # oh god, i'm connected, there's no going back

    # sources and targets, like my hopes and dreams, scattered
    sources = input("Enter source channels (comma-separated usernames/IDs): ").split(",")
    targets = input("Enter target channels (comma-separated usernames/IDs): ").split(",")

    # choose what type of media to drag into the void
    print("\nSelect media types (comma-separated numbers):")
    print("1.Documents 2.Photos 3.Videos 4.Audio/Voice 5.Everything")
    media_choices = set(input("Choices: ").split(","))

    # resume from last time because apparently i have a memory
    progress = {}
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)

    # load logs to remind myself i'm actually doing things
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

    # should we forward this sad little message?
    async def should_forward(msg):
        if not msg.media:
            # nothing here, much like my motivation
            return False
        if "5" not in media_choices:
            if "1" in media_choices and msg.document:
                pass  # documents, my life in PDFs
            elif "2" in media_choices and msg.photo:
                pass  # photos, frozen moments of failure
            elif "3" in media_choices and msg.video:
                pass  # videos, moving sadness
            elif "4" in media_choices and (msg.audio or msg.voice):
                pass  # audio, the sound of me crying
            else:
                # skip it, skip my feelings
                return False
        return True

    # loop through sources, i guess
    for source in sources:
        source = source.strip()
        last_id = progress.get(source, 0)
        print(f"\nProcessing {source}, resuming after ID {last_id}")
        # iterating like a zombie through my life choices
        async for msg in client.iter_messages(source, offset_id=last_id):
            try:
                if await should_forward(msg):
                    # decide if today we're extra chaotic
                    if random.random() < 0.5:
                        new_caption = random.choice(TROLL_CAPTIONS)  # full replacement
                    else:
                        # append sadness to existing caption
                        new_caption = (msg.message or "") + " " + random.choice(TROLL_CAPTIONS)

                    for target in targets:
                        # send into the void
                        await client.send_file(
                            target.strip(),
                            msg.media,
                            caption=new_caption
                        )
                        print(f"Forwarded {msg.id} from {source} → {target.strip()} with troll caption")
                        # wow i did something, pat self on back

                    # log it so i can feel productive
                    logs.append({
                        "time": datetime.now().isoformat(),
                        "source": source,
                        "message_id": msg.id,
                        "targets": targets,
                        "caption": new_caption
                    })
                    with open(LOG_FILE, "w") as f:
                        json.dump(logs, f, indent=2)

                # update progress because i'm slightly responsible
                progress[source] = msg.id
                with open(PROGRESS_FILE, "w") as f:
                    json.dump(progress, f, indent=2)

                # take a small existential nap
                await asyncio.sleep(random.uniform(0.5, 3.0))

            except errors.FloodWaitError as e:
                print(f"FloodWait {e.seconds}s, sleeping like a depressed gremlin...")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                # everything's broken, like me
                print(f"Error with msg {msg.id} from {source}: {e}")
                continue

    print("\nAll done! Logs saved in", LOG_FILE)
    # i did it, somehow

if __name__ == "__main__":
    asyncio.run(main())
