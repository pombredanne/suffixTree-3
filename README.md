Linear Time implementation of Suffix Tree
=========================================

What is [suffix tree](http://en.wikipedia.org/wiki/Suffix_tree)? What is it good for?
=====================================================================================

In computer science, a suffix tree (also called PAT tree or, in an earlier form,
 position tree) is a data structure that presents the suffixes of a given string
 in a way that allows for a particularly fast implementation of many important string 
 operations.

The suffix tree for a string  is a tree whose edges are labeled with strings, 
such that each suffix of  corresponds to exactly one path from the tree's root to 
a leaf. It is thus a radix tree (more specifically, a Patricia tree) for the 
suffixes of. A suffix tree is a special kind of a Trie.

Constructing such a tree for the string takes time and space linear to the length of 
string. Once constructed, several operations can be performed quickly. For 
instance locating a substring allowing or not allowing certain number of mismatches, 
locating matches using a regex pattern etc. Suffix trees also provided one of the 
first linear-time solutions for the longest common substring problem. These speedups 
come at a cost: storing a string's suffix tree typically requires significantly more 
space than storing the string itself.

Requirements
=============
Python version >2.7

Example Usage
=============
Below command will construct the suffix tree for the string stored in file test1 

    ./SuffixTree.py -f test1 

Below command will construct the suffix tree for string "ABCDAGCD" 

    ./SuffixTree.py -s "ABCDAGCD" 

Using below commands to see more options of this program

    ./SuffixTree.py -h
    
Send Bugs/Commnents to
======================
Zhigang Wu (zhigang.wu@email.ucr.edu)



LICENSE
=========
Copyright (c) <2013>, <Zhigang Wu>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, 
       this list of conditions and the following disclaimer.
    
    2. Redistributions in binary form must reproduce the above copyright 
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

