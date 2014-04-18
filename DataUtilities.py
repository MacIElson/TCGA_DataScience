import glob
import numpy
import os
import csv
import xml.etree.ElementTree as ET
import numpy as np

class Patient:
	"""A class for a Single Patient"""
	mutations = []
	compwt=float
	sei=float
	masei=float
	pasei=float

	def __init__(self, patientRootElement):
		self.patientRootElement = patientRootElement

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

def findPatientFiles(location = os.path.abspath("Data/PatientXML")):
	"takes the location of the clinical xml files"
	"returns a list of the file paths of all the patients"
	print location
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
		patient.assignVariablesToSelf()
		patientDict[patient.getBcr_patient_barcode()] = patient
	return patientDict

class Mutation:
	"""A class for a Single Mutation"""
	def __init__(self, mutationRow):
		self.mutationRow = mutationRow

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
			print "hello"
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
	for row in reader:
		if row[15][0:12] in patientBarcodeList:
			mutation = Mutation(row)
			patientDict[row[15][0:12]].addMutation(mutation)
	return patientDict

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
