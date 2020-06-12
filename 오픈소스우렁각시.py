import discord
import urllib.request
import re
import json

client = discord.Client()

@client.event
async def on_ready():
    print("다음으로 로그인합니다: ") # 화면에 봇의 이름 아이디가 출력
    print(client.user.name)
    print(client.user.id)
    print("=========")
    game = discord.Game("!도움 으로 도움을 받으세요")
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if channel.name == '일반':
            print("on_member_join")
            temp = member.mention + ' 환영의 메시지'
            await channel.send(temp)
            
            json_data = {}
            with open("user.json", "r") as json_file:
                json_data = json.load(json_file)
            
            temp = 0;

            
            
            for i in range(int(json_data['userNum'])):
                if (json_data['user'][i]['id'] == str(member.id)):
                    print(json_data['user'][i]['name'])
                    str(member)
                    temp = 1
                    
            if(temp == 0):
                json_data['user'].append({
                    "name": str(member),
                    "id": str(member.id),
                    "wanning": "0",
                    "kick": "0"
                })
            
                json_data['userNum'] = str(int(json_data['userNum']) + 1)
            
                with open("user.json", 'w') as outfile:
                    json.dump(json_data, outfile, indent=4)
            json_file.close
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!핑'):
        await message.channel.send("퐁")

    if message.content.startswith('!도움'):
        temp = '!환영 : 환영의 메시지. \n!네이버 <검색내용> : 네이버 검색으로 이어지는 링크를 만듭니다.\n!구글 <검색내용> : 구글 검색으로 이어지는 링크를 만듭니다.'
        temp = temp + '\n!파파고 <번역언어2글자> <번역할 내용> : 파파고로 번역합니다. 한영, 영한, 한일, 일한 지원.'
        await message.channel.send(temp)

    if message.content.startswith('!경고 '):
        tempid = message.content[7:len(message.content)-1]
        json_data = {}
        with open("user.json", "r") as json_file:
            json_data = json.load(json_file)
            
        temp = 0;
            
        for i in range(int(json_data['userNum'])):
            print(json_data['user'][i]['id'])
            print(tempid)

            if (json_data['user'][i]['id'] == tempid):
                print(i)

                temp = i

        if(temp != 0):
            user = message.guild.get_member(int(tempid))
            
            if(int(json_data['user'][temp]['kick']) > 2):
                await user.ban(reason=None) 
            elif(int(json_data['user'][temp]['wanning']) > 2):
                json_data['user'][temp]['kick'] = str(int(json_data['user'][temp]['kick']) + 1)
                json_data['user'][temp]['wanning'] = '0'

                with open("user.json", 'w') as outfile:
                    json.dump(json_data, outfile, indent=4)
                json_file.close

                await user.kick(reason=None)

            else:
                json_data['user'][temp]['wanning'] = str(int(json_data['user'][temp]['wanning']) + 1)
                
                with open("user.json", 'w') as outfile:
                    json.dump(json_data, outfile, indent=4)
                json_file.close

            tempStr = "경고 누적 " + json_data['user'][temp]['wanning'] + "회, 킥 누적 " + json_data['user'][temp]['kick'] + "회"    
        else:
            tempStr = "없는 유저입니다."
        await message.channel.send(tempStr)

    if message.content.startswith('!환영'):
        await message.channel.send("환영의 메시지")

    if message.content.startswith('!네이버 '):
        temp = "https://search.naver.com/search.naver?&query=" + message.content[5:len(message.content)]
        await message.channel.send(temp)

    if message.content.startswith('!구글 '):
        temp = "https://www.google.com/search?q=" + message.content[4:len(message.content)]
        await message.channel.send(temp)
        
    if message.content.startswith('!파파고 '):
        client_id = "Hm6MApouvICl3o7fRMPO"
        client_secret = "95U6xiUkGm"

        if (len(message.content) > 5):
            if (message.content[5:7] == '한영'):
                data = "source=ko&target=en&text=" + urllib.parse.quote(message.content[7:len(message.content)])
            elif (message.content[5:7] == '영한'):
                data = "source=en&target=ko&text=" + urllib.parse.quote(message.content[7:len(message.content)])
            elif (message.content[5:7] == '한일'):
                data = "source=ko&target=ja&text=" + urllib.parse.quote(message.content[7:len(message.content)])
            elif (message.content[5:7] == '일한'):
                data = "source=ja&target=ko&text=" + urllib.parse.quote(message.content[7:len(message.content)])
            else:
                data = "source=ko&target=en&text=" + urllib.parse.quote(message.content[5:len(message.content)])
        else:
            data = "source=ko&target=en&text=" + urllib.parse.quote(message.content[5:len(message.content)])

        request = urllib.request.Request("https://openapi.naver.com/v1/papago/n2mt")
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        responseData = json.loads(response.read())
        rescode = response.getcode()
        if(rescode==200):
            temp = responseData['message']['result']['translatedText']
        else:
            temp = "Error Code:" + rescode

        await message.channel.send(temp)
                
    if message.content.startswith('!백과사전 '):
        client_id = "Hm6MApouvICl3o7fRMPO"
        client_secret = "95U6xiUkGm"

        encText = urllib.parse.quote(message.content[6:len(message.content)])
        url = "https://openapi.naver.com/v1/search/encyc.json?display=1&query=" + encText
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        responseData = json.loads(response.read())
        rescode = response.getcode()
        if(rescode==200):
            temp = responseData['items'][0]['description'].replace('<b>', '**').replace('</b>', '**')
        else:
            temp = "Error Code:" + rescode

        await message.channel.send(temp)

            
client.run('NjI2NzM1NjkxNDc2NTAwNDgx.XYybcg.V8EjehxxEiJC4JvKZbv1Pa8pPuY')
