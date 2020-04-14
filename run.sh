#!/bin/bash

docker rmi thesheff17/chromelinuxbootstrap:latest
time docker build . -t thesheff17/chromelinuxbootstrap:latest

echo "run.sh completed"
