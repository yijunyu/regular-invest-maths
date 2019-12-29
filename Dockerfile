FROM gitpod/workspace-full
USER root
RUN apt-get update -y
RUN pip3 install jupyter pandas matplotlib numpy
RUN ipython3 kernel install
USER gitpod
