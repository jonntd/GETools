# GETOOLS is under the terms of the MIT License

# Copyright (c) 2018-2024 Eugene Gataulin (GenEugene). All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author: Eugene Gataulin tek942@gmail.com https://www.linkedin.com/in/geneugene

import maya.cmds as cmds

from ..utils import Selector

def Create(*args):
	selectedList = Selector.MultipleObjects(1)
	if (selectedList == None):
		return
	
	name = "MotionTrail_1"
	step = 1
	start = cmds.playbackOptions(query = True, minTime = True)
	end = cmds.playbackOptions(query = True, maxTime = True)
	cmds.snapshot(name = name, motionTrail = True, increment = step, startTime = start, endTime = end)
	selected = cmds.ls(type = "motionTrail")
	
	for item in selected:
		cmds.setAttr(item + "Handle" + "Shape.trailDrawMode", 1)
		cmds.setAttr(item + "Handle" + "Shape.template", 1)

def Select(*args):
	selected = cmds.ls(type = "motionTrail")
	if (len(selected) == 0):
		return
	
	cmds.select(clear = True)
	for item in selected:
		cmds.select(item + "Handle", add = True)

def Delete(*args):
	selected = cmds.ls(type = "motionTrail")
	if (len(selected) == 0):
		return
	
	for item in selected:
		cmds.delete(item + "Handle")

def CreateCurveFromTrajectory(): # TODO rework tool and add to module
	# Variables
	step = 1
	degree = 3
	# Names
	mtName = "newMotionTrail"
	mtFinalName = mtName + "Handle"
	curveName = "testCurve"


	# Get time start/end
	start = cmds.playbackOptions(q=1, min=1)
	end = cmds.playbackOptions(q=1, max=1)
	# Create motion trail
	cmds.snapshot(n = mtName, mt=1, i=step, st = start, et = end)

	# Get points from motion trail
	cmds.select(mtFinalName, r=1)
	selected = cmds.ls(sl=1, dag=1, et="snapshotShape")
	pts = cmds.getAttr(selected[0] + ".pts")
	size = len(pts)
	for i in range(size):
		pts[i] = pts[i][0:3]
		#print "{0}: {1}".format(i, pts[i])

	# Create curve
	newCurve = cmds.curve(n = curveName, d = degree, p = pts)

	# End
	cmds.delete(mtFinalName)
	cmds.select(cl=1)