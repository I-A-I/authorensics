# authorensics
 
By Philipp Steinmann, Richard Zhan, Steven Zabolotny, Ziwei Ye

[Demo Video](https://youtu.be/XksrKfxEprg)

An easily usable tool for anonymous author attribution, drawing sample texts from Facebook messaging. If you have an anonymous text and several candidate authors, *authorensics* uses one of two algorithms to calculate the most likely author.

The first algorithm is the Source Code Authorship Profile (SCAP) method (as described in "Identifying Authorship by Byte-Level N-Grams"). The second algorithm is the Visualizable Evidence-Driven Approach (VEA) to Attribution, as described in a paper of the same name.

**Dependencies**

This program is a Flask server.

Packages needed: 
- flask
- scipy
- nltk (with "Punkt" and "Maxent" models installed)


Stuyvesant High School, Software Development Final Project 2015
