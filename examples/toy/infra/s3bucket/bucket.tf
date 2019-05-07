variable "AWS_ACCESS_KEY" {}
variable "AWS_SECRET_KEY" {}
variable "AWS_REGION" {}

provider "aws" {
  access_key = "${var.AWS_ACCESS_KEY}"
  secret_key = "${var.AWS_SECRET_KEY}"
  region = "${var.AWS_REGION}"
}

variable "BUCKET_NAME" {}

resource "aws_s3_bucket" "boom-storage" {
  bucket = "${var.BUCKET_NAME}"
  acl = "public-read"

  tags {
    Name = "${var.BUCKET_NAME}"
  }

}
