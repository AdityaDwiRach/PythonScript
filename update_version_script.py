import os
import sys
import fileinput

fileMakeFull = 'make_full_OTA.sh'
fileMakeIncrement = 'make_incremental_OTA.sh'

textOSVer = 'export TSM_OS_VERSION'
textCLNTver = 'export TSM_OS_CLIENT_VERSION'
textToSearchCLNT = ''
textToSearchOS = ''

def findString(file):
	openMakeFull = open(file)

	line_num_CLNT = 0
	line_num_OS = 0

	for num, line in enumerate(openMakeFull, 1):
		if textCLNTver in line :
			line_num_CLNT = num
			print 'found : ', num
		if textOSVer in line :
			line_num_OS = num
			print 'found : ', num

	openMakeFull.seek(0)
	textMakeFull = openMakeFull.readlines()
	textFullCLNT = textMakeFull[line_num_CLNT-1]
	textFullOS = textMakeFull[line_num_OS-1]
	global textToSearchCLNT
	textToSearchCLNT = textFullCLNT[29:None]
	global textToSearchOS
	textToSearchOS = textFullOS[22:None]

	print (line_num_CLNT)
	print (line_num_OS)
	print (textToSearchCLNT)
	print (textToSearchOS)

	openMakeFull.close()

def replaceString(file):

	openMakeFull = open(file)

	fileRead = openMakeFull.read()

	fileCLNTVer = fileRead.replace(textToSearchCLNT, textToReplaceCLNTver+"\n")
	fileAll = fileCLNTVer.replace(textToSearchOS, textToReplaceOSver+"\n")

	openMakeFull = open(file, "w")
	openMakeFull.write(fileAll)
	openMakeFull.close()

def replaceMakeFull():
	findString(fileMakeFull)
	replaceString(fileMakeFull)

def replaceMakeIncrement():
	findString(fileMakeIncrement)
	replaceString(fileMakeIncrement)

if __name__ == "__main__":

	print ("Text to replace for TSM_OS_VERSION : ")
	textToReplaceOSver = raw_input("> ")

	print ("Text to replace for TSM_OS_CLIENT_VERSION : ")
	textToReplaceCLNTver = raw_input("> ")

	replaceMakeFull()
	replaceMakeIncrement()

raw_input('\n\n Press Enter to Exit...')