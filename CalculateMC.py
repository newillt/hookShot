import xlrd
import xlwt
import optimus
import csv
import sys
import os
import ctypes  # An included library with Python install.
from datetime import datetime
from optimus import DistributionType,InputVarArray, InputVar, InputVarType, InputVarRangeType, OutputVarArray, OutputVar, Position
import glob
from summaryreader import SummaryReader
import win32com.client
xl=win32com.client.Dispatch("Excel.Application")
dateTimeString=datetime.today().strftime('%Y%m%d_%H%M%S')




		
####################################################################################################
##### PARAMETRIZE FILE NAMES #######################################################################
####################################################################################################


dir = os.path.dirname(__file__)
path_string=str(dateTimeString+'.csv')
filename=os.path.join(dir,'LINEUPS',path_string)
logFile = open(filename, 'w')
sys.stdout = logFile
sys.stderr = logFile
xls_file = os.path.join(dir, 'CalculateMC.xlsm')
xls_workbook = xlrd.open_workbook(xls_file)
xls_sheet = xls_workbook.sheet_by_index(0)

lowCutOff=xls_sheet.cell(15,1).value
numExp=xls_sheet.cell(16,1).value

def summary_reader(method):
#	post using Summary File Reader
	winner=0
	methodSummaryFileName = glob.glob(method.getWorkingPath()+"*.summary")[0]
	methodSummaryReader = SummaryReader(methodSummaryFileName)
	
	methodSummary = methodSummaryReader.getSummary()
	print ''
	print 'LowPointCutoff,',lowCutOff
	print 'Experiments run,',len(methodSummary)
		
	for index in range(len(methodSummary)):
		#print methodSummary.values()[index][9]
		if float(methodSummary.values()[index][9]) > lowCutOff:
			winner=winner+1
		valueList = methodSummary.values()[index]
	outputString="Probability of success: "+str(float(winner)/float(len(methodSummary))*100)+"%"
	print 'Success, ',winner
	print 'ProbabilityOfSuccess, ',float(winner)/float(len(methodSummary))
	ctypes.windll.user32.MessageBoxA(0, outputString, "Your Lineup", 1)


playerList=[]
for i in range(5,15):
	playerList.append(xls_sheet.cell(i,1).value)

### READ IN CSV FILE WITH FLOOR AND CEILING DATA
playerData=[]
path_string=xls_sheet.cell(1,0).value
filename=os.path.join(dir, 'DATA','preProcessed',path_string)
with open(filename, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		playerData.append(row)

k=0
inputDct={}

for player in playerList:
	for data in playerData:
		if (player==data[1]):
			try:
				inputDct[player]={}
				inputDct[player]["Nominal"]=data[6]
				inputDct[player]["High"]=data[7]
				inputDct[player]["Low"]=data[8]
				inputDct[player]["Sigma6"]=(float(data[7])-float(data[8]))/6
				k=k+1
			except:
				print data
				next

projectDir = r"\OPTIMUS"
projectFileName = r"\OPTIMUS\CalculateMC.opt"
project = optimus.createProject(projectDir)
graph = project.getActiveGraph()
inputarray = InputVarArray("Players", Position(100, 200))
graph.addInputVarArray(inputarray)

calc_string="$"
print "Name,ProjectedFP,SeasonLowFP,SeasonHighFP,Sigma"
for i in inputDct:
	print i,',',inputDct[i]['Nominal'],',',inputDct[i]['Low'],',',inputDct[i]['High'],',',inputDct[i]['Sigma6']
	input1 = InputVar(i, Position(0,0))
	inputarray.appendInputVar(input1)
	input1.setType(InputVarType.IV_REAL)
	input1.setRange(InputVarRangeType.IV_RANGE)
	input1.setDoubleNominal(float(inputDct[i]['Nominal']))
	input1.setDoubleLow(float(inputDct[i]['Low']))
	input1.setDoubleHigh(float(inputDct[i]['High']))
	input1.setIvDistributionOn(1)
	input1Dist = input1.getIvDistribution()
	input1Dist.setType(DistributionType.DISTR_NORMAL)
	sigVal=str(inputDct[i]['Sigma6'])
	input1Dist.setSigma(sigVal)
	calc_string=calc_string+"$+$"+i
	
calc_string=calc_string+"$"
calc_string=calc_string[3:]

#Create an output array
outputarray = OutputVarArray("OutputArray1", Position(400,200))
graph.addOutputVarArray(outputarray)
# Add outputs to output array
output1 = OutputVar("Output1", Position(0,0))
output1.setLowOn(1)
output1.setLow(float(lowCutOff))
outputarray.appendOutputVar(output1)
# Create connection between input and output array
inputarray.newConnection(outputarray)
# Set formula for the outputs
output1.setFormula(calc_string)

mc = optimus.createMethod(graph, optimus.MethodType().TYPE_MC)
mcMethodOptions = mc.getOptions()
mcMethodOptions.setNumberOfExperiments(int(numExp))

mc.calculate()
mc.blockTillDone()
mc.loadResults()
summary_reader(mc)
optimus.saveProject(projectFileName,True)

####################################################################################################


