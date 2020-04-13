#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Dan Sheffner Digital Imaging Software Solutions, INC
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

# TODO
# basic vim tooling

import os
import sys
import subprocess as sb
import shutil
import time

# easily change vars

# apt-get packages
PACKAGES_LIST = ["build-essential",
                 "ca-certificates",
                 "code",
                 "default-mysql-server",
                 "htop",
                 "openjdk-11-jdk",
                 "nodejs",
                 "npm",
                 "postgresql-11",
                 "python3-pip",
                 "python3-dev",
                 "vim",
                 "wget",
                 "tmux"]

# ruby gems
GEMS = "bundler jekyll"

# global pip packages
PIP_PACKAGES = ["virtualenvwrapper",
                "virtualenv"]

# golang url
GOLANG = "https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz"
GOLANGFILE = GOLANG.split("/")[-1]

def add_to_file(filename, contents):
    f1 = open(filename, 'r')
    data = f1.read()
    f1.close()

    if os.path.isfile(filename):
        if contents not in data:
            with open(filename, 'a') as outfile:
                outfile.write(contents + "\n")
        else:
            print ("contents already in file skipping. file: " + filename + " contents: " + contents) 
    else:
        with open(filename, 'w') as outfile:
            outfile.write(contents + "\n")

def check_for_root():
	if os.geteuid() != 0:
		print ("Sorry you have not ran this script with root privileges...")
		print ("Please use root or sudo")
		sys.exit(1)

def set_git_info():
    email = input("Please enter your email? ")

    sys.stderr.write("\x1b[2J\x1b[H")
    name = input("Please enter  your full name? ")

    command1 = 'git config --global user.email "' + email + '"'
    command2 = 'git config --global user.name "' + name + '"'

    sb.run(command1, shell=True, check=True)
    sb.run(command2, shell=True, check=True)
    
    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in subdirs:
        command3 = "su - " + each.split("/")[-1] + " -c " + '"' + command1 + '"'
        sb.run(command3, shell=True, check=True)
     
def apt_get_packages():
    # vscode stuff
    command1 = "curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg"
    command2 = "mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg"

    sb.run(command1, shell=True, check=True)

    sb.run(command2, shell=True, check=True)

    sb.run(["apt-get", "update"], check=True)

    packages = " ".join(PACKAGES_LIST)
    install_command = "export DEBIAN_FRONTEND=noninteractive && apt-get -y install " + packages
    sb.run(install_command, shell=True, check=True)
    
def generate_ssh_keys():
    command1 = "ssh-keygen -t rsa -f /root/.ssh/id_rsa -N '' -b 4096"
    if not os.path.isfile("/root/.ssh/id_rsa"):
        sb.run(command1, shell=True, check=True)

    # generate keys for anyone users in the home directory
    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in subdirs:
        if not os.path.isfile(each + "/.ssh/id_rsa"):
            command2 = "ssh-keygen -t rsa -f " + each + "/.ssh/id_rsa -N '' -b 4096"
            sb.run(command2, shell=True, check=True)
            
def install_ruby_rails():
    command1 = "gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB"
    command2 = "curl -sSL https://get.rvm.io | bash -s stable --rails"
    command3 = "sudo ln -s /usr/local/rvm/rubies/ruby*/bin/ruby /usr/bin/ruby"
    command4 = "/usr/local/rvm/rubies/ruby*/bin/gem install " + GEMS 

    sb.run(command1, shell=True, check=True)
    sb.run(command2, shell=True, check=True)

    if os.path.isfile("/usr/bin/ruby"):
        os.remove("/usr/bin/ruby")
    sb.run(command3, shell=True, check=True)
    
    sb.run(command4, shell=True)
    
def install_rust():
    command1 = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
    sb.run(command1, shell=True, check=True)

def install_golang():
    # clean up if we alrady installed it
    if os.path.isfile(GOLANGFILE):
        os.remove(GOLANGFILE)

    if os.path.isdir("/usr/local/go"):
        shutil.rmtree("/usr/local/go")

    command1 = ["wget", GOLANG]
    command2 = "tar -C /usr/local -xzf go*.tar.gz"

    sb.run(command1, check=True)
    sb.run(command2, shell=True, check=True)

    s1 = "export PATH=$PATH:/usr/local/go/bin"
    add_to_file('/root/.bashrc', s1)

    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in subdirs:
        add_to_file(each + "/.bashrc", s1)

def configure_pip():
    command1 = ["pip3", "install", "pip", "--upgrade"]
    command2 = ["pip3", "install",] + PIP_PACKAGES

    sb.run(command1, check=True)
    sb.run(command2, check=True)
   
if __name__ == "__main__":
    start = time.time()
    
    # clear screen
    # sys.stderr.write("\x1b[2J\x1b[H")
    print ("bootstrap.py started...")
    
    check_for_root()
    set_git_info()
    apt_get_packages()
    generate_ssh_keys()
    install_ruby_rails()
    install_rust()
    install_golang()
    configure_pip()

    done = time.time()
    elapsed = done - start
    print ("bootstrap.py completed. Time elapsed in seconds: %s" % (elapsed))
