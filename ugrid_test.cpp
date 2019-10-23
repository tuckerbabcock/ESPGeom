#include <apfMDS.h>
#include <PCU.h>
#include <gmi_null.h>
#include <pumi.h>
#include <iostream>

int main(int argc, char *argv[])
{
   MPI_Init(&argc, &argv);
   PCU_Comm_Init();
	gmi_register_null();

	std::cout << "in file" << std::endl;
   const char *in_mesh_file = "stator.lb8.ugrid";
	const char *out_mesh_file = "stator.smb";
	gmi_model *null_model;
	null_model = gmi_load("null.null");
	std::cout << "loaded null model!" << std::endl;
	apf::Mesh2 *ugrid_mesh;
	ugrid_mesh = apf::loadMdsFromUgrid(null_model, in_mesh_file);
	std::cout << "loaded ugrid mesh" << std::endl;
	ugrid_mesh->verify();
	std::cout << "verified ugrid mesh" << std::endl;
	ugrid_mesh->writeNative(out_mesh_file);
	std::cout << "wrote ugrid mesh to pumi mesh" << std::endl;


	// pumi_mesh_write(ugrid_mesh, "stator", "vtk");
	ugrid_mesh->destroyNative();
   apf::destroyMesh(ugrid_mesh);
   PCU_Comm_Free();
   MPI_Finalize();
   return 0;
}