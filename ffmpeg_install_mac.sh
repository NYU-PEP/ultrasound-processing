curl -O http://ffmpegmac.net/resources/SnowLeopard_Lion_Mountain_Lion_Mavericks_Yosemite_08.12.2014.zip
unzip -d ffmpeg SnowLeopard_Lion_Mountain_Lion_Mavericks_Yosemite_08.12.2014.zip
rm SnowLeopard_Lion_Mountain_Lion_Mavericks_Yosemite_08.12.2014.zip
sudo cp -r ffmpeg/ /usr/bin/
rm -r ffmpeg
