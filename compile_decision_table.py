#! /bin/env python

from sys import stdin
from typer import run
from os.path import exists
import os

"""
Node Class: Each node in the BDD is represented by a node.
The node keeps track of the value, which is the condition being asked, the children and the parents as well as a unique ID.
There are class attributes nodeCount, counting the total number of nodes created to assign unique IDs, 
nodesList, which is a list that includes all the nodes ordered by ID (as they are added),
and node0, node1 which are leaf nodes with value 0 or 1.
"""
class node:
    nodeCount = 0
    nodesList = []
    node0 = None
    node1 = None
    def __init__(self, value):
        #first node in the class created initializes node0 and node1
        if value != "0" and value != "1":
            try:
                a = node.node1.value
            except:
                node.node0 = node("0")
                node.node1 = node("1")
        self.ID = node.nodeCount
        node.nodeCount += 1
        node.nodesList.append(self)
        self.value = value
        self.children = [-1,-1] # default -1 for "no children"
        self.parents = [[],[]] # index 0 for reaching node after taking a decision for 0 and index 1 for reaching node after taking decision 1.

    def __repr__(self) -> str:
        if self.value != "0" and self.value != "1":
            return f"ID: {self.ID}, Value: {self.value}, children: {self.children}\n"
        return f"ID: {self.ID}"
    
    """
    addParent: takes an index (0 or 1) and a parent node (node). Adds the parent node to the given side of the index (0 or 1) to the current node
    """
    def addParent(self, index, parent):
        self.parents[index].append(parent)

    """
    setChild: takes an index (0 or 1) and a value (str). Sets the child of the current node in the direction of index (0 or 1) to the value.
    If the value is 0 or 1, the leaf nodes of the class are used.
    """
    def setChild(self, index, value):
        if value == "0":
            self.children[index] = node.nodesList[0]
        elif value == "1":
            self.children[index] = node.nodesList[1]
        else:
            self.children[index] = node(value)
        self.children[index].addParent(index, self)

    """
    changeChild: takes an index (0 or 1) and a newNode (node). Removes self as a parent of the current child 
    and then replace the current child with newNode. Add self to the parents of the newNode.
    """
    def changeChild(self, index, newNode):
        if self.children[index] != -1:
            self.children[index].parents[index].remove(self)
        self.children[index] = newNode
        self.children[index].parents[index].append(self)

    """
    changeParents: takes an index (0 or 1), an oldParent (node) and a newParents(list of nodes). it removes the old parent from the self node
    and adds all nodes in newParents to the current node's parents. 
    Used to move all parents of one node to connect to a different node instead
    """
    def changeParents(self, index, oldParent, newParents):
        if oldParent != None:
            self.parents[index].remove(oldParent)
        for i in newParents:
            self.parents[index].append(i)
    
    """
    printClassInfo: prints the BDD starting from the root Node downwards and the number of nodes.
    """
    def printClassInfo(node):
        print(f"Nodes: {node.nodesList[2]}, Node Count: {node.getNodeCount()}")
    
    """
    checkIdenticalChildren: checks a node on the condition if both children have the same value.
    In that case the current node is removed and all parents of the current node are directly linked to the child of the current node.
    """
    def checkIdenticalChildren(self):
        if self.children[0] == self.children[1] and self.children[0] != -1:
            for parent in self.parents[0]:
                parent.changeChild(0, self.children[0])
            for parent in self.parents[1]:
                parent.changeChild(1, self.children[0])
            self.children[0].changeParents(0,self, self.parents[0])
            self.children[0].changeParents(1, self, self.parents[1])
            node.nodesList.remove(self)
            
    """
    checkIdenticalSibling: checks a node on the condition if one of it's siblings (another node that is asking for the same letter) has the same children.
    In that case it removes the current node and makes its parents, parents of the sibling instead. It also makes the sibling the new child of the parents.
    """        
    def checkIdenticalSibling(self):
        min_index = node.nodesList.index(self)
        siblings = [i for i in node.nodesList[min_index:] if i.value == self.value and i.ID != self.ID]
        for s in siblings:
            if s.children[0] == self.children[0] and s.children[1] == self.children[1]:
                for parent in self.parents[0]:
                    parent.changeChild(0, s)
                for parent in self.parents[1]:
                    parent.changeChild(1, s)
                s.changeParents(0,None,self.parents[0])
                s.changeParents(1,None,self.parents[1])
                node.nodesList.remove(self)
                break
    
    """
    getNodecount: returns the number of nodes in the nodesList. This is the amount of nodes that remain in the BDD.
    """
    def getNodeCount(node):
        return len(node.nodesList)

"""
line_parts: takes a line of text (string) and splits it at the separator |.
It returns a list of the single elements that were in the line of text, without the separator.
"""
def line_parts(line):
    return [v for v in [v.strip() for v in line.split("|")] if v]

"""
reduceBDD: takes a root node (node) as input and reduces the BDD as far as possible using the checkIdenticalSibling and checkIdenticalChildren functions.
"""
def reduceBDD(root):
    count = 0
    newCount = node.getNodeCount(node)
    while newCount != count:
        count = newCount
        for nodei in node.nodesList[2:]:
            nodei.checkIdenticalChildren()
        for nodei in node.nodesList[2:]:
            nodei.checkIdenticalSibling()
        newCount = node.getNodeCount(node)

"""
split: takes nodei (node), indent (int) and f (file). 
It takes the given node and writes the if-statements and "return 0"/"return 1" in the file at the correct indentation.
If an if statement is written it recursively goes deeper down the BDD to continue the branch.
"""
def split(nodei, indent,f):
    if nodei.value == "0":
        line = 4*indent*" "+"return 0\n"
        f.write(line)
        return
    elif nodei.value == "1":
        line = 4*indent*" "+"return 1\n"
        f.write(line)
        return
    line = 4*indent*" "+f"if {nodei.value}:\n"
    f.write(line)
    split(nodei.children[1], indent+1, f)
    split(nodei.children[0], indent, f)

"""
createText: takes a root (node) and arglist (string) which is the list of variables joined by ",".
It checks whether the current solution is better than the best previous solution. 
If this is the case, it overwrites the file with the new solution.
The file is a fully functional python file with a function decider which entails if statements as written by the split function.
"""
def createText(root, arglist):
    if exists("decision_maker.py"):
        f = open("decision_maker.py", "r")
        line1 = f.readline()[1:]
        nrNodes = int(line1)
        if nrNodes <= root.getNodeCount():
            f.close()
            return
        f.close()
    f = open("decision_maker.py", "w")
    f.write(f"#{len(node.nodesList)}\n")
    f.write("#! /bin/env python\n")
    f.write("from typer import run\n")
    f.write(f"def decide({arglist}):\n")
    f.write(f"    {arglist} = [int(a) for a in [{arglist}]]\n")
    split(root, 1, f)
    f.write(
        """\nif __name__ == "__main__":
    run(decide)"""
    )
    f.close()

"""
compile_decision_table: The main function that is called when the program is executed.
It checks if an output file exists, and removes it if it does.
It saves the input in an input file.
The function then goes through all possible permutations of the variables, creates the BDD, and reduces it to find the most efficient BDD.
"""
def compile_decision_table():
    if exists("decision_maker.py"):
        os.remove("decision_maker.py")
    fIn = open("input_file.txt", "w")
    for line in stdin:
        fIn.write(line)
    fIn.close()
    fInBefore = open("input_file.txt", "r")
    header = fInBefore.readline()
    varsInitial = line_parts(header)

    """
    permutations: takes vars (array) and returns all possible permutations of these variables.
    """
    def permutations(vars):
        if len(vars) == 0:
            yield []
        elif len(vars) == 1:
            yield vars
        else:
            for i in range(len(vars)):
                first_element = vars[i]
                remaining_elements = vars[:i] + vars[i+1:]
                for perm in permutations(remaining_elements):
                    yield [first_element] + perm

    # Generate and iterate through all permutations
    for vars in permutations(varsInitial):
        fIn = open("input_file.txt", "r")
        header = fIn.readline()

        node.nodeCount = 0  # reset node class
        node.nodesList = []
        node.node0 = None
        node.node1 = None
        arglist = ", ".join(vars)

        """
        extend: takes a node1 (node), vars (array) and count (int).
        This function recursively creates an empty BDD of the size given by len(vars).
        """
        def extend(node1, vars, count):
            if count == len(vars):
                return
            node1.setChild(0, vars[count])
            node1.setChild(1, vars[count])
            extend(node1.children[0], vars, count+1)
            extend(node1.children[1], vars, count+1)
        root = node(vars[0])
        extend(root, vars, 1)

        """
        change_order: takes the combination of 0's and 1's in the initial order parts (array) and the variables in new order vars (array).
        It reorders the parts array according to the new permutation of the variables.
        """
        def change_order(parts, vars):
            newParts = [i for i in range(len(vars))]
            for i in range(len(parts)-1):
                newParts[vars.index(chr(97+i))] = parts[i]
            return newParts
        for n, line in enumerate(fIn.readlines()):
            parts_init = line_parts(line) # get input choices by variable
            parts = change_order(parts_init, vars) # reoder input choices to match the permutation of variables
            nodei = root
            j = 0
            while nodei.children[int(parts[j])] != -1:
                nodei = nodei.children[int(parts[j])]
                j += 1
            nodei.changeChild(int(parts[j]), node.nodesList[int(parts_init[-1])]) # fill in the position with the correct value
        reduceBDD(root)
        createText(root, arglist)
        fIn.close()
    fInBefore.close()

    #Print file and remove used files from the system
    os.remove("input_file.txt")
    printFile = open("decision_maker.py", "r")
    print("\n\n")
    for line in printFile.readlines():
        print(line, end="")
    printFile.close()
    os.remove("decision_maker.py")

if __name__ == "__main__":
    run(compile_decision_table)
