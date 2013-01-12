# coding=utf-8
# To change this template, choose Tools | Templates
# and open the template in the editor.

from cmath import sqrt
import array
from numpy import *
import scipy

__author__="qwazix"
__date__ ="$Jan 12, 2013 2:52:56 PM$"

class point:
    x = 0
    y = 0
    def __init__(self, x=0,y=0):
       self.x = x
       self.y = y
    def distance(self, point):
        return sqrt(pow(self.x - point.x, 2) + pow(self.y - point.y, 2))
    def __add__(self, p):
        return point(self.x+p.x, self.y+p.y);
    def __sub__(self, p):
        return point(self.x-p.x, self.y-p.y);
    def __str__(self):
        return str(self.x) + "," + str(self.y)

class joint:
    id
    coordinates = point() # Δίνουμε τα χαρακτηριστικά της κλάσης
    support = point()
    displacement = point()
    loads = array(0)
    totalMagnitude = point()
    def __init__(self, id, x, y):
        self.id = id
        self.coordinates = point(x,y)

class load:
    direction = "x"
    magnitude = 0

#    def turnOn(self):
#        print "turning on"

class beam:
    id = 0
    startNode = 0
    endNode = 0
    sectionArea = 0.002
    elasticity = 2e11
    distances = point()
    length = 0
    sin = 0
    cos = 0
    ktemp = matrix(0)
    klocal = zeros((4,4))
    T = matrix(0)
    kglobal = matrix(0)
    def __init__(self, id, start, end):
        # @type start joint
        # @type end joint

        #scipy for matlab users http://www.scipy.org/NumPy_for_Matlab_Users
        self.id = id
        self.startNode = start
        self.endNode = end
        self.distances = end.coordinates - start.coordinates
        self.length = start.coordinates.distance(end.coordinates)
        self.sin = self.distances.y/self.length
        self.cos = self.distances.x/self.length
        self.ktemp = self.sectionArea*self.elasticity/self.length * mat("1 0;0 0")
#        self.klocal = self.ktemp
        for i in range(4):
            for j in range(4):
                #βάζουμε τον πίνακα ktemp 4 φορές στον πίνακα klocal ως εξής
                # __________
                #|  1 |  2 | --> klocal
                #|____|____|  /
                #|  3 |  4 | /
                #|____|____|
                self.klocal[i,j] = self.ktemp[i%2,j%2]
        #build transformation matrix
        self.T = array([[self.cos, self.sin, 0, 0],[-self.sin, self.cos, 0, 0],[0, 0, self.cos, self.sin],[0, 0, -self.sin, self.cos]])
        #compute stiffness matrix in global coords
        self.kglobal=(self.T).T.dot(self.klocal).dot(self.T)
    def __str__(self):
        res= "\n"
        res+= "BEAM\n"
        res+= "---------\n"
        res+= 'Beam No:      %d\n' % self.id;
        res+= 'Length:       %d\n' % self.length;
        res+= 'Elasticity:   %.1e\n' % self.elasticity;
        res+= 'Section Area: %d\n' % self.sectionArea;
        res+= 'cos:          %d\n' % self.cos;
        res+= 'sin:          %d\n' % self.sin;
        res+= 'start:        joint  %d\n' % self.startNode.id;
        res+= 'end:          joint  %d\n' % self.endNode.id;
        return res;

def addToGeneral(generalK, b):
    # @type b beam
    startC=2*b.startNode.id-1
    endC=2*b.endNode.id-1
    for i in range(2):
        for j in range(2):
            generalK[startC+i,startC+j]=b.kglobal[i,j]
            generalK[startC+i,endC+j]=b.kglobal[i,2+j]
            generalK[endC+i,startC+j]=b.kglobal[2+i,j]
            generalK[endC+i,endC+j]=b.kglobal[2+i,2+j]
    return generalK

def computeAxialForces(b, u):
    # @type b beam
    myu = array();
    myu[i,0]=u[2*b.startNode.id-1,1]
    myu[i,0]=u[2*b.startNode.id,1]
    myu[i,0]=u[2*b.endNode.id-1,1]
    myu[i,0]=u[2*b.endNode.id,1]
    return b.klocal.dot(b.T).dot(myu);


if __name__ == "__main__":
    n1 = joint(0,0,0)
    n2 = joint(1,0,1)

    myBeam = beam(1, n1, n2)

    print myBeam
