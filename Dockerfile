# Build a container with all dependencies for the Halo event connector
FROM awilson/python27
MAINTAINER Ash Wilson

RUN apt-get update && apt-get install -y \
    vim
    
RUN mkdir -p /opt/cloudpassage/
COPY ./*.py /opt/cloudpassage/
COPY ./README.md /
COPY ./README.md /root/

CMD /bin/bash cat /README.md
