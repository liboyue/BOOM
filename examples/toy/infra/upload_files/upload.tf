

resource "aws_s3_bucket_object" "file_1" {
  bucket = "${var.BUCKET_NAME}"
  key = "1.zip"
  source = "/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/1.zip"
  etag = "${md5(file("/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/1.zip"))}"
}


resource "aws_s3_bucket_object" "file_2" {
  bucket = "${var.BUCKET_NAME}"
  key = "2.zip"
  source = "/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/2.zip"
  etag = "${md5(file("/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/2.zip"))}"
}


resource "aws_s3_bucket_object" "file_3" {
  bucket = "${var.BUCKET_NAME}"
  key = "3.zip"
  source = "/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/3.zip"
  etag = "${md5(file("/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/3.zip"))}"
}


resource "aws_s3_bucket_object" "file_4" {
  bucket = "${var.BUCKET_NAME}"
  key = "4.zip"
  source = "/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/4.zip"
  etag = "${md5(file("/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/4.zip"))}"
}


resource "aws_s3_bucket_object" "file_5" {
  bucket = "${var.BUCKET_NAME}"
  key = "5.zip"
  source = "/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/5.zip"
  etag = "${md5(file("/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/5.zip"))}"
}


resource "aws_s3_bucket_object" "file_6" {
  bucket = "${var.BUCKET_NAME}"
  key = "pipeline.zip"
  source = "/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/pipeline.zip"
  etag = "${md5(file("/Users/paritosh/Documents/capstone/BOOM/examples/toy/tmp/pipeline.zip"))}"
}


resource "aws_s3_bucket_object" "data_file" {
  bucket =  "${var.BUCKET_NAME}"
  key = "data.json"
  source = "/Users/paritosh/Documents/capstone/BOOM/examples/toy/data.json"
  etag = "${md5(file("/Users/paritosh/Documents/capstone/BOOM/examples/toy/data.json"))}"
}

