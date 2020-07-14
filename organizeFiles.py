import os
import time

#### HELPERS ####
# getFileOutpath(): finds a valid path for a file in the output folder (organized by date)
# 
def getFileOutpath(fileName, fileYear, outputFolder):
	fileOutPath = outputFolder + str(fileYear) + '/' + fileName

	i = 1
	while os.path.exists(fileOutPath) == True:
		if '.' in fileName:
			fileNameArr = fileName.split('.')
			modifiedExt = '(' + str(i) + ')' + '.' + fileNameArr[len(fileNameArr) - 1]

			newFileName = fileNameArr[0]
			for k in range(1, len(fileNameArr) - 1):
				newFileName += '.' + fileNameArr[k]
			newFileName += modifiedExt
		else:
			newFileName = fileName + '(' + str(i) + ')'
		
		fileOutPath = outputFolder + str(fileYear) + '/' + newFileName
		i += 1

	return fileOutPath


# getFileYear(): finds the earliest year of a files existence
# searches a files access date, creation date, and modified date for earliest year
# params: file, string; name/path of the input file
# return; int, earliest year the file was found to be in existence
def getFileYear(file):
	atime = time.ctime(os.path.getatime(file))
	mtime = time.ctime(os.path.getmtime(file))
	ctime = time.ctime(os.path.getctime(file))
	
	atimeArr = atime.split()
	mtimeArr = mtime.split()
	ctimeArr = ctime.split()
	
	ayear = int(atimeArr[4])
	myear = int(mtimeArr[4])
	cyear = int(ctimeArr[4])
	
	year = ayear
	if year > myear:
		year = myear
	if year > cyear:
		year = cyear

	return year

#### ROUTINES #####
# checkPath(): checks a path and its subdirectories to count how many files and search for a specific file
# meant to check if a programs own files are within a path given to it
# params: path (string)- directory path to search; file_name (string)- name of file being searched for
# return: int; if file is found -1 is returned, otherwise the number of files found is returned
def checkPath(path, outPath, file_name):
	num_files = 0
	ret = 0

	if path[len(path)-1] != '/':
		path += '/'
	if outPath[len(outPath)-1] != '/':
		outPath += '/'

	if path in outPath:
		print("organizeFiles(): ERROR output directory cannot be a child of the input directory.\n")
		exit()

	pathArr = os.listdir(path)
	for item in pathArr:
		if item == file_name:
			return -1

		elif os.path.isfile(path + item):
			num_files += 1

		elif os.path.isdir(path + item):
			ret = checkPath(path + item, outPath, file_name)
			if ret < 0:
				return -1
			num_files += ret

	return num_files


# organizeFiles(): Moves the files of an input directory into an output directory where they are organized by their earliest year
def organizeFiles(inPath, outPath):
	if inPath[len(inPath)-1] != '/':
		inPath += '/'
	if outPath[len(outPath)-1] != '/':
		outPath += '/'

	if inPath in outPath:
		print("organizeFiles(): ERROR output directory cannot be a child of the input directory.\n")
		exit()

	pathArr = os.listdir(inPath)
	for item in pathArr:
		itemPath = inPath + item
		if os.path.isfile(itemPath):
			year = getFileYear(itemPath)
			if os.path.exists(outPath + str(year)) == False:
				os.mkdir(outPath + str(year))
			itemOutPath = getFileOutpath(item, year, outPath)
			os.rename(itemPath, itemOutPath)

		elif os.path.isdir(itemPath):
			organizeFiles(itemPath, outPath)


#### MAIN ####
def main():
	thisFile = "organizePictures.py"
	path = ''
	outPath = ''

	while os.path.exists(path) != True and path != "exit":
		path = input("\nEnter the directory path you wish to organize (or exit): ")

	outPath = input("\nEnter a unique name for the new folder: ")
	while os.path.exists(outPath) == True and outPath != path:
		print(outPath + " already exists")
		outPath = input("\nEnter a unique name for the new folder: ")

	if path == "exit":
		exit()

	num_files = checkPath(path, outPath, thisFile)
	
	if num_files < 0:
		print("Warning: " + thisFile + " cannot be within the specified directory path.\n")
		exit()

	print("Number of files found: {}\n".format(num_files))

	os.mkdir(outPath)
	organizeFiles(path, outPath)

	exit()

'''
def main():
	path = ''

	while path != "exit":
		path = input("Enter a folder name: ")
		if path != "exit":
			i = 1
			while os.path.isdir(path + '(' + str(i) + ')') == True:
				i += 1
			os.mkdir(path + '(' + str(i) + ')')
'''

main()