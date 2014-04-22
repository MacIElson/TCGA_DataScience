import DataUtilities

def getSummaryGender(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getGender()
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

def getSummaryNumber_pack_years_smoked(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getNumber_pack_years_smoked()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Number_pack_years_smoked Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict



def getSummaryTobacco_smoking_history(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getTobacco_smoking_history()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "getTobacco_smoking_history Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict

def getSummaryPrimary_therapy_outcome_success(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getPrimary_therapy_outcome_success()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Primary_therapy_outcome_success Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict

def getSummaryVital_status(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getVital_status()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Vital_status Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""
	return dataDict

def getSummaryYears_to_Birth(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient.getYears_to_birthClean()
		if data == None:
			data = "Unknown"
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Years_to_Birth Breakdown"
	for key, value in dataDict.iteritems():
		print str(key) + ": " + str(value)
	print ""
	return dataDict


def getAllSummary():
	patientList = DataUtilities.getListofPlatPatients()
	getSummaryGender(patientList)
	getSummaryPrior_dx(patientList)
	getSummaryRace(patientList)
	getSummaryEthnicity(patientList)
	getSummaryPathologic_stage(patientList)
	getSummaryNumber_pack_years_smoked(patientList)
	getSummaryTobacco_smoking_history(patientList)
	getSummaryPrimary_therapy_outcome_success(patientList)
	getSummaryVital_status(patientList)
	getSummaryYears_to_Birth(patientList)

getAllSummary()