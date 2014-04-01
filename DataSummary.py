import DataUtilities

def getSummaryGender(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient. getGender()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Gender Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict

def getSummaryPrior_dx(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getPrior_dx()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Prior_dx Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict

def getSummaryRace(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getRace()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Race Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict

def getSummaryEthnicity(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getEthnicity()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Ethnicity Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict

def getSummaryPathologic_stage(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getPathologic_stage()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Pathologic_stage Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict


def getAllSummary():
	patientList = DataUtilities.getListofPatients()
	getSummaryGender(patientList)
	getSummaryPrior_dx(patientList)
	getSummaryRace(patientList)
	getSummaryEthnicity(patientList)
	getSummaryPathologic_stage(patientList)
	getSummaryClinical_stage(patientList)

getAllSummary()