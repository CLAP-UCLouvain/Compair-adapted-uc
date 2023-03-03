#!/bin/bash

. $PWD/env/bin/activate

python3.10 script.py

deactivate
echo "Would you like to rebuild compair automatically [y/n]"
read -r ans
 if [ "$ans" == 'y' ]
then
  /bin/bash ../rebuildcompair.sh
fi
