import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
import random

class Fun(Cog):
    def __init__(self, client):
        self.client = client

    ### EVENTS ###
    
    @Cog.listener()
    async def on_ready(self):
        print('Fun cog for bot is online.')


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            channel = message.channel
            msg = message.content.lower()
            say = msg.startswith

            ## Good bot ##
            if say('good bot'):
                happy = [':smile:', '^_^', ':blush:', ':kissing_heart:', ':smiling_face_with_3_hearts:', ':sob: :heart:',
                ':kissing_closed_eyes:', ':heart_eyes:', ':smiley:', ':heart:', '<:1happy:760407392969818112>']
                await channel.send(f'{random.choice(happy)}')

            if say('goo bot'):
                await channel.send('GOO bot? :confounded:')

            if say('good boot'):
                await channel.send(":hiking_boot:")
                await channel.send("These boots were made for walking.")

            if say('bad bot'):
                await channel.send("I'm sorry :sob:")

            if say('damn the tremere'):
                await channel.send('https://cdn.discordapp.com/attachments/821291420458418236/821830278648430642/0ivq9l2mfx531.png')

            if say(('brujah bear', 'dimi the bear')):
                await channel.send("https://cdn.discordapp.com/attachments/780155399504134157/823078693945081886/AB6JhC8.jpg")

            if say(('d i love you', 'i love you d', 'd, i love you', 'i love you, d')):
                await channel.send("<a:0hearts:841074116618223637>")


    ### COMMANDS ###

    @command(aliases=['pc'])
    async def peacock(self, ctx):
        peacock_pic = ['https://www.onegreenplanet.org/wp-content/uploads/2020/05/shutterstock_567926224-1536x1024.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Peacock_Plumage.jpg/1280px-Peacock_Plumage.jpg',
        'https://resize.hswstatic.com/w_828/gif/peacock-feathers.jpg',
        'https://pyxis.nymag.com/v1/imgs/2ae/a6c/1989c87daca92bac5c472990bbf5694334-rowdy-peacock.jpg',
        'https://www.wideopenpets.com/wp-content/uploads/2020/01/Peacock-in-full-color.png',
        'https://i.guim.co.uk/img/media/fc9fe5200c6a3f35f2a8e24dcc596b6d3639a5c6/0_125_2336_1401/master/2336.jpg?width=620&quality=85&auto=format&fit=max&s=e765649b0ca5e650f6fa9a472d8b9109',
        'https://animal4u.files.wordpress.com/2013/01/peacock2.jpg',
        'https://animal4u.files.wordpress.com/2013/01/peacock.jpg',
        'https://s.wsj.net/public/resources/images/B3-CS117_HoWRow_M_20181219153434.jpg',
        'https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iU5u1orulcgQ/v1/-1x-1.jpg',
        'https://www.advancedsciencenews.com/wp-content/uploads/2020/05/peacock-feathers-3013486_1280.jpg',
        'https://news.umanitoba.ca/wp-content/uploads/2015/03/Head_Peacock.jpg',
        'https://news.umanitoba.ca/wp-content/uploads/2016/04/bdoPOQ7-Imgur.gif',
        'https://media0.giphy.com/media/9Y5thftRDHmGpkGhEi/giphy-downsized-large.gif',
        'https://media.giphy.com/media/61Re9DsXj8LIM1CxTi/giphy.gif',
        'https://thumbs.gfycat.com/CommonAromaticDodo-size_restricted.gif',
        'https://toronto.citynews.ca/wp-content/blogs.dir/sites/10/2020/07/06/maail-mDr9qzGbAD8-unsplash-scaled.jpg',
        'https://images.saymedia-content.com/.image/c_limit%2Ccs_srgb%2Cq_auto:good%2Cw_435/MTczOTIyMzg1MTI3NjEzNTA0/the-proud-peackcock-eight-fun-facts-on-the-indian-peacock.webp',
        'https://images.saymedia-content.com/.image/c_limit%2Ccs_srgb%2Cq_auto:good%2Cw_468/MTc0NjQxMDAyNjgwOTUyODIy/the-proud-peackcock-eight-fun-facts-on-the-indian-peacock.webp',
        'https://media.giphy.com/media/2495p4BproMwPteJxR/giphy.gif',
        'https://tenor.com/view/peacock-dont-go-stay-hold-on-kitty-gif-12645116',
        'https://tenor.com/view/peacock-nature-beautiful-bird-feathers-gif-15474292',
        'https://tenor.com/view/beauty-peacock-strut-strutting-chest-out-gif-9995368',
        'https://tenor.com/view/peacock-gif-10264455',
        'https://tenor.com/view/peacock-scream-what-gif-12645123',
        'https://tenor.com/view/nat-geo-nat-geo-wild-worlds-weirdest-weird-animals-animals-gif-5502245',
        'https://media.giphy.com/media/9Y5thftRDHmGpkGhEi/giphy.gif',
        'https://media.giphy.com/media/Q8rZSkY7TnonOtYrEf/giphy.gif',
        'https://media.giphy.com/media/cJLsav7RcSehOvtQNg/giphy.gif',
        'https://media.giphy.com/media/C7ueqbXi6VKrC/giphy.gif',
        'https://media.giphy.com/media/GHFm2uDTIWWzC3unEV/giphy.gif',
        'https://media.giphy.com/media/XIZ6sL7RrqObe/giphy.gif',
        'https://media.giphy.com/media/C7ueqbXi6VKrC/giphy.gif',
        'https://media.giphy.com/media/PhGRPKOIThnd6hfgNc/giphy.gif',
        'https://tenor.com/view/beauty-peacock-strut-strutting-chest-out-gif-14884888',
        'https://media.giphy.com/media/xCFCSlzF0sURa/giphy.gif',
        'https://media.giphy.com/media/hWeCPFq9mvTG9Nu38A/giphy.gif',
        'https://media.giphy.com/media/lQgzJVgQgxhaOTT1ZB/giphy.gif',
        'https://media.giphy.com/media/MgXkWmP4OYyB2/giphy.gif',
        'https://media.giphy.com/media/jsfvOm5LsiwRtB6XSR/giphy.gif']

        await ctx.send(f"{random.choice(peacock_pic)}")


def setup(client):
    client.add_cog(Fun(client))