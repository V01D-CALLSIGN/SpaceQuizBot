import os
import random
from dataclasses import dataclass
from typing import Dict, List
import discord
from discord import app_commands
from dotenv import load_dotenv
from thefuzz import fuzz

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

@dataclass(frozen=True)
class QuizItem:
    label: str
    aliases: List[str]
    path: str

QUIZ_ITEMS = [

    QuizItem(
        label="Orion Molecular Cloud Complex",
        aliases=["orion molecular cloud", "orion complex", "omcc"],
        path="images/orion_molecular_cloud_complex.png"
    ),

    QuizItem(
        label="Sharpless 29",
        aliases=["sh2-29", "ngc 6559", "sharpless 29 ngc 6559"],
        path="images/sharpless_29_ngc_6559.png"
    ),

    QuizItem(
        label="Ophion Star Family",
        aliases=["ophion", "ophion family"],
        path="images/ophion_star_family.png"
    ),

    QuizItem(
        label="HP Tau",
        aliases=["hp tau", "hp tauri"],
        path="images/hp_tau.png"
    ),

    QuizItem(
        label="Mira",
        aliases=["mira", "omicron ceti"],
        path="images/mira_omicron_ceti.png"
    ),

    QuizItem(
        label="Helix Nebula",
        aliases=["helix nebula", "ngc 7293"],
        path="images/helix_nebula_ngc_7293.png"
    ),

    QuizItem(
        label="Janus",
        aliases=["ztf j203349.8+322901.1", "janus ztf"],
        path="images/janus_ztf_j203349.png"
    ),

    QuizItem(
        label="WDJ181058.67+311940.94",
        aliases=["wdj181058", "white dwarf j181058"],
        path="images/wdj181058.png"
    ),

    QuizItem(
        label="Crab Nebula",
        aliases=["crab", "m1", "messier 1"],
        path="images/crab_m1.png"
    ),

    QuizItem(
        label="The Bone",
        aliases=["g359.13", "bone g359.13"],
        path="images/bone_g359_13.png"
    ),

    QuizItem(
        label="Cassiopeia A",
        aliases=["cas a", "cassiopeia a"],
        path="images/cas_a.png"
    ),

    QuizItem(
        label="Tycho's SNR",
        aliases=["tycho", "tychos snr", "sn 1572"],
        path="images/tychos_snr.png"
    ),
]

@dataclass
class Session:
    current: int
    order: List[int]
    score: int
    active: bool

sessions: Dict[int, Session] = {}

def normalize(s):
    return s.strip().lower()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

@tree.command(name="quiz_start", description="Start quiz")
async def start(interaction: discord.Interaction):
    order = list(range(len(QUIZ_ITEMS)))
    random.shuffle(order)

    sessions[interaction.user.id] = Session(
        current=0,
        order=order,
        score=0,
        active=True
    )

    item = QUIZ_ITEMS[order[0]]
    file = discord.File(item.path)
    embed = discord.Embed(title="Identify this object!")
    embed.set_image(url=f"attachment://{os.path.basename(item.path)}")

    await interaction.response.send_message(embed=embed, file=file)

@tree.command(name="quiz_guess", description="Guess the image")
async def guess(interaction: discord.Interaction, answer: str):
    await interaction.response.defer()

    session = sessions.get(interaction.user.id)

    if not session or not session.active:
        await interaction.followup.send("Start a quiz first.", ephemeral=True)
        return

    item = QUIZ_ITEMS[session.order[session.current]]
    correct_answers = [item.label.lower()] + item.aliases

    user_answer = normalize(answer)
    best_score = max(fuzz.ratio(user_answer, ca) for ca in correct_answers)

    if user_answer in correct_answers:
        session.score += 1
        response = f"✅ Correct! It was {item.label}."
    elif best_score >= 80:
        session.score += 1
        response = f"✅ Close enough! It was {item.label}."
    else:
        response = f"❌ Incorrect. It was {item.label}."

    session.current += 1

    if session.current >= len(session.order):
        session.active = False
        await interaction.followup.send(
            f"{response}\n\nFinal Score: {session.score}/{len(session.order)}"
        )
        return

    next_item = QUIZ_ITEMS[session.order[session.current]]
    file = discord.File(next_item.path)
    embed = discord.Embed(title="Next image!")
    embed.set_image(url=f"attachment://{os.path.basename(next_item.path)}")

    await interaction.followup.send(
        response,
        embed=embed,
        file=file
    )

client.run(TOKEN)