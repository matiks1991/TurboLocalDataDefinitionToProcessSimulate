from datetime import date
import os


def checkLineData(line, semicolon):

    checkedLine = ''
    typesSource = [' robtarget ', ' jointtarget ', ' grp_part ', 
                ' grp_config ', ' loaddata ', ' grp_pos ', 
                'CONST aktion_pos ', 'CONST Bauteil_num ', ' tooldata ', 
                ' wobjdata ', ' GunNr ', ' TipDresserNr ', ' MobileTipDressNr ', 
                ' TypId ', ' speeddata ', ' zonedata ']
    
    if "PROC " not in line:

        for typeSource in typesSource:
            
            if typeSource in line:
                checkedLine = line
                
            if checkedLine != "":
                break

        if semicolon == 0:
            checkedLine = line
        
    return checkedLine

def checkSemicolon(oneLine, semicolon):

    if (oneLine != ''):

        if (";" in oneLine):
            semicolon = 1
        else:
            semicolon = 0
    
    return semicolon

def generateTotalFromOneFile(content):

    oneFile = ''
    oneLine = ''
    semicolon = 1

    for line in content:
        
        oneLine += checkLineData(line, semicolon)
        oneFile += checkLineData(line, semicolon)
        
        semicolon = checkSemicolon(oneLine, semicolon)

        if semicolon == 1:
            oneLine = ''

    return oneFile

def readFile(filePath):

    file = open(str(filePath), "r")
    content = file.readlines()
    
    file.close()
    
    return content

def getTotalFromFile(filePath):

    content = readFile(filePath)

    oneFile = generateTotalFromOneFile(content)

    return oneFile

def getCurrentDate():

    currentDate = date.today()
    formatedDate = currentDate.strftime("%Y%m%d")

    return formatedDate

def prepareOutput(nameBackup):

    templateFile = 'LocalDataDefinitionTemplate.sys'
    sourceFiles = ["PROGMOD\ComUser.mod", "PROGMOD\GrpData.mod", "PROGMOD\GrpUser.mod", "PROGMOD\SW_User_LU.mod", "SYSMOD\SW_Service_LU.sys", "SYSMOD\ComBase_LU.sys"]
    sumFiles = ''

    nameRobot = getNameRobot(nameBackup)
    nameMainModule = ["PROGMOD\\" + nameRobot + ".mod"]
    sourceFiles += nameMainModule
    
    if (os.path.isfile(templateFile)):
            sumFiles += getTotalFromFile(templateFile)
    else:
        input("Brak pliku z wartościami początkowymi! Kliknij Enter aby kontynuawać")

    backupsPath = getBackupsPath()

    for sourceFile in sourceFiles:
        
        filePath = backupsPath + nameBackup + "\RAPID\TASK1\\" + sourceFile
        
        fileExist = os.path.isfile(filePath)

        if fileExist:
            sumFiles += getTotalFromFile(filePath)

    return sumFiles

def writeToFile(nameRobot, outputFile, nameOutputFolder):
    
    currentDate = getCurrentDate()

    nameNewFolder = nameOutputFolder + "_" + currentDate + "_LocalDataDefinition"
    
    folderExist = os.path.isdir(nameNewFolder)

    if not folderExist:
        os.mkdir(nameNewFolder)

    filePath = nameNewFolder + "\\" + nameRobot + "_" + currentDate + "_LocalDataDefinition.sys"

    fileExist = os.path.isfile(filePath)

    if fileExist:
        print("Nadpisany " + nameRobot)

    file = open(filePath, "w")
    file.write(outputFile)

    file.close()

def getBackupsPath():

    fileName = "BackupsPath.txt"

    fileExist = os.path.isfile(fileName)

    if fileExist:
        file = open(str(fileName), "r")
        backupsPath = file.readline()

        accessIsOk = os.access(backupsPath, os.R_OK)

        if not accessIsOk:
            input("Nie znaleziono w pliku poprawnej ścieżki do backupów. Kliknij Enter aby zakończyć.")
            exit()

    else:
        input("Nie znaleziono pliku BackupsPath.txt. Kliknij Enter aby zakończyć.")
        exit()

    if backupsPath[-1] != "\\":
        backupsPath += "\\"
    

    return backupsPath

def getNameRobot(nameBackup):

    nameRobot = nameBackup[0:4] + "BG" + nameBackup[4:12]

    return nameRobot

def getNamesAllBackups():

    backupsPath = getBackupsPath()
    namesBackups = list(os.listdir(backupsPath))

    return namesBackups


def getNameOutputFolder():

    backupsPath = getBackupsPath()

    positionSignificantSlash = backupsPath.rfind("\\", 0, len(backupsPath)-1)

    nameOutputFolder = backupsPath[positionSignificantSlash+1:-1]
    
    return nameOutputFolder


namesBackup = getNamesAllBackups()

nameOutputFolder = getNameOutputFolder()

numberOfBackup = 1

for nameBackup in namesBackup:

    nameRobot = getNameRobot(nameBackup)

    sumFiles = prepareOutput(nameBackup)

    writeToFile(nameRobot, sumFiles, nameOutputFolder)

    print(str(numberOfBackup) + " - " + nameBackup)
    numberOfBackup += 1

input("Operacja zakończona pomyślnie. Aby zamknąć kliknij Enter.")