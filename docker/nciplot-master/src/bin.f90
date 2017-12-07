!JS - 15 Oct 2017
!tools for binning NCI data

module bin
  implicit none

  public
  integer, parameter :: nGrid = 100
  
  real, parameter :: integrationExp = 4.0/3.0
  
  real, parameter :: minRho=-0.1, maxRho = +0.1, minRDG=0.0, maxRDG=0.5
  real,parameter :: dRho=(maxRho-minRho)/(real(nGrid)), dRDG=(maxRDG-minRDG)/real(nGrid)

  integer :: pointHist(nGrid,nGrid)
  real :: integralDens(nGrid)
  real :: totalIntegralDens=0.0

contains

  integer function whichBin(min, dx, val) 
    real, intent(in) :: min, dx, val
!    integer, intent(out) :: position
    whichBin = floor((val-min)/dx)+1    
  end function whichBin

  subroutine initBin()
    pointHist(:,:) = 0
    integralDens(:) = 0.0
    totalIntegralDens = 0.0
  end subroutine initBin

  subroutine binPointHist(rho,rdg)
    real, intent(in) :: rho,rdg
    integer :: rhoBin,rdgBin

    rhoBin = whichBin(minRho,dRho,rho)
    rdgBin = whichBin(minRDG,dRDG,rdg)
    
    if ((rdg.lt.maxRDG).and.(rdg.gt.minRDG).and.(rho.lt.maxRho).and.(rho.gt.minRho)) then
       pointHist(rhoBin,rdgBin) = pointHist(rhoBin,rdgBin)+1
       integralDens(rhoBin) = integralDens(rhoBin)+ abs(rho)**integrationExp  !TODO:  assumes constant voxel size across comparison files
    end if
    
    totalIntegralDens = totalIntegralDens+sign(abs(rho)**integrationExp,rho)

  end subroutine binPointHist

  subroutine write_hist(filename)
    character (len=*), intent(in) :: filename
    integer :: i,j
    open (unit=123, file = filename, status='replace')
!    do i=1,nGrid
       write (123,*) ( (pointHist(i,j), j=1,nGrid ), i=1,nGrid)
!    end do
    close(123)
  end subroutine write_hist

  subroutine write_integrals(filename)
    character (len=*), intent(in) :: filename
    integer :: i
    open (unit=123, file = filename, status='replace')
    write (123,*) (integralDens(i), i=1,nGrid )
    write (123,*) totalIntegralDens
    close(123)
  end subroutine write_integrals

end module bin
  
