import argparse
import os

parser = argparse.ArgumentParser(description = 'Extract audio from ultrasound video.')
parser.add_argument('files',metavar='U',type=str,nargs=2,help='csv file with files, directory for output')

args = parser.parse_args()
vidfile,target_directory = args.files

if not os.path.isdir(target_directory):
    os.mkdir(target_directory)

print "opening",vidfile
if target_directory != '':
  print "writing to",target_directory
  target_directory += "/"
else:
    target_directory = os.getcwd()

temp = open(vidfile,'rU')

files = temp.readlines()

temp.close()

for f in files:
  try:
    print 'extracting frames from %s'%f[0]
    new_command = "ffmpeg -v 0 -i %s -vn -ac 1 -f wav %s%s.wav" %(f,target_directory, f.strip(".avi"))
    #new_command = "ffmpeg -v 0 -r 30 -i %s -t %s -ss %s %s%s_%s-%%3d.jpg" %(f[0], dur, f[2], target_directory, f[0].strip(".avi"), f[1])
    #print new_command
    os.system(new_command)
  except:
    print 'failed to extract frames from %s'%f[0]


print 'finished'
