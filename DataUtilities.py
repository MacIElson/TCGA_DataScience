import glob
import numpy
import os
import csv
import xml.etree.ElementTree as ET
import numpy as np
import random
import mutationDict

class Patient:
	"""A class for a Single Patient"""
	compwt=float
	sei=float
	masei=float
	pasei=float

	def __init__(self, patientRootElement):
		self.patientRootElement = patientRootElement
		self.mutations = []
		self.mutationNames = []

	def addBioSpecimenRootElement(self, biospecimenRootElement):
		self.biospecimenRootElement = biospecimenRootElement

	def getBcr_patient_barcode(self):
		self.caseid = self.patientRootElement.find('luad:patient/shared:bcr_patient_barcode' , namespaces=getPatientXMLNameSpaces()).text
		return self.caseid

	def getPrior_dx(self):
		prior_dx = self.patientRootElement.find('luad:patient/shared:prior_dx' , namespaces=getPatientXMLNameSpaces()).text
		if prior_dx == "Yes, History of Prior Malignancy":
			prior_dx = "Yes"
		return prior_dx

	def getPrior_dxClean(self):
		prior_dx = self.getPrior_dx()
		if prior_dx == "Yes":
			return 1
		elif prior_dx == "No":
			return 0
		else:
			return "Unknown"

	def getPrimary_therapy_outcome_success(self):
		primary_therapy_outcome_success = self.patientRootElement.find('luad:patient/shared:primary_therapy_outcome_success' , namespaces=getPatientXMLNameSpaces())
		if primary_therapy_outcome_success != None:
			return primary_therapy_outcome_success.text
		else:
			return "Unknown"

	def getGender(self):
		return self.patientRootElement.find('luad:patient/shared:gender' , namespaces=getPatientXMLNameSpaces()).text

	def getGenderClean(self):
		gender = self.getGender()
		if gender == "FEMALE":
			return 0
		elif gender == "MALE":
			return 1
		else:
			return "Unknown"

	def getVital_status(self):
		return self.patientRootElement.find('luad:patient/shared:vital_status' , namespaces=getPatientXMLNameSpaces()).text

	def getVital_statusClean(self):
		status = self.getVital_status()
		if status == "Dead":
			return 0
		elif status == "Alive" or status == "LIVING":
			return 1
		else:
			return "Unknown"

	def getDays_to_birth(self):
		return self.patientRootElement.find('luad:patient/shared:days_to_birth' , namespaces=getPatientXMLNameSpaces()).text

	def getYears_to_birthClean(self):
		days = self.getDays_to_birth()
		if days == None:
			return "Unknown"
		else:
			return abs(int(float(days)/365.25))
	def getDays_to_last_known_alive(self):
		return self.patientRootElement.find('luad:patient/shared:days_to_last_known_alive' , namespaces=getPatientXMLNameSpaces()).text

	def getDays_to_death(self):
		return self.patientRootElement.find('luad:patient/shared:days_to_death' , namespaces=getPatientXMLNameSpaces()).text

	def getRace(self):
		return self.patientRootElement.find('luad:patient/shared:race' , namespaces=getPatientXMLNameSpaces()).text

	def getDays_to_initial_pathologic_diagnosis(self):
		return self.patientRootElement.find('luad:patient/shared:days_to_initial_pathologic_diagnosis' , namespaces=getPatientXMLNameSpaces()).text

	def getAge_at_initial_pathologic_diagnosis(self):
		return self.patientRootElement.find('luad:patient/shared:age_at_initial_pathologic_diagnosis' , namespaces=getPatientXMLNameSpaces()).text

	def getYear_of_initial_pathologic_diagnosis(self):
		return self.patientRootElement.find('luad:patient/shared:year_of_initial_pathologic_diagnosis' , namespaces=getPatientXMLNameSpaces()).text

	def getEthnicity(self):
		return self.patientRootElement.find('luad:patient/shared:ethnicity' , namespaces=getPatientXMLNameSpaces()).text

	def getPathologic_stage(self):
		return self.patientRootElement.find('luad:patient/shared_stage:stage_event/shared_stage:pathologic_stage' , namespaces=getPatientXMLNameSpaces()).text

	def getPathologic_stageClean(self):
		stage = self.getPathologic_stage()
		if stage == "Stage IA":
			return 1
		elif stage == "Stage IB":
			return 2
		elif stage == "Stage IIA":
			return 3
		elif stage == "Stage IIB":
			return 4
		elif stage == "Stage IIIA":
			return 5
		elif stage == "Stage IIIB":
			return 6
		elif stage == "Stage IV":
			return 7
		else:
			return "Unknown"

	def getNumber_pack_years_smoked(self):
		return self.patientRootElement.find('luad:patient/shared:number_pack_years_smoked' , namespaces=getPatientXMLNameSpaces()).text

	def getTobacco_smoking_history(self):
		return self.patientRootElement.find('luad:patient/shared:tobacco_smoking_history' , namespaces=getPatientXMLNameSpaces()).text

	def getNumber_pack_years_smokedClean(self):
		packYears = self.getNumber_pack_years_smoked()
		history = self.getTobacco_smoking_history()
		if packYears:
			return int(float(packYears))
		elif history:
			if history == "Lifelong Non-smoker":
				return 0
			elif history == "Current reformed smoker for < or = 15 years":
				return 31 #assume average for a "Current reformed smoker for < or = 15 years"
		return "Unknown"


	def getListofDrugsTaken(self):
		namespaces = getPatientXMLNameSpaces()
		self.drugs = []
		for drugs in self.patientRootElement.findall("luad:patient/rx:drugs", namespaces=namespaces):
			for drug in drugs:
				drugName = drug.find('rx:drug_name' , namespaces=namespaces).text
				if drugName:
					self.drugs.append(getTrueDrugName(drugName.lower()))
		return self.drugs



	def assignVariablesToSelf(self):
		self.caseid = self.getBcr_patient_barcode()
		self.vital_status = self.getVital_statusClean()
		self.gender = self.getGenderClean()
		self.pathologic_stage = self.getPathologic_stageClean()
		self.drugs = self.getListofDrugsTaken()
		self.prior_dx = self.getPrior_dxClean()
		self.years_to_birth  = self.getYears_to_birthClean()
		self.number_pack_years_smoked = self.getNumber_pack_years_smokedClean()
		for mutationName in self.getNonSilentMutationNames():
			setattr(self, mutationName, 1)

	def is_complete(self, attrs):
		"""Checks whether a respondent has all required variables.

		attrs: list of attributes

		Returns: boolean
		"""
		t = [getattr(self, attr) for attr in attrs]
		complete = ('Unknown' not in t and ("carboplatin" in self.drugs or "cisplatin" in self.drugs))
		return complete

	def addMutation(self, mutation):
		self.mutations.append(mutation)

	def getAllMutations(self):
		return mutations

	def getNonSilentMutationNames(self):
		if len(self.mutationNames) > 0:
			return self.mutationNames
		else:
			self.mutationNames = []
			for mutation in self.mutations:
				if not mutation.getIfSilent():
					name = mutation.getName()
					if name not in self.mutationNames:
						self.mutationNames.append(name)
			#print "Number of mutations for patient: " + str(len(self.mutationNames))
		return self.mutationNames

def findPatientFiles(location = os.path.abspath("Data/PatientXML")):
	"takes the location of the clinical xml files"
	"returns a list of the file paths of all the patients"
	files = glob.glob(location + "/*.xml")
	matching = [s for s in files if "_clinical" in s]
	return matching

def getPatientXMLNameSpaces():
	namespaces = {}
	namespaces["luad"] = "http://tcga.nci/bcr/xml/clinical/luad/2.6"
	namespaces["rx"] = "http://tcga.nci/bcr/xml/clinical/pharmaceutical/2.6"
	namespaces["xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
	namespaces["admin"] = "http://tcga.nci/bcr/xml/administration/2.6"
	namespaces["shared"] = "http://tcga.nci/bcr/xml/clinical/shared/2.6"
	namespaces["shared_stage"] = "http://tcga.nci/bcr/xml/clinical/shared/stage/2.6"
	namespaces["lusc_luad_shared"] = "http://tcga.nci/bcr/xml/clinical/shared/lusc_luad/2.6"
	namespaces["luad_nte"] = "http://tcga.nci/bcr/xml/clinical/luad/shared/new_tumor_event/2.6/1.0"
	namespaces["nte"] = "http://tcga.nci/bcr/xml/clinical/shared/new_tumor_event/2.6"
	namespaces["rad"] = "http://tcga.nci/bcr/xml/clinical/radiation/2.6"
	namespaces["cqcf"] = "http://tcga.nci/bcr/xml/clinical/cqcf/2.6"
	namespaces["follow_up_v1.0"] = "http://tcga.nci/bcr/xml/clinical/luad/followup/2.6/1.0"
	return namespaces

def getBiospecimenXMLNameSpaces():
	namespaces = {}
	namespaces["bio"] = "http://tcga.nci/bcr/xml/biospecimen/2.6"
	namespaces["admin"] = "http://tcga.nci/bcr/xml/administration/2.6"
	namespaces["bio_shared"] = "http://tcga.nci/bcr/xml/biospecimen/shared/2.6"
	namespaces["cqcf"] = "http://tcga.nci/bcr/xml/clinical/cqcf/2.6"
	namespaces["shared"] = "http://tcga.nci/bcr/xml/clinical/shared/2.6"
	namespaces["xsi"] = "http://www.w3.org/2001/XMLSchema-instance"

	return namespaces

def getPatientsWithDrugsLocation(location = os.path.abspath("Data/PatientXML")):
	patientsWithDrugsList = []
	for patient in findPatientFiles(location):
		tree = ET.parse(patient)
		rootElement = tree.getroot()

		for drugs in rootElement.findall("luad:patient/rx:drugs", namespaces=getPatientXMLNameSpaces()):
			if len(drugs) != 0:
				patientsWithDrugsList.append(patient)
	return patientsWithDrugsList

def getPatientWithDrugBarcodes():
	barcodeList = []
	for patient in getPatientsWithDrugsXMLTrees():
		barcodeList.append(patient.find('luad:patient/shared:bcr_patient_barcode' , namespaces=getPatientXMLNameSpaces()).text)
	return barcodeList

def getPatientsWithDrugsXMLTrees(location = os.path.abspath("Data/PatientXML")):
	patientsWithDrugsList = []
	for patient in findPatientFiles(location):
		tree = ET.parse(patient)
		rootElement = tree.getroot()

		for drugs in rootElement.findall("luad:patient/rx:drugs", namespaces=getPatientXMLNameSpaces()):
			if len(drugs) != 0:
				patientsWithDrugsList.append(rootElement)
	return patientsWithDrugsList

def getTrueDrugName(drugName):
	if drugName == 'cisplatinum' or drugName == 'cisplastin':
		drugName = 'cisplatin'
	elif drugName == 'carboplatinum':
		drugName = 'carboplatin'
	elif drugName == 'altima' or drugName == 'pemetrexed disodium' or drugName == 'pemethexed' or drugName == 'alimta' or drugName == 'premetrexed':
		drugname = 'pemetrexed'
	elif drugName == 'gemzar':
		drugName = 'gemcitabine'
	elif drugName == 'tarceva (erlotinib)' or drugName == 'tarceva':
		drugName = 'erlotonib'
	elif drugName == 'vinorelbine tartrate' or drugName == 'vinorelbin' or drugName == 'navalbine':
		drugName = 'vinorelbine'
	elif drugName == 'vepesid':
		drugName = 'etoposide'
	elif drugName == 'abraxane' or drugName == 'taxol':
		drugName = 'paclitaxel'
	elif drugName == 'docetoxel/taxotere' or drugName == 'taxotere':
		drugName = 'docetaxel'
	elif drugName == 'chemo, multi-agent, nos':
		drugName = 'chemo, nos'
	elif drugName == 'rec mage 3-as + as15 acs1 / placebo vaccine' or drugName == 'recprame+as15 asci':
		drugName = 'placebo'
	elif drugName == 'avastin':
		drugName = 'bevacizumab'
	return drugName

def getBiospecimenRootElement(patient_barcode):
	location = os.path.abspath("Data/BiospecimenXML")
	bioFiles = glob.glob(location + "/*.xml")
	matching = [s for s in bioFiles if patient_barcode in s]
	tree = ET.parse(matching[0])
	rootElement = tree.getroot()
	return rootElement

def getListOfPatientObjects():
	PatientList = []
	for PatientXML in getPatientsWithDrugsXMLTrees():
		patient = Patient(PatientXML)
		patient.addBioSpecimenRootElement(getBiospecimenRootElement(patient.getBcr_patient_barcode()))
		PatientList.append(patient)
	return PatientList

def getDictionaryOfPatients():
	"""get a dictionary of Patients with their barcodes as keys"""
	patientDict = {}
	patientList = getListOfPatientObjects()
	for patient in patientList:

		patientDict[patient.getBcr_patient_barcode()] = patient
	return patientDict

class Mutation:
	"""A class for a Single Mutation"""
	def __init__(self, mutationRow):
		self.mutationRow = mutationRow

	def getName(self):
		return self.mutationRow[0]

	def getIfSilent(self):
		return self.mutationRow[8].lower() == "silent"

def getDictofMutationNames():
	ifile  = open(os.path.abspath("Data/broad.mit.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.csv"), "rb")
	reader = csv.reader(ifile, delimiter='	')
	patientBarcodeList = getPatientWithDrugBarcodes()
	mutationDict = {}
	for row in reader:
		if row[15][0:12] in patientBarcodeList:
			mutation = Mutation(row)
			name = mutation.getName()
			if name in mutationDict.keys():
				mutationDict[name] += 1
			else:
				mutationDict[name] = 1
	valueDict = {}
	for value in mutationDict.values():
		if value in valueDict.keys():
			valueDict[value] += 1
		else:
			valueDict[value] = 1
	print valueDict

def getDictofMutationNamesImproved():
	patientDict = getDictReadofPatients()
	num = 0
	mutationDict = {}
	for patient in patientDict.values():
		mutationNames = patient.getNonSilentMutationNames()
		for name in mutationNames:
			if name in mutationDict.keys():
				mutationDict[name] += 1
			else:
				mutationDict[name] = 1
		num += 1
	valueDict = {}
	for key, value in mutationDict.items():
		if value in valueDict.keys():
			valueDict[value] += 1
		else:
			valueDict[value] = 1
	print "number of mution names: "+ str(len(mutationDict.values()))
	print "Dictionary of mutation counts: " + str(mutationDict)
	print "valueDict: " + str(valueDict)

def getMutationsOccuringGreaterThan(num,patientDict):
	mutationDict = {}
	for patient in patientDict.values():
		mutationNames = patient.getNonSilentMutationNames()
		for name in mutationNames:
			if name in mutationDict.keys():
				mutationDict[name] += 1
			else:
				mutationDict[name] = 1
	mutationsMatter = []
	for key, value in mutationDict.items():
		if value>num:
			mutationsMatter.append(key)
	return mutationsMatter

def getMutationOccuringDict():
	patientDict = getDictReadofPatientsFilled()
	mutationDictofLists = {}
	for num in range(1,63):
		mutationDictofLists[num] = getMutationsOccuringGreaterThan(num,patientDict)
	return mutationDictofLists

def getListofMutations():
	"""get a List of Mutations for patients that have drug data"""
	ifile  = open(os.path.abspath("Data/broad.mit.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.csv"), "rb")
	reader = csv.reader(ifile, delimiter='	')
	patientBarcodeList = getPatientWithDrugBarcodes()
	mutationList = []
	for row in reader:
		if row[15][0:12] in patientBarcodeList:
			mutation = Mutation(row)
			mutationList.append(mutation)

def getListofPatients():
	"""returns a list of Patients that have drug information, their patient xml tree, biospecimen xml tree and a list of mutations"""
	ifile  = open(os.path.abspath("Data/broad.mit.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.csv"), "rb")
	reader = csv.reader(ifile, delimiter='	')
	patientBarcodeList = getPatientWithDrugBarcodes()
	patientDict = getDictionaryOfPatients()
	mutationList = []
	for row in reader:
		if row[15][0:12] in patientBarcodeList:
			mutation = Mutation(row)
			patientDict[row[15][0:12]].addMutation(mutation)
	return patientDict.values()

def getListofPlatPatients():
	"""returns a list of Patients that have drug information, their patient xml tree, biospecimen xml tree and a list of mutations"""
	ifile  = open(os.path.abspath("Data/broad.mit.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.csv"), "rb")
	reader = csv.reader(ifile, delimiter='	')
	patientBarcodeList = getPatientWithDrugBarcodes()
	patientDict = getDictionaryOfPatients()
	for key, patient in patientDict.items():
		drugs = patient.getListofDrugsTaken()
		if "cisplatin" not in drugs and "carboplatin" not in drugs:
			patientDict.pop(key, None)
			if key in patientBarcodeList: patientBarcodeList.remove(key)
	mutationList = []
	for row in reader:
		if row[15][0:12] in patientBarcodeList:
			mutation = Mutation(row)
			patientDict[row[15][0:12]].addMutation(mutation)
	return patientDict.values()

def getDictReadofPatients():
	"""returns a dict of Patients that have drug information, their patient xml tree, biospecimen xml tree and a list of mutations"""
	ifile  = open(os.path.abspath("Data/broad.mit.edu__Illumina_Genome_Analyzer_DNA_Sequencing_level2.csv"), "rb")
	reader = csv.reader(ifile, delimiter='	')
	patientBarcodeList = getPatientWithDrugBarcodes()
	patientDict = getDictionaryOfPatients()
	mutationList = []
	count = 0
	for row in reader:
		if row[15][0:12] in patientBarcodeList:
			count += 1
			mutation = Mutation(row)
			patientDict[row[15][0:12]].addMutation(mutation)
	#print "count: " + str(count)
	return patientDict

def getDictReadofPatientsFilled(patientDict = -1):
	if patientDict == -1:
		patientDict = getDictReadofPatients()
	dep, control = get_version()
	knownVariableDict = {}
	for attribute in control:
		knownVariableDict[attribute] = []
	for patient in patientDict.values():
		patient.assignVariablesToSelf()
		for attribute in control:
			try:
				attr = getattr(patient, attribute)
				if attr != "Unknown":
					knownVariableDict[attribute].append(attr)
			except AttributeError:
				setattr(patient, attribute, 0)
	for patient in patientDict.values():
		for attribute in control:
			attr = getattr(patient, attribute)
			if attr == "Unknown":
				ran = random.choice(knownVariableDict[attribute])
				setattr(patient, attribute, ran)
	#print knownVariableDict["years_to_birth"]
	return patientDict

def get_versionNUmberofMutations(version=(1,-1)):
		mut = mutationDict.getMutationsGreaterThan(version[0])
		return len(mut)

def get_version(version=(1,-1)):
	"""Gets the variables for different versions of the model.

	version: int

	Returns: string, list of strings
	"""
	print "version: " + str(version)
	dep = 'vital_status'

	control = ['pathologic_stage', 'gender','prior_dx', 'years_to_birth', 'number_pack_years_smoked']
	if version[1] == -1:
		mut = mutationDict.getMutationsGreaterThan(version[0])
	else:
		mut = [mutationDict.getMutationsGreaterThan(version[0])[version[1]]]
		#print mut
	control += mut
	#print control
	#return ('vital_status', ['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'PCDHGC5'])
	return dep, control


def getDataForScikit():
	DESCR = ["Gender","Stage"]
	patientDict = getDictReadofPatients()
	data = []
	target= []
	for patient in patientDict.values():
		gender = patient.getGenderClean()
		stage = patient.getPathologic_stageClean()
		pdata = [gender, stage]
		ptarget = patient.getVital_statusClean()
		data.append(pdata)
		target.append(ptarget)
	return {"data": np.array(data), "target":np.array(target)}

#getDictofMutationNamesImproved()
#print getMutationOccuringDict()