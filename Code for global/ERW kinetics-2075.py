from scipy.interpolate import interp1d
import scipy.optimize, os, time, struct
from math import *
from socket import *
import numpy as np
import matplotlib.pyplot as plt
import math

####This Program is for the ERW project####

xh=[]; yh=[] ####### Prepare for reading the data
f=open('Cropland Area.txt','r') #
line=f.readline() # Read data from the txt file into a long array
while line:
    arr=line.split()
    xh.append(float(arr[0]))
    yh.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata=interp1d(xh,yh)
def dland(T):
    return dHcata(T) # This section contains real data

xh2=[]; yh2=[] ####### Prepare for reading the data
f=open('WR.txt','r') #
line=f.readline() # Read data from the txt file into a long array
while line:
    arr=line.split()
    xh2.append(float(arr[0]))
    yh2.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata2=interp1d(xh2,yh2)
def dWR(T):
    return dHcata2(T) # This section contains real data

i=0
M=4.0*1e3 # Unit: t/km²
x=20 # um
m=125 # g mol⁻¹ basalt
t=3.155*1.e7 # s a⁻¹ - converting time to years
R=8.314 # Ideal gas constant
A=1
Ea=47500 # J/mol
p=0.3
k1=588
k2=0.0822
n1=1.16
n2=0.16
Deploy_year=26
CDR_Region=[]; Rock_TOT=[]; Rate=[]; fnpp=[]
while i<1558: # Note: Adjust the number of regions, i represents the region
    i=i+1
    m_rock=[]; m_rock_tot=[]; m_consume_year=[]
    year=0; CDR=0; M_rock=0
    while year<51:
        year=year+1
        WR=dWR(i) # WR is SSA*m*t*WR, already processed
        if WR>1:
            WR=1
        Land=dland(i)
        if year<Deploy_year:
            M_rock=M_rock+M*Land # Total amount of rock applied in each region
            m_rock.append(M*Land)
        else:
            M_rock=M_rock
            m_rock.append(0)

        dx=WR*(1-(CDR/p)/M_rock) # WR is weathering rate in mol m⁻² s⁻¹

        RCO2=dx*p # Unit rate, corresponds to formula 1 in the paper before multiplying by M

        aa=sum(m_rock)
        k=0
        while k<min(year, Deploy_year):
            # print((m_rock[k])/(M*Land))
            m_rock[k]=m_rock[k]-M*Land*dx*((m_rock[k])/(M*Land))
            
            if m_rock[k]<0:
                m_rock[k]=0
            k=k+1
        bb=sum(m_rock)
        
        m_rock_tot.append(bb) # Load remaining amount each year
        cc=aa-bb
        m_consume_year.append(cc)
        CDR=CDR+cc*p
    CDR_Region.append(CDR/1.e9) # Unit: Gt
    # Rate.append(dx*f_npp)
    # fnpp.append(f_npp)
    Rock_TOT.append(M_rock/1.e9) # Unit: Gt

print("CDR-region") # Output in units of tons
for i in range (len(CDR_Region)):
    print(CDR_Region[i])
print("\n")

## print("RockTOT")
## for i in range (len(Rock_TOT)):
##     print(Rock_TOT[i])
## print("\n")

## print("Rate")
## for i in range (len(Rate)):
##     print(Rate[i])
## print("\n")
##
## print("fnpp")
## for i in range (len(fnpp)):
##     print(fnpp[i])
## print("\n")
