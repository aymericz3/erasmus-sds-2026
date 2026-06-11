from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/travel_guide"
    google_maps_api_key: str = ""

    model_config = {"env_file": ".env"}
    
settings = Settings()