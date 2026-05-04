FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install pytest google-generativeai requests --break-system-packages && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER jenkins
