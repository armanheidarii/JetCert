import os
import sys

sys.path.append(".")

from app import app

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
    )
