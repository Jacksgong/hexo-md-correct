#!/usr/bin/python -u

"""
Copyright 2018, JacksGong(https://jacksgong.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import argparse
import os
from os.path import join
from tempfile import mkstemp

from shutil import move

from md_utils import derrickCount, replaceDerrick

__version__ = '1.0'
__author__ = 'JacksGong'

print("---------------------------------------------------")
print("             format-md v" + __version__)
print("")
print("You can use this tool to correct the format of mark-\n"
      "down for hexo post")
print("---------------------------------------------------")

parser = argparse.ArgumentParser(description="Markdown format corrector for Hexo post")
parser.add_argument("postPath", nargs="*", help="path of post markdown files directory")

dirPath = parser.parse_args().postPath[0]
print "Correct markdown files on " + dirPath + " directory!"

for subdir, dirs, files in os.walk(dirPath):
    for file_name in files:
        if not file_name.endswith('.md'):
            continue

        md_file_path = join(subdir, file_name)
        # scan file
        lineIndex = 0
        lineList = list()
        derrickList = list()

        lineIndexMakeGiveUp = -1
        md_file = open(md_file_path)
        isCodeArea = False
        for line in md_file:
            if line.strip().startswith("```"):
                if not isCodeArea:
                    isCodeArea = True
                else:
                    isCodeArea = False

            if isCodeArea:
                continue

            if line.lstrip().startswith("#"):
                # derrick area
                array = lineIndex, line, derrickCount(line)
                derrickList.append(array)
            lineList.append(line)
            lineIndex += 1
        md_file.close()

        preNewDerrickCount = 0

        fixedLineMap = {}
        preOldDerrickCount = 0
        minDerrickCount = 0

        # format file
        for lineIndex, line, count in derrickList:
            if preNewDerrickCount == 0:
                # first one.
                preOldDerrickCount = count
                preNewDerrickCount = count
                minDerrickCount = count
                continue

            if count < minDerrickCount:
                lineIndexMakeGiveUp = lineIndex
                break

            oldCount = count
            newCount = count
            levelOffset = count - preOldDerrickCount
            # cover the case of pre-changed
            if levelOffset == 0:
                # same level
                if preNewDerrickCount != count:
                    # pre count changed
                    newCount = preNewDerrickCount
                    newLine = replaceDerrick(line, count, newCount)
                    fixedLineMap[lineIndex] = newLine
            elif levelOffset > 0:
                # level lower
                if levelOffset > 1:
                    # level jump, adapter
                    newCount = preNewDerrickCount + 1
                    if newCount != count:
                        newLine = replaceDerrick(line, count, newCount)
                        fixedLineMap[lineIndex] = newLine
            else:
                # level higher
                if count - preNewDerrickCount >= 0:
                    # on new case, pre level higher than this level, this is very serious issue
                    lineIndexMakeGiveUp = lineIndex
                    # print str(count) + ":" + str(preOldDerrickCount) + ":" + str(
                    #     preNewDerrickCount) + line.rstrip() + ":" + preLine.rstrip()
                    break
            preOldDerrickCount = oldCount
            preNewDerrickCount = newCount
            preLine = line

        if fixedLineMap.__len__() > 0 or lineIndexMakeGiveUp >= 0:
            print " change " + md_file_path
            # Create temp file
            fh, tmpAbsPath = mkstemp()
            with os.fdopen(fh, 'w') as new_file:
                with open(md_file_path) as old_file:
                    lineIndex = 0
                    for line in old_file:
                        if lineIndexMakeGiveUp == lineIndex:
                            # case of give-up
                            new_file.write("todo " + line)
                        # case of fixed
                        elif lineIndex in fixedLineMap:
                            new_file.write(fixedLineMap[lineIndex])
                        else:
                            new_file.write(line)
                        lineIndex += 1
            # Remove original file
            os.remove(md_file_path)
            # Move new file
            move(tmpAbsPath, md_file_path)
