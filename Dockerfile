FROM toxchat/compcert

# RUN apt update && apt upgrade -y
RUN apt update
RUN apt install python3-pip -y
RUN pip3 install numba
RUN echo y | /bin/bash -c "$(curl -fsSL https://exaloop.io/install.sh)"

WORKDIR /home
COPY self-adaptive-system/requirements.txt /home/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/
RUN python3 self-adaptive-system/