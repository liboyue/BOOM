#! /bin/bash

# This script is run when the EC2 instance is launched
# It is responsible for download the python zipped modules from an S3 bucket
# and the input data file.
# Then it uses RabbitMQ to run all the modules and upload the results
# back to the S3 bucket

#### Install basic software ####
#### These steps are not required if you are using the custom ami ####
# Please enable these commands if you want to use a base ubuntu image (Ubuntu 16.04)
# sudo apt update -y
# sudo apt install awscli -y
# sudo apt install make -y
# sudo apt-get install python-pip -y
# # Install RabbitMQ (https://www.rabbitmq.com/install-debian.html#apt)
# wget -O - "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | sudo apt-key add -
# sudo apt-key adv --keyserver "hkps.pool.sks-keyservers.net" --recv-keys "0x6B73A36E6026DFCA"
# wget -O - "https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc" | sudo apt-key add -
# sudo apt-get install apt-transport-https -y
# echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
# sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list <<EOF
# deb https://dl.bintray.com/rabbitmq-erlang/debian xenial erlang
# deb https://dl.bintray.com/rabbitmq/debian xenial main
# EOF
# sudo apt-get update -y
# sudo apt-get install -y rabbitmq-server
# sudo apt install virtualenv -y
# cd /home/ubuntu
# virtualenv env
# source env/bin/activate
# git clone https://github.com/paritoshgpt1/BOOM.git
# cd /home/ubuntu/BOOM
# pip install -r requirements.txt
# cd /home/ubuntu


#### Start RabbitMQ Server ####
sudo service rabbitmq-server start

cd /home/ubuntu

# Make a tmp directory to download all the python modules
mkdir tmp
cd tmp

# Download all the python zipped modules
for (( i=1; i<=${files}; i++ ))
do
   aws s3 cp s3://${s3_bucket_name}/$i.zip $i.zip
done

# Download the pipeline.zip module
aws s3 cp s3://${s3_bucket_name}/pipeline.zip pipeline.zip

cd /home/ubuntu

# Download the input data file
aws s3 cp s3://${s3_bucket_name}/${data_filename} ${data_filename}

# Copy the runner to execute the python zipped modules and run them
cp BOOM/bin/run.py run.py
python run.py

# Upload the results back to the S3 bucket
find . -type d -regex ".*[0-9]+s$" | while read i; do
    results_dir=$(basename "$i")
    aws s3 sync "$results_dir" s3://${s3_bucket_name}/"$results_dir"
done
