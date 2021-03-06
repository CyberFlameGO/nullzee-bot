import time

from api_key import userColl
from helpers.events import Subscriber
from helpers.utils import get_user
from helpers.constants import Role, Channel

ACHIEVEMENT_BORDERS = {
    0.2: "bronze",
    0.5: "silver",
    0.8: "gold"
}

achievements = {
    "Hello, World!": {
        "listeners": {
            "message": lambda msg: not msg.author.bot
        },
        "description": "Send your first message in the server",
        "db_rewards": {
            "experience": 25,
        },
    },
    "Level Collector I": {
        "listeners": {
            "level_up": lambda _, level: level == 10
        },
        "description": "Reach level 10",
        "value": 1,
        "db_rewards": {
            "experience": 100
        },
    },
    "Level Collector II": {
        "listeners": {
            "level_up": lambda _, level: level == 30
        },
        "description": "Reach level 30",
        "value": 3,
        "db_rewards": {
            "experience": 250,
        },
    },
    "Level Collector III": {
        "listeners": {
            "level_up": lambda _, level: level == 50
        },
        "description": "Reach level 50",
        "value": 3,
        "db_rewards": {
            "experience": 500,
        },
    },
    "Role collector I": {
        "listeners": {
            "update_roles": lambda _, roles: len(roles) > 10
        },
        "description": "Have 10 roles",
        "value": 1,
    },
    "Role collector II": {
        "listeners": {
            "update_roles": lambda _, roles: len(roles) > 25
        },
        "description": "Have 25 roles",
        "value": 3
    },
    "Role collector III": {
        "listeners": {
            "update_roles": lambda _, roles: len(roles) > 50
        },
        "description": "Have 50 roles",
        "value": 6,
    },
    "Rich": {
        "listeners": {
            "update_roles": lambda ctx, roles: Role.BOOSTER in [z.id for z in roles]
            # "update_roles": lambda ctx, roles: print(Role)
        },
        "description": "Nitro boost the server",
        "value": 5,
    },
    "Prime Log": {
        "listeners": {
            "update_roles": lambda _, roles: Role.TWITCH_SUB in [z.id for z in roles]
        },
        "description": "Subscribe to Nullzee on twitch and link your account through discord!",
        "value": 5,
    },
    "Full of ideas": {
        "listeners": {
            "command": lambda _, name: name == "suggest"
        },
        "description": "Make your first suggestion",
        "value": 3,
        "db_rewards": {
            "experience": 500
        },
    },
    "Talkative I": {
        "listeners": {
            "update_role": lambda _, roles: Role.VC_LORD in [z.id for z in roles]
        },
        "description": "Become a VC lord",
        "value": 3,
    },
    "Talkative II": {
        "listeners": {
            "update_role": lambda _, roles: Role.VC_GOD in [z.id for z in roles]
        },
        "description": "Become a VC god",
        "value": 5,
    },
    "Mean": {
        "listeners": {
            "points_spent": lambda _, name: name == "staffNickChange"
        },
        "description": "Purchase staffNickChange from -shop",
        "value": 2,
    },
    "Frugal I": {
        "listeners": {
            "point_earned": lambda _, points: points == 100
        },
        "description": "Save up 100 points",
        "value": 6,
    },
    "Frugal II": {
        "listeners": {
            "point_earned": lambda _, points: points == 200
        },
        "description": "Save up 200 points",
        "value": 8,
    },
    "Frugal III": {
        "listeners": {
            "point_earned": lambda _, points: points == 300
        },
        "description": "Save up 300 points",
        "value": 11,
    },
    "Necromancer": {
        "listeners": {
            "points_spent": lambda _, name: name == "deadChatPing"
        },
        "description": "Purchase deadChatPing from -shop",
        "value": 3,
    },
    "Up to date": {
        "listeners": {
            "update_roles": lambda _, roles: {Role.POLL_PING, Role.QOTD_PING, Role.EVENT_PING,
                                              Role.DEAD_CHAT_PING,
                                              Role.GIVEAWAY_PING, Role.ANNOUNCEMENT_PING} <= set(
                [z.id for z in roles])
        },
        "description": "Have all ping roles",
        "value": 2,
    },
    "Agreeable": {
        "listeners": {
            "suggestion_stage_2": lambda _: True
        },
        "description": "Get 15 more upvotes than downvotes on one of your suggestions",
        "db_rewards": {
            "experience": 300,
        },
    },
    "Generous I": {
        "listeners": {
            "giveaway_create[donor]": lambda _, payload: payload["channel"] == Channel.MINI_GIVEAWAY
        },
        "description": "Donate for a mini-giveaway",
        "value": 5,
        "db_rewards": {
            "experience": 250,
            "points": 1
        },
    },
    "Generous II": {
        "listeners": {
            "giveaway_create[donor]": lambda _, payload: payload["channel"] == Channel.GIVEAWAY
        },
        "description": "Donate for a large giveaway",
        "value": 5,
        "db_rewards": {
            "experience": 750,
            "points": 3
        }

    },
    "Lucky!": {
        "listeners": {
            "giveaway_win": lambda ctx: ctx.channel.id == Channel.GIVEAWAY
        },
        "description": "Win a large giveaway",
        "value": 2,
    },
    "Funny": {
        "listeners": {
            "pinned_starred": lambda _: True
        },
        "description": "Have one of your messages pinned or starred",
        "value": 1,

    },
    "Establishing Connections": {
        "listeners": {},
        "description": "Send a message in twitch chat after linking your twitch to your discord",
        "value": 2,
    },
    "Bad boy": {
        "listeners": {
            "point_change": lambda _, points: points > 0
        },
        "description": "Have some points refunded",
        "db_rewards": {
            "points": -1
        },
    },
    "Colourful": {
        "listeners": {
            "points_spent": lambda _, name: name == "embedColour"
        },
        "description": "Change your embed colour",
        "value": 2
    },
    "Great Job": {
        "listeners": {
            "message": lambda msg: msg.guild and msg.author.guild_permissions.manage_messages,
            "update_roles": lambda ctx, _: ctx.author.guild_permissions.manage_messages
        },
        "description": "Get any staff position ",
        "db_rewards": {
            "experience": -69
        },
        "hidden": True
    },
    "Help at the wrong place": {
        "listeners": {
            "message": lambda msg: msg.guild and msg.guild.get_member(540953289219375146) in msg.mentions and "help" in msg.content
        },
        "hidden": True,
        "value": 1,
    },
    "Twitch Main": {
        "listeners": {},
        "description": "",
        "hidden": True
    }

    # TODO:
    #   Establishing Connections (*)
    #   Twitch Main (*)
}


async def award_achievement(ctx, data, name):
    return
    if name in data["achievements"]:
        return
    string = ""
    if "cb" in achievements[name]:
        await achievements[name]["cb"](ctx)
    if "response" in achievements[name]:
        await ctx.send(achievements[name]["response"].format(ctx))
    if "db_rewards" in achievements[name]:
        await userColl.update_one({"_id": str(ctx.author.id)}, {"$inc": achievements[name]["db_rewards"]})
        string += f" and earned {','.join(f'{v} {k}' for k, v in achievements[name]['db_rewards'])}"
    await ctx.send(f"Congratulations {ctx.author.mention}, you just achieved `{name}`{string}!")
    await userColl.update_one({"_id": str(ctx.author.id)},
                              {"$set": {f"achievements.{name}": time.time()},
                               "$inc": "achievement_points": achievements[name]["value"]})


def listeners_for(event):
    return [z for z in achievements if "listeners" in achievements[z] and event in achievements[z]["listeners"]]


@Subscriber().listen_all()
async def listen(event, ctx, *args, **kwargs):
    user_data = kwargs.get("user_data", await get_user(ctx.author))
    for achievement in listeners_for(event):
        if achievements[achievement]["listeners"][event](ctx, *args, **kwargs):
            await award_achievement(ctx, user_data, achievement)
