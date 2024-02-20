FROM kalilinux/kali-rolling:latest

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    unzip \
    wget

RUN apt-get install -y sublist3r nmap whatweb

ENV DIRBLE_URL="https://github.com/nccgroup/dirble/releases/download/v1.4.2/dirble-1.4.2-20190709-x86_64-linux.zip"
ENV DIRBLE_ZIP="dirble.zip"
RUN wget $DIRBLE_URL -O $DIRBLE_ZIP \
    && unzip $DIRBLE_ZIP \
    && chmod +x dirble \
    && mv dirble /usr/local/bin/

COPY . /app/

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
