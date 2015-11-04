#include <hwloc.h>
#include <stdio.h>

int main(void) {
  hwloc_topology_t topology;
  int nbcores;
  
  hwloc_topology_init(&topology);  // initialization
  hwloc_topology_load(topology);   // actual detection
  
  nbcores = hwloc_get_nbobjs_by_type(topology, HWLOC_OBJ_CORE);
  printf("%d cores\n", nbcores);

  hwloc_topology_destroy(topology);

  return 0;
}