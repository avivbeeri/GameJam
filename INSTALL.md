# How to install and run *Ghost*
When the jam is completed and at regular intervals afterwards, we will aim to provide binaries for OSX and Linux using py2app and pyinstaller. We may additionally provide packages for some common flavours of Linux, but we cannot promise this. The instructions below describe how to get *Ghost* running fom source.

## OSX and Linux
* Clone the git repository.
* Install python 2.7.x and [pip](https://pip.pypa.io/en/stable/installing/), if you haven't already, and upgrade pip to the latest version.
* Download and install [pygame](http://www.pygame.org/download.shtml).
* If you don't already have it, make sure you grab libvorbis from your package manager.
* If you're on a mac, you may need to downgrade SDL to 1.2.10 - see [here](https://bitbucket.org/pygame/pygame/issues/284/max-osx-el-capitan-using-the-deprecated)
* Run (in any terminal): 
```shell
pip install pytmx
python game.py
```

## Windows
Windows is tricky, for some reason. The advice here may or may not result in a working game, but you are welcome to try.
* Clone the git repository.
* Install a 64-bit version of python 2.7.x
* Install pip and upgrade it to the latest version.
* Download a 64-bit version of [pygame](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) - do not rename it!
* Run the following in a terminal running as an administrator:
```cmd
pip install <path to downloaded pygame whl>
pip install pytmx
```
Hopefully you should now be able to run *Ghost* by double-clicking game.py or by running from a terminal:
```cmd
python game.py
```

## Binaries
When released, binaries will be uploaded to itch.io. Only a few versions will be kept around there, so if you want to play an arbitrary version you will have to keep up to date with the github repository.