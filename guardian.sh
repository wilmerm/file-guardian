#!/bin/bash

command_name=$1

option1=$2

option2=$3

echo "python3 app/main.py $command_name $option1 $option2"

python3 app/main.py $command_name $option1 $option2

