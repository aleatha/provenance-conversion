#!/usr/bin/env python

import sys
import numpy as np
import math
import datetime

class PNodeStore:
    
    pnodes = {}
    
    def __init__(self):
        pnodes = {}
        
    def insert(self,name):
        if not (name in self.pnodes.keys()):
            pnodes[name] = PNode(name)
            
    def insertEdge(self, fro, to):
        if not (fro in self.pnodes.keys()):
            self.pnodes[fro] = PNode(fro)
        if not (to in self.pnodes.keys()):
          self.pnodes[to] = PNode(to)
        self.pnodes[fro].outedges.append(to)
        self.pnodes[to].inedges.append(fro)

class PNode:
    def __init__(self, name):
        self.name = name
        self.inedges = []
        self.outedges = []
        self.time = datetime.datetime.min
        self.height = 0

class PGraphAnalyzer:
  
  pnodestore = None
  maxHeight = 0
  
  def __init__(self, pnodestore):
    self.pnodestore = pnodestore
  
  #How many nodes are in the graph?
  def getTotalNodes(self):
    return len(self.pnodestore.pnodes.values())
  
  def getHeight(self):
    if self.maxHeight == 0:
      self.calcHeights()
    return maxHeight

  
  #What is the min, max, and average in-degree and out-degree?
  def calcDegree(self):
    maxIn = -sys.maxint-1
    minIn = sys.maxint
    avgIn = 0
    maxOut = -sys.maxint-1
    minOut = sys.maxint
    avgOut = 0
    count = len(self.pnodestore.pnodes.values())

    for n in self.pnodestore.pnodes.values():
      inDeg = len(n.inedges)
      maxIn = max(inDeg,maxIn)
      minIn = min(inDeg,minIn)
      avgIn += inDeg

      outDeg = len(n.outedges)
      maxOut = max(outDeg,maxOut)
      minOUt = min(outDeg,minOut)
      avgOut += outDeg
        
    avgIn = avgIn/count
    avgOut = avgOut/count

    print "Min In %d" % (minIn)
    print "Average In %d" % (avgIn)
    print "Max In %d" % (maxIn)
    print "Min Out %d" % (minOut)
    print "Average Out %d" % (avgOut)
    print "Max Out %d" % (maxOut)

  #what is the min, max, and average height of the nodes?
  #Easiest way to do this is a BFS, starting from the leaves
  def calcHeights(self):
      leaves = filter(lambda x:len(x.outedges) == 0 ,self.pnodestore.pnodes.values())
      #find the leaves
      queue = []
      for n in leaves:
        queue.append(n)
        n.height = 1
        
        while len(queue) > 0:
          p = queue.pop(0)
          for q in p.inedges:
            q = self.pnodestore.pnodes[q]
            queue.append(q)
            q.height = max(q.height, p.height+1)
            self.maxHeight = max(q.height, self.maxHeight)
      for node in self.pnodestore.pnodes.values():
        print "Node %s is at height %d" % (node.name, node.height)
        
  
  
  #First, can we do a simple implementation of our ranking algorithm, and just spit out a ranked list of nodes? Yes, we can.
  def TaPiR(self):
    np.set_printoptions(precision=3, suppress=True)
    alpha = .1
    #Build up an adjacency matrix for numpy
    size = len(self.pnodestore.pnodes.values())
    array_matrix = [[None] * size for i in range(size)]
    row=-1
    col =-1
    for x_node in self.pnodestore.pnodes.keys():
      row+=1
      for y_node in self.pnodestore.pnodes.keys():
        col+=1
        if y_node in self.pnodestore.pnodes[x_node].outedges:
          array_matrix[row][col] = 1.0
        else:
          array_matrix[row][col] = 0.0
      col = -1
    matrix = np.matrix(array_matrix)

    #calculate an exponential decay factor for the graph based on max height.
    weights = []
    l = self.maxHeight/4 #Need to tweak l for appropriate decay rate.  4 is totally a made-up number.

    #Now calculate the weights of each of the nodes in the graph
    for node in self.pnodestore.pnodes.values():
      weights.append(1*math.exp(-l*float(node.height)))
    #Normalize the weights so that the entire thing adds up to alpha
    weights_matrix = np.matrix(weights)
    weight_sum = weights_matrix.sum(1).item(0,0)
    weights_matrix = weights_matrix/weight_sum
    print weights_matrix
  
    #Use the scaled weights to define the teleport probabilities, and generate the transition probability matrix
    rowsums = matrix.sum(axis=1)
    for i in range(size):
      scaling = rowsums.item(i,0)
      #If there are already links, then scale back the teleports to alpha of the total prob...
      if scaling > 0:
        scaling = (1-alpha)/scaling
        matrix[i] = matrix[i] * scaling
        rescaled_weights = weights_matrix * alpha
        matrix[i] = matrix[i] + rescaled_weights
      #Otherwise, teleports need to add up to 1.
      else:
        matrix[i] = matrix[i] + weights_matrix
    print matrix

    
    
    #Get the left eigenvector
    import scipy.linalg
    w,vl = scipy.linalg.eig(matrix, left=True, right=False)
    ranks = vl[:,0]
    ranks = ranks/sum(ranks) #normalize it to a probability
    
    print ranks
 

  #Second, how can we set up good test and train sets on the provenance graph to do access prediction?
  #We have several different machines, so we can set up an arbitrary threshold of "X% of data, or Y entries, whichever is larger".
  #How big is big enough?  Do rolling predictions and look for the knee in the curve.
  #Use pearson rank correlation coefficient to discount what the user actually selected relative to how we ranked it
  def AccessPrediction(self):
    
    pass


def main():
   pnodestore = PNodeStore()


if __name__ == "__main__":
   main()
