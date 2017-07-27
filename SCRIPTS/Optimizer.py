import optimus
import csv
import sys
import os
from datetime import datetime
from optimus import DistributionType,InputVarArray, InputVar, InputVarType, InputVarRangeType, OutputVarArray, OutputVar, Position
import glob
from summaryreader import SummaryReader

dateTimeString=datetime.today().strftime('%Y%m%d_%H%M%S')
####################################################################################################
##### PARAMETRIZE FILE NAMES #######################################################################
####################################################################################################

dir = os.path.dirname(__file__)
path_string=str(dateTimeString+'.txt')
filename=os.path.join(dir,path_string)
#logFile = open(filename, 'w')
#sys.stdout = logFile
#sys.stderr = logFile

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

### READ IN CSV FILE WITH FLOOR AND CEILING DATA
playerData=[]
filename=os.path.join(dir, '..\\DATA','preProcessed',path_string)
with open(r"C:\Users\tnewill\Dropbox\Business Ideas\NBAPredictor\DATA\preProcessed\20151118_1200_floor_ceil.csv", 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		#print row
		playerData.append(row)

k=0
inputDct={}
iterplayers = iter(playerData)
next(iterplayers)
for data in iterplayers:
	if (float(data[6])>15.0):
		try:
			inputDct[data[1]]={}
			inputDct[data[1]]["Position"]=data[0]
			inputDct[data[1]]["Projection"]=data[6]
			inputDct[data[1]]["YearHigh"]=data[7]
			inputDct[data[1]]["YearLow"]=data[8]
			inputDct[data[1]]["Sigma6"]=(float(data[7])-float(data[8]))/6
			k=k+1
		except:
			print data
			next
	else:
		next

#for player in inputDct:
#	if inputDct[player]["Position"]=="C":
#		print player,inputDct[player]['Position']

projectDir = r"C:\Users\tnewill\Dropbox\Business Ideas\NBAPredictor\OPTIMUS"
projectFileName = r"C:\Users\tnewill\Dropbox\Business Ideas\NBAPredictor\OPTIMUS\OptimizeLineup.opt"
project = optimus.createProject(projectDir)
graph = project.getActiveGraph()
inputarray = InputVarArray("Positions", Position(100, 200))
graph.addInputVarArray(inputarray)
		
posList=("C","PG_1","PG_2","SG_1","SG_2","PF_1","PF_2","SF_1","SF_2")
for position in posList:
	input1 = InputVar(position, Position(0,0))
	input1.setType(InputVarType.IV_STRING)
	input1.setRange(InputVarRangeType.IV_CATALOG)
	for player in inputDct:
		if inputDct[player]['Position']==position[:2]:
			input1.addStringValue(player.replace(" ","_"))
		
	inputarray.appendInputVar(input1)

staticAction = optimus.Action('PythonLookup',optimus.Position(200,200))
actionString="c:\\anaconda\\python.exe \"C:\\Users\\tnewill\\Dropbox\\Business Ideas\\NBAPredictor\\SCRIPTS\\LookupPython.py\" \"$C$\" \"$PG_1$\" \"$PG_2$\" \"$SG_1$\" \"$SG_2$\" \"$PF_1$\" \"$PF_2$\" \"$SF_1$\" \"$SF_2$\" > $OutputFile$"
staticAction.setCommand(actionString)
graph.addAnalysis(staticAction)
connection = optimus.Connection(inputarray,staticAction)
graph.addConnection(connection)


### OUTPUTS
FDFP = optimus.OutputVar('FDFP', optimus.Position(400, 100))
graph.addOutputVar(FDFP)
Sigma6 = optimus.OutputVar('Sigma6', optimus.Position(400, 200))
graph.addOutputVar(Sigma6)
Salary = optimus.OutputVar('Salary', optimus.Position(400, 200))
Salary.setHigh(60000.0)
Salary.setHighOn(1)
graph.addOutputVar(Salary)
MeanSigma = optimus.OutputVar('MeanSigma', optimus.Position(500, 200))
MeanSigma.setFormula("$Sigma6$/9")
graph.addOutputVar(MeanSigma)
#Reliability = optimus.OutputVar('Reliability', optimus.Position(400, 300))
#graph.addOutputVar(Reliability)

### OUTPUT FILE
outputFile = optimus.File('OutputFile',optimus.Position(300,200))
graph.addFile(outputFile)

### CONNECCTIONS
connection = optimus.Connection(outputFile,FDFP)
graph.addConnection(connection)
connection = optimus.Connection(outputFile,Sigma6)
graph.addConnection(connection)
connection = optimus.Connection(outputFile,Salary)
graph.addConnection(connection)
connection = optimus.Connection(Sigma6,MeanSigma)
graph.addConnection(connection)

### EXTRACTION RULES
extrRule = outputFile.getExtrRule(0)
extrRule.setWordNr(4)

extrRule = outputFile.getExtrRule(1)
extrRule.setWordNr(6)

extrRule = outputFile.getExtrRule(2)
extrRule.setWordNr(2)

connection = optimus.Connection(staticAction,outputFile)
graph.addConnection(connection)

doe = optimus.createMethod(graph, optimus.MethodType().TYPE_DOE)
doe.setType(optimus.DOEMethodType().MAT_RANDOM)
doeMethodOptions = doe.getOptions()   
doeMethodOptions.setNumberOfExperiments(10)
doe.setName("RANDOM_DOE_1")
doe.calculate()
doe.blockTillDone()
doe.loadResults()

optimus.saveProject(projectFileName,True)
