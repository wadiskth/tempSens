import os

maxFileName = 0
currentFile = 0
folderRoot = '/media/usb0/'
fileType = '.csv'
for filename in os.listdir(folderRoot):
    if filename.lower().endswith('.csv'):
        try:
            currentFile = int(os.path.splitext(filename)[0])
            if currentFile > maxFileName:
                maxFileName = currentFile
        except ValueError:
            print 'File name ' + str(filename) + ' not within naming conventions.'
currentFile = currentFile + 1
print folderRoot + str(currentFile) + fileType
