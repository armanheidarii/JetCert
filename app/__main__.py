# install dependencies in docker file (python and linux packages)

import sys

sys.path.append(".")

# Setup app
from app import app

# Setup Handlers
from app.handlers import signup, get_all_users

if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True)
