variable "AMI" {}
variable "INSTANCE_TYPE" {}
variable "KEY_NAME" {}
variable "BUCKET_NAME" {}
variable "FILE_COUNT" {}
variable "data_filename" {}

# The tag for the resources on AWS
locals {
  common_tags = {
    Project = "BOOM"
  }
}

# Create a security group for EC2 instance
resource "aws_security_group" "boom_sg" {
  name = "boom-sg"
  description = "Allow SSH Acces from Anywhere"
  # HTTP access from anywhere
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  # SSH Access from anywhere
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  # outbound internet access
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  tags = "${local.common_tags}"
}

############################ S3 Objects and Permissions ############################

resource "aws_iam_role" "ec2-s3-access-role" {
  name = "ec2-s3-access-role"
  assume_role_policy = "${file("assumerolepolicy.json")}"
}

resource "aws_iam_policy" "ec2-s3-policy" {
  name = "ec2-s3-policy"
  policy = "${file("policys3bucket.json")}"
}

resource "aws_iam_policy_attachment" "ec2-s3-policy-to-role-attachment" {
  name = "ec2-s3-policy-to-role-attachment"
  roles = [
    "${aws_iam_role.ec2-s3-access-role.name}"]
  policy_arn = "${aws_iam_policy.ec2-s3-policy.arn}"
}

resource "aws_iam_instance_profile" "ec2-s3-profile" {
  name = "ec2-s3-profile"
  role = "${aws_iam_role.ec2-s3-access-role.name}"
}

# The shell script to run on server startup
data "template_file" "user_data" {
  template = "${file("initialize.sh")}"

  # Variables for the shell script
  vars = {
    s3_bucket_name = "${var.BUCKET_NAME}"
    files = "${var.FILE_COUNT}"
    data_filename = "${var.data_filename}"
  }
}

# EC2 isntance
resource "aws_instance" "boom" {
  ami = "${var.AMI}"
  instance_type = "${var.INSTANCE_TYPE}"
  key_name = "${var.KEY_NAME}"
  security_groups = ["${aws_security_group.boom_sg.name}"]
  user_data = "${base64encode(data.template_file.user_data.rendered)}"
  iam_instance_profile = "${aws_iam_instance_profile.ec2-s3-profile.name}"
  tags = "${local.common_tags}"
}