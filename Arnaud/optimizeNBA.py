import xlrd
import xlwt
import csv
import sys
import os
from datetime import datetime
import glob
import copy
import math
dateTimeString=datetime.today().strftime('%Y%m%d_%H%M%S')

####################################################################################################
##### PARAMETRIZE FILE NAMES #######################################################################
####################################################################################################
def open_csv(to_read):
    """
    Open a text file for reading, then iterate over it with a csv reader,
    returning a list of lists, each containing 1 row.
    """
    def unicode_csv_reader(unicode_csv_data, dialect = csv.excel, **kwargs):
        """ Encode utf-8 strings from CSV as Unicode """
        csv_reader = csv.reader(unicode_csv_data,delimiter=",")
        i=0
        for row in csv_reader:
            print i
            # decode UTF-8 back to Unicode, cell by cell:
            yield [unicode(cell.strip(), 'utf-8') for cell in row if cell]
            i += 1
    try:
        with open(to_read, 'rU') as got_a_file:
            return [line for line in unicode_csv_reader(got_a_file)]
    except (IOError, csv.Error):
        print "Couldn't read from file %s. Exiting." % (to_read)
        raise

def open_excel(to_read):
    """
    Open an Excel workbook and read rows from first sheet into sublists
    """
    def read_lines(workbook):
        """ decode strings from each row into unicode lists """
        sheet = workbook.sheet_by_index(0)
        for row in range(sheet.nrows):
            yield [sheet.cell(row, col).value for col in range(sheet.ncols)]
    try:
        workbook = xlrd.open_workbook(to_read)
        return [line for line in read_lines(workbook)]
    except (IOError, ValueError):
        print "Couldn't read from file %s. Exiting" % (to_read)
        raise

def save_as_xls(lines_to_write, output_filename):
    """
    Write a list of lists to an Excel (xls) sheet, one row per nested list
    """
    # initialise a new Excel workbook object, and a worksheet
    from xlwt import Workbook
    from xlwt import XFStyle
    book = Workbook(encoding = 'utf-8')
    sheet = book.add_sheet('Sheet 1')
    style = XFStyle()
    style.num_format_str = 'general'
    # iterate through the nested lists
    for row_index, row_contents in enumerate(lines_to_write):
        for column_index, cell_value in enumerate(row_contents):
            sheet.write(row_index, column_index, cell_value, style)
    # write the file to the current working directory
    book.save(os.path.join(os.getcwd(), output_filename))

#save_as_xls(open_csv(sys.argv[1]),'test.xls')
dir = os.path.dirname(__file__)
#path_string=str(dateTimeString+'.csv')
#filename=os.path.join(dir,'LINEUPS',path_string)
#filename = 'log.txt'
#logFile = open(filename, 'w')
#sys.stdout = logFile
#sys.stderr = logFile
#xls_file = os.path.join(dir, 'CalculateMC.xlsm')

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
print 'PF',len(paretoPF.keys())
print 'PG',len(paretoPG.keys())
print 'SF',len(paretoSF.keys())
print 'SG',len(paretoSG.keys())
print 'C',len(paretoCenter.keys())
print 'Total tries',len(paretoPF.keys())*len(paretoPG.keys())*len(paretoSF.keys())*len(paretoSG.keys())*len(paretoCenter.keys())

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
                            print candidate, candidatePoints,candidateSalary,candidateProb


							
for player in candidate:
	try:
		print player.split('\\')[0]
		print player.split('\\')[1]
	except:
		next
		
print candidatePoints
print candidateSalary
print candidateProb
print '\n'
print candidate[0]
print paretoPF[candidate[0]]['salary']
print paretoPF[candidate[0]]['avg']
print math.sqrt(paretoPF[candidate[0]]['sigma2'])
print '\n'
print candidate[1]
print paretoPG[candidate[1]]['salary']
print paretoPG[candidate[1]]['avg']
print math.sqrt(paretoPG[candidate[1]]['sigma2'])
print '\n'
print candidate[2]
print paretoSF[candidate[2]]['salary']
print paretoSF[candidate[2]]['avg']
print math.sqrt(paretoSF[candidate[2]]['sigma2'])
print '\n'
print candidate[3]
print paretoSG[candidate[3]]['salary']
print paretoSG[candidate[3]]['avg']
print math.sqrt(paretoSG[candidate[3]]['sigma2'])
print '\n'
print candidate[4]
print paretoCenter[candidate[4]]['salary']
print paretoCenter[candidate[4]]['avg']
print math.sqrt(paretoCenter[candidate[4]]['sigma2'])

                        #elif points > 282:
                        #    candidate = [PF,PG,SF,SG,Cent]
                        #    candidatePoints = points
                        #    candidateSalary= salary
                        #    print 'above 282: ',candidate, candidatePoints,candidateSalary