#!/bin/bash

docker rmi thesheff17/chromelinuxbootstrapbase:latest
time docker build . -t thesheff17/chromelinuxbootstrapbase:latest -f Dockerfilebase
