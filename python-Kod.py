import tracemalloc
import requests
import asyncio
from telegram import Bot

# Enable tracemalloc
tracemalloc.start()

# Replace 'YOUR_THINGSPEAK_API_KEY' with your ThingSpeak API key
thingspeak_api_key = 'CO4NCKIR4JRLUTCU'
thingspeak_channel_id = '2379138'

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your Telegram bot token
telegram_bot_token = '6966539103:AAFSMbqWAHf7dTFPue6TQrHOnXunlGYbiGs'
telegram_chat_id = '6366006828'

# Gas counter threshold (adjust as needed)
gas_counter_threshold = 1000
gas_counter = 0

async def get_thingspeak_data():
    url = f'https://api.thingspeak.com/channels/2379138/fields/1.json?api_key=CO4NCKIR4JRLUTCU&results=2'
    params = {'api_key': thingspeak_api_key, 'results': 2}
    response = await loop.run_in_executor(None, lambda: requests.get(url, params=params))
    data = response.json()
    return data['feeds'][0] if 'feeds' in data else None

async def send_telegram_message(message):
    bot = Bot(token=telegram_bot_token)
    await bot.send_message(chat_id=telegram_chat_id, text=message)

# Main script
async def main():
    global gas_counter
    while True:
        try:
            # Get ThingSpeak data
            thingspeak_data = await get_thingspeak_data()

            if thingspeak_data:
                # Extract relevant information from ThingSpeak data
                field1_value = int(thingspeak_data.get('field1', '0'))
                created_at = thingspeak_data.get('created_at', 'N/A')

                # Check if gas level is above threshold
                if field1_value > gas_counter_threshold:
                    gas_counter += 1

                    # Compose message with gas detection information
                    message = f"Gas detected!\nGas counter: {gas_counter}\nGas level: {field1_value} PPM\nTimestamp: {created_at}"

                    # Send message to Telegram
                    await send_telegram_message(message)
                    print("Significant gas detected. Message sent to Telegram.")
                else:
                    print("No significant gas detected.")

            else:
                print("Error fetching ThingSpeak data.")

        except Exception as e:
            print(f"General error: {e}")

        # Delay between iterations (in seconds)
        await asyncio.sleep(60)  # Adjust the delay as needed

# Create a new event loop explicitly
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Run the event loop
loop.run_until_complete(main())

# Print object allocation traceback
print(tracemalloc.get_object_traceback(tracemalloc.get_traced_memory()))

