from perks.perkSystem import perk, PerkError
from discord.ext import commands
import discord
from api_key import userColl
from helpers.utils import get_user, Embed


@perk(name="AskNullzee", description="Ask Nullzee a question!", cost=5, aliases=["NullzeeQuestion", "askNull"],
      require_arg=True)
async def askNullzee(ctx, arg):
    msg = await ctx.guild.get_channel(738350726417219645).send(
        embed=discord.Embed(description=arg, color=0x00FF00)
            .set_author(name=ctx.author, icon_url=ctx.author.avatar_url))
    await ctx.send(embed=discord.Embed(title="Bought!", url=msg.jump_url, color=0x00FF00))


@perk(name="embedColour", description="Change the colour of your embeds!", cost=10,
      aliases=["embedColor", "commandColour"])
async def embedColour(ctx, arg):
    if not (len(arg.replace('#', '')) == 6):
        raise PerkError(embed=discord.Embed(title="Error!", description="please specify a valid hex code",
                                            color=discord.Color.red()))
    await get_user(ctx.author)
    await userColl.update_one({"_id": str(ctx.author.id)}, {"$set": {"embed_colour": arg.replace('#', '')}})


@perk(name="deadChatPing", description="Ping <@&749178299518943343> with a topic of your choice!", cost=15,
      aliases=["deadchat", "ping"], require_arg=True)
async def deadChat(ctx, arg):
    await ctx.send("<@&749178299518943343>", embed=await Embed(ctx.author, description=arg).set_author(name=ctx.author,
                                                                                                       icon_url=ctx.author.avatar_url).user_colour())
