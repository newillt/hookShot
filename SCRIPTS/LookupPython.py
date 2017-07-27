import optimus
import csv
import os
import sys
from datetime import datetime
startTime = datetime.now()
from optimus import DistributionType,InputVarArray, InputVar, InputVarType, InputVarRangeType, OutputVarArray, OutputVar, Position
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
for data in playerData:
	#if (player==data[1]):
	try:
		inputDct[data[1]]={}
		inputDct[data[1]]["Position"]=data[0]
		inputDct[data[1]]["Salary"]=data[5]
		inputDct[data[1]]["Projection"]=data[6]
		inputDct[data[1]]["YearHigh"]=data[7]
		inputDct[data[1]]["YearLow"]=data[8]
		inputDct[data[1]]["Sigma6"]=(float(data[7])-float(data[8]))/6
		
		k=k+1
	except:
		#print data
		next

from collections import Counter
double=False
y=Counter(sys.argv).items()
for k in y:
	if k[1]>1:
		double=True

if double:
	print "Salary: ", "-1 ","Duplicate: ","-1 ", "Duplicate: ", "-1"
else:
	print "Salary: ",float(inputDct[sys.argv[1].replace("_"," ")]["Salary"])+float(inputDct[sys.argv[2].replace("_"," ")]["Salary"])+\
	float(inputDct[sys.argv[3].replace("_"," ")]["Salary"])+float(inputDct[sys.argv[4].replace("_"," ")]["Salary"])+\
	float(inputDct[sys.argv[5].replace("_"," ")]["Salary"])+float(inputDct[sys.argv[6].replace("_"," ")]["Salary"])+\
	float(inputDct[sys.argv[7].replace("_"," ")]["Salary"])+float(inputDct[sys.argv[8].replace("_"," ")]["Salary"])+\
	float(inputDct[sys.argv[9].replace("_"," ")]["Salary"]),"FDFP: ",float(inputDct[sys.argv[1].replace("_"," ")]["Projection"])+float(inputDct[sys.argv[2].replace("_"," ")]["Projection"])+\
	float(inputDct[sys.argv[3].replace("_"," ")]["Projection"])+float(inputDct[sys.argv[4].replace("_"," ")]["Projection"])+\
	float(inputDct[sys.argv[5].replace("_"," ")]["Projection"])+float(inputDct[sys.argv[6].replace("_"," ")]["Projection"])+\
	float(inputDct[sys.argv[7].replace("_"," ")]["Projection"])+float(inputDct[sys.argv[8].replace("_"," ")]["Projection"])+\
	float(inputDct[sys.argv[9].replace("_"," ")]["Projection"]), "Sigma6: ",float(inputDct[sys.argv[1].replace("_"," ")]["Sigma6"])+float(inputDct[sys.argv[2].replace("_"," ")]["Sigma6"])+\
	float(inputDct[sys.argv[3].replace("_"," ")]["Sigma6"])+float(inputDct[sys.argv[4].replace("_"," ")]["Sigma6"])+\
	float(inputDct[sys.argv[5].replace("_"," ")]["Sigma6"])+float(inputDct[sys.argv[6].replace("_"," ")]["Sigma6"])+\
	float(inputDct[sys.argv[7].replace("_"," ")]["Sigma6"])+float(inputDct[sys.argv[8].replace("_"," ")]["Sigma6"])+\
	float(inputDct[sys.argv[9].replace("_"," ")]["Sigma6"])
	
print datetime.now() - startTime