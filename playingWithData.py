import glob
import xml.etree.ElementTree as ET
import thinkplot
import DataUtilities
import numpy

matching = DataUtilities.findPatientFiles()
namespaces = DataUtilities.getPatientXMLNameSpaces()

drugList = {}
patientsWithDrugs = 0
drugsPerPatient = []

patientWithPlat = 0

"getDataOverview"
for patient in matching:
	tree = ET.parse(patient)
	rootElement = tree.getroot()
	plat = False
	for drugs in rootElement.findall("luad:patient/rx:drugs", namespaces=namespaces):
		if len(drugs) != 0:
			drugsPerPatient.append(len(drugs))
			patientsWithDrugs += 1
			for drug in drugs:
				drugName = drug.find('rx:drug_name' , namespaces=namespaces).text
				if drugName:
					drugName = DataUtilities.getTrueDrugName(drugName.lower())
					# I think this is where FixingErrors.py should go.
					if drugName.lower() == "cisplatin" or drugName.lower() == "carboplatin":
						plat = True
					print (drugName)
					if drugName.lower() in  drugList:
						drugList[drugName.lower()] += 1
					else:
						drugList[drugName.lower()] = 1
			#print (drug.tag, drug.attrib)
	if plat:
		patientWithPlat += 1
print drugList
print patientWithPlat

# print patientsWithDrugs
# print sum(drugList.itervalues())
# drugsPerPatientHist = thinkstats2.MakeHistFromList(drugsPerPatient)
# thinkplot.Hist(drugsPerPatientHist)
# thinkplot.Save(root='Distribution_of_Drugs_per_Patient',
# 			title='Distribution of Drugs per Patient',
#           xlabel='Number of Drugs taken',
#            ylabel='NUmber of Patients')
# thinkplot.Show(title='Distribution of Drugs per Patient',
#         	xlabel='Number of Drugs taken', 
#         	ylabel='NUmber of Patients')

patientsWithDrugs = DataUtilities.getPatientsWithDrugsLocation(location = "/home/apatterson1/Desktop/XML")

# "Death Distribution"
# c=0
# noFollowUps = 0
# daysToDeathList = []
# "days to death"
# for patient in patientsWithDrugs:
# 	tree = ET.parse(patient)
# 	rootElement = tree.getroot()

# 	patientDaysToDeathListStr = []
# 	for follow_ups in rootElement.findall("luad:patient/luad:follow_ups", namespaces=namespaces):
# 		if len(follow_ups) == 0:
# 			noFollowUps += 1
# 		for follow_up in follow_ups:
# 			daysToDeath = follow_up.find("shared:days_to_death", namespaces=namespaces).text
# 			if daysToDeath is not None:
# 				c += 1
# 				patientDaysToDeathListStr.append(daysToDeath)
# 				break
# 	print(patientDaysToDeathListStr)
# 	if len(patientDaysToDeathListStr) != 0:
# 		averageDaysToDeath = numpy.mean(map(int, patientDaysToDeathListStr))
# 		daysToDeathList.append(averageDaysToDeath)
# print "noFollowUps", noFollowUps
# print "DaysToDeath", len(daysToDeathList)
# Binned_Data = DataUtilities.roundToYear(daysToDeathList)
# DaysToDeathHist = thinkstats2.MakeHistFromList(Binned_Data)
# thinkplot.Hist(DaysToDeathHist)
# thinkplot.Save(root='Distribution_of_Days_to_Death',
# 			title='Distribution of Days to Death',
#         	xlabel='Years to Death',
#         	ylabel='Patient Count')
# thinkplot.Show(title='Distribution of Days to Death',
#         	xlabel='Years to Death',
#         	ylabel='Patient Count')
# VitalStatusList = {}
# for patient in patientsWithDrugs:
# 	tree = ET.parse(patient)
# 	rootElement = tree.getroot()
# 	vitalStatus = rootElement.find("luad:patient/shared:vital_status",namespaces=namespaces).text
# 	if vitalStatus:
# 		if vitalStatus.lower() in  VitalStatusList:
# 			VitalStatusList[vitalStatus.lower()] += 1
# 		else:
# 			VitalStatusList[vitalStatus.lower()] = 1
# print VitalStatusList
# thinkplot.Hist(VitalStatusHist)

vital_status ['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'MUC16']

['PCDHGC5']
['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'PCDHGC5']
['PCDHGC5']
['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'PCDHGC5']
('vital_status', ['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'PCDHGC5'])

['PCDHAC2']
['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'PCDHAC2']
['PCDHAC2']
['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'PCDHAC2']
('vital_status', ['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'PCDHAC2'])

['CSMD3']
['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'CSMD3']
['CSMD3']
['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'CSMD3']
('vital_status', ['pathologic_stage', 'gender', 'prior_dx', 'years_to_birth', 'number_pack_years_smoked', 'CSMD3'])