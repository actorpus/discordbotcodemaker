import discord
import os


__version__ = "V0.0.2"
__licence__ = """
This work is licensed under the Creative Commons 
Attribution-ShareAlike 4.0 International License. 
To view a copy of this license, visit
https://creativecommons.org/licenses/by-sa/4.0/.
"""
__author__ = "https://discord.gg/UanfyFTFX8"


bot = discord.Bot(
    intents=discord.Intents.all()
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(
    name="help",
    description="Brings up the help menu!",
)
async def command_help(
        ctx: discord.ApplicationContext,
        command: discord.Option(
            str,
            choices=["ping", "help", "role"],
            required=False,
            default="help"
        )
):
    if command == "help":
        await ctx.respond("""
Here is a list of commands:
/ping: Use this command to check if the bot is online. It should respond with pong.
/help: Use this to get info. Use /help <command> to get info about a specific command.
/role: Use this command to get a role. /role <role-name>
/source: returns the link to this bots github. 
""")

    elif command == "ping":
        await ctx.respond("""
Use this command to check if the bot is online.

usage: 
`/ping`
""")

    elif command == "role":
        await ctx.respond("""
Use this command to get a role.

usage: 
`/role <role-name>`

Options role-name:
- test
""")

    else:
        await ctx.respond(
            "What?? How??",
            ephemeral=True
        )
        # the ephemeral=True prevents the message from being publicly viewable


@bot.command(
    name="ping",
    description="Use this command to check if the bot is online."
)
async def command_ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! That only took {bot.latency:0.2f}ms!")


@bot.command(
    name="role",
    description="Use this command to get a role."
)
async def command_role(
        ctx: discord.ApplicationContext,
        role: discord.Option(
            str,
            choices=[
                "test",
            ]
        )
):
    role_id = {
        "test": 1110271813642100877
    }

    if role not in role_id.keys():
        await ctx.respond(
            f"Unknown role!",
            # being careful not to include the users input in any output
            ephemeral=True
        )
        return

    role = ctx.guild.get_role(role_id[role])

    if role in ctx.user.roles:
        await ctx.user.remove_roles(
            role,
            reason="response of /role command"
        )
        await ctx.respond(
            f"Removed the role `{role.name}`",
            ephemeral=True
        )
        return

    await ctx.user.add_roles(
        role,
        reason="response of /role command"
    )
    await ctx.respond(
        f"Added the role `{role.name}`",
        ephemeral=True
    )


@bot.event
async def on_message(ctx: discord.Message):
    if ctx.author == bot.user:
        return

    content = ctx.content

    if content == "":
        print("Error getting message content, bad intents?")
        return

    if "im " in content.lower():
        await ctx.channel.send(
            "Hi " +
            content[content.lower().find("im ") + 3:]
            .strip()
            .split(".")[0]
            .split(",")[0] +
            "! I'm ~~only here to provide a skeleton for custom messages~~ Dad!")

    if "i'm " in content.lower():
        await ctx.channel.send(
            "Hi " +
            content[content.lower().find("i'm ") + 4:]
            .strip()
            .split(".")[0]
            .split(",")[0] +
            "! I'm ~~only here to provide a skeleton for custom messages~~ Dad!")


@bot.command(
    name="source",
    description="returns the link to this bots github."
)
async def command_source(ctx: discord.ApplicationContext):
    await ctx.respond(
        "https://github.com/actorpus/discordbotcodemaker",
        ephemeral=True
    )


if __name__ == '__main__':
    bot.run(os.environ['token'])
