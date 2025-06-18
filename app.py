from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import random
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

choices = ["rock", "paper", "scissors"]
game_stats = {"wins": 0, "losses": 0, "ties": 0, "total": 0}

@app.get("/", response_class=HTMLResponse)
async def select_mode(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reset")
async def reset_game():
    game_stats.update({"wins": 0, "losses": 0, "ties": 0, "total": 0})
    return RedirectResponse(url="/", status_code=302)

@app.post("/play", response_class=HTMLResponse)
async def play_page(request: Request, mode: str = Form(...)):
    return templates.TemplateResponse("game.html", {
        "request": request,
        "result": "",
        "user": "",
        "computer": "",
        "user_emoji": "",
        "comp_emoji": "",
        "mode": mode,
        "wins": game_stats["wins"],
        "losses": game_stats["losses"],
        "ties": game_stats["ties"],
        "total": game_stats["total"]
    })

@app.post("/", response_class=HTMLResponse)
async def play_game(request: Request, mode: str = Form(...), choice: str = Form(...)):
    user = choice
    computer = get_computer_choice(mode, user)
    result = get_result(user, computer)

    game_stats["total"] += 1
    if result == "Win":
        game_stats["wins"] += 1
    elif result == "Lose":
        game_stats["losses"] += 1
    else:
        game_stats["ties"] += 1

    return templates.TemplateResponse("game.html", {
        "request": request,
        "result": result,
        "user": user,
        "computer": computer,
        "user_emoji": emoji(user),
        "comp_emoji": emoji(computer),
        "mode": mode,
        "wins": game_stats["wins"],
        "losses": game_stats["losses"],
        "ties": game_stats["ties"],
        "total": game_stats["total"]
    })

def get_result(user, comp):
    if user == comp:
        return "Tie"
    elif (user == "rock" and comp == "scissors") or          (user == "scissors" and comp == "paper") or          (user == "paper" and comp == "rock"):
        return "Win"
    else:
        return "Lose"

def get_computer_choice(mode, user):
    if mode == "easy":
        return random.choice(choices)
    elif mode == "medium":
        return {0: counter_choice(user), 1: random.choice(choices)}[random.randint(0, 1)]
    elif mode == "hard":
        return counter_choice(user)
    return random.choice(choices)

def counter_choice(choice):
    return {
        "rock": "paper",
        "paper": "scissors",
        "scissors": "rock"
    }[choice]

def emoji(choice):
    return {
        "rock": "🪨",
        "paper": "📄",
        "scissors": "✂️"
    }[choice]

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
