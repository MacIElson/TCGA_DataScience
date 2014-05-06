import random
import glm
import re
import thinkstats2
import thinkplot
import math
import numpy as np
import matplotlib.pyplot as pyplot

import DataUtilities

def run_regression_and_print(survey, version, means):
	"""Runs a logistic regression and prints results

	survey: Survey
	version: which model to run
	means: map from variables to nominal values
	"""
	print 'Version', version
	print 'N', survey.len()
	regs = run_regression(survey, version)
	regs.print_regression_reports(means)
	regs.summarize(means)
	return regs

def run_regression(survey, version):
	"""Runs logistic regressions.

	survey: Survey
	version: which model to run

	Returns: Regressions object
	"""
	dep, control = DataUtilities.get_version(version)

	print dep, control
	reg = survey.make_logistic_regression(dep, control)
	#print reg
	return Regressions([reg])



def read_complete(version,patients):
	survey = read_survey(patients)

	# give respondents random values
	#[r.clean_random() for r in survey.respondents()]

	# select complete records
	dep, control = DataUtilities.get_version(version)
	#for var in [dep] + control:
	#	print r'\verb"%s",' % var

	attrs = [dep] + control
	complete = survey.subsample(lambda r: r.is_complete(attrs))

	return survey, complete

class Survey(object):
	"""Represents a set of respondents as a map from caseid to Respondent."""

	def __init__(self, rs=None):
		if rs is None:
			self.rs = {}
		else:
			self.rs = rs
		self.cdf = None

	def add_respondent(self, r):
		"""Adds a respondent to this survey."""
		self.rs[r.caseid] = r

	def add_respondents(self, rs):
		"""Adds respondents to this survey."""
		[self.add_respondent(r) for r in rs]

	def len(self):
		"""Number of respondents."""
		return len(self.rs)

	def respondents(self):
		"""Returns an iterator over the respondents."""
		return self.rs.itervalues()

	def lookup(self, caseid):
		"""Looks up a caseid and returns the Respondent object."""
		return self.rs[caseid]

	def loadPatients(self, patients):
		self.rs = patients

	def subsample(self, filter_func):
		"""Form a new cohort by filtering respondents

		filter_func: function that takes a respondent and returns boolean

		Returns: Survey
		"""
		pairs = [(r.caseid, r) for r in self.respondents() if filter_func(r)]
		rs = dict(pairs)
		return Survey(rs)

	def make_logistic_regression(self, dep, control, exp_vars=[]):
		"""Runs a logistic regression.

		dep: string dependent variable name
		control: list of string control variables
		exp_vars: list of string independent variable names

		Returns: LogRegression object
		"""
		s = ' + '.join(control + exp_vars)
		model = '%s ~ %s' % (dep, s)

		reg = self.logistic_regression(model)

		null_model = make_null_model(self, dep)
		reg.null_sip = self.self_information_partition(dep, null_model)

		reg.model_sip = self.self_information_partition(dep, reg)
		reg.sip = reg.null_sip - reg.model_sip

		#print reg.null_sip, reg.model_sip, reg.sip

		return reg
	def logistic_regression(self, model, print_flag=False):
		"""Performs a regression.

		model: string model in r format
		print_flag: boolean, whether to print results

		Returns: LogRegression object
		"""
		def clean(attr):
			m = re.match('as.factor\((.*)\)', attr)
			if m:
				return m.group(1)
			return attr
				
		# pull out the attributes in the model
		rows = []
		t = model.split()
		attrs = [clean(attr) for attr in model.split() if len(attr)>1]

		for r in self.respondents():
			row = [getattr(r, attr) for attr in attrs]
			rows.append(row)

		rows = [row for row in rows if 'NA' not in row]

		# inject the data and runs the model
		col_dict = dict(zip(attrs, zip(*rows)))
		glm.inject_col_dict(col_dict)

		res = glm.logit_model(model, print_flag=print_flag)

		return LogRegression(res)

	def make_pmf(self, attr, na_flag=False):
		"""Make a PMF for an attribute.  Uses compwt to weight respondents.

		attr: string attr name
		na_flag: boolean, whether to remove NAs

		Returns: normalized PMF
		"""
		pmf = thinkstats2.Pmf()
		for r in self.respondents():
			val = getattr(r, attr)
			wt = 1 #r.compwt
			pmf.Incr(val, wt)

		if na_flag:
			pmf.Set('NA', 0)

		pmf.Normalize()
		return pmf

	def self_information_partition(self, attr, model):
		"""Computes the self information of a partition.

		Does not take into account compwt

		attr: string binary attribute
		model: object with a fit_prob method that takes a respondent

		Returns: float number of bits
		"""
		def log2(x, denom=math.log(2)):
			return math.log(x) / denom

		total = 0.0
		n = 0.0
		for r in self.respondents():
			x = getattr(r, attr)
			if x == 'NA':
				# if we don't know the answer, we got zero bits of info
				continue

			p = model.fit_prob(r)
			assert p != 'NA'

			if x == 1:
				total += -log2(p)
			elif x == 0:
				total += -log2(1-p)
			else:
				raise ValueError('Values must be 0, 1 or NA')

		return total

def fraction_one(pmf):
	yes, no = pmf.Prob(1), pmf.Prob(0)
	return float(yes) / (yes+no)

def cumulative_odds(estimates, means):
    """Computes cumulative odds based on a sequence of estimates.

    Iterates the attributes and computes the odds ratio, for
    the given value, and the probability that corresponds to
    the cumulative odds.

    estimates: list of (name, est, error, z)
    means: map from attribute to value

    Returns: list of (name, odds, p)
    """
    total_odds = 1.0
    res = []

    for name, est, _, _ in estimates:
        mean = means.get(name, 1)
        odds = math.exp(est * mean)
        total_odds *= odds
        p = 100 * total_odds / (1 + total_odds)
        res.append((name, odds, p))

    return res
def print_cumulative_odds(cumulative_odds):
    """Prints a summary of the estimated parameters.

    cumulative_odds: list of (name, odds, p)
    """
    print '\t\todds\tcumulative'
    print '\t\tratio\tprobability\tdiff'
    prev = None

    for name, odds, p in cumulative_odds:
        if prev:
            diff = p - prev
            print '%11s\t%0.2g\t%0.2g\t%0.2g' % (name, odds, p, diff)
        else:
            print '%11s\t%0.2g\t%0.2g' % (name, odds, p)
        prev = p

def compute_ci(col):
    """Computes a 95% confidence interval.

    col: sequence of values

    Returns: CI tuple, p-value
    """
    n = len(col)
    index = n / 40
    mid = n / 2

    t = list(col)
    t.sort()
    median = t[mid]
    
    pval = compute_pvalue(median, t)

    low, high = t[index], t[-index-1]
    ci = np.array([median, low, high])

    return ci, pval


def compute_pvalue(median, t):
    """Computes the p-value for a list of outcomes.

    Counts the fraction of outcomes with the opposite sign from the median
    (or 0).

    median: median value from the list
    t: list of outcomes

    Returns: float prob
    """
    if median > 0:
        opp = [x for x in t if x <= 0]
    else:
        opp = [x for x in t if x >= 0]

    fraction = float(len(opp)) / len(t)
    return fraction

class LogRegression(object):
	def __init__(self, res):
		"""Makes a LogRegression object

		res: result object from rpy2
		estimates: list of (name, est, error, z)
		"""
		self.res = res
		self.estimates, self.aic = glm.get_coeffs(res)

	def fit_prob(self, r):
		"""Computes the fitted probability for the given respondent.

		r: Respondent

		Returns: float prob
		"""
		log_odds = 0
		for name, est, error, z in self.estimates:
			if name == '(Intercept)':
				log_odds += est
			else:
				x = getattr(r, name)
				if x == 'NA':
					print name
					return 'NA'
				log_odds += est * x

		odds = math.exp(log_odds)
		p = odds / (1 + odds)
		return p

	def validate(self, respondents, attr):
		for r in respondents:
			dv = getattr(r, attr)
			p = self.fit_prob(r)
			#print r.caseid, dv, p

	def report(self):
		"""Prints a summary of the glm results."""
		if self.res is None:
			print 'No summary'
		glm.print_summary(self.res)

	def report_odds(self, means, printCum = True):
		"""Prints a summary of the estimated parameters.

		Iterates the attributes and computes the odds ratio, for
		the given value, and the probability that corresponds to
		the cumulative odds.

		means: map from attribute to value
		"""
		cumulative = cumulative_odds(self.estimates, means)
		if printCum:
			print_cumulative_odds(cumulative)
		return cumulative

	def make_pickleable(self):
		self.res = None

def make_null_model(survey, attr):
	"""Computes the self information of an attribute.

	Total surprisal of the attr if we knew nothing about the respondents.

	survey: Survey
	attr: string attribute name
	"""
	pmf = survey.make_pmf(attr)
	p = fraction_one(pmf)
	model = NullModel(p)
	return model

class NullModel(object):
	def __init__(self, p):
		"""Make a NullModel.

		p: probability that a respondent has some property
		"""
		self.p = p

	def fit_prob(self, r):
		"""Computes the fitted probability for the given respondent.

		r: Respondent

		Returns: float prob
		"""
		return self.p

class Regressions(object):
	def __init__(self, regs):
		self.regs = regs
		reg = regs[0]
		self.names = [name for name, _, _, _ in reg.estimates]
		
	def get(self, i):
		return self.regs[i]

	def print_regression_reports(self, means):
		for reg in self.regs:
			reg.report()
			reg.report_odds(means)
			print 'AIC', reg.aic
			print 'SIP', reg.sip


	def median_model(self):
		rows = []

		# for each regression, make a list of estimates
		for reg in self.regs:
			row = [est for name, est, _, _ in reg.estimates]
			rows.append(row)

		# cols is one column per variable
		cols = zip(*rows)

		# compute cis for the estimates
		medians = []
		for col in cols:
			ci, pval = compute_ci(col)
			median, low, high = ci
			medians.append(median)

		for name, median in zip(self.names, medians):
			print name, median

	def summarize(self, means):
		self.summarize_estimates(means)
		self.summarize_cumulatives(means)
		self.summarize_information()
		
	def summarize_estimates(self, means):
		"""Generate summary statistics for a set of regressions.

		regs: list of LogRegression
		means: map from variable to reference value
		"""
		rows = []

		# for each regression, make a list of estimates
		for reg in self.regs:
			row = [est * means.get(name, 1) 
				   for name, est, _, _ in reg.estimates]
			rows.append(row)

		# cols is one column per variable
		cols = zip(*rows)

		# compute cis for the estimates
		cis = []
		pvals = []
		for col in cols:
			ci, pval = compute_ci(col)
			cis.append(ci)
			pvals.append(pval)

		self.estimate_cis = cis
		self.pvals = pvals

	def summarize_cumulatives(self, means):
		"""Generate summary statistics for a set of regressions.

		means: map from variable to reference value
		"""
		rows = []

		for reg in self.regs:
			cumulative = cumulative_odds(reg.estimates, means)
			rows.append([p for _, _, p in cumulative])

		# compute cis for the cumulative probabilities
		cols = zip(*rows)
		cis = []
		for col in cols:
			ci, pval = compute_ci(col)
			cis.append(ci)

		self.cumulative_cis = cis

	def summarize_information(self):
		"""Generate summary statistics for a set of regressions.

		regs: list of LogRegression
		means: map from variable to reference value
		"""
		self.aics = [reg.aic for reg in self.regs]
		self.sips = [reg.sip for reg in self.regs]

	def print_table(self):
		"""Prints the table in human-readable form."""

		data = zip(self.names, 
				   self.estimate_cis, 
				   self.pvals,
				   self.cumulative_cis)

		for name, ci, pval, cumulative in data:
			odds_ci = np.exp(ci)
			print '%15.15s  \t' % name,
			print format_range(odds_ci), '  \t',
			print format_range(cumulative), '\t',
			print format_pvalue(pval)

		ci, pval = compute_ci(self.sips)
		print 'SIP:', format_range(ci, 3), format_pvalue(pval)

	def write_table(self, filename):
		"""Writes the table in latex."""

		data = zip(self.names, 
				   self.estimate_cis, 
				   self.pvals,
				   self.cumulative_cis)

		header = ['Variable',
				  'Odds ratio',
				  'Probability',
				  'p-value',
				  ]

		rows = []
		for name, ci, pval, cumulative in data:
			odds_ci = np.exp(ci)
			row = [
				r'\verb"%s"' % name,
				format_range(odds_ci),
				format_range(cumulative),
				format_pvalue(pval),
				]
			rows.append(row)

		fp = open(filename, 'w')
		format = '|l|r|r|r|'
		write_latex_table(fp, header, rows, format)
		fp.close()

def read_survey(patients):
	survey = Survey()
	survey.loadPatients(patients)
	return survey

def test_models(version=(30,-1), resample_flag=False, patients = -1, printReg = True):
	means = dict(educ_from_12=4,
			born_from_1960=10)

	if patients == -1:
		patients = DataUtilities.getDictReadofPatientsFilled()
	#patients = getDictReadofPatientsFilled()
	# read the survey
	survey, complete = read_complete(version, patients)

	print DataUtilities.get_version(version)

	#compare_survey_and_complete(survey, complete)

	#print 'all respondents', survey.len()

	#print 'complete', complete.len()

	# run the models
	if printReg:
		regs = run_regression_and_print(survey, version=version, means=means)
	else:
		regs = run_regression(survey, version)
	return regs

def main(script):
	test_models(version = (30,-1))
	return

if __name__ == '__main__':
	import sys
	main(*sys.argv)