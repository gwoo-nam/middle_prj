FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    pip3 install pytest requests --break-system-packages && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @anthropic-ai/claude-code && \
    pip3 install pytest requests pytest-timeout --break-system-packages && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER jenkins
