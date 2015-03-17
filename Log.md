MAS-site assignments:
http://sites.google.com/site/matthijssnel/teaching/mas2011

TO DO:
  * Lijst van Lijst van Tuples (dis,x,y) voor de Distance Matrix
  * Sorteren van Preys op manhattan distance

# Monday September 12th #

Solved cloning sourecode with saved pass:
  * delete current clone from disk
  * Add the following to your .netrc: " machine code.google.com login EMAILADRESS password GOOGLECODEPASS "
  * clone: " git clone https://code.google.com/p/elmer-fudd/ "

Encountered problems running the python start.sh:
  * missing: libstdc++.so.5 (Fedora 15, Ubuntu 11.04)
  * missing: libglut.so.3 (Fedora 15, Ubuntu 11.04)
  * missing: libXmu (Fedore 15)

Fix Fedore 15:
  * yum install compat-libstdc++-33-3.2.3-68.1
  * yum install freeglut-2.6.0-6
  * yum install libXmu-1.1.0-2

Fix Ubuntu 11.04
  * apt-get install libstdc++5
  * apt-get install freeglut3