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
                 "cowsay",
                 "default-libmysqld-dev",
                 "default-mysql-server",
                 "fortune",
                 "gnupg2",
                 "htop",
                 "locate",
                 "lolcat",
                 "openjdk-11-jdk",
                 "postgresql-11",
                 "postgresql-server-dev-11",
                 "python3-dev",
                 "python3-pip",
                 "python3-psycopg2",
                 "python3-venv",
                 "vim",
                 "sl",
                 "tmux",
                 "wget"]

# ruby gems
GEMS = "bundler jekyll"

# global pip packages
PIP_PACKAGES = ["bpython",
                "virtualenv",
                "virtualenvwrapper"]
# virtual env packages
VIRT_PIP_PACKAGES = ["alembic",
                     "awscli",
                     "boto3",
                     "bpython",
                     "coverage",
                     "django",
                     "django-autoslug",
                     "django-braces",
                     "django-compressor",
                     "django-crispy-forms",
                     "django-debug-toolbar",
                     "django-environ",
                     "django-floppyforms",
                     "django-model-utils",
                     "django-nose django-axes",
                     "django-redis",
                     "django-sass-processor",
                     "django-secure",
                     "django-test-plus",
                     "django_extensions",
                     "factory_boy",
                     "flask",
                     "flask-bcrypt",
                     "flask-login",
                     "flask-migrate",
                     "flask-script",
                     "flask-sqlalchemy",
                     "flask-testing",
                     "flask-wtf",
                     "gunicorn",
                     "ipdb",
                     "itsdangerous",
                     "jupyter",
                     "libsass",
                     "mako",
                     "markupsafe",
                     "pillow django-allauth",
                     "psycopg2",
                     "py-bcrypt",
                     "pyflakes",
                     "pylibmc",
                     "pymysql",
                     "python-dateutil",
                     "pytz",
                     "redis",
                     "sphinx",
                     "sqlalchemy",
                     "unicode-slugify",
                     "werkzeug",
                     "whitenoise",
                     "wtforms"]

# golang url
GOLANG = "https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz"
GOLANGFILE = GOLANG.split("/")[-1]

# vscode extentions
VSCODE_EXTENTIONS = ["code --install-extension dbaeumer.vscode-eslint",
                     "code --install-extension HookyQR.beautify",
                     "code --install-extension kalitaalexey.vscode-rust",
                     "code --install-extension ms-python.python",
                     "code --install-extension ms-vscode.Go",
                     "code --install-extension rust-lang.rust"]

home_dir = os.path.expanduser("~")

def add_to_file(filename, contents):
    if os.path.isfile(filename):
        f1 = open(filename, 'r')
        data = f1.read()
        f1.close()

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
    # we can add a file called gitinfo in our home directory to auotmate this
    # email
    # username 
    # and I will automatically read it here otherwise it prompts you for this info

    print ("config git info")
    email = ""
    name = ""

    print (home_dir + "/gitinfo")
    if os.path.isfile(home_dir + "/gitinfo"):
        f1 = open(home_dir + "/gitinfo", 'r')
        data = f1.readlines()
        f1.close()
        email = data[0]
        name = data[1]
    else:
        email = input("Please enter your email? ")
        name = input("Please enter  your full name? ")

    command1 = 'git config --global user.email "' + email + '"'
    command2 = 'git config --global user.name "' + name + '"'

    sb.run(command1, shell=True, check=True)
    sb.run(command2, shell=True, check=True)
    
    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in subdirs:
        
        command3 = "sudo -H -u " + each.split("/")[-1] + " bash -c 'git config --global user.email " + email.strip("\n") + "'"
        command4 = "sudo -H -u " + each.split("/")[-1] + " bash -c 'git config --global user.name " + name.strip("\n") + "'"
        print (command3)
        sb.run(command3, shell=True, check=True)
        sb.run(command4, shell=True, check=True)
     
def apt_get_packages():
    # vscode stuff
    command1 = "curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg"
    command2 = "install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/"

    vscodestring = "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main"
    add_to_file('/etc/apt/sources.list.d/vscode.list', vscodestring)

    sb.run(command1, shell=True, check=True)
    sb.run(command2, shell=True, check=True)

    sb.run(["apt-get", "update"], check=True)

    packages = " ".join(PACKAGES_LIST)
    install_command = "DEBIAN_FRONTEND=noninteractive apt-get -y install " + packages
    sb.run(install_command, shell=True, check=True)
    
def generate_ssh_keys():
    command1 = "ssh-keygen -t rsa -f /root/.ssh/id_rsa -N '' -b 4096"
    if not os.path.isfile("/root/.ssh/id_rsa"):
        sb.run(command1, shell=True, check=True)

    # generate keys for anyone users in the home directory
    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in subdirs:
        if not os.path.isdir(each + "/.ssh"):
            os.mkdir(each + "/.ssh")

        if not os.path.isfile(each + "/.ssh/id_rsa"):
            command2 = "ssh-keygen -t rsa -f " + each + "/.ssh/id_rsa -N '' -b 4096"
            sb.run(command2, shell=True, check=True)
            command3 = "chown " + each.split("/")[-1] + ":" + each.split("/")[-1] + " " + each + "/.ssh/id_rsa"
            command4 = "chown " + each.split("/")[-1] + ":" + each.split("/")[-1] + " " + each + "/.ssh/id_rsa.pub"

            sb.run(command3, shell=True, check=True)
            sb.run(command4, shell=True, check=True)

def install_ruby_rails():
    command1 = "gpg2 --yes --always-trust --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB"
    command2 = "curl -sSL https://get.rvm.io | bash -s stable --rails"
    command3 = "sudo ln -s /usr/local/rvm/rubies/ruby*/bin/ruby /usr/bin/ruby"
    command4 = "sudo ln -s /usr/local/rvm/rubies/ruby*/bin/gem /usr/bin/gem"
    command5 = "/etc/profile.d/rvm.sh && gem install " + GEMS
    command6 = "curl -sSL https://get.rvm.io | bash -s stable"
    command7 = "/usr/local/rvm/bin/rvm all do rvm docs generate"

    sb.run(command1, shell=True, check=True)
    sb.run(command2, shell=True, check=True)

    if os.path.isfile("/usr/bin/ruby"):
        os.remove("/usr/bin/ruby")

    if os.path.isfile("/usr/bin/gem"):
        os.remove("/usr/bin/gem")

    sb.run(command3, shell=True, check=True)
    sb.run(command4, shell=True, check=True)
    sb.run(command5, shell=True, check=True)
    sb.run(command6, shell=True, check=True)
    sb.run(command7, shell=True, check=True)

def install_rust():
    command1 = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
    sb.run(command1, shell=True, check=True)

def install_golang():
    # clean up if we alrady installed it
    if os.path.isfile(GOLANGFILE):
        os.remove(GOLANGFILE)

    if os.path.isdir("/usr/local/go"):
        shutil.rmtree("/usr/local/go")

    command1 = ["wget", "-q", GOLANG]
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
    # I could not get virtualenvwrapper installed correctly under the non privileged user
    # there is allot of problems with the way you have to "source" certain files.
    # for now I will just create an venv one.  
    # feel free to provide a PR if you can get this working...

    virt_pip_packages = " ".join(VIRT_PIP_PACKAGES)
    command1 = ["pip3", "install", "pip", "--upgrade"]
    command2 = ["pip3", "install",] + PIP_PACKAGES
   
    sb.run(command1, check=True)
    sb.run(command2, check=True)
   
    add_to_file("/root/.bashrc", "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3")
    add_to_file("/root/.bashrc", "source /usr/local/bin/virtualenvwrapper.sh")

    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in subdirs:
        add_to_file(each + "/.bashrc", "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3")
        add_to_file(each + "/.bashrc", "source /usr/local/bin/virtualenvwrapper.sh")
        
        if not os.path.isdir(each + "/.virtualenvs/"):
            os.mkdir(each + "/.virtualenvs/")
            command3 = "chown " + each.split("/")[-1] + ":" + each.split("/")[-1] + " " + each + "/.virtualenvs/"
            sb.run(command3, shell=True, check=True)

        # command3 = "su - " + each.split("/")[-1] + " && python3 -m venv " + each + "/.virtualenvs/venv3"
        command3 = "sudo -H -u " + each.split("/")[-1] + " bash -c 'python3 -m venv " + each + "/.virtualenvs/venv3'"
        sb.run(command3, shell=True, check=True)

        command4 =  'sudo -H -u ' + each.split("/")[-1] + " bash -c 'source " + each + "/.virtualenvs/venv3/bin/activate && pip3 install --no-cache-dir " + virt_pip_packages + "'"
        sb.run(command4, shell=True, check=True)

def install_node():
    command1 = "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash"
    command2 = "chmod +x /root/.nvm/nvm.sh"
    command3 = 'bash -c "source /root/.bashrc && nvm install node --lts"'

    sb.run(command1, shell=True, check=True)
    sb.run(command2, shell=True, check=True)
    sb.run(command3, shell=True, check=True)

def install_vscode_extentions():
    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in subdirs:
        for each1 in VSCODE_EXTENTIONS:
            sb.run("sudo -H -u " + each.split("/")[-1] + " bash -c '" + each1 + "'", shell=True, check=True)

def update_locate_db():
    # this command throws some find errors
    # so for now I'm going to suppress the error
    command1 = "updatedb 2>/dev/null"
    sb.run(command1, shell=True, check=True)

def add_to_bashrc():
    s1 = "source $HOME/.cargo/env"
    s2 = "export PATH=$PATH:/usr/games/"
    s3 = 'export NVM_DIR="$HOME/.nvm"'
    s4 = '''[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm'''
    s5 = '''[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion'''

    add_to_file("/root/.bashrc", s1)
    add_to_file("/root/.bashrc", s2)

    d = '/home/'
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    for each in subdirs:
        add_to_file(each + "/.bashrc", s1)
        add_to_file(each + "/.bashrc", s2)
        add_to_file(each + "/.bashrc", s3)
        add_to_file(each + "/.bashrc", s4)
        add_to_file(each + "/.bashrc", s5)


if __name__ == "__main__":
    start = time.time()
    
    # clear screen
    sb.run(["clear"])
    print ("bootstrap.py started...")
    
    check_for_root()
    set_git_info() 
    apt_get_packages()
    generate_ssh_keys()
    install_ruby_rails()
    install_rust()
    install_golang()
    configure_pip()
    install_node()
    install_vscode_extentions()
    add_to_bashrc()
    update_locate_db()

    done = time.time()
    elapsed = done - start
    print ("bootstrap.py completed. Time elapsed in seconds: %s" % (elapsed))
