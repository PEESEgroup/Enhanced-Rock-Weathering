from scipy.interpolate import interp1d
import scipy.optimize, os, time, struct
from math import *
from socket import *
import numpy as np
import matplotlib.pyplot as plt
import math

####This Program is for the ERW project####

xh=[]; yh=[] ####### prepare for reading the data
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

xh2=[]; yh2=[] ####### prepare for reading the data
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

xh4=[]; yh4=[] ####### prepare for reading the data
f=open('Carbon Price Initial.txt','r') #
line=f.readline() # Read data from the txt file into a long array
while line:
    arr=line.split()
    xh4.append(float(arr[0]))
    yh4.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata4=interp1d(xh4,yh4)
def dCPI(T):
    return dHcata4(T) # This section contains real data

xh5=[]; yh5=[] #######prepare for reading the data
f=open('Carbon Price Low.txt','r') # 
line=f.readline() # Read data from the txt file into a long array
while line:
    arr=line.split()
    xh5.append(float(arr[0]))
    yh5.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata5=interp1d(xh5,yh5)
def dCPL(T):
    return dHcata5(T) # This section contains real data

xh6=[]; yh6=[] ####### prepare for reading the data
f=open('Carbon Price Medium.txt','r') # 
line=f.readline() # Read data from the txt file into a long array
while line:
    arr=line.split()
    xh6.append(float(arr[0]))
    yh6.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata6=interp1d(xh6,yh6)
def dCPM(T):
    return dHcata6(T) # This section contains real data

xh7=[]; yh7=[] ####### prepare for reading the data
f=open('Carbon Price High.txt','r') #
line=f.readline() # Read data from the txt file into a long array
while line:
    arr=line.split()
    xh7.append(float(arr[0]))
    yh7.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata7=interp1d(xh7,yh7)
def dCPH(T):
    return dHcata7(T) # This section contains real data

xh8=[]; yh8=[] ####### prepare for reading the data
f=open('COST.txt','r') # 
line=f.readline() # Read data from the txt file into a long array
while line:
    arr=line.split()
    xh8.append(float(arr[0]))
    yh8.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata8=interp1d(xh8,yh8)
def dCost(T):
    return dHcata8(T) # This section contains real data

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
r=0.02
CDR_Region=[]; Rock_TOT=[]; Rate=[]; fnpp=[]
COST=[]; Ben_low=[]; Ben_medium=[]; Ben_high=[]
while i<1558: # Note: Adjust the number of regions, i represents region
    i=i+1
    m_rock=[]; m_rock_tot=[]; m_consume_year=[]
    year=0; CDR=0; M_rock=0; Net_Cost=0
    Benefit_low=0; Benefit_medium=0; Benefit_high=0
    while year<76:
        year=year+1
        if year<26:
            CP_low=dCPI(i)+year*(dCPL(i)-dCPI(i))/26
            CP_medium=dCPI(i)+year*(dCPM(i)-dCPI(i))/26
            CP_high=dCPI(i)+year*(dCPH(i)-dCPI(i))/26
        else:
            CP_low=dCPL(i)
            CP_medium=dCPM(i)
            CP_high=dCPH(i)
        
        if year<26:
            Cost=dCost(i)*M*dland(i) # Unit: USD
            Net_Cost=Net_Cost+(Cost/(pow(1+r, year)))/1.e6 # Unit: million USD
        else:
            Cost=0
            Net_Cost=Net_Cost
   
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
            m_rock[k]=m_rock[k]-M*Land*dx*((m_rock[k])/(M*Land))
            
            if m_rock[k]<0:
                m_rock[k]=0
            k=k+1
        bb=sum(m_rock)
        
        m_rock_tot.append(bb) # Load remaining amount each year
        cc=aa-bb # Unit: t
        m_consume_year.append(cc)
        CDR=CDR+cc*p
        Benefit_low=Benefit_low+cc*p*CP_low/(pow(1+r, year))/1.e6 # Unit: million USD
        Benefit_medium=Benefit_medium+cc*p*CP_medium/(pow(1+r, year))/1.e6
        Benefit_high=Benefit_high+cc*p*CP_high/(pow(1+r, year))/1.e6

    COST.append(Net_Cost)
    Ben_low.append(Benefit_low)
    Ben_medium.append(Benefit_medium)
    Ben_high.append(Benefit_high)
    

print("COST") # Output in units of tons
for i in range (len(COST)):
    print(COST[i])
print("\n")

print("Ben_low")
for i in range (len(Ben_low)):
    print(Ben_low[i])
print("\n")

print("Ben_medium")
for i in range (len(Ben_medium)):
    print(Ben_medium[i])
print("\n")

print("Ben_high")
for i in range (len(Ben_high)):
    print(Ben_high[i])
print("\n")
