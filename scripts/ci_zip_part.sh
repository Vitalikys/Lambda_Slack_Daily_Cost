#!/bin/bash

echo "----- Start CI part, installing Packages -----"

python3 -V

python3 -mpip install -r requirements.txt --target .

echo " ---- Print work directory:"
pwd

# Delete Directories *.dist.info
rm -r *.dist-info

zip -r cost_notif_$BUILD_NUMBER ./ -x *.git*  -x *.dist-info
ls -la

echo '------------------  END application commands ------------------'