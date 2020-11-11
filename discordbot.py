import discord
from discord import Webhook, RequestsWebhookAdapter
import configparser
import argparse
import time
import numpy
import re

from conditional_model import conditional_model
from CModel import CModel

#room codes
gil_room = 719716464399089715
lr_room = 719988902148178072
yuri_room = 720003297703886929
gaming_room = 720134440411594862
wak_room = 775965189081268265

# webhooks
webhook_gil1 = Webhook.partial(719719440639590400, '1p3kgVBClXhd3GFUzx874tmYLNQjPbTjMZtGPABHj7jgfDhAMZN0PFH1yCQRfgqBGgfU', adapter=RequestsWebhookAdapter())
webhook_gil2 = Webhook.partial(719719628338626561, 'pCem7HKeqCo7yxFEroR-He7z70r8OoesMD2-PeOh-lf4EMVRDkCMQOAZaBTJ4yygszBv', adapter=RequestsWebhookAdapter())

webhook_lr1 = Webhook.partial(720003814316310540, 'QPObBD2sP3cXTsYJaupsZNMp7ZkvjWf2zEmPZ77ueUCxpWlBpqIC0Aq_E9_N0CAOH5LN', adapter=RequestsWebhookAdapter())
webhook_lr2 = Webhook.partial(720003904971997216, 'RqbpGrjN74CdCZbExaI7Bbm_BxMLVKqMjVpZMMldwzMDF6Kn3OmipTtaZ9e2mCLsVQiz', adapter=RequestsWebhookAdapter())

webhook_gaming = Webhook.partial(720138814571544668, '1W4syMnRBn1DsTl0xFD0PgvRuPpNZyv7_PWiZa6E6wZYyPQHx8tEHIgswAHdr7eILEAW', adapter=RequestsWebhookAdapter())

webhook_wak = Webhook.partial(720138814571544668, 'H5fArbRbHvq3KvzWis4cxuEEfEI4Xe4-gIOWs2Ea3OB4jFMF5SYjdqjdgmcvl0n-8ekc', adapter=RequestsWebhookAdapter())


gaming_dict = {"simplex":"https://cdn.discordapp.com/avatars/221888287533563904/b023d075d2d907feefbc4bf64b5d3e5b.png", "rlin":"https://cdn.discordapp.com/avatars/217870308433068033/f57d543fd16b0f35c443a1edbe37e16b.png", "surfaceintegral": "https://cdn.discordapp.com/avatars/355217077037957122/c2dd8c5bb4aef833433a4aed669bc60e.png", "Marblelemons": "https://cdn.discordapp.com/avatars/150039751888601088/7c76d2fa79b905328c727b111190ea90.png", "Chet": "https://cdn.discordapp.com/avatars/274050798403452928/aa6f1b3c069487dc3d94ac7a540b3bf2.png", "Minimax": "https://cdn.discordapp.com/avatars/171729697082834944/11b0695ea1d153057d27ac1e93554ae4.png", "An1ket":"https://cdn.discordapp.com/avatars/222217668026040325/fe4c239ca5b9abd155fc7c5fa7cf6e27.png"}
gil_dict = { "STAS1S_OW":
   'https://cdn.discordapp.com/avatars/157331161054445568/a_2a973ccfff1e90d18d39200c32912dea.gif',
  "Marblelemons":
   'https://cdn.discordapp.com/avatars/150039751888601088/a_5081ef5d46f5e0cd10d579ead9a85242.gif',
  "AlbatroS":
   'https://cdn.discordapp.com/avatars/150050060598640647/44eac98bef6788270928203ffc1ae816.png',
  "simplex":
   'https://cdn.discordapp.com/avatars/221888287533563904/b023d075d2d907feefbc4bf64b5d3e5b.png',
  "Chloechoo":
   'https://cdn.discordapp.com/avatars/230557878619078656/ea9e068665275ad7d4a11603196bc52f.png',
  "An1ket":
   'https://cdn.discordapp.com/avatars/222217668026040325/fe4c239ca5b9abd155fc7c5fa7cf6e27.png',
  "DarkAngel":
   'https://cdn.discordapp.com/avatars/289258110420254722/5823c357e13d39a3e4362704e32747c5.png',
  "theaudacity":
   'https://cdn.discordapp.com/avatars/253673311412813827/4124a5a76d76fec9d2ea66fca070a621.png',
  "rlin":
   'https://cdn.discordapp.com/avatars/217870308433068033/f57d543fd16b0f35c443a1edbe37e16b.png',
  "Scipio":
   'https://cdn.discordapp.com/avatars/165329466803879936/8f7a50599a22acbf0b6163cdb3ebec6e.png',
  "Tatsu":
   'https://cdn.discordapp.com/avatars/172002275412279296/f5f65755f67ae1dc88d9bb271d0f5bef.png',
  "Interstellar":
   'https://cdn.discordapp.com/avatars/348596248565121036/a_038c4cb65b5e9037df68508a05315c18.gif',
  "Minimax":
   'https://cdn.discordapp.com/avatars/171729697082834944/11b0695ea1d153057d27ac1e93554ae4.png',
  "proplayer101":
   'https://cdn.discordapp.com/avatars/289983109024186369/d74f687cf08ff6feb422b6ce33fb82df.png',
  "Ayana":
   'https://cdn.discordapp.com/avatars/185476724627210241/50a12a857cbdbdb85c8bc3dc7ba8f1f0.png',
  "Pringles":
   'https://cdn.discordapp.com/avatars/150782393601622016/a2f6b0bf22eb098e6f78346597db3547.png',
  "FryingHamster": 'https://cdn.discordapp.com/embed/avatars/3.png',
  'Vinay (FOZ)':
   'https://cdn.discordapp.com/avatars/313813512931508225/7a9eadf080f67e9a7056409fea143c71.png',
  "yokedoodle":
   'https://cdn.discordapp.com/avatars/231870473338617856/627c70e14e59b4bd7a8d1770ce66dca7.png',
  "SqrtOfPi":
   'https://cdn.discordapp.com/avatars/291041817795756042/efe1ed455d713cd4c3170ba3b26721ee.png',
  "surfaceintegral":
   'https://cdn.discordapp.com/avatars/355217077037957122/c2dd8c5bb4aef833433a4aed669bc60e.png',
  "UserName":
   'https://cdn.discordapp.com/avatars/461697769565061120/8342cf22b6be4f6971d1a231e1dc7b96.png',
  'ҒŁॆฟ » ΌภωαяÐ': 'https://cdn.discordapp.com/embed/avatars/1.png',
  "Chet":
   'https://cdn.discordapp.com/avatars/274050798403452928/aa6f1b3c069487dc3d94ac7a540b3bf2.png',
  "evt":
   'https://cdn.discordapp.com/avatars/150043134754029568/2fe657c5d2bca549e7e8af514ce5b6a7.png',
  "ani":
   'https://cdn.discordapp.com/avatars/284507912615755776/e6a208c9f7ef200aace76c2545e137d1.png',
  'I am left brazo':
   'https://cdn.discordapp.com/avatars/397470820638654464/62df56449e980a632634b86ee5557052.png',
  'Cissy ♡':
   'https://cdn.discordapp.com/avatars/320378801869553664/c432d81562bd4e13a21a166ad9738131.png',
  "SubwaySandwiches":
   'https://cdn.discordapp.com/avatars/193806857184215041/8a792d766351ec27337695d2722a45de.png',
  'I am vegetable hooker':
   'https://cdn.discordapp.com/avatars/213452299731861504/692cfd9a9643cbb859da81fc0cb91dae.png',
  "simplegeometry":
   'https://cdn.discordapp.com/avatars/168211034706935809/dcc368884dfc0a43fd0c3892bf9f652f.png',
  'World Time':
   'https://cdn.discordapp.com/avatars/447266583459528715/bc6d8794326ef2fd57690a852eefde1b.png',
  'YAGPDB.xyz':
   'https://cdn.discordapp.com/avatars/204255221017214977/2fa57b425415134d4f8b279174131ad6.png',
  "FJfighter":
   'https://cdn.discordapp.com/avatars/249054955263098881/2568dc45cef144b36f705660183068ba.png',
  'd🔺lta':
   'https://cdn.discordapp.com/avatars/420447320430346246/6bc30cf8eacdc11799eb00356869ef83.png',
  "RayToo":
   'https://cdn.discordapp.com/avatars/428331874318942218/955dcca23809bc17bf60f2e9f1dae478.png',
  "RayBot":
   'https://cdn.discordapp.com/avatars/591021209685327945/b5ef687a396cbe009da0c38eed70941d.png',
  "Golgo":
   'https://cdn.discordapp.com/avatars/108380548413571072/08d9d043a2f9cc2b1514b7766ef4ddd2.png',
  "Silver_sniper67": 'https://cdn.discordapp.com/embed/avatars/4.png',
  'uncomfortable cat':
   'https://cdn.discordapp.com/avatars/166316524188073984/a_2a219cf6abc852892475ced64920e262.gif',
  "Mythbustman":
   'https://cdn.discordapp.com/avatars/129753745549557760/0921373f98eba589ef5cd8f714180eac.png',
  'Dad Bot':
   'https://cdn.discordapp.com/avatars/503720029456695306/107fc57eb6e92993400c329380e3d71b.png',
  "Nishiki":
   'https://cdn.discordapp.com/avatars/320821848130715649/a654a5c4e069726c9631739333ab6e85.png',
  "helloserina":
   'https://cdn.discordapp.com/avatars/467025796863885315/cc5d25d8b7d9ad1e3455d69d026d5b7f.png',
  'chillax bro':
   'https://cdn.discordapp.com/avatars/396179573668052993/409d6452627924b8f86110362fbe1c4e.png',
  "aazhengg":
   'https://cdn.discordapp.com/avatars/287014078734663683/36b1067e6519447c9b9d32909569cec1.png',
  'Tyler McNierney':
   'https://cdn.discordapp.com/avatars/642804806393659404/9abc6491390bc81bc6a9c0372e9077dc.png',
  '<fkje>moonryu':
   'https://cdn.discordapp.com/avatars/167849013003943936/6385dd19583798f5c0960526fabf4e84.png',
  "sinpi":
   'https://cdn.discordapp.com/avatars/152161715545440256/820f61bf33257dd1a8f3e0e5157fa4d0.png',
  "Guilded":
   'https://cdn.discordapp.com/avatars/216816090712506378/c532cc755224b3860a7484009dd03683.png',
  "Bonfire":
   'https://cdn.discordapp.com/avatars/183749087038930944/bb87e8cd14defbb679ec8f761c796d52.png',
  'Rythm 2':
   'https://cdn.discordapp.com/avatars/252128902418268161/87108885d0914c63a4d54cefb56306f0.png',
  'SŦǍŜ1Ŝ(瘀)':
   'https://cdn.discordapp.com/avatars/568220099442376724/1298918a56f622fdb49886de623d7aa9.png',
  "lineintegral":
   'https://cdn.discordapp.com/avatars/568222647352033282/7ebee73dfc97bef1227a8829d9f3aba8.png',
  "GamesROB":
   'https://cdn.discordapp.com/avatars/383995098754711555/64b98adf6267a6513cd1f9409b49cd28.png',
  "lilMinimax":
   'https://cdn.discordapp.com/avatars/707078522513915924/f302350000c8b39d421821c12c82b5b9.png' }

client = discord.Client()
config = ""
gil_model = ""
lr_model = ""
yuri_model = ""
gaming_model = ""

wak_model = ""


@client.event
async def on_message(message): #when someone sends a message
    if message.channel.id == gil_room and message.author != client.user and not message.author.bot:
        #await message.channel.send("test on message") #send a good morning message
        print(message.author.id)
        await message.channel.send("Received Request. Please wait patiently for generation "+message.author.mention)
        sentences = []
        sentences.append(message.content)
        #d = conditional_model(model_name=config.get('model', 'model_size'),temperature=0.75,seed=4,sentences=sentences)
        #d = conditional_model(model_name='GIL',temperature=float(config.get('decoder', 'temperature')),seed=numpy.random.randint(1,100000),sentences=sentences)
        d = gil_model.runModel(sentences, numpy.random.randint(1,100000))
        await message.channel.send("Now responding to request '"+ message.content+"' from "+message.author.mention)
        for i in d:
            listofmessages = d[i].split('\n')
            print(listofmessages)
            current_user_is_1 = True
            for x in listofmessages:
                x = x.replace("@everyone", "@ everyone")
                x = x.replace("@here", "@ here")
                # if(x != "<|end of text|>"):
                #     numwait = len(x) / 10
                #     if numwait < 1:
                #         numwait = 1
                #     elif numwait > 3:
                #         numwait = 3
                #     time.sleep(numwait)
                #     if(current_user_is_1):
                #         if(len(x)>0):
                #             webhook_gil1.send(x)
                #     else:
                #         if(len(x)>0):
                #             webhook_gil2.send(x)
                # else:
                #     current_user_is_1 = not current_user_is_1
                myRegexp = r"\[(.*)\]"
                match = re.findall(myRegexp, x)
                name ="No Name"
                try:
                    name = match[0]
                except IndexError:
                    name = "No Name"
                x = re.sub(myRegexp, "", x).strip()
                if(x != "<|end of text|>"):
                    numwait = len(x) // 8
                    if numwait < 1:
                        numwait = 1
                    elif numwait > 3:
                        numwait = 3
                    time.sleep(numwait)
                    if(len(x)>0):
                        webhook_gil1.send(x, username=name, avatar_url=gil_dict.get(name))
        await message.channel.send("Finished request from "+message.author.mention)
    elif message.channel.id == wak_room and message.author != client.user and not message.author.bot:
        await message.channel.send("Received Request. Please wait patiently for generation "+message.author.mention)
        sentences = []
        sentences.append(message.content)
        d = wak_model.runModel(sentences, numpy.random.randint(1,100000))
        await message.channel.send("Now responding to request '"+ message.content+"' from "+message.author.mention)
        for i in d:
            listofmessages = d[i].split('\n')
            print(listofmessages)
            current_user_is_1 = True
            for x in listofmessages:
                x = x.replace("@everyone", "@ everyone")
                x = x.replace("@here", "@ here")
                myRegexp = r"\[(.*)\]"
                match = re.findall(myRegexp, x)
                name ="No Name"
                try:
                    name = match[0]
                except IndexError:
                    name = "No Name"
                x = re.sub(myRegexp, "", x).strip()
                if(x != "<|end of text|>"):
                    numwait = len(x) // 8
                    if numwait < 1:
                        numwait = 1
                    elif numwait > 3:
                        numwait = 3
                    time.sleep(numwait)
                    if(len(x)>0):
                        webhook_wak.send(x, username=name)
        await message.channel.send("Finished request from "+message.author.mention)
    elif message.channel.id == lr_room and message.author != client.user and not message.author.bot:
        await message.channel.send("Received Request. Please wait patiently for generation "+message.author.mention)
        sentences = []
        sentences.append(message.content)
        #d = conditional_model(model_name=config.get('model', 'model_size'),temperature=0.75,seed=4,sentences=sentences)
        #d = conditional_model(model_name='LR',temperature=float(config.get('decoder', 'temperature')),seed=numpy.random.randint(1,100000),sentences=sentences)
        d = lr_model.runModel(sentences, numpy.random.randint(1,100000))
        await message.channel.send("Now responding to request '"+ message.content+"' from "+message.author.mention)
        for i in d:
            listofmessages = d[i].split('\n')
            print(listofmessages)
            current_user_is_1 = True
            for x in listofmessages:
                x = x.replace("@everyone", "@ everyone")
                x = x.replace("@here", "@ here")
                if(x != "<|end of text|>"):
                    numwait = len(x) // 10
                    if numwait < 1:
                        numwait = 1
                    elif numwait > 3:
                        numwait = 3
                    time.sleep(numwait)
                    if(current_user_is_1):
                        if(len(x)>0):
                            webhook_lr1.send(x)
                    else:
                        if(len(x)>0):
                            webhook_lr2.send(x)
                else:
                    current_user_is_1 = not current_user_is_1
        await message.channel.send("Finished request from "+message.author.mention)
    elif message.channel.id == yuri_room and message.author != client.user and not message.author.bot:
        await message.channel.send("Received Request. Please wait patiently for generation "+message.author.mention)
        sentences = []
        sentences.append(message.content)
        #d = conditional_model(model_name=config.get('model', 'model_size'),temperature=0.75,seed=4,sentences=sentences)
        d = yuri_model.runModel(sentences, numpy.random.randint(1,100000))
        #d = conditional_model(model_name='yuri',temperature=float(config.get('decoder', 'temperature')),seed=numpy.random.randint(1,100000),sentences=sentences)
        await message.channel.send("Now responding to request '"+ message.content+"' from "+message.author.mention)
        for i in d:
            await message.channel.send(d[i])
        await message.channel.send("Finished request from "+message.author.mention)
    elif message.channel.id == gaming_room and message.author != client.user and not message.author.bot:
        await message.channel.send("Received Request. Please wait patiently for generation "+message.author.mention)
        sentences = []
        sentences.append(message.content)
        #d = conditional_model(model_name=config.get('model', 'model_size'),temperature=0.75,seed=4,sentences=sentences)
        d = gaming_model.runModel(sentences, numpy.random.randint(1,100000))
        #d = conditional_model(model_name='gaming',temperature=float(config.get('decoder', 'temperature')),seed=numpy.random.randint(1,100000),sentences=sentences)
        await message.channel.send("Now responding to request '"+ message.content+"' from "+message.author.mention)
        for i in d:
            listofmessages = d[i].split('\n')
            print(listofmessages)
            for x in listofmessages:
                x = x.replace("@everyone", "@ everyone")
                x = x.replace("@here", "@ here")
                if(x != "<|end of text|>"):
                    myRegexp = r"\[(.*)\]"
                    match = re.findall(myRegexp, x)
                    name ="No Name"
                    try:
                        name = match[0]
                    except IndexError:
                        name = "No Name"
                    x = re.sub(myRegexp, "", x).strip()
                    if(x != "<|end of text|>"):
                        numwait = len(x) // 8
                        if numwait < 1:
                            numwait = 1
                        elif numwait > 3:
                            numwait = 3
                        time.sleep(numwait)
                        if(len(x)>0):
                            webhook_gaming.send(x, username=name, avatar_url=gaming_dict.get(name))
        await message.channel.send("Finished request from "+message.author.mention)

def main():
    global config
    global gil_model
    global lr_model
    global yuri_model
    global gaming_model
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', type=str, default="chatbot.cfg")
    args = arg_parser.parse_args()
    # Read the config
    config = configparser.ConfigParser(allow_no_value=True)
    with open(args.config) as f:
        config.read_file(f)
    gil_model = CModel(model_name="GIL", temperature= float(config.get('decoder', 'temperature')))
    #lr_model = CModel(model_name="LR", temperature= float(config.get('decoder', 'temperature')))
    yuri_model = CModel(model_name="yuri", temperature= float(config.get('decoder', 'temperature')))
    gaming_model = CModel(model_name="gaming", temperature= float(config.get('decoder', 'temperature')))
    wak_model = CModel(model_name="wak", temperature= float(config.get('decoder', 'temperature')))

    client.run(config.get('chatbot', 'discord_token'))

if __name__ == '__main__':
    main()
