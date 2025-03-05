import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # NOTE Can be used to render/ Can use things other than HTML. Use it to send text messages or as a template engine. 
from cassandra.cqlengine.management import sync_table
from . import db, config  # or can use from app.db import func.
from contextlib import asynccontextmanager  # New equivalent to on_event
from .users.models import User

# NOTE Running on python 3.8, later versions not supported by astra.

DB_SESSION = None  # Create a global variable, so can be referenced from anywhere.

# We want to sync table after creating FastAPI app. After fastapi application boots
@asynccontextmanager
async def lifespan(app: FastAPI):  # app is input argument of type FastAPI
    print("App is starting...")  # Equivalent to @app.on_event("startup")
    # await db.connect()  # Equivalent to startup
    
    global DB_SESSION
    DB_SESSION = db.get_session()  # setting to global variable so if I want to access it anywhere else, I dont need to re-initialize it.
    sync_table(User)  # Need to sync whenever new table created or schema change, else gives error when creating object. And does the mapping
    print("tables synced")
     
    yield  # Application runs while in this context
    # await db.disconnect()  # Equivalent to shutdown
    
    # DB_SESSION.shutdown()
    print("App is shutting down...")  # Equivalent to @app.on_event("shutdown")
    

BASE_DIR = pathlib.Path(__file__).resolve().parent  # Parent of curr dir, cross platform and cross system
TEMPLATE_DIR = BASE_DIR / "templates"
    
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))  # App is not tied to this "templates"

# NOTE : By default any sort of req in fastapi is gonna res with json obj as it is for REST api.
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    # return {"hello":"world"}  # json data -> REST API , by default
    context = {
        "request": request,  # This context by default with Jinja templates we need to pass with req itself, compulsory. Other variables can be added.
        "username": "Govind"
    }
    return templates.TemplateResponse("home.html", context)  # home.html is relative path to templates folder

@app.get("/users")
def users_list_view():
    qs = User.objects.all().limit(10)
    return list(qs)