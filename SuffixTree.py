#!/usr/bin/env python2.7
"""
Linear time implementation of Suffix Tree (Ukkonnen's algorithm)

Ukkonnen's algorithm to implementation of Suffix Tree in 
linear time is well known. However, based on my past one month's
research both on academic paper and goolging on various forums, 
I found out that the implementation detail has never been crystal 
clearly being presented. Text book, like Dan Gusfield's and others 
give you a general idea on how a suffix tree can ben built in 
linear time but glossing over a lot of implementation details,
without which it is basically very difficult to implement suffix 
tree.

It's been a quite painful experience to figure out the details of 
implementation. After spending tens of hours in reading various 
materials, below I am listing out two main resources that I think 
they were, or were trying to, giving clear describptions on how to 
implement suffix tree in great detail.
[1] http://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english
[2] http://yeda.cs.technion.ac.il/~yona/suffix_tree/index.html


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
"""

import sys
import argparse
import itertools
import pdb


def check_args(args):
  if not(args.s or args.f):
    e.write("Error! Either choose to supply a string or a file!\n")
    exit(1)
  if args.s and args.f:
    e.write("Error! Either choose to supply a string or a file. Not both!\n")
    exit(1)
  
def line_yielder(file):
  with open(file) as IN:
    while True:
      line = IN.readline()
      if not line.endswith('\n') and line == "":
        break
      yield(line)
  IN.close() 

def fileToString(file):
  string = ""
  for line in line_yielder(file):
    line = line.strip()
    if not line == "":
      string += line
  return string

def get_str(args):
    if args.s:
        if len(args.s) == 1:
          return args.s[0]
        elif len(args.s) == 2:
          return args.s[0] + '#' + args.s[1] + '$'
        else:
          e.write("Error! You can only specify two strings at most!\n")
          exit(1)
    else:
      string = ""
      if len(args.f) == 1:
          for f in args.f:
            return fileToString(f) 
      elif len(args.f) == 2:
          return fileToString(args.f[0]) + '#' + fileToString(args.f[1]) + '$'
      else:
          e.write("Error! You can only specify two strings at most!\n")
          exit(1)

class Node(object):
  counter = itertools.count().next
  def __init__(self, start = None, end = None, SuffixLink = None, parent = None, id = None):
    self.start = start
    self.end = end
    self.id = Node.counter()
    self.SuffixLink = SuffixLink
    self.parent = parent
    self.children = {}
  def __repr__(self):
      return "Node(id=%d, start=%d, end=%d, SuffixLink=%s)" % (self.id, self.start, self.end, self.SuffixLink) 
  def edgeLen(self):
    return self.end - self.start 


class SuffixTree:
    def __init__(self, string, nodes = None):
        self.string = string
        self.currentNode = 0
        self.first_str_end = None # this is the end index for the first string
        self.position = -1
        self.nodes = nodes if nodes else []
        self.root = self.newNode(-1, -1, parent=None)
        self.active_node = self.root
        self.active_edge = 0
        self.active_len = 0
        self.remainder = 0
        self.memSize = 0
        self.end = len(self.string) 
        self.needSuffixLink = 0
        for i in self.string:
            self.__addChar(i)
        
    def newNode(self, start, end, parent = None):
        n = Node(start, end, parent = parent)
        self.nodes.append(n)
        return n

    def active_edge_c(self):
        return self.string[self.active_edge]

    def walkDown(self, node):
        if self.active_len >= node.edgeLen():
            self.active_edge += node.edgeLen()
            self.active_len -= node.edgeLen()
            self.active_node = node
            return True
        return False

    def addSuffixLink(self, node):
        if self.needSuffixLink:
            self.needSuffixLink.SuffixLink = node
        self.needSuffixLink = node

    def __addChar(self, c):
        self.position += 1
        if c == '#':
            self.first_str_end = self.position
        self.remainder += 1
        self.needSuffixLink = None
        while self.remainder > 0:
            if self.active_len == 0: self.active_edge = self.position
            if self.active_edge_c() not in self.active_node.children:
                leaf = self.newNode(self.position, self.end)
                self.active_node.children[self.active_edge_c()] = leaf
                leaf.parent = self.active_node
                self.addSuffixLink(self.active_node) #rule 2
            else:
                original_leaf = self.active_node.children[self.active_edge_c()]

                if self.walkDown(original_leaf): continue # observation 2
                if self.string[original_leaf.start + self.active_len] == c: #observation 1
                    self.active_len += 1
                    self.addSuffixLink(self.active_node) # observation 3
                    break

                split = self.newNode(original_leaf.start, 
                                     original_leaf.start + self.active_len)

                self.active_node.children[self.active_edge_c()] =  split
                split.parent = self.active_node
                leaf = self.newNode(self.position, self.end)
                split.children[c] = leaf
                leaf.parent = split
                original_leaf.start += self.active_len
                split.children[self.string[original_leaf.start]] =  original_leaf
                original_leaf.parent = split
                self.addSuffixLink(split) 
            self.remainder -= 1

            if self.active_node == self.root and self.active_len > 0: # rule 1
                self.active_len -= 1
                self.active_edge = self.position - self.remainder + 1
            else: # rule3
                self.active_node = self.active_node.SuffixLink if self.active_node.SuffixLink  else self.root
                    
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
        if type(nodeID) == type(Node()):
            return "".join(self.string[nodeID.start:nodeID.end])

    def printLeaves(self, nodeID, buffer):
        if len(nodeID.children) == 0:
            buffer.write("\tnode"+str(nodeID.id)+" [label=\"\",shape=point]\n")
        else:
            for child in nodeID.children.values():
                self.printLeaves(child, buffer)
    def printInternalNodes(self, nodeID, buffer):
        if (not nodeID == self.root) and len(nodeID.children) > 0:
            buffer.write("\tnode"+str(nodeID.id)+
                    " [label=\"\",style=filled,fillcolor=lightgrey,shape=circle,width=.07,height=.07]\n")
        for child in nodeID.children.values():
            self.printInternalNodes(child, buffer)
    def printEdges(self, nodeID, buffer):
        for child in nodeID.children.values():
            buffer.write("\tnode"+str(nodeID.id)+" -> node"+
                    str(child.id)+" [label=\""+self.edgeString(child)+"\",weight=3]\n")
            self.printEdges(child, buffer)

    def printSLinks(self, nodeID, buffer):
        if nodeID.SuffixLink:
            buffer.write("\tnode"+str(nodeID.id)+" -> node"+ 
                    str(nodeID.SuffixLink.id)+" [label=\"\",weight=1,style=dotted]\n")
        for child in nodeID.children.values():
            self.printSLinks(child, buffer)

    def check_node(self, node):
        """
        This is one essential step in find the longest common ancestor for two strings.
        The criteria is that, there must be a child on the first string, and
        there must be another child from another string
        """
        hasPoundSign = hasDollarSign = False
        for child in node.children.values():
            if child.start <= self.first_str_end:
                hasPoundSign = True
            else:
                hasDollarSign = True
        if hasPoundSign and hasDollarSign:
            return True
        return False

    def PathString(self, node):
        if node.parent:
            prev = self.PathString(node.parent)
            return prev + self.edgeString(node)
        else:
            return ""

    def LongestUniqueStr(self):
        max_len = 0
        max_nodes = [None]
        for node in self.nodes:
            if self.check_node(node):
                if len(self.PathString(node)) > max_len:
                  max_len = len(self.PathString(node))
                  max_nodes[0] = node
                elif len(self.PathString(node)) == max_len:
                  max_nodes.append(node)
        if max_nodes[0]:
          return "\t".join([self.PathString(max_node) for max_node in max_nodes])
        return ""

    def findSubString(self, qString):
        i = 0
        node = self.root
        start = 0
        first_time = True
        while i < len(qString):
            c = qString[i]
            if c not in node.children:
                return False
            else:
                tNode = node.children[c]
                if first_time:
                    start = tNode.start # let start store the start index for the match
                    first_time = False
                tString = self.edgeString(tNode)
                steps = check_identity(tString, qString, i)
                if steps:
                    if steps + i >= len(qString) - 1:
                      return start, start+len(qString)-1
                    else:
                        i += steps
                        node = tNode
                else:
                    return False
    def memStatistics(self):
      for k, v in vars(self).items():
        self.memSize += sys.getsizeof(v)
       
def check_identity(tString, qString, qStart):
    """
    return 0 if not equal, otherwise number of steps moved
    """
    step = 0
    for c in tString:
        if qStart < len(qString):
            if c == qString[qStart]:
                qStart += 1
                step += 1
                continue
            else:
                return 0
    return step

if __name__ == '__main__':
    o = sys.stdout
    e = sys.stderr

    parser=argparse.ArgumentParser(description="Given a string or a file, constrution a suffix tree  " +
            "in linear time. If you wanna test out finding the longest common substring for two sequences " +
            "you can either supply with these two strings to -s, or two files to -f. " + 
            "This program will produce a dot file, which you can visulaize it by using tools like " +
            "graphviz. dot -Tpng -O sty.dot")
    parser.add_argument('-s', '--string', dest= 's', nargs='*', 
            help="specify a string")
    parser.add_argument('-f', '--file', dest= 'f', nargs='*', 
            help="specify a file")
    parser.add_argument('-q', '--query', 
            help="query sequence you try to known whether is a substring")
    parser.add_argument('-o', help="specify a output file name for dot file. Default=[sty.dto]", 
            default = "sty.dot")
    parser.add_argument('-r', '--report', default=False, action='store_true', help="report costed memory " +
            "size. Default=[False]")
    parser.add_argument('-g', '--graph', default=False, action='store_true', help="whether to print the " +
            "dot graph file. Default=[False]")
    args = parser.parse_args()

    check_args(args)
    string = get_str(args)
    suffixtree= SuffixTree(string)
    if args.report:
        suffixtree.memStatistics()
        str_len = str(len(string))
        mem_size = str(suffixtree.memSize)
        e.write("\t".join([str_len, mem_size]) + "\n")

    if args.graph:
        O = open(args.o, 'w')
        suffixtree.printTree(O)
        O.close()
    if args.query:
        result = suffixtree.findSubString(args.query)
        if not result:
            print "%s is NOT a substring of %s" % (args.query, string)
        else:
            print "%s is a substring of %s: index: %s" % (args.query, string, str(result) )
    if args.s and len(args.s) == 2:
        e.write("str1: %s\nstr2: %s\nLongestUniqueStr: %s\n" % (args.s[0], args.s[1], 
            suffixtree.LongestUniqueStr()))
