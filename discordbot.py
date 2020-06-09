import discord
from discord import Webhook, RequestsWebhookAdapter
import configparser
import argparse

from conditional_model import conditional_model

#room codes
gil_room = 719716464399089715

# webhooks
webhook_gil1 = Webhook.partial(719719440639590400, '1p3kgVBClXhd3GFUzx874tmYLNQjPbTjMZtGPABHj7jgfDhAMZN0PFH1yCQRfgqBGgfU', adapter=RequestsWebhookAdapter())
webhook_gil2 = Webhook.partial(719719628338626561, 'pCem7HKeqCo7yxFEroR-He7z70r8OoesMD2-PeOh-lf4EMVRDkCMQOAZaBTJ4yygszBv', adapter=RequestsWebhookAdapter())

client = discord.Client()
config = ""

@client.event
async def on_message(message): #when someone sends a message
    if message.channel.id == gil_room and message.author != client.user and not message.author.bot:
        #await message.channel.send("test on message") #send a good morning message
        print(message.author.id)
        await message.channel.send("Received Request. Please wait patiently for generation "+message.author.mention)
        sentences = []
        sentences.append(message.content)
        d = conditional_model(model_name=config.get('model', 'model_size'),temperature=0.75,seed=4,sentences=sentences)
        for i in d:
            listofmessages = d[i].split('\n')
            print(listofmessages)
            current_user_is_1 = True
            for x in listofmessages:
                if(x != "<|end of text|>"):
                    if(current_user_is_1):
                        webhook_gil1.send(x, username='GIL1')
                    else:
                        webhook_gil2.send(x, username='GIL2')
                else:
                    current_user_is_1 = not current_user_is_1

def main():
    global config
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', type=str, default="chatbot.cfg")
    args = arg_parser.parse_args()
    # Read the config
    config = configparser.ConfigParser(allow_no_value=True)
    with open(args.config) as f:
        config.read_file(f)
    client.run(config.get('chatbot', 'discord_token'))

if __name__ == '__main__':
    main()