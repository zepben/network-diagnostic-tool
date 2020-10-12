from pydantic import BaseSettings


class Settings(BaseSettings):
    """Format of settings variables.
    """
    ewb_host: str
    ewb_port: int
    ewb_scheme: str

    class Config:
        """Link to environment variables
        """
        env_file = '.env'
