# chromeLinuxBootstrap
This script will bootstrap chrome linux container based on debian.

You should read the contents of what bootstrap.py does before you run it!

if you agree to configure your machine with the script copy/paste the below command:
```
git clone https://github.com/thesheff17/chromeLinuxBootstrap.git && cd chromeLinuxBootstrap && sudo ./bootstrap.py
```

The goal of this script will try to follow these goals:
* The main goal is to bootstrap your chromebook into a development box.
* This script should always be able to run again if something goes wrong.
  * For example if you loose internet connection we want to run bootstrap.py and have it finish a 2nd time.
  * Also this makes it allot easier when people are testing the bootstrap.py script.
* Isolate definitions as much as possible.  Allow commenting out of these.