Metricify (v1.0.1)
==================

**NOTE: This project is a work in progress and is not yet functional software!**

Metricify is a command line Python script designed to scan through a PDF file and replace all imperial units with metric ones. 

![UI Screenshot](https://github.com/Mblizzard/metricify/blob/main/Screenshot.png)

The below tutorial explains how to set up and use this software to convert a PDF of the Dungeons and Dragons Players Handbook (phb.pdf) to the metric system.

Note that this tutorial is designed for and tested on Ubuntu Linux. I have included a windows tutorial (scroll down), but please be aware that this is untested, and will almost certainly require basic python programming ability in order to resoulve any compatibility errors.


How to convert a PDF to the Metric System: Linux tutorial.
----------------------------------------------------------

**Step 1 - Update repositories:** 

Update apt package repositories using `sudo apt update` to ensure that the apt package manager has access to the latest versions of the below dependencies.

**Step 2 - Install APT dependencies:** 

First, install python by running `sudo apt install python3.10` in a terminal. Metricify is tested on python 3.10, but any 3.x version should (probably) also work just fine.

Next, install the optical content recognition algorithm using `sudo apt install ocrmypdf`.

**Step 3 - Download Metricify**: 

Download Tom by cloning the GitHub repository into your home folder using `git clone https://github.com/Mblizzard/metricify`.

**Step 4 - Install Python dependencies:** 

Open a terminal inside the `metricify` application folder, or navigate using `cd ~/metricify/`. Now run `sudo pip3 install -r requirements.txt`. Note that some systems may use `pip` in place of `pip3`.

**Step 5 - Running Metricify:** 

Go ahead and run `python3.10 ~/metricify/metricify.py`. A window will appear prompting you to select a file. This will be the input file, with the imperial units that you want converted.




How to convert a PDF to the Metric System: Windows tutorial.
------------------------------------------------------------

Please be aware that this winown tutorial is **entirely untested**. There will almost certainly be a few compatibility errors. You will need at least a basic level of python programming experience to make this work.





Planned Features
----------------

New capabilities to look forward to in future versions of Metricify:

 - Input files specified via the command line.
 - 
Features I'm not currently planning to include in Metricify, but that I'll consider adding if enough people are interested:

 - Complete tested Windows support.


**Versioning:** Releases will follow a [semantic versioning format](http://semver.org/): `<major>.<minor>.<patch>`


License
-------

    Metricify: A software to convert Imperial units in a PDF file to Metric values.
    Copyright (C) 2022  Murray Jones

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
