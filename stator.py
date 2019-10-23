from __future__ import print_function

from pyCAPS import capsProblem

# Instantiate our CAPS problem "myProblem"
print("Initiating capsProblem")
myProblem = capsProblem()


# stator = myProblem.loadCAPS("stator.csm")
# # Save egads file of the geometry
# stator.saveGeometry("stator.egads")

# Load CSM file and build the geometry explicitly
myGeometry = myProblem.loadCAPS("stator.egads")
print("Loaded geometry")
# myGeometry.buildGeometry()

# Load AFLR4 aim
aflr4 = myProblem.loadAIM(aim = "aflr4AIM",
                          altName = "aflr4",
                          analysisDir= "workDir")
print("set up aim")
# # Set output grid format since a project name is being supplied
aflr4.setAnalysisVal("Proj_Name", "stator0")
aflr4.setAnalysisVal("Mesh_Format", "VTK")

# Use 5 segements on farfield faces
# aflr4.setAnalysisVal("ff_nseg", 5)


aflr4.setAnalysisVal("Mesh_Length_Factor", 5)
# Relative scale of maximum spacing bound relative to ref_len
# max_spacing = max_scale * ref_len
# aflr4.setAnalysisVal("max_scale", 0.1)
# Relative scale of minimum spacing bound relative to ref_len
# min_spacing = min_scale * ref_len
# aflr4.setAnalysisVal("min_scale", 0.01)

# # Set maximum and minimum edge lengths relative to capsMeshLength
aflr4.setAnalysisVal("max_scale", 0.5)
aflr4.setAnalysisVal("min_scale", 0.05)

# Run AIM pre-/post-analysis
aflr4.preAnalysis()
aflr4.postAnalysis()

# ######################################
# ## Build volume mesh off of surface ##
# ##  mesh(es) using AFLR3            ##
# ######################################

# Load AFLR3 aim
aflr3 = myProblem.loadAIM(aim = "aflr3AIM",
                              analysisDir= "workDir",
                              parents = aflr4.aimName)

# Set output grid format since a project name is being supplied - Tecplot tetrahedral file
aflr3.setAnalysisVal("Proj_Name", "stator")
# aflr3.setAnalysisVal("Mesh_Format", "VTK")
aflr3.setAnalysisVal("Mesh_Format", "AFLR3")
# aflr3.setAnalysisVal("Mesh_ASCII_Flag", False)

# Run AIM pre-/post-analysis
aflr3.preAnalysis()
aflr3.postAnalysis()

# Close our problem
print("Closing our problem")
myProblem.closeCAPS()