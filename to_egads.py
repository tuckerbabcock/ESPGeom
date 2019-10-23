from __future__ import print_function

from pyCAPS import capsProblem

# Instantiate our CAPS problem "myProblem"
print("Initiating capsProblem")
myProblem = capsProblem()


stator = myProblem.loadCAPS("stator.csm")
# Save egads file of the geometry
stator.saveGeometry("stator.egads")