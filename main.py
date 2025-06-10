# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from rich.console import Console
from rich.text import Text

app = FastAPI()
console = Console()

class GameState:
    def __init__(self):
        self.location = "village_square"
        self.npcs = {"aldric": {"name": "Aldric the Wise", "dialogue": "Greetings, traveler!"}}

game = GameState()

class PlayerAction(BaseModel):
    command: str

@app.post("/game")
async def game_loop(action: PlayerAction):
    response = process_command(action.command)
    return {"output": response, "location": game.location}

def process_command(cmd: str) -> str:
    parts = cmd.lower().split()
    if not parts:
        return "What would you do?"
    
    verb = parts[0]
    if verb == "look":
        return "You stand in the village square. Aldric the Wise awaits."
    elif verb == "talk" and len(parts) > 1:
        npc = parts[1]
        if npc in game.npcs:
            return game.npcs[npc]["dialogue"]
        return "There's no one here by that name."
    elif verb == "quit":
        return "Farewell, adventurer..."
    else:
        return "I don't understand that command."

# Run with: uvicorn main:app --reload