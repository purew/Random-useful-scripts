#/usr/bin/env python
# Create or update a mirrored folder with (resized) pictures
#
# By Anders Bennehag, anders@bennehag.com
#

originalDir = "/home/anders/Blandat/Pictures/Yearly/"
cloneDir = "/home/anders/Blandat/Pictures/Yearly_720p/"
smallerSize = 1280 # 720p

import os
import sys
import subprocess

def resizePicture( root, picture, newPicture ):
	''' Resize one picture '''
	if not os.path.isfile( newPicture ):
		args = ["convert", \
			os.path.join(root, picture), \
			"-auto-orient", \
			"-resize", \
			str(smallerSize)+"x"+str(smallerSize), \
			newPicture ]
		subprocess.call(args)


def iterateTree():
	''' Traverse a tree directory and resize each picture '''
	for root, dirs, files in os.walk( originalDir ):
		shorterRoot = root[len(originalDir):] # A bit ugly here
		newDir = cloneDir+shorterRoot
		try:
			os.makedirs(newDir)
			print "Creating "+newDir
		except OSError:
			pass
		for file in files:
			originalFile = os.path.join(root,file)
			newFile = os.path.join(newDir,file)
			resizePicture( root, originalFile, newFile )

def checkPrerequisites():
	''' Check if everything is set up '''
	override = False
	for arg in sys.argv:
		if arg == "-f":
			override = True
	if not os.path.isfile( '/usr/bin/convert' ) and not override:
		print "Imagemagick's convert does not seem to be installed."
		print "If it is, override this check with -f"
		sys.exit()

	if originalDir[-1] != "/" or cloneDir[-1]!="/":
		print "Directories needs an ending slash"
		sys.exit()
	if len(originalDir)<1 or len(cloneDir)<1:
		print "Need to specify directories inside script"
		sys.exit()

if __name__ ==  '__main__':
	checkPrerequisites()
	iterateTree()
