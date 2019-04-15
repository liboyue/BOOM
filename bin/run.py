import glog as log
import os
import subprocess


def file_filter(filename, radical='', extension=''):
    """Check if a filename matches a radical and extension"""
    if not filename:
        return False
    filename = filename.strip()
    return filename.startswith(radical) and filename.endswith(extension)


def dir_filter(dirname='', radical='', extension=''):
    """Filter filenames in directory according to radical and extension"""
    if not dirname:
        dirname = '.'
    return [filename for filename in os.listdir(dirname)
            if file_filter(filename, radical, extension)]


# The function to execute a command in a subprocess
#  @param cmd The command to be executed
#  @return None if in debug mode, the subprocess instance otherwise
def execute_cmd(cmd):
    log.debug('Execute ' + ' '.join(cmd))
    return subprocess.Popen(cmd)


dirname = './tmp'
filenames = dir_filter(dirname=dirname, extension='.zip')
print(filenames)

process_list = []

for filename in filenames:
    cmd = ['python', dirname + "/" + filename, ' -v']
    log.debug(cmd)
    process_list.append(execute_cmd(cmd))

# Wait for processes to finish.
for process in process_list:
    process.wait()
