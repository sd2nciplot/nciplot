#!/usr/bin/awk -f
##############################################################################
# A script to discard data with a density less than rhomin or greater than   #
# rhomax                                                                     #
#                                                                            #
# Usage:                                                                     #
#  user:$ ./cutden.awk rhomin rhomax file.dat                                #
#                                                                            #
##############################################################################

BEGIN{
    if (ARGC < 3){
	print "Usage: cutden.awk rhomin rhomax file.dat"
	exit
    }
    #Read density range
    rhomin = ARGV[1]; rhomax = ARGV[2]
    #Remove range from arguments list
    for (i=1;i<=ARGC-1;i++)
	ARGV[i] = ARGV[i+2]
    ARGC -= 2
}
#Print data in the range (rhomin < rho < rhomax) to the screen
($1<rhomax)&&($1>rhomin)
