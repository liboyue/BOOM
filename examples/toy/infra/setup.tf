module "create_server" {
  source = "./servers"

  AMI = "${var.AMI}"
  INSTANCE_TYPE = "${var.INSTANCE_TYPE}"
  BUCKET_NAME = "${var.BUCKET_NAME}"
  KEY_NAME = "${var.KEY_NAME}"
  FILE_COUNT = "${var.FILE_COUNT}"
  data_filename = "${var.data_filename}"
}

module "upload_files" {
  source = "./upload_files"

  BUCKET_NAME = "${var.BUCKET_NAME}"
  data_filename = "${var.data_filename}"
}