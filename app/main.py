from fastapi import FastAPI
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
    DB_SESSION = db.get_session()  # setting to global variable so if I want to use it anywhere else, I dont need to re-initialize it.
    sync_table(User)  # Need to sync whenever new table created or schema change, else gives error when creating object. And does the mapping
    print("tables synced")
     
    yield  # Application runs while in this context
    # await db.disconnect()  # Equivalent to shutdown
    
    # DB_SESSION.shutdown()
    print("App is shutting down...")  # Equivalent to @app.on_event("shutdown")
    
    
app = FastAPI(lifespan=lifespan)


@app.get("/")
def homepage():
    return {"hello":"world"}  # json data -> REST API , by default

@app.get("/users")
def users_list_view():
    qs = User.objects.all().limit(10)
    return list(qs)