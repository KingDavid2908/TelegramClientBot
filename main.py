# Import Required Libraries and ensure you have the virtual environment activated when installing the libraries.
from telethon import TelegramClient, events      # For connecting with telegram client API
import os     # For accessing operating system and locating files on your computer
from dotenv import load_dotenv     # For loading environment variables (Variables stored in .env file which are not made accessible on github for privacy reasons by using .gitignore)
from telethon.tl.functions.channels import JoinChannelRequest     # For joining telegram groups
from telethon.tl.types import PeerChannel         # For joining supergroups
import asyncio       # For making your program run asynchronously leading to faster speed than running synchronously

# A personal group id created for experimenting on the bot = -1002427302453. Replace where you see this number with the group id of your choice

# Load environment variables (API_ID and API_HASH) stored in .env file which is not commited in the github repository
load_dotenv()

api_id = int(os.getenv("API_ID"))  
api_hash = os.getenv("API_HASH")  

# Create the Telegram client
client = TelegramClient("session_name", api_id, api_hash)

# 1. Receive messages with the user ID
@client.on(events.NewMessage(incoming=True))   #catch all incoming messages
async def receive_message(event):
    sender = await event.get_sender()
    sender_id = sender.id   #get sender id
    username = sender.username   #get sender username
    message_text = event.message.text   #get the message sent
    print(f"Received message from {username} with an ID({sender_id}) : {message_text}")

    # Don't uncomment the next two lines or the bot would start spamming group messages and replying to all messages
    # Optionally, reply to the message
    #await event.reply(f"Hello! I received your message: {message_text}")


# 2. Send and receive messages in a group
async def send_message_to_group(group_id, message):
    """
    Sends a message to a group by its username or ID.
    """
    entity = PeerChannel(group_id)    # Used Peerchannel since I am trying to access a supergroup. 
    await client.send_message(entity, message)
    print(f"Message sent to group ('{entity}'): {message}")


# Listen to group messages
@client.on(events.NewMessage(chats=PeerChannel(-1002427302453)))  # Replace the number with group id or username for the particular group you want to listen to.
async def group_message_handler(event):
    sender = await event.get_sender()
    if sender is None:  # checks if the sender is None to avoid throwing error if it is a bot or doesn't have the information to be extracted
        print("Sender information not available.")
        return

    # Extract sender information
    sender_id = sender.id 
    group_name = event.chat.title  # access the name of the group
    message_text = event.message.text
    print(f"Received message in group '{group_name}' from {sender_id}: {message_text}")
        

# 3. Send multimedia (image, voice, video) to user or group
async def send_media(recipient, file_path, caption=None): 
    """
    Sends multimedia to a user or group.
    Takes three parameters
    1. Recipent: which is the username of the person you want to send the file.
    2. File Path: which is the location of the file in your local directory
    3. Caption: message you want to send along with the file. # Used None to make it optional
    """
    await client.send_file(recipient, file_path, caption=caption)
    print(f"Media sent to {recipient}: {file_path}")


# 4. Join any group using the client
async def join_group(group_invite_link):
    """
    Joins a group using an invite link.
    """
    group_entity = await client.get_entity(group_invite_link)
    await client(JoinChannelRequest(group_entity))
    print(f"Joined group: {group_entity.title}")


# Start the client and listen for events
async def main():
    await client.start()
    print("Bot started. Listening for events...")

    # Example Usage:
    # Sending a message to a group
    await send_message_to_group(-1002427302453, "I think I am done testing this bot")

    # Sending media to a user
    await send_media("@king_david_2908", "./ProfilePicture.jpg", "Let's use this as our linkedIn profile picture. Check it out at https://www.linkedin.com/in/chukwumam-david-77367a317/")

    # Joining a group
    await join_group("https://t.me/datasciencefun")

    # Keep the bot running
    await client.run_until_disconnected()


# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
