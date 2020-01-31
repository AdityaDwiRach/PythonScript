import os
import sys, getopt
import fileinput
import argparse
from argparse import RawTextHelpFormatter

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

		if textOSVer in line :
			line_num_OS = num

	openMakeFull.seek(0)
	textMakeFull = openMakeFull.readlines()
	textFullCLNT = textMakeFull[line_num_CLNT-1]
	textFullOS = textMakeFull[line_num_OS-1]
	global textToSearchCLNT
	textToSearchCLNT = textFullCLNT[29:None]
	global textToSearchOS
	textToSearchOS = textFullOS[22:None]

	openMakeFull.close()

def replaceString(file):

	openMakeFull = open(file)

	fileRead = openMakeFull.read()

	enterOSver = "\n"
	enterCLNTver = "\n"

	textToReplaceOSver = textToReplaceOSInput
	textToReplaceCLNTver = textToReplaceCLNTInput

	if textToReplaceOSInput == '':
		textToReplaceOSver = textToSearchOS
		enterOSver = ''

	if textToReplaceCLNTInput == '':
		textToReplaceCLNTver = textToSearchCLNT
		enterCLNTver = ''

	fileOSVer = fileRead.replace(textToSearchOS, textToReplaceOSver+enterOSver,1)
	fileAll = fileOSVer.replace(textToSearchCLNT, textToReplaceCLNTver+enterCLNTver,1)
	
	openMakeFull.close()

	openMakeFull = open(file, "w")
	openMakeFull.write(fileAll)
	openMakeFull.close()

def replaceMakeFull():
	findString(fileMakeFull)
	replaceString(fileMakeFull)

def replaceMakeIncrement():
	findString(fileMakeIncrement)
	replaceString(fileMakeIncrement)

def helpMessage():
	parser = argparse.ArgumentParser(
		description = 'Example = \n\tpython update_version_script.py -o ID30S-QD-1.2.5 -c 1.0.2 \n\tpython update_version_script.py -o ID30S-QD-1.3.5 \n\tpython update_version_script.py -c 1.2.1',
		usage = 'python update_version_script.py -o|--os <os_version> -c|--clnt <clnt_version>',
		formatter_class=RawTextHelpFormatter)
	parser.add_argument("-o", "--os", type=str, help='the updated os version')
	parser.add_argument("-c", "--clnt", type=str, help='the updated client version')
	args = parser.parse_args()

if __name__ == "__main__":

	helpMessage()

	textToReplaceOSInput = ''
	textToReplaceCLNTInput = ''

	# get all arguments from command line
	myopt, args = getopt.getopt(sys.argv[1:],"o:c:")

	# pass the argument into each variable
	for c, i in myopt:
		if c == '-o':
			textToReplaceOSInput = "\""+i+"\""
		elif c == '-c':
			textToReplaceCLNTInput = "\""+i+"\""

	replaceMakeFull()
	replaceMakeIncrement()

	fileMakeFullPath = os.path.abspath(fileMakeFull)
	fileMakeIncrementPath = os.path.abspath(fileMakeIncrement)

	os.system("git add " + fileMakeFullPath + " " + fileMakeIncrementPath)
	os.system("git commit")