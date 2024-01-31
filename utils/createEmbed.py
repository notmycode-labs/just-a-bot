import discord

def create_embed(title, description, color=discord.Color.blue(), fields=None, author=None, footer=None):
    """
    Create a Discord embed using a dictionary-like structure.

    Parameters:
        title (str): The title of the embed.
        description (str): The description of the embed.
        color (discord.Color, optional): The color of the embed (default is blue).
        fields (list, optional): List of dictionaries containing fields for the embed.
        author (dict, optional): Dictionary containing information for the author field.
        footer (dict, optional): Dictionary containing information for the footer field.

    Returns:
        discord.Embed: The constructed Discord embed.
    """
    embed_dict = {
        "title": title,
        "description": description,
        "color": color,
        "fields": fields,
        "author": author,
        "footer": footer
    }

    embed = discord.Embed(
        title=embed_dict["title"],
        description=embed_dict["description"],
        color=embed_dict["color"]
    )

    if embed_dict["fields"]:
        for field in embed_dict["fields"]:
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

    if embed_dict["author"]:
        embed.set_author(name=embed_dict["author"]["name"], icon_url=embed_dict["author"].get("icon_url", None))

    if embed_dict["footer"]:
        embed.set_footer(text=embed_dict["footer"]["text"], icon_url=embed_dict["footer"].get("icon_url", None))

    return embed
