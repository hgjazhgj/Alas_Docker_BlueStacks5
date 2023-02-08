# docker build -t hgjazhgj/alas:latest .
# docker run -v ${PWD}:/alas -p 22267:22267 --name alas -it --rm hgjazhgj/alas

FROM python:3.7-slim

WORKDIR /alas

COPY requirements.txt /tmp/requirements.txt

RUN apt update \
 && apt install -y git adb netcat libgomp1 \
 && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && echo 'Asia/Shanghai' > /etc/timezone \
 && pip install -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt \
 && rm -r ~/.cache/pip

CMD python gui.py