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


def derrickCount(line):
    if line.lstrip().startswith("#######"):
        return 7
    elif line.lstrip().startswith("######"):
        return 6
    elif line.lstrip().startswith("#####"):
        return 5
    elif line.lstrip().startswith("####"):
        return 4
    elif line.lstrip().startswith("###"):
        return 3
    elif line.lstrip().startswith("##"):
        return 2
    elif line.lstrip().startswith("#"):
        return 1
    else:
        return 0


def replaceDerrick(originLine, oldCount, newCount):
    oldDerrick = ""
    count = 0
    while count < oldCount:
        oldDerrick += "#"
        count += 1

    newDerrick = ""
    count = 0
    while count < newCount:
        newDerrick += "#"
        count += 1

    return originLine.replace(oldDerrick, newDerrick)
