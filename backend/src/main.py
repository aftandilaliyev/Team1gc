import uvicorn

from src.core.api import get_app
from src.core.logger import setup_logger


setup_logger() # NOTE: Logger setup should be first executed function in application after environment variables are loaded
app = get_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
