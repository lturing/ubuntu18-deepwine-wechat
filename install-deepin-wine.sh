#!/bin/bash
echo '准备添加32位支持'
sudo dpkg --add-architecture i386

echo "updating cache"
sudo apt update -y

echo "installing libs..."
sudo dpkg -i --force-overwrite ./libs/*.deb
sudo apt  install -fy -o Dpkg::Options::="--force-overwrite"

sudo apt autoremove -y

echo "done."

#sudo dpkg --configure -a
