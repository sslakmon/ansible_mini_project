FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install SSH + Python (required for Ansible)
RUN apt-get update && \
    apt-get install -y openssh-server python3 python3-pip && \
    apt-get clean

# Create ansible user
RUN useradd -m -s /bin/bash ansible

# Prepare SSH directory (authorized_keys will be mounted)
RUN mkdir -p /home/ansible/.ssh && \
    chmod 700 /home/ansible/.ssh && \
    chown -R ansible:ansible /home/ansible/.ssh

# SSHD setup
RUN mkdir /var/run/sshd

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
