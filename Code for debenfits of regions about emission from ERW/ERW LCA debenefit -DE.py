from scipy.interpolate import interp1d
import scipy.optimize, os, time, struct
from math import *
from socket import *
import numpy as np
import matplotlib.pyplot as plt
import math

####This Program is for the ERW project####

xh=[]; yh=[]  # Prepare for the reading data
f=open('Cropland Area.txt','r')  # Open the 'Cropland Area.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh.append(float(arr[0]))
    yh.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata=interp1d(xh,yh)
def dland(T):
    return dHcata(T)  # This section is for calculations

xh2=[]; yh2=[]  # Prepare for the reading data
f=open('Temperature.txt','r')  # Open the 'Temperature.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh2.append(float(arr[0]))
    yh2.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata2=interp1d(xh2,yh2)
def dtemperature(T):
    return dHcata2(T)  # This section is for calculations

xh1=[]; yh1=[]  # Prepare for the reading data
f=open('pH.txt','r')  # Open the 'pH.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh1.append(float(arr[0]))
    yh1.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata1=interp1d(xh1,yh1)
def dpH(T):
    return dHcata1(T)  # This section is for calculations

xh3=[]; yh3=[]  # Prepare for the reading data
f=open('NPP.txt','r')  # Open the 'NPP.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh3.append(float(arr[0]))
    yh3.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata3=interp1d(xh3,yh3)
def dNPP(T):
    return dHcata3(T)  # This section is for calculations

xh4=[]; yh4=[]  # Prepare for the reading data
f=open('Carbon Price Initial.txt','r')  # Open the 'Carbon Price Initial.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh4.append(float(arr[0]))
    yh4.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata4=interp1d(xh4,yh4)
def dCPI(T):
    return dHcata4(T)  # This section is for calculations

xh5=[]; yh5=[]  # Prepare for the reading data
f=open('Carbon Price Low.txt','r')  # Open the 'Carbon Price Low.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh5.append(float(arr[0]))
    yh5.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata5=interp1d(xh5,yh5)
def dCPL(T):
    return dHcata5(T)  # This section is for calculations

xh6=[]; yh6=[]  # Prepare for the reading data
f=open('Carbon Price Medium.txt','r')  # Open the 'Carbon Price Medium.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh6.append(float(arr[0]))
    yh6.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata6=interp1d(xh6,yh6)
def dCPM(T):
    return dHcata6(T)  # This section is for calculations

xh7=[]; yh7=[]  # Prepare for the reading data
f=open('Carbon Price High.txt','r')  # Open the 'Carbon Price High.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh7.append(float(arr[0]))
    yh7.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata7=interp1d(xh7,yh7)
def dCPH(T):
    return dHcata7(T)  # This section is for calculations

xh8=[]; yh8=[]  # Prepare for the reading data
f=open('COST.txt','r')  # Open the 'COST.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh8.append(float(arr[0]))
    yh8.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata8=interp1d(xh8,yh8)
def dCost(T):
    return dHcata8(T)  # This section is for calculations

xh9=[]; yh9=[]  # Prepare for the reading data
f=open('DE.txt','r')  # Open the 'DE.txt' file
line=f.readline()  # Read data into an array
while line:
    arr=line.split()
    xh9.append(float(arr[0]))
    yh9.append(float(arr[1]))
    line=f.readline()
f.close()
dHcata9=interp1d(xh9,yh9)
def dLCA(T):
    return dHcata9(T)  # This section is for calculations

M=4.0*1e3  # Unit: t/km2
x=20  # um
m=125  # g/mol basalt
t=3.155*1.e7  # s/year, convert time to years
R=8.314  # Ideal gas constant
A=1
Ea=47500  # J/mol
p=0.3
k1=588
k2=0.0822
n1=1.16
n2=0.16
Deploy_year=26
r=0.02
CDR_Region=[]; Rock_TOT=[]; Rate=[]; fnpp=[]
COST=[]; Ben_low=[]; Ben_medium=[]; Ben_high=[]

i=345
while i<362:  # Adjust the number of regions, i represents the region
    i=i+1
    m_rock=[]; m_rock_tot=[];m_consume_year=[]
    year=0;CDR=0; M_rock=0; Net_Cost=0;
    Benefit_low=0; Benefit_medium=0; Benefit_high=0; deben_low=0; deben_medium=0; deben_high=0
    while year<26:
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
            Cost=dCost(i)*M*dland(i)  # Unit: USD
            Net_Cost=Net_Cost+(Cost/(pow(1+r, year)))/1.e6  # Unit: million
        else:
            Cost=0
            Net_Cost=Net_Cost
        if year<26:
            decost=dLCA(year)*M*dland(i)  # Unit: tons
            deben_low=deben_low+(decost*CP_low/(pow(1+r, year)))/1.e6
            deben_medium=deben_medium+(decost*CP_medium/(pow(1+r, year)))/1.e6
            deben_high=deben_high+(decost*CP_high/(pow(1+r, year)))/1.e6
        else:
            decost=0
            deben_low=deben_low
            deben_medium=deben_medium
            deben_high=deben_high

    Ben_low.append(deben_low)
    Ben_medium.append(deben_medium)
    Ben_high.append(deben_high)

print("deBen_low")
for i in range(len(Ben_low)):
    print(Ben_low[i])
print("\n")

print("deBen_medium")
for i in range(len(Ben_medium)):
    print(Ben_medium[i])
print("\n")

print("deBen_high")
for i in range(len(Ben_high)):
    print(Ben_high[i])
print("\n")
