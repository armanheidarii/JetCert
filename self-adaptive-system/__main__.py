import os
import sys
from waitress import serve

from main import logger, app

if __name__ == "__main__":
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    try:
        serve(app, host=host, port=int(port))
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
    finally:
        logger.info("Server has been shut down.")
