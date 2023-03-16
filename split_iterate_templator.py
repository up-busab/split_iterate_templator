import os
import json

class obj(object):
    def __init__(self, d):
        if isinstance(d, dict):
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, obj(b) if isinstance(b, dict) else b)

iterateData = {}
masterBinding = {}

def clean(text):
    return text.replace('/',' or ').replace('&','and').replace('(','').replace(')','')

def kabob_case(cleanSpacedText):
    return '-'.join(cleanSpacedText.split()).lower()
	
def CamelCase(cleanSpacedText):
    return ''.join(x for x in cleanSpacedText.title() if not x.isspace())

def lowerCamelCase(camelCaseText):
    toReturn = list(camelCaseText)
    toReturn[0] = camelCaseText[0].lower()
    return "".join(toReturn)	
	
def applyTemplate(templateString, templateBinding):
    return templateString.format(**templateBinding) 

def applyTemplateToFiles(inFileName,outFileName,outFileMode,templateMapping):
    with open(inFileName, 'r') as ftemp:
        templateString = ftemp.read()
    with open(outFileName, outFileMode) as f:
        f.write(applyTemplate(templateString,templateMapping))

def applyTemplateAndWrite(inFileName,outFileName,templateMapping):
    applyTemplateToFiles(inFileName,outFileName,'w',templateMapping)
	
def applyTemplateAndAppend(inFileName,outFileName,templateMapping):
    applyTemplateToFiles(inFileName,outFileName,'a',templateMapping)	

def createStandardTemplate(customTemplate):
    return customTemplate.replace('{','{{').replace('}','}}').replace('[[','{').replace(']]','}')

def splitIntoBlocks(template):
    return template.split("/*<SPLIT>*/")

def getOuterKeySignature(outerKey):
    return "[["+outerKey

def getIndexedOuterKey(outerKey,index):
    return outerKey+"_"+str(index)

def getIndexedOuterKeySignature(outerKey,index):
    return getOuterKeySignature(getIndexedOuterKey(outerKey,index))

def createInnerTemplate(template,outerKey,index):
    return template.replace(getOuterKeySignature(outerKey), getIndexedOuterKeySignature(outerKey, index))

def initMasterBinding(inputBinding):
    for outerKey in inputBinding:
        value = inputBinding[outerKey]
        if not isinstance(value, (dict,list,tuple)):
            masterBinding[outerKey] = value

def updateMasterBinding(outerKey,index):
    masterBinding[getIndexedOuterKey(outerKey,index)] = obj(iterateData[outerKey][index])

def parseIterateTemplate(template):
    token = template.split("<ITERATE>(",1)
    if(len(token)<=1):
        return []
    right = token[1]
    token = right.split(")*/",1)
    left = token[0]
    template = token[1]
    token = left.split(",",1)
    outerKey = token[0]
    delimiter = token[1].replace("'","")
    return [outerKey,delimiter,template]

def isIterate(template):
    return len(parseIterateTemplate(template)) >= 1

def getOuterKey(template):
    return parseIterateTemplate(template)[0]

def getDelimiter(template):
    return parseIterateTemplate(template)[1]

def getTrimmedTemplate(template):
    return parseIterateTemplate(template)[2]

def processIterateBlock(template):
    compositeTemplate = ""
    outerKey = getOuterKey(template)
    delimeter = getDelimiter(template)
    trimmedTemplate = getTrimmedTemplate(template)
    outerList = iterateData[outerKey]
    for index in range(0,len(outerList)):
        compositeTemplate += createInnerTemplate(trimmedTemplate,outerKey,index)
        if(index<len(outerList)-1):
            compositeTemplate += delimeter
        updateMasterBinding(outerKey,index)
    return compositeTemplate

def processBlocks(templateBlocks):
    compositeTemplate = ""
    for template in templateBlocks:
        if(isIterate(template)):
            compositeTemplate += processIterateBlock(template)
        else:
            compositeTemplate += template
    
    return compositeTemplate
 
def loadJSONBindings(jsonFilename):
    with open(jsonFilename) as jsonFile:    
        return json.load(jsonFile)
   
def preprocessBindings(inputBindings):
    outputBindings = {};
    for k in inputBindings:
        if k == "property":
            outputBindings[k] = []
            for prop in inputBindings[k]:
                prop["name_lower"] = lowerCamelCase(prop["name"])
                outputBindings[k].append(prop)
        else:
            outputBindings[k] = inputBindings[k]
    return outputBindings
        

bindings = loadJSONBindings("bindings.json")
iterateData = preprocessBindings(bindings[0])

print iterateData

initMasterBinding(iterateData)

templateFiles = ["vmTemplate.java", "mapperTemplate.java"]


for filename in templateFiles:
    with open(filename) as inputTemplate:
        template=createStandardTemplate(processBlocks(splitIntoBlocks(inputTemplate.read()))) 
    #print template
    #print masterBinding
    print applyTemplate(template, masterBinding)


























