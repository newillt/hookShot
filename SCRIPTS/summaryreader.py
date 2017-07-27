import os
import sys
import re
import random

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment


class SummaryReader:
    def __init__(self, summaryFilename=''):
        self.summaryFilename = summaryFilename
        
    def readSummary(self):
        try:
            return self.summaryDct
        except AttributeError:
        # if self.summaryDct is None:
            summaryFile = open(self.summaryFilename, 'r')

            self.summaryDct = {}
            self.failValueDct = {}

            cpt = 0

            nbInputs = 0
            nbOutputs = 0
            nbGroups = 0

            doeFlag = 0
            optFlag = 0
            mooFlag = 0

            self.inputNameList = []
            self.outputNameList = []
            self.constraintsDct = {}

            beginIO = 1e5
            
            expNb = 0
            summaryExpDct={}

            for line in summaryFile:
                line = re.sub('\s+',' ',line.rstrip('\n'))
                cpt+=1
                if cpt == 3:
                    nbInputs = int(line.split(' ')[0])
                if cpt == 4:
                    nbOutputs = int(line.split(' ')[0])
                if cpt == 5:
                    if line.count('DOE'):
                        doeFlag = 1
                        failPosition = 6
                        self.preHeader = ['Exp. Num.']
                    elif line.count('OPT'):
                        optFlag = 1
                        failPosition = 7
                        self.preHeader = ['Exp. Num.','Label','Annot','Iter']
                    elif line.count('MOO'):
                        mooFlag = 1
                        failPosition = 8
                        self.preHeader = ['Exp. Num.', 'Label', 'Group','Iter','Annot',]
                if mooFlag == 1 and cpt == 8:
                    nbGroups = int(line.split(' ')[0])
                if line.count('Exp SubExp1 SubExp2 SubExp3'):
                    beginIO = cpt + 1
                if cpt >= beginIO and cpt < beginIO + nbInputs:    
                    inputName=line.split(' ')[0].lstrip('"').rstrip('"')
                    self.inputNameList.append(inputName)
                if cpt >= beginIO + nbInputs and cpt < beginIO + nbInputs + nbOutputs: 
                    lineSplitList=line.split(' ')
                    outputName=lineSplitList[0].lstrip('"').rstrip('"')
                    self.outputNameList.append(outputName)
                    
                    if int(lineSplitList[1])>0:
                        self.constraintsDct[outputName]={}
                        self.constraintsDct[outputName]['low']=float(lineSplitList[2])
                    if int(lineSplitList[3])>0:
                        try:
                            self.constraintsDct[outputName]['high']=float(lineSplitList[4])
                        except KeyError:
                            self.constraintsDct[outputName]={}
                            self.constraintsDct[outputName]['high']=float(lineSplitList[4])
                    
                if cpt >= beginIO + nbInputs + nbOutputs :
                        
                    failValue = line.split(' ')[failPosition-1]
                    if True:
                        lineList = line.split(' ')
                        lineList.pop(failPosition-1)
                        
                        # group the Exp with the SubExps if needed
                        Exp = lineList[0]
                        fullExp = Exp
                        SubExp1 = lineList.pop(1)
                        SubExp2 = lineList.pop(1)
                        SubExp3 = lineList.pop(1)
                        if SubExp3 != '0':
                            fullExp = Exp+'.'+SubExp1+'.'+SubExp2+'.'+SubExp3
                            lineList[0] = fullExp
                        
                        # remove iter value
                        if doeFlag == 1:
                            lineList.pop(0)
                            lineList.pop(0)
                        if mooFlag == 1:
                            # lineList.pop(0)
                            tmpVal = lineList[2]
                            lineList[2] = lineList[3]
                            lineList[3] = lineList[1]
                            lineList[1] = tmpVal
                            
                        # format the numbers
                        newList = []
                        scpt=0
                        for nb in lineList:
                            scpt+=1
                            if scpt <= 2 - doeFlag*2 + optFlag + mooFlag*2:
                                nbs = nb
                            else:
                                
                                nbf=float(nb)
                                if (nbf>0 and nbf<0.0001) or (nbf<0 and nbf>-0.0001) or (nbf>0 and nbf>=1000000) or (nbf<0 and nbf<=-1000000):
                                    nbs="%.5e" % nbf
                                else:
                                    nbs="%.5f" % nbf
                                
                            newList.append(nbs)

                        if fullExp not in summaryExpDct.keys():
                            expNb += 1
                            summaryExpDct[fullExp]=expNb
                        
                        self.summaryDct[summaryExpDct[fullExp]]=newList
                    
            summaryFile.close()
            
            return self.summaryDct
            
    def getSummary(self):    
        try:
            return self.summaryDct
        except AttributeError:
            self.readSummary()
            return self.summaryDct
            
    def getNameList(self):    
        try:
            nameList = self.preHeader[1:]
            nameList.extend(self.inputNameList)
            nameList.extend(self.outputNameList)        
            return nameList
        except AttributeError:
            self.readSummary()
            
            nameList = self.preHeader[1:]
            nameList.extend(self.inputNameList)
            nameList.extend(self.outputNameList)        
            return nameList 
            
    def getNbInputs(self):    
        try:
            return len(self.inputNameList)
        except AttributeError:
            self.readSummary()
            
            return len(self.inputNameList) 
            
    def getNbOutputs(self):    
        try:
            return len(self.outputNameList)
        except AttributeError:
            self.readSummary()
            
            return len(self.outputNameList) 
            

    def getValueForExperiment(self, expNb, name):    
        try:
            expValueList = self.summaryDct[expNb]
        except AttributeError:
            self.readSummary()
            expValueList = self.summaryDct[expNb]
            
        nameList = self.preHeader[1:]
        nameList.extend(self.inputNameList)
        nameList.extend(self.outputNameList)
        # print nameList
        # print expValueList
        
        return float(expValueList[nameList.index(name)])
        
    def getInputValuesForExperiment(self, expNb):    
        try:
            expValueList = self.summaryDct[expNb]
        except AttributeError:
            self.readSummary()
            expValueList = self.summaryDct[expNb]
            
        nameList = self.preHeader[1:]
        nameList.extend(self.inputNameList)
        nameList.extend(self.outputNameList)
        
        ret = {}
        for inputName in self.inputNameList:
            ret[inputName] = float(expValueList[nameList.index(inputName)])
        
        return ret
        
    def getOutputValuesForExperiment(self, expNb):    
        try:
            expValueList = self.summaryDct[expNb]
        except AttributeError:
            self.readSummary()
            expValueList = self.summaryDct[expNb]
            
        print "preHeader:"+str(self.preHeader)
        nameList = self.preHeader[1:]
        nameList.extend(self.inputNameList)
        nameList.extend(self.outputNameList)
        print nameList
        print expValueList
        
        ret = {}
        for outputName in self.outputNameList:
            ret[outputName] = float(expValueList[nameList.index(outputName)])
        
        return ret        
        
    def getNbExp(self):    
        try:
            return len(self.summaryDct.keys())
        except AttributeError:
            self.readSummary()
            return len(self.summaryDct.keys())
        
 
    def getGroups(self):  
        try:
            return self.groupList
        except AttributeError:
            self.readSummary()
        
        # if self.groupList is None:
            self.groupList = []
            groupDct = {}
            
            nameList = self.preHeader + self.inputNameList + self.outputNameList
            groupIndex = nameList.index('Group')-1
            for key in sorted(self.summaryDct.iterkeys()):
                item=self.summaryDct[key]
                
                if int(item[groupIndex]):
                    objList=[]
                    cpt=0
                    for value in item:
                        if len(re.findall('^GOAL[1-9]{1}[0-9]*$',nameList[cpt+1])):
                            objList.append(float(value))
                            
                        cpt+=1
                    groupDct[int(item[groupIndex])]=objList
                    
            for key in sorted(groupDct.iterkeys()):
                self.groupList.append(groupDct[key])
                    
        return self.groupList        

    def toElementTree(self, parentElement):
        self.readSummary()

        nameList = self.preHeader + self.inputNameList + self.outputNameList
        print "nameList"+str(nameList)
        table = SubElement(parentElement, 'table')
        tableHeader = SubElement(table, 'thead')
        nameRow = SubElement(tableHeader, 'tr')
        for item in nameList:
            nameCol = SubElement(nameRow, 'th')
            nameCol.text = item
            
        tableBody = SubElement(table, 'tbody')
        secondSwitch=False
        for key in sorted(self.summaryDct.iterkeys()):
            item=self.summaryDct[key]
            currentRow = SubElement(tableBody, 'tr')
            if ((key-1)/5)%2:
                currentRow.attrib['class']="secondswitch"
                
            expCol = SubElement(currentRow, 'td')
            expCol.text = str(key)
            cpt=0
            # print "item:"+str(item)
            for value in item:
                currentCol = SubElement(currentRow, 'td')
                currentCol.text = value
                try:
                    if float(value)<self.constraintsDct[nameList[cpt+1]]['low'] and not nameList[cpt+1].count('GOAL'):
                        currentCol.attrib['class']="unfeasible"
                        expCol.attrib['class']="unfeasible"
                except (KeyError,ValueError):
                    pass
                try:
                    if float(value)>self.constraintsDct[nameList[cpt+1]]['high'] and not nameList[cpt+1].count('GOAL'):
                        currentCol.attrib['class']="unfeasible"
                        expCol.attrib['class']="unfeasible"
                except (KeyError,ValueError):
                    pass  
                    
                if nameList[cpt+1]=='Group' and int(value)!=0:
                    currentRow.attrib['class']="idealcalculation"

                cpt+=1