FROM phusion/baseimage:0.10.1

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# Update Apt
RUN apt-get update

# Install Git, GraphViz, pip
RUN apt-get install -y git graphviz python3-pip

# Install RabbitMQ
RUN curl https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y rabbitmq-server

# Install MongoDB
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.6.list
RUN apt-get update
RUN apt-get install -y mongodb-org

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python dependencies
RUN pip3 install glog numpy pika pydotplus pymongo pytest pyyaml six
RUN pip3 install rouge

# Install BOOM
# RUN git clone https://github.com/liboyue/BOOM.git
COPY . /boom
RUN ls /boom
RUN cd /boom && make install

# Create data dir for MongoDB
RUN mkdir /data
WORKDIR /

# RabbitMQ port
EXPOSE 5672
EXPOSE 15672

# MongoDB port
EXPOSE 27017
