import glm
import re
import thinkstats2
import thinkplot
import math
import numpy as np
import matplotlib.pyplot as pyplot
import random
import itertools

import mutationDict
import DataUtilities
import TCGAlogReg

def errorMissing():
	means = {}
	version  = (30,-1)
	cumDict = {}

	patientDict = DataUtilities.getDictReadofPatients()

	for i in range(100):
		patients = DataUtilities.getDictReadofPatientsFilled(patientDict = patientDict)
		regs = TCGAlogReg.test_models(version = version, patients = patients, printReg = False)
		for reg in regs.regs:
			cumulative_odds = reg.report_odds(means, printCum = False)
			for name, odds, p in cumulative_odds:
				if name in cumDict.keys():
					cumDict[name].append(odds)
				else:
					cumDict[name] = [odds]


	print "ErrorMissing"
	#create table
	print r"\begin{table}[h]"
	print r"\begin{tabular}{|l|l|l|}"
	print r"\hline"
	print r"\textbf{Type} & \textbf{Odds} & \textbf{Confidence Interval}\\ \hline"

	namesL = []
	averagesL = []
	lowersL = []
	uppersL = []
	for key, oddsList in sorted(cumDict.items(), key=lambda e: sum(e[1])):
		if key not in mutationDict.getMutationsGreaterThan(1):
			average = sum(oddsList) / float(len(oddsList))
			lower = getLowerConfidence(oddsList)
			upper= getUpperConfidence(oddsList)
			print key  + " & "  "{:.3f}".format(average) + " & (" + "{:.3f}".format(lower)  + ", "  "{:.3f}".format(upper) + r")\\ \hline"
			namesL.append(key)
			averagesL.append(average)
			lowersL.append(lower)
			uppersL.append(upper)
	print "\end{tabular}"
	print "\end{table}"

	plotRegMult(namesL, averagesL, lowersL, uppersL, "Life Factor Log Odds With Sampling Error","Factor", "Log Odds")

	print ""
	print r"\begin{table}[h]"
	print r"\begin{tabular}{|l|l|l|}"
	print r"\hline"
	print r"\textbf{Type} & \textbf{Odds} & \textbf{Confidence Interval}\\ \hline"

	namesM = []
	averagesM = []
	lowersM = []
	uppersM = []
	for key, oddsList in sorted(cumDict.items(), key=lambda e: sum(e[1])):
		if key in mutationDict.getMutationsGreaterThan(1):
			average = sum(oddsList) / float(len(oddsList))
			lower = getLowerConfidence(oddsList)
			upper= getUpperConfidence(oddsList)
			print key  + " & "  "{:.3f}".format(average) + " & (" + "{:.3f}".format(lower)  + ", "  "{:.3f}".format(upper) + r")\\ \hline"
			namesM.append(key)
			averagesM.append(average)
			lowersM.append(lower)
			uppersM.append(upper)
	print "\end{tabular}"
	print "\caption{The above table shows the effect each mutation has when tested independently the other mutations. The confidence intervals are shown for the error due to missing data.}"
	print "\end{table}"
	plotRegMult(namesM, averagesM, lowersM, uppersM, "Mutation Log Odds With Sampling Error","Mutation", "Log Odds")
	plotRegMult(namesL + namesM, averagesL + averagesM, lowersL + lowersM, uppersL + uppersM, "Log Odds With Sampling Error","Factor", "Log Odds")


def errorTotal():
	means = {}
	version  = (30,-1)
	cumDict = {}

	patientDict = DataUtilities.getDictReadofPatients()

	for i in range(100):
		patients = DataUtilities.getDictReadofPatientsFilled(patientDict = patientDict)
		#resample
		sPatients = sample_wr(patients, 91)

		regs = TCGAlogReg.test_models(version = version, patients = sPatients, printReg = False)
		for reg in regs.regs:
			cumulative_odds = reg.report_odds(means, printCum = False)
			for name, odds, p in cumulative_odds:
				if name in cumDict.keys():
					cumDict[name].append(odds)
				else:
					cumDict[name] = [odds]


	print "ErrorTotal"
	#create table
	print r"\begin{table}[h]"
	print r"\begin{tabular}{|l|l|l|l|}"
	print r"\hline"
	print r"\textbf{Type} & \textbf{Odds} & \textbf{Odds Lower} & \textbf{Odds Upper}\\ \hline"

	for key, oddsList in sorted(cumDict.items(), key=lambda e: sum(e[1])):
		if key not in mutationDict.getMutationsGreaterThan(1):
			average = sum(oddsList) / float(len(oddsList))
			lower = getLowerConfidence(oddsList)
			upper= getUpperLowerConfidence(oddsList)
			print key  + " & "  "{:.3f}".format(average) + " & " + "{:.3f}".format(lower)  + " & "  "{:.3f}".format(upper) + r"\\ \hline"

	print "\end{tabular}"
	print "\end{table}"

	print ""
	print r"\begin{table}[h]"
	print r"\begin{tabular}{|l|l|l|l|}"
	print r"\hline"
	print r"\textbf{Type} & \textbf{Odds} & \textbf{Odds Lower} & \textbf{Odds Upper}\\ \hline"

	names = []
	averages = []
	lowers = []
	uppers = []
	for key, oddsList in sorted(cumDict.items(), key=lambda e: sum(e[1])):
		if key in mutationDict.getMutationsGreaterThan(1):
			average = sum(oddsList) / float(len(oddsList))
			lower = getLowerConfidence(oddsList)
			upper= getUpperConfidence(oddsList)
			print key  + " & "  "{:.3f}".format(average) + " & (" + "{:.3f}".format(lower)  + ", "  "{:.3f}".format(upper) + r")\\ \hline"
			names.append(key)
			averages.append(average)
			lowers.append(lower)
			uppers.append(upper)
	
	print "\end{tabular}"
	print "\caption{The above table shows the effect each mutation has when tested in conjunction with the other mutations}"
	print "\end{table}"
	plotRegMult(names, averages, lowers, uppers, "Mutation Log Odds With Total Error","Mutations", "Log Odds")

def sample_wr(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    iList = population.items()
    fList = []
    for i in range(k):
    	ran = random.choice(iList)
    	ran1 = (ran[0] + str(i), ran[1])
    	fList.append(ran1)
    return dict(fList)

def getLowerConfidence(numList):
	sList = sorted(numList)
	return sList[int(round((len(sList)*.05)))]

def getUpperConfidence(numList):
	sList = sorted(numList, reverse=True)
	return sList[int(round(len(sList)*.05))]

def errorTotalInd():
	means = {}
	version1  = 30

	numMut = DataUtilities.get_versionNUmberofMutations((version1,-1))
	print numMut
	cumDict = {}

	patientDict = DataUtilities.getDictReadofPatients()

	for i in range(100):
		patients = DataUtilities.getDictReadofPatientsFilled(patientDict = patientDict)
		#resample
		sPatients = sample_wr(patients, 91)
		for j in range(numMut-1):
			print (version1,j)
			regs = TCGAlogReg.test_models(version = (version1,j), patients = sPatients, printReg = True)
			for reg in regs.regs:
				cumulative_odds = reg.report_odds(means, printCum = False)
				for name, odds, p in cumulative_odds:
					if name in cumDict.keys():
						cumDict[name].append(odds)
					else:
						cumDict[name] = [odds]


	print "ErrorTotalInd"
	#create table
	print r"\begin{table}[h]"
	print r"\begin{tabular}{|l|l|l|l|}"
	print r"\hline"
	print r"\textbf{Type} & \textbf{Odds} & \textbf{Odds Lower} & \textbf{Odds Upper}\\ \hline"

	for key, oddsList in sorted(cumDict.items(), key=lambda e: sum(e[1])):
		if key not in mutationDict.getMutationsGreaterThan(1):
			average = sum(oddsList) / float(len(oddsList))
			lower = getLowerConfidence(oddsList)
			upper= getUpperLowerConfidence(oddsList)
			print key  + " & "  "{:.3f}".format(average) + " & " + "{:.3f}".format(lower)  + " & "  "{:.3f}".format(upper) + r"\\ \hline"

	print "\end{tabular}"
	print "\end{table}"

	print ""
	print r"\begin{table}[h]"
	print r"\begin{tabular}{|l|l|l|l|}"
	print r"\hline"
	print r"\textbf{Type} & \textbf{Odds} & \textbf{Odds Lower} & \textbf{Odds Upper}\\ \hline"

	names = []
	averages = []
	lowers = []
	uppers = []
	for key, oddsList in sorted(cumDict.items(), key=lambda e: sum(e[1])):
		if key in mutationDict.getMutationsGreaterThan(1):
			average = sum(oddsList) / float(len(oddsList))
			lower = getLowerConfidence(oddsList)
			upper= getUpperConfidence(oddsList)
			print key  + " & "  "{:.3f}".format(average) + " & (" + "{:.3f}".format(lower)  + ", "  "{:.3f}".format(upper) + r")\\ \hline"
			names.append(key)
			averages.append(average)
			lowers.append(lower)
			uppers.append(upper)

	print "\end{tabular}"
	print "\caption{The above table shows the effect each mutation has when tested independently the other mutations}"
	print "\end{table}"

	plotRegMult(names, averages, lowers, uppers, "Mutation Log Odds With Independent Computation and Total Error","Mutations", "Log Odds")


def plotRegMult(names, averageValues, lowerLimit, upperLimit, title, xlabel, ylabel):
	pyplot.figure()
	averageValues = np.log(np.array(averageValues))
	upperLimit = np.log(np.array(upperLimit))
	lowerLimit = np.log(np.array(lowerLimit))

	ytop = upperLimit-averageValues
	ybot = averageValues-lowerLimit
	pyplot.errorbar( range(len(names)), averageValues, yerr=(ybot, ytop), marker='o', linestyle = 'None' )
	pyplot.xticks(range(len(names)), names, size='small')
	pyplot.axhline(y=0, linestyle = '--',color = "r" )
	#pyplot.autofmt_xdate()
	pyplot.setp(pyplot.xticks()[1], rotation=30)
	pyplot.xlim([-1,len(names)])
	pyplot.title(title)
	pyplot.xlabel(xlabel)
	pyplot.ylabel(ylabel)
	pyplot.tight_layout()
	pyplot.show()

#errorTotalInd()
#print sample_wr({"A":1, "B":2, "C":3, "D":4, "E":5, "F":6}, 9)
errorMissing()
