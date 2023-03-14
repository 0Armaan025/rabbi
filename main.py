import discord
from discord.ext import commands 
import random;
from PIL import Image, ImageDraw, ImageSequence,ImageFont
import io;
import json;
from discord import ui;

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.',intents=intents)
token = "<YOUR TOKEN HERE>";

#==========================HELLO==========================

@client.command(aliases=[ 'wassup', 'hi','howdy','heyyy','hloooo'])
async def hello(ctx):

    responses = ["Howdy", "Hiiiiii","Hloooo","Hello there","Hiii there","How's you?"];
    response = random.choice(responses);

    if ctx.author.nick == True:
        await ctx.send(f"{response} {ctx.author.nick.mention}")
    else:
        await ctx.send(f"{response} {ctx.author.mention}")

#==========================!8ball==========================

@client.command(name="!8ball")       
async def ball(ctx):
    responses = ["It is decided so","Maybe","Try sometime later!","I hate you!","Go, see the sun", "hehe","maybe","idk"];
    response = random.choice(responses);
    await ctx.send(f"{response}");
         
#==========================WHO IS==========================

@client.command()
async def whois(ctx,*,user: discord.Member = None):
    role_id = 1085091539786682408;
    if user.nick == True:
        username = user.nick
    else:
        username = user.name;    
    em = discord.Embed(title = f"Who is {username}");
    joined_at = user.joined_at.strftime("%b %d, %Y, %T")
    joined_di = user.created_at.strftime("%b %d, %Y, %T")
    em.add_field(name=f"{username} joined {ctx.message.guild.name} at ",value=f"{joined_at}");
    em.add_field(name=f"{username} joined discord at ",value=f"{joined_di}",inline=False);

    pfp = user.avatar
    em.set_image(url=pfp)

    if role_id in [role.id for role in user.roles]:
        em.add_field(name="\nThey are the Admin",value="",inline=False)
    else:
        em.add_field(name="\nThey are a Member",value="",inline=False)    
        

    await ctx.send(embed=em);

#==========================DESTROY==========================

@client.command()
async def destroy(ctx,user: discord.Member,*,reason = None, ):
    
    pokemons = ['pokemons/arceus.gif','pokemons/electrode.gif','pokemons/mewtwo.gif','pokemons/hehe.gif','pokemons/pikachu.gif'];
    pokemon = random.choice(pokemons)
    im = Image.open(pokemon)
    if reason and user != None:
        await ctx.send(f"Destroying {user.mention} for {reason}")
    frames = []
    for frame in ImageSequence.Iterator(im):
        d = ImageDraw.Draw(frame)
        fontsize=20
        font = ImageFont.truetype("arial.ttf", fontsize)
        d.text((230,100), f"I am gonna destroy\n{user.name}",font=font)
        del d

        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)

        frames.append(frame)
        frames[0].save('out.gif', save_all=True, append_images=frames[1:])

    await ctx.channel.send(file=discord.File('out.gif'))    


@client.command()
async def give(ctx,name=None,time=None):

        role_id = 1085091539786682408;
        if role_id in [role.id for role in ctx.message.author.roles]:
            await open_give_away(ctx,ctx.message.author,name,time);
        else:
            await ctx.send(content="Sorry, but only admins can use it!",ephemeral=True)
    
class MyView(discord.ui.View): 
    @discord.ui.button(label="Enter the Give Away!", style=discord.ButtonStyle.red, emoji="😎") 
    async def button_callback(self, interaction, button):
        await interaction.response.send_message("you have entered the give away now!",ephemeral=True)

#======================OPEN GIVE AWAYS============================== 

async def open_give_away(ctx,user,name,timeRemaining):
    random_number = random.randint(1, 10000000)
    await ctx.send(f"_{name} giveaway by {user.name} opened successfully!_ **GIVEAWAY ID:- {random_number}**");
    await ctx.send("Enter the Give away!", view=MyView());
    await store_give_away(ctx,user,name,timeRemaining,random_number,0)

#======================STORE GIVE AWAY==============================  
async def store_give_away(ctx,user,name,timeRemaining,giveAwayId,entries):
    users = await get_store_house_data()
    await ctx.send(users)

    if users['giveaways'] in users:
        await ctx.send("it's there");

#======================OPEN STORE HOUSE==============================   

async def open_store_house(user):
    users = await get_store_house_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]={}
        users[str(user.id)]["points"]=0
        users[str(user.id)]["warnings"]=0
        users[str(user.id)]["money"] = 0   

    with open("mainbank.json","w") as f:
        json.dump(users,f)   
    return True             

#======================GET STORE HOUSE DATA==============================    

async def get_store_house_data():
    with open("storehouse.json","r") as f:
        users = json.load(f)

    return users        
        

client.run(token)    