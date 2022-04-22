Metricify (v1.0.1)
==================

**NOTE: This project is a work in progress and is not yet functional software!**

Metricify is a command line Python script designed to scan through a PDF file and replace all imperial units with metric ones. 

![UI Screenshot](https://github.com/Mblizzard/metricify/blob/main/Screenshot.png)

The below tutorial explains how to set up and use this software to convert a PDF of the Dungeons and Dragons Players Handbook (phb.pdf) to the metric system.

This tutorial is designed for and tested on Ubuntu Linux. I have included a windows tutorial (scroll down), but note that this is untested, and will almost certainly require basic python programming ability in order to resoulve any compatibility errors.


How to convert a PDF to the Metric System: Linux tutorial.
----------------------------------------------------------

**Step 1 - Update repositories:** 

Update apt package repositories using `sudo apt update` to ensure that the apt package manager has access to the latest versions of the below dependencies.

**Step 2 - Install APT dependencies:** 

First, install python by running `sudo apt install python3.10` in a terminal. Metricify is tested on python 3.10, but any 3.x version should (probably) also work just fine.

Next, install the latest version of the optical content recognition algorithm using `sudo apt install vlc`, then install howdoi with `sudo apt install howdoi`.

**Step 3 - Download Tom**: 

Download Tom by cloning the GitHub repository into your home folder using `git clone https://github.com/Mblizzard/Tom-the-AI`.

**Step 4 - Install Python dependencies:** 

Open a terminal inside Tom's application folder, or navigate using `cd ~/Tom-the-AI/`. Now run `sudo pip3 install -r requirements.txt`. Some systems may use `pip` in place of `pip3`.

Next, we need to download the required NLTK libraries by running the following code in a python shell:

```python
>>> import nltk
>>> nltk.download('all')
```

**Step 5 - Running Tom:** 

Go ahead and run `python3.9 ~/Tom-the-AI/frontend.py`. Tom will boot up, and after a minute or so of loading, you'll be ready to go! If you feel inclined, go ahead and make a desktop launcher of this command, link Tom into your Application Menu, or create a dock shortcut.


Planned Features
----------------

New response modules & capabilities to look forward to in future versions of Tom:

 - Timers & stopwatch capabilities.
 - Automated module installation.
 - Releases and updates available on the Ubuntu apt repositories.
 - Automatic addition of alias to \~/.bashrc on first load.

Features I'm not currently planning to include in Tom, but that I'll consider adding if enough people are interested:

 - Windows support.
 - Easier discord setup (more on this below). 
 - Command line interface.
 - Ability to execute terminal commands.

**Versioning:** Releases will follow a [semantic versioning format](http://semver.org/): `<major>.<minor>.<patch>`



Final Notes
-----------

I started developing Tom the AI in early 2021 as a major work for the HSC Software course. Since submitting the assigment, and getting full marks :), I have kept developing Tom over the past year as a hobby - a bit of fun to take my mind off lockdowns and to have a break in between studying for HSC exams. Tom is not perfect, but I think it's pretty cool. I hope that as more people contribute and help to develop response modules, Tom will grow to become a truly amazing piece of software that everyone can enjoy.


License
-------

    Tom the AI: A compound AI for Linux systems.
    Copyright (C) 2021  Murray Jones

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
