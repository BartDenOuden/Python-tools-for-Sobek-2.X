## Python tools voor Sobek 2.x

This repo contains several python modules to work with Sobek models. Sobek is a program by Deltares for the modelling of water systems. 
https://www.deltares.nl/en/software/sobek/

Functionality:
- read data from Sobek His-files into a python data structure; *sobekdatafetcher.py*
- generate (matplotlib) graphs showing data from Sobek and Excel-files; *sobekgraph.py*
- manipulation of Sobek boundary and lateral data; *sobekboundary.py and sobeklateral.py*

Prerequisites: 
- Python 3.6 or later
- the external libraries needed differ per module. sobekgraph.py uses pandas (numpy, matplotlib)

License: GNU General Public License v3.0
This is a free software, copyleft license, which means that any derivative work must be distributed under the same or equivalent license terms. 
https://www.gnu.org/licenses/gpl-3.0.en.html
https://en.wikipedia.org/wiki/GNU_General_Public_License

Examples of the use of the modules is given by these files:
- sobekgraph_tutorial.py
- use_sobekboundary.py
- use_sobekdatafetcher.py
- use_sobeklateral.py