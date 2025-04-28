FROM toxchat/compcert

# RUN apt update && apt upgrade -y
RUN apt update
RUN apt install -y python3-pip libjson-c-dev libsqlite3-dev
RUN pip3 install numba
RUN echo y | /bin/bash -c "$(curl -fsSL https://exaloop.io/install.sh)"

WORKDIR /home
COPY self-adaptive-system/requirements.txt /home/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/
RUN chmod +x /home/entrypoint.sh
ENTRYPOINT ["/home/entrypoint.sh"]
