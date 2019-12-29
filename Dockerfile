FROM gitpod/workspace-full
USER root
RUN apt-get update -y
RUN pip3 install jupyter pandas matplotlib numpy
RUN ipython3 kernel install
RUN usermod -a -G root gitpod
RUN chmod -R g+rwx /usr /etc /var /proc /lib /opt /root
USER gitpod
