FROM mirror.gcr.io/library/ubuntu:latest
RUN apt update
RUN apt install cowsay fortune-mod netcat-openbsd -y 
RUN rm -rf /var/lib/apt/lists/*
ENV PATH="/usr/games:${PATH}"
COPY  wisecow.sh /
EXPOSE 4499
CMD ["bash","wisecow.sh"] 
