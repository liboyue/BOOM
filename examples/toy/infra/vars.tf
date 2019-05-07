
# Mandatory Variables
variable "AWS_ACCESS_KEY" {}
variable "AWS_SECRET_KEY" {}
variable "BUCKET_NAME" {}
variable "FILE_COUNT" {}
variable "data_filename" {}

# Optional Variables
variable "AWS_REGION" {
  default = "us-east-1"
}
variable "KEY_NAME" {
  default = ""
}
variable "INSTANCE_TYPE" {
  default = "t2.micro"
}

# Please only change them if you are sure what you are doing.
variable "AMI" {
  default = "ami-00644f6c30c4524fb" // Custom image with BOOM
//  default = "ami-13be557e"
}