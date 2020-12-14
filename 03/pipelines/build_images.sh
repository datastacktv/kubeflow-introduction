#!/bin/bash

# Script for executing build processes of all components
# In case you get a run permission error uncomment line 11

for d in */ ;
do
	if [ "$d" != "src" ]
	then 
		cd "$d"
		chmod +x *.sh
		./*.sh
		echo "$d built"
		cd ..
    fi
done
