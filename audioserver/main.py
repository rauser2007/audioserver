from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import aiofiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

#tracks = []
#for filename in os.listdir("static/tracks"):
#    tracks.append(filename)

tracks = [filename for filename in os.listdir(os.path.join("static", "tracks"))]
print("T")
print(tracks)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", context={"tracks": enumerate(tracks)})

@app.get("/track/add")
def add_track_form(request: Request):
    return templates.TemplateResponse(request, "add.html")

@app.post("/track/add")
async def add_track(request: Request, track: UploadFile):
    contents = await track.read()
    full_path = os.path.join("static", "tracks", track.filename)
    async with aiofiles.open(full_path, "wb") as f:
        await f.write(contents)

    tracks.append(track.filename)
    return RedirectResponse("/track/" + str(len(tracks) -1), status_code=303)

@app.post("/track/delete/{track_id}")
def delete_track(request: Request, track_id: int):
    track_to_remove = tracks[track_id]
    full_path = os.path.join("static", "tracks", track_to_remove)
    os.remove(full_path)
    tracks.pop(track_id)
    return "Successfully deleted"

@app.get("/track/{track_id}")
def get_track(request: Request, track_id: int):
    return templates.TemplateResponse(request, "track.html", context={"track": tracks[track_id], "track_id": track_id})

