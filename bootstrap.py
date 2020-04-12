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
# TODO
# look for nodejs installation
# lets start configuring vim
# what other tools should I install? database tools?

import os
import sys
import subprocess as sb
import shutil
import time

# easily change vars

# apt-get packages
PACKAGES = ["ca-certificates", "build-essential", "htop", "vim", "wget", "tmux"]

# ruby gems
GEMS = "bundler jekyll"

# golang url
GOLANG = "https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz"
GOLANGFILE = GOLANG.split("/")[-1]

def check_return_status(result, message):
    try:
        if result.returncode != 0:
            print (message)
            sys.exit(1)
    except AttributeError:
        print ("could not find returncode value")
        sys.exit(1)

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

def apt_get_packages():
    result = sb.run(["apt-get", "update"])
    check_return_status(result, "could not run apt-get update")

    install_command = ["apt-get", "-y", "install"] + PACKAGES
    result = sb.run(install_command)
    check_return_status(result, "could not apt-get install packages")

def install_ruby_rails():
    command1 = "gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB"
    command2 = "curl -sSL https://get.rvm.io | bash -s stable --rails"
    command3 = "sudo ln -s /usr/local/rvm/rubies/ruby*/bin/ruby /usr/bin/ruby"
    command4 = "/usr/local/rvm/rubies/ruby*/bin/gem install " + GEMS 

    result = sb.run(command1, shell=True)
    check_return_status(result, "could not run gpg install for rvm")

    result = sb.run(command2, shell=True)
    check_return_status(result, "could not install ruby or rails")

    if os.path.isfile("/usr/bin/ruby"):
        os.remove("/usr/bin/ruby")
    result = sb.run(command3, shell=True)
    check_return_status(result, "could not make ruby symlink")

    result = sb.run(command4, shell=True)
    check_return_status(result, "could not install custom gems")

def install_rust():
    command1 = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
    result = sb.call(command1, shell=True)

    # this returns a weird status code for now I'm not going to check this
    # check_return_status(result, "could not install rust with rustup")

def install_golang():
    # clean up if we alrady installed it
    if os.path.isfile(GOLANGFILE):
        os.remove(GOLANGFILE)

    if os.path.isdir("/usr/local/go"):
        shutil.rmtree("/usr/local/go")

    command1 = ["wget", GOLANG]
    command2 = "tar -C /usr/local -xzf go*.tar.gz"

    result = sb.call(command1)
    result = sb.call(command2, shell=True)

    s1 = "export PATH=$PATH:/usr/local/go/bin"
    add_to_file('/root/.bashrc', s1)

    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in subdirs:
        add_to_file(each + "/.bashrc", s1)

if __name__ == "__main__":
    start = time.time()
    print ("bootstrap.py started...")
    
    check_for_root()
    # apt_get_packages()
    # install_ruby_rails()
    # install_rust()
    install_golang()

    done = time.time()
    elapsed = done - start
    print ("bootstrap.py completed. Time elapsed in seconds: %s" % (elapsed))
