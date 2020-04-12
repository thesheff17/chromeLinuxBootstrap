#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Dan Sheffner Digital Imaging Software Solutions, INC
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""
This program will bootstrap the debian container on chromebooks
"""
import os
import sys
import subprocess
import time

def check_for_root():
	if os.geteuid() != 0:
		print ("Sorry you have not ran this script with root privileges...")
		print ("Please use root or sudo")
		sys.exit(1)

def apt_get_packages():
    packages = ["ca-certificates", "build-essential", "htop", "vim", "tmux"]
    subprocess.run(["apt-get", "update"])
    install_command = ["apt-get", "-y", "install"] + packages
    subprocess.run(install_command)

def install_ruby_rails():
    command1 = "gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB"
    command2 = "curl -sSL https://get.rvm.io | bash -s stable --rails"
    subprocess.run(command1, shell=True)
    subprocess.run(command2, shell=True)

if __name__ == "__main__":
    start = time.time()
    
    check_for_root()
    apt_get_packages()
    install_ruby_rails()

    done = time.time()
    elapsed = done - start
    print ("Time elapsed in seconds: %s" % (elapsed))
