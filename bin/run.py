import glog as log
import os
import subprocess


## Check if a filename matches the startswith string and extension"
#  @param filename The name of the file
#  @param startswith The string with which the file should start
#  @param extension The extension of the files that we want to filter
#  @return boolean indicating if it is a match or not
def file_filter(filename, startswith='', extension=''):
    """Check if a filename matches the startswith string and extension"""
    if not filename:
        return False
    filename = filename.strip()
    return filename.startswith(startswith) and filename.endswith(extension)


## Filter filenames in directory according to radical and extension
#  @param dirname The directory in which we want to search for the files
#  @param startswith The string with which the file should start
#  @param extension The extension of the files that we want to filter
#  @return list of files matching our filters
def dir_filter(dirname='', startswith='', extension=''):
    if not dirname:
        dirname = '.'
    return [filename for filename in os.listdir(dirname)
            if file_filter(filename, startswith, extension)]


## The function to execute a command in a subprocess
#  @param cmd The command to be executed
#  @return the subprocess instance
def execute_cmd(cmd):
    log.debug('Execute ' + ' '.join(cmd))
    return subprocess.Popen(cmd)


## Directory containing all the zipped modules
dirname = './tmp'
filenames = dir_filter(dirname=dirname, extension='.zip')
log.debug(filenames)

process_list = []

for filename in filenames:
    cmd = ['python', dirname + "/" + filename, ' -v']
    log.debug(cmd)
    process_list.append(execute_cmd(cmd))

## Wait for processes to finish.
for process in process_list:
    process.wait()
