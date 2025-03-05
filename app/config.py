from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
from functools import lru_cache  # For efficiency, this helps cache it. 

class Settings(BaseSettings):  # Inheritance, inherits everything from BaseSettings
    # ... means its a req field. Fields func helps provide metadata.
    # env= , means setting its value to env variable ASTRADB_KEYSPACE, and if ASTRADB_KEYSPACE is not available, then field will be left empty and thus give error while creating object
    astradb_keyspace: str = Field(..., json_schema_extra="ASTRADB_KEYSPACE")  # In Pydantic v2, you should replace env inside Field with json_schema_extra
    astradb_client_id: str = Field(..., json_schema_extra="ASTRADB_CLIENT_ID") 
    astradb_client_secret: str = Field(..., json_schema_extra="ASTRADB_CLIENT_SECRET") 
    # astradb_client_secret: str = Field(..., env="ASTRADB_CLIENT_SECRET") 
    
    # In Pydantic, defining an inner class Config inside a model like Settings(BaseSettings) is used for configuration options. It helps customize how the model behaves, including how environment variables are read.
    # class Config:
    #     env_file = '.env'  # '.env' file should be wherever uvicorn command is called. Without this, Pydantic would only check for system environment variables.
    # NOTE model_config attribute is the preferred way to define model configurations
    model_config = ConfigDict(env_file=".env")  # NOTE Replacing class Config
    

@lru_cache  # It gets called one time and doesnt create instances again.
def get_settings():
    return Settings()  # Instance of Settings class.