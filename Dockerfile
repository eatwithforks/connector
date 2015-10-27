# Build a container with all dependencies for the Halo event connector
FROM awilson/python27
MAINTAINER Ash Wilson

RUN apt-get update && apt-get install -y \
    vim
    
RUN mkdir -p /opt/cloudpassage/connector
COPY ./* /opt/cloudpassage/connector
COPY ./README.md /
COPY ./README.md /root/
RUN echo "cat /root/README.md" >> /root/.bashrc

CMD /bin/bash cat /README.md
