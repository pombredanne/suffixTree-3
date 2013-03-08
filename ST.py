#!/usr/bin/env python2.7
"""
Linear time implementation of Suffix Tree (Ukkonnen's algorithm)

Ukkonnen's algorithm to implementation of Suffix Tree in 
linear time is well known. However, based on my past one month's
research either on academic paper or goolging on various forums, 
I found out that the implementation detail is never clear.
Text book, like Dan Gusfield's and others give you a general idea on how a
suffix tree can ben built but glossing over a lot implementation details,
without which you basically very difficult to implement it.

It's been quite painful experience to implement the suffix tree. After spending
tens of hours in reading various material, Below I listing out
two main resources that I think they were, or were trying to, giving clear describptions on how to 
implement suffix tree in great detail.
http://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english
http://yeda.cs.technion.ac.il/~yona/suffix_tree/index.html

Here are rules and observations I used to implement the suffix tree

Rule 1:
After an insertion from root:
	active_node remains root
	active_edge is set to the first character of the new suffix we need to insert
	active_length is reduced by 1

Rule 2:
If we create a new internal node OR make an inserter from an internal node, and this is not the first SUCH internal node at current step, then we link the previous SUCH node with THIS one through a suffix link.

Rule 3:
After splitting an edge from an active_node that is not the root node, we follow the suffix link going out of that node, if there is any, and reset the active_node to the node it points to. If there is no suffix link, we set the active_node to the root. active_edge and active_length remain unchanged.

Observation 1
When the final suffix we need to insert is found to exist in the tree already, the tree itself is not changed at all (we only update the active point, active_len and remainder).

Observation 2:
If at some point active_length is greater or equal to the length of current edge (edge_length), we move our active point down until edge_length is not strictly greater than active_length.

Reference:
http://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english

"""

import sys
import argparse
import itertools
import pdb


def check_args(args):
  if not(args.s or args.f):
    e.write("Error! Either choose to supply a string or a file!")
    exit(1)
  if args.s and args.f:
    e.write("Error! Either choose to supply a string or a file. Not both!")
    exit(1)

def line_yielder(file):
  with open(file) as IN:
    while True:
      line = IN.readline()
      if not line.endswith('\n') and line == "":
        break
      yield(line)
  IN.close() 

def get_str(args):
    if args.s:
      return args.s
    else:
      string = ""
      for line in line_yielder(args.f):
        line = line.strip()
        if not line == "":
          string += line
      return string

class Node(object):
  def __init__(self, start = None, end = None, SuffixLink = None):
    self.start = start
    self.end = end
    self.SuffixLink = SuffixLink
    self.next = {}
  def __repr__(self):
      return "Node(start=%d, end=%d, SuffixLink=%s)" % (self.start, self.end, self.SuffixLink) 
  def edgeLen(self):
    return self.end - self.start 


class SuffixTree:
    def __init__(self, string):
        self.string = string
        self.nodes = [None] * (len(self.string) * 2 + 2)
        self.currentNode = 0
        self.position = -1
        self.root = self.newNode(-1, -1)
        self.active_node = self.root
        self.active_edge = 0
        self.active_len = 0
        self.remainder = 0
        self.end = len(self.string)
        self.text = [None] * len(self.string)
        self.needSuffixLink = 0
        for i in self.string:
            self.__addChar(i)
        
    def newNode(self, start, end):
      self.currentNode += 1
      self.nodes[self.currentNode] = Node(start=start, end=end)
      return self.currentNode

    def active_edge_c(self):
        return self.text[self.active_edge]

    def walkDown(self, node):
        if self.active_len >= self.nodes[node].edgeLen():
            self.active_edge += self.nodes[node].edgeLen()
            self.active_len -= self.nodes[node].edgeLen()
            self.active_node = node
            return True
        return False

    def addSuffixLink(self, node):
        if self.needSuffixLink > 0:
            self.nodes[self.needSuffixLink].SuffixLink = node
        self.needSuffixLink = node

    def __addChar(self, c):
        self.position += 1
        self.text[self.position] = c
        self.remainder += 1
        self.needSuffixLink = -1
        while self.remainder > 0:
            if self.active_len == 0: self.active_edge = self.position
            if self.active_edge_c() not in self.nodes[self.active_node].next:
                leaf = self.newNode(self.position, self.end)
                self.nodes[self.active_node].next[self.active_edge_c()]=  leaf
                self.addSuffixLink(leaf) #rule 2
            else:
                original_leaf = self.nodes[self.active_node].next[self.active_edge_c()]
                if self.walkDown(original_leaf): continue # observation 2
                if self.text[self.nodes[original_leaf].start + self.active_len] == c: #observation 1
                    self.active_len += 1
                    self.addSuffixLink(self.active_node) # observation 3
                    break

                split = self.newNode(self.nodes[original_leaf].start, 
                                     self.nodes[original_leaf].start + self.active_len)
                self.nodes[self.active_node].next[self.active_edge_c()] =  split
                leaf = self.newNode(self.position, self.end)
                self.nodes[split].next[c] = leaf
                self.nodes[original_leaf].start += self.active_len
                self.nodes[split].next[self.text[self.nodes[original_leaf].start]] =  original_leaf
                self.addSuffixLink(split) 
            self.remainder -= 1

            if self.active_node == self.root and self.active_len > 0: # rule 1
                self.active_len -= 1
                self.active_edge = self.position - self.remainder + 1
            else: # rule3
                self.active_node = self.nodes[self.active_node].SuffixLink if self.nodes[self.active_node].SuffixLink  else self.root
                    
            



    
              

    def printTree(self, buffer):
        buffer.write("digraph {\n")
        buffer.write("\trankdir = LR\n")
        buffer.write("\tedge [arrbufferwsize=0.4,fbufferntsize=10]\n")
        buffer.write("\tnode1 [label=\"\",style=filled,fillcbufferlbufferr=lightgrey,shape=circle,width=.1,height=.1]\n")
        buffer.write("//------leaves------\n")
        self.printLeaves(self.root, buffer)
        buffer.write("//------internal nbufferdes------\n")
        self.printInternalNodes(self.root, buffer)
        buffer.write("//------edges------\n")
        self.printEdges(self.root, buffer)
        buffer.write("//------suffix links------\n")
        self.printSLinks(self.root, buffer)
        buffer.write("}\n")
    def edgeString(self,nodeID):
        return "".join(self.text[self.nodes[nodeID].start:self.nodes[nodeID].end])

    def printLeaves(self, nodeID, buffer):
        if len(self.nodes[nodeID].next) == 0:
            buffer.write("\tnode"+str(nodeID)+" [label=\"\",shape=point]\n")
        else:
            for child in self.nodes[nodeID].next.values():
                self.printLeaves(child, buffer)
    def printInternalNodes(self, nodeID, buffer):
        if (not nodeID == self.root) and len(self.nodes[nodeID].next) > 0:
            buffer.write("\tnode"+str(nodeID)+
                    " [label=\"\",style=filled,fillcolor=lightgrey,shape=circle,width=.07,height=.07]\n")
        for child in self.nodes[nodeID].next.values():
            self.printInternalNodes(child, buffer)
    def printEdges(self, nodeID, buffer):
        for child in self.nodes[nodeID].next.values():
            buffer.write("\tnode"+str(nodeID)+" -> node"+
                    str(child)+" [label=\""+self.edgeString(child)+"\",weight=3]\n")
            self.printEdges(child, buffer)

    def printSLinks(self, nodeID, buffer):
        if self.nodes[nodeID].SuffixLink:
            buffer.write("\tnode"+str(nodeID)+" -> node"+ 
                    str(self.nodes[nodeID].SuffixLink)+" [label=\"\",weight=1,style=dotted]\n")
        for child in self.nodes[nodeID].next.values():
            self.printSLinks(child, buffer)

#def compare_str():

def search(ST, node, tString, i, start, end):
    """
    start, the beginning match position index
    end, the last match position index
    i, the position index in tString from which searching begins
    """
    if i >= len(tString):
        return (start, end)
    if tString[i] in ST.nodes[node].next:
        tNode = ST.nodes[node].next[tString[i]]
        if start == 0: # only run this step for the first time
            start = ST.nodes[tNode].start
        end = ST.nodes[tNode].start
        flag = True
        for index, char in enumerate(ST.text[ST.nodes[tNode].start:ST.nodes[tNode].end]):
            if i+index < len(tString) and tString[i+index] == char:
                continue
            else:
                flag = False
                break
        if not flag: #means match stops in the middle of edge
            end +=  index  # index is 0-based offset
            return (start, end)
        else:
            end +=  index+1  # index is 0-based offset
            return search(ST, tNode, tString, i+index+1, start, end)
    else:
        return (start, end)

if __name__ == '__main__':
    o = sys.stdout
    e = sys.stderr

    parser=argparse.ArgumentParser(description="Constrution a suffix tree given a string or a file" +
            " in linear time.")
    parser.add_argument('-s', help="specify a string default=[mississippi].", default="mississipi")
    parser.add_argument('-f', help="specify a file")
    parser.add_argument('-t', help="specify the searching string", required=True)
    parser.add_argument('-o', help="specify a output file name for dot file", default = "sty.dot")
    
    args = parser.parse_args()

    check_args(args)
    string = get_str(args)
    suffixtree= SuffixTree(string)
    O = open(args.o, 'w')
    suffixtree.printTree(O)
    O.close()
    start, end = search(suffixtree, suffixtree.root,args.t,0, 0, 0)
    print start, end
