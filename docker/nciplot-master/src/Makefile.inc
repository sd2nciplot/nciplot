#############
# Compiler
#############

## The Intel(R) fortran compiler (ifort)
#ifeq ($(DEBUG),1)
#  FC = /opt/intel/bin/ifort
#  FCFLAGS = -g -CU -C -traceback -fpe0 -debug -openmp
#  LDFLAGS = -O3
#else
#  FC = /opt/intel/bin/ifort
#  FCFLAGS =  -Ofast -inline-forceinline -unroll-aggressive -openmp 
#  LDFLAGS =  -Ofast  -inline-forceinline -unroll-aggressive -openmp
#endif

# The GNU fortran compiler (gfortran)
ifeq ($(DEBUG),1)
  FC=gfortran
  FCFLAGS=-O3 -g -fbounds-check -Wall -Wunused-parameter -ffpe-trap=invalid -fbacktrace -fdump-core -fopenmp
  LDFLAGS=-fopenmp
else
  FC=gfortran
  FCFLAGS=-O3 -fopenmp
  LDFLAGS=-fopenmp
endif

