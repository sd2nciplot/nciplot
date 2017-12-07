program main 

  use bin
  implicit none
  real :: dens

  call initBin()
  
  write (*,*) 'test bin position:'

  dens = minRho
  write (*,*) minRho, dRho, dens, whichBin(minRho,dRho,dens)

  dens = maxRho - 0.000001
  write (*,*) minRho, dRho, dens, whichBin(minRho,dRho,dens)

  dens = minRDG
  write (*,*) minRDG, dRDG, minRDG, whichBin(minRDG,dRDG,dens)

  dens = maxRDG - 0.00001
  write (*,*) minRDG, dRDG, dens, whichBin(minRDG,dRDG,dens)
  
  call write_hist("sample_histogram")
  call write_integrals("sample_integrals")

end program main

