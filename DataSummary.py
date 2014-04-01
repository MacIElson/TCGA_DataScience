import DataUtilities

def getSummaryGender(patientList=None):
	if patientList is None:
		patientList = DataUtilities.getListofPatients()
	dataDict = {}
	for patient in patientList:
		data = patient. getGender()
		if data in dataDict.keys():
			dataDict[data] += 1
		else:
			dataDict[data] = 1
	print "Gender Breakdown"
	for key, value in dataDict.iteritems():
		print key + ": " + str(value)
	print ""

getSummaryGender()