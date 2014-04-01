import glob
import numpy
import os
import csv
import xml.etree.ElementTree as ET

class Patient:
    """A class for a Single Patient"""
    mutations = []

    def __init__(self, patientRootElement):
        self.patientRootElement = patientRootElement

    def addBioSpecimenRootElement(self, biospecimenRootElement):
    	self.biospecimenRootElement = biospecimenRootElement

    def getbcr_patient_barcode(self):
    	return self.patientRootElement.find('luad:patient/shared:bcr_patient_barcode' , namespaces=getPatientXMLNameSpaces()).text

    def getGender(self):
    	return self.patientRootElement.find('luad:patient/shared:gender' , namespaces=getPatientXMLNameSpaces()).text

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
		patient.addBioSpecimenRootElement(getBiospecimenRootElement(patient.getbcr_patient_barcode()))
		PatientList.append(patient)
	return PatientList

def getDictionaryOfPatients():
	"""get a dictionary of Patients with their barcodes as keys"""
	patientDict = {}
	patientList = getListOfPatientObjects()
	for patient in patientList:
		patientDict[patient.getbcr_patient_barcode()] = patient
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