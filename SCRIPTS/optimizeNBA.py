import xlrd
#import xlwt
import csv
import sys
import os
from datetime import datetime
import glob
import copy
import math
startTime = datetime.now()
dateTimeString=datetime.today().strftime('%Y%m%d_%H%M%S')

####################################################################################################
##### PARAMETRIZE FILE NAMES #######################################################################
####################################################################################################


dir = os.path.dirname(__file__)
xls_file = os.path.join(dir,sys.argv[1])
xls_workbook = xlrd.open_workbook(xls_file)
xls_sheet = xls_workbook.sheet_by_index(0)

playerList=[]
position = xls_sheet.cell(1,0).value
center = {}
powerForward = {}
pointGuard = {}
smallForward = {}
shootingGuard = {}
i = 1
while position != '':
    try:
        position = xls_sheet.cell(i,0).value
        name = xls_sheet.cell(i,1).value
        salary = float(xls_sheet.cell(i,5).value)
        fppg = float(xls_sheet.cell(i,6).value)
        fpmax = float(xls_sheet.cell(i,7).value)
        fpmin = float(xls_sheet.cell(i,8).value)
        floor = float(xls_sheet.cell(i,9).value)
        ceil = float(xls_sheet.cell(i,10).value)
        avg =  float(xls_sheet.cell(i,11).value)
        sigma = (ceil-floor)/6.0
        sigma2 = sigma*sigma
        i +=1
    except:
        break
    if position == 'C':
        center[name]={'salary':salary,'fppg':fppg,'fpmax':fpmax,'fpmin':fpmin,'floor':floor,'ceil':ceil,'avg':avg,'sigma':sigma,'sigma2':sigma2}
    if position == 'PF':
        powerForward[name]={'salary':salary,'fppg':fppg,'fpmax':fpmax,'fpmin':fpmin,'floor':floor,'ceil':ceil,'avg':avg,'sigma':sigma,'sigma2':sigma2}
    if position == 'PG':
        pointGuard[name]={'salary':salary,'fppg':fppg,'fpmax':fpmax,'fpmin':fpmin,'floor':floor,'ceil':ceil,'avg':avg,'sigma':sigma,'sigma2':sigma2}
    if position == 'SF':
        smallForward[name]={'salary':salary,'fppg':fppg,'fpmax':fpmax,'fpmin':fpmin,'floor':floor,'ceil':ceil,'avg':avg,'sigma':sigma,'sigma2':sigma2}
    if position == 'SG':
        shootingGuard[name]={'salary':salary,'fppg':fppg,'fpmax':fpmax,'fpmin':fpmin,'floor':floor,'ceil':ceil,'avg':avg,'sigma':sigma,'sigma2':sigma2}

def addPareto(paretoDict,candidateDict, candidateName):
    for name in paretoDict.keys():
        dominatedStatus=True
        dominatingStatus=True
        #objList = ['summary','avg']
        #for obj in objList:
        if dominatedStatus:
            if  candidateDict[candidateName]['salary']<paretoDict[name]['salary']:
                dominatedStatus=False
            elif candidateDict[candidateName]['avg']>paretoDict[name]['avg']:
                dominatedStatus=False
        if dominatingStatus:
            if  candidateDict[candidateName]['salary']>paretoDict[name]['salary']:
                dominatingStatus=False
            elif candidateDict[candidateName]['avg']<paretoDict[name]['avg']:
                dominatingStatus=False
        if dominatingStatus:
            paretoDict.pop(name)
        else:
            if not dominatedStatus:
                continue
            else:
                return paretoDict
    paretoDict[candidateName] = {'salary':candidateDict[candidateName]['salary'],'avg':candidateDict[candidateName]['avg'],'sigma2':candidateDict[candidateName]['sigma2']}
    return paretoDict

def addPareto2(paretoDict,candidateDict, candidateName1,candidateName2):
    candidateSalary = candidateDict[candidateName1]['salary']+candidateDict[candidateName2]['salary']
    candidateAvg = candidateDict[candidateName1]['avg']+candidateDict[candidateName2]['avg']
    candidateName = candidateName1 + '\\' + candidateName2
    candidateSigma2 = candidateDict[candidateName1]['sigma2']+candidateDict[candidateName2]['sigma2']
    for name in paretoDict.keys():
        dominatedStatus=True
        dominatingStatus=True
        if dominatedStatus:
            if  candidateSalary<paretoDict[name]['salary']:
                dominatedStatus=False
            elif candidateAvg>paretoDict[name]['avg']:
                dominatedStatus=False
        if dominatingStatus:
            if  candidateSalary>paretoDict[name]['salary']:
                dominatingStatus=False
            elif candidateAvg<paretoDict[name]['avg']:
                dominatingStatus=False
        if dominatingStatus:
            paretoDict.pop(name)
        else:
            if not dominatedStatus:
                continue
            else:
                return paretoDict
    paretoDict[candidateName] = {'salary':candidateSalary,'avg':candidateAvg,'sigma2':candidateSigma2}
    return paretoDict

paretoCenter = {}
for name in center.keys():
    paretoCenter= addPareto(paretoCenter,center,name)          

paretoPF = {}
for name1 in powerForward.keys():
    for name2 in powerForward.keys():
        if name1 != name2:
            paretoPF = addPareto2(paretoPF,powerForward,name1,name2)  
paretoPG = {}
for name1 in pointGuard.keys():
    for name2 in pointGuard.keys():
        if name1 != name2:
            paretoPG = addPareto2(paretoPG,pointGuard,name1,name2)  
paretoSF = {}
for name1 in smallForward.keys():
    for name2 in smallForward.keys():
        if name1 != name2:
            paretoSF = addPareto2(paretoSF,smallForward,name1,name2)  
paretoSG = {}
for name1 in shootingGuard.keys():
    for name2 in shootingGuard.keys():
        if name1 != name2:
            paretoSG = addPareto2(paretoSG,shootingGuard,name1,name2) 

print '### POOL OF PLAYERS ###'			
print 'PF',len(paretoPF.keys())
print 'PG',len(paretoPG.keys())
print 'SF',len(paretoSF.keys())
print 'SG',len(paretoSG.keys())
print 'C',len(paretoCenter.keys())
print '-----------------------'

print 'Total tries: ',len(paretoPF.keys())*len(paretoPG.keys())*len(paretoSF.keys())*len(paretoSG.keys())*len(paretoCenter.keys())
print ''

candidate = None 
candidatePoints = 0.0
candidateProb = 0.0
maxSalary = 60000
threshold = 280

for PF in paretoPF:
    for PG in paretoPG:
        for SF in paretoSF:
            for SG in paretoSG:
                for Cent in paretoCenter:
                    salary = paretoPF[PF]['salary']+paretoPG[PG]['salary']+paretoSF[SF]['salary']+paretoSG[SG]['salary']+paretoCenter[Cent]['salary']
                    if salary < maxSalary: 
                        points = paretoPF[PF]['avg']+paretoPG[PG]['avg']+paretoSF[SF]['avg']+paretoSG[SG]['avg']+paretoCenter[Cent]['avg']
                        sigma2 = paretoPF[PF]['sigma2']+paretoPG[PG]['sigma2']+paretoSF[SF]['sigma2']+paretoSG[SG]['sigma2']+paretoCenter[Cent]['sigma2']
                        prob = (1.0+math.erf((points-threshold)/math.sqrt(sigma2)/math.sqrt(2)))/2.0
                        if prob > candidateProb:
                            candidate = [PF,PG,SF,SG,Cent]
                            candidatePoints = points
                            candidateSalary= salary
                            candidateProb = prob
                            #print candidate, candidatePoints,candidateSalary,candidateProb



print "Predicted Fantasy Points: ",candidatePoints
print "Predicted Fantasy Salary: ",candidateSalary
print "Probability of",threshold,':',candidateProb*100,"%"
print ''
							
for player in range(0,9):
	try:
		print candidate[player].split('\\')[0]
		print candidate[player].split('\\')[1]
	except:
		next

print ''
print "Started at:", startTime		
print "Completed in:", datetime.now() - startTime
