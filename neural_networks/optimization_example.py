__author__ = 'estsauver'
from numpy import array
import pylab
def objF(x): return sum(x**2)

x0 = array([2.1, -1])

from pybrain.optimization import CMAES

l=CMAES(objF,x0)
l.minimize = True
l.maxEvaluations = 200
print l.learn()
