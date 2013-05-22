Linear Time implementation of Suffix Tree
===========================================


### What is suffix tree? What is it good for?

In computer science, a suffix tree (also called PAT tree or, in an earlier form,
 position tree) is a data structure that presents the suffixes of a given string
 in a way that allows for a particularly fast implementation of many important s
tring operations.

The suffix tree for a string  is a tree whose edges are labeled with strings, su
ch that each suffix of  corresponds to exactly one path from the tree's root to 
a leaf. It is thus a radix tree (more specifically, a Patricia tree) for the suf
fixes of . A suffix tree is a special kind of a Trie.

Constructing such a tree for the string  takes time and space linear in the leng
th of . Once constructed, several operations can be performed quickly, for insta
nce locating a substring in , locating a substring if a certain number of mistak
es are allowed, locating matches for a regular expression pattern etc. Suffix tr
ees also provided one of the first linear-time solutions for the longest common 
substring problem. These speedups come at a cost: storing a string's suffix tree
 typically requires significantly more space than storing the string itself.


Author
=========
Zhigang Wu

Deparment of Botany and Plant Sciences

University of California Riverside


LICENSE
=========
BSD LICENSE


