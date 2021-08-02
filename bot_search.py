import discord
from discord.ext import commands
import os
from googleapiclient.discovery import build
from discord.utils import get
from discord import Embed, Emoji
#! Import this
import random

client = commands.Bot(command_prefix="$")
api_key = "AIzaSyAQUOahI-j-bKMdelPijFZPbGCNTe0D4lo"


@client.event
async def on_ready():
    print("!!! Bot Is Online !!!\n")


@client.command(aliases=["show"])
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="94634b59d39db1d45", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Here Your Image ({search.title()})")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)

@client.command(pass_context=True)
async def about(ctx,*args,user: discord.Member=None):
    if user==None:
        user = client.user
    n1 = str("""*` 1: `*""")
    n2 = str("""*` 2: `*""")
    emoji = '\N{THUMBS UP SIGN}'
    embed=discord.Embed(title="About This BOT:", url="https://www.url.com", description="This BOT already on Developing so give us sometime hopefully you can enjoy with this BOT when will be finish!", color=0xe9d601)
    embed.set_author(name="Skafkaf Bot", url="https://discord.com/channels/@me/868859063251914794", icon_url="https://www.midiaresearch.com/storage/uploads/blog/featured/1353/cover_image-1617206921.jpg")
    embed.set_thumbnail(url="https://icons.iconarchive.com/icons/alecive/flatwoken/256/Apps-Development-icon.png")
    embed.add_field(name=f"{emoji}$about", value="get bot informations card[in use]", inline=True)
    embed.add_field(name="$who", value="get your info and your role[on Developing]", inline=True)
    embed.add_field(name="$showpic", value="type this command following with your words to search.[in use]", inline=True)
    embed.add_field(name="$play", value="use !play music_tile/url[on Developing]", inline=True)
    embed.set_image(url="https://www.midiaresearch.com/storage/uploads/blog/featured/1353/cover_image-1617206921.jpg")
    embed2= discord.Embed(title="***Roules: ***\n", description=" ", color=0xff5757)
    
    embed2.add_field(name=" "+n1, value="> Any try off spaming this server or some-one below this server will be banned by awner.", inline=True)
    embed2.add_field(name=" "+n2, value="> Make sure do not destract anyone!",inline=True)
    
    await ctx.send(f'requested by: {ctx.author.mention} \n')
    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)


#start

import random


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

#end



client.run("ODY4ODMwNjM3NjEwNjM1Mjc0.YP1Xlg.2pmZbMZ9PCqQRplPmmbUT8kVuvo")