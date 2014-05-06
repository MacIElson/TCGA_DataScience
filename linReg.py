import random
import glm
import re
import thinkstats2
import thinkplot
import math
import numpy as np
import matplotlib.pyplot as pyplot
import random
from DataUtilities import *


def ageAndVitalCorrelation():
    ageL = []
    vitalL = []
    patientDict = getDictReadofPatientsFilled()
    for patient in patientDict.values():
        patient.assignVariablesToSelf()
        age = patient.years_to_birth
        vital = patient.vital_status
        if age != "Unknown" and vital != "Unknown":
            ageL.append(age)
            vitalL.append(vital)
    runReg(ageL, vitalL)

def runReg(xs,ys):
    print 'mean, var of x', thinkstats2.MeanVar(xs)
    print 'mean, var of y', thinkstats2.MeanVar(ys)
    print 'Pearson corr', thinkstats2.Corr(xs, ys)

    inter, slope = thinkstats2.LeastSquares(xs, ys)
    print 'inter', inter
    print 'slope', slope
    
    fxs, fys = thinkstats2.FitLine(xs, inter, slope)
    res = thinkstats2.Residuals(xs, ys, inter, slope)
    R2 = thinkstats2.CoefDetermination(ys, res)
    print 'R2', R2

    thinkplot.Plot(fxs, fys, color='gray', alpha=0.2)
    thinkplot.Scatter(xs, ys)
    thinkplot.Show()

ageAndVitalCorrelation()