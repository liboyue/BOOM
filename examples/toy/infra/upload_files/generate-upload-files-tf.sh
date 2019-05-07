#! /bin/sh

# The path containing all the zipped modules
SRC="${1}/tmp"
# The path to write the terraform file containing the configuration for
# zipped modules and data file
TF_FILE="${2}/upload_files/upload.tf"

# The name of file containing the input data
DATA_FILENAME=$3

# Create a terraform file which will contain the configuration to upload all
# the zipped modules and the data file to an S3 bucket
COUNT=1

if [[ -f ${TF_FILE} ]]
then
	> ${TF_FILE}
else
	touch ${TF_FILE}
fi


find ${SRC} -iname '*.zip' | while read path; do
    name=$(basename "$path")
    zip_path="${path}"
#    zip_path="../${path}"
    cat >> ${TF_FILE} << EOM


resource "aws_s3_bucket_object" "file_${COUNT}" {
  bucket = "\${var.BUCKET_NAME}"
  key = "${name}"
  source = "${zip_path}"
  etag = "\${md5(file("${zip_path}"))}"
}
EOM

    COUNT=$(expr ${COUNT} + 1)

done

cat >> ${TF_FILE} << EOM


resource "aws_s3_bucket_object" "data_file" {
  bucket =  "\${var.BUCKET_NAME}"
  key = "${DATA_FILENAME}"
  source = "${1}/${DATA_FILENAME}"
  etag = "\${md5(file("${1}/${DATA_FILENAME}"))}"
}

EOM