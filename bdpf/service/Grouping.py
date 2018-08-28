#-*- coding:utf-8 -*-
from TableInfo import TableInfo
def GenGroup(requirements):
    listMatch=list()
    listUnmatch=list()
    listMaybe=list()
    for x in requirements:
      if x.result==1 :
         listMatch.append(x)
      elif x.result==2 :
         listUnmatch.append(x)
      else:
         listMaybe.append(x)
    return (listMatch,listUnmatch,listMaybe)

