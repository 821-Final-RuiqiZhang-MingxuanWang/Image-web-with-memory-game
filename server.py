"""The web server."""
import base64
import sqlite3
import SQL
import random
from starlette.requests import Request
from fastapi import FastAPI, Form, UploadFile, File
from starlette.templating import Jinja2Templates

APP = FastAPI()
templates = Jinja2Templates(directory="./web_html")

num_1 = 0
num_2 = 0


@APP.get("/")
async def Game(request: Request):
    """Go to the game."""
    global num_1, num_2
    random_list = random.sample(range(100, 999), 8)
    random_list.append(random_list[0])
    random.shuffle(random_list)
    for i in range(9):
        for j in range(9):
            if random_list[i] == random_list[j] and i != j:
                num_1 = i + 1
                num_2 = j + 1
    return templates.TemplateResponse(
        "game.html", {"request": request, "random_list": random_list}
    )


@APP.post("/pass/")
async def Pass_game(request: Request, answer: str = Form(...)):
    """Go to the image library if the answer is correct."""
    if (
        answer == "BIOSTAT821"
        or answer == f"{num_1},{num_2}"
        or answer == f"{num_2},{num_1}"
    ):
        con = sqlite3.connect("image_data.db")
        cur = con.cursor()
        image_dict = SQL.image_dict(cur)
        image_number = int(SQL.image_number(cur))
        con.close()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "image_dict": image_dict,
                "image_number": image_number,
            },
        )
    return templates.TemplateResponse("incorrect.html", {"request": request})


@APP.get("/passed/")
async def Direct_way(request: Request):
    """Go to the image library directly."""
    con = sqlite3.connect("image_data.db")
    cur = con.cursor()
    image_dict = SQL.image_dict(cur)
    image_number = int(SQL.image_number(cur))
    con.close()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "image_dict": image_dict, "image_number": image_number},
    )


@APP.post("/passed/")
async def Direct_way(request: Request, search: str = Form(...)):
    """Search image that name include required str"""
    con = sqlite3.connect("image_data.db")
    cur = con.cursor()
    image_dict = SQL.search_image_dict(cur, search)
    image_number = int(len(image_dict["name"]))
    con.close()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "image_dict": image_dict, "image_number": image_number},
    )


@APP.get("/upload/")
async def upload_image(request: Request):
    """Go to the upload page."""
    return templates.TemplateResponse("upload.html", {"request": request})


@APP.post("/success/")
async def upload(
    request: Request,
    File: bytes = File(...),
    Image_Name: str = Form(...),
    Description: str = Form(...),
    Source: str = Form(...),
    Date: str = Form(...),
):
    """Upload Image."""
    with open(f"./image/{Image_Name}.png", "wb") as f:
        f.write(File)
    value_list = [Image_Name, Description, Source, Date]
    print(value_list)
    con = sqlite3.connect("image_data.db")
    cur = con.cursor()
    SQL.load_str(cur, value_list)
    con.commit()
    image_dict = SQL.image_dict(cur)
    image_number = int(SQL.image_number(cur))
    con.close()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "image_dict": image_dict, "image_number": image_number},
    )
