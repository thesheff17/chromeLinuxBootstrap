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

## testing

Testing this script gets increasily harder as it gets more complicated and longer.
There are a number of ways we can speed this testing up of bootstrap.py.

```
Dockerfilebase - base docker container running only apt-get configuration
buildBase.sh   - builds Dockerfilebase file
Dockerfile     - inheritance Dockerfilebase and runs bootstrap.py
run.sh         - builds Dockerfile file
```
## problems I ran into with this script

* virtualenvwrapper
  * this tool wants you to source a file after installation and your not running this in bash
  * what makes it even more complicated is you are using sudo to run bootstrap.py and then trying to
    switch to this user during the script.  At this time I just used virtualenv instead.  Feel free
    to still use virtualenvwrapper.  packages should be cached I believed.  

* GemWrappers: Can not wrap missing file
  * when running inside the docker container I get these weird errors about can not wrap missing
    file over and over again.  The script still runs fine and I beleive I only see them inside
    docker when testing.  I will keep an eye for a fix for this.  If you have an idea how to fix
    this let me know with a PR.

