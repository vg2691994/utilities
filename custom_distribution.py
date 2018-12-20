#!/home/vgupta/Codes/miniconda2/bin/python

import numpy as N

class crandom():
  def my_pdf(self, x):
    '''
    Definition of the custom probability distribution function
    Has to be normalized so that the range (y) is exactly 0 to 1, Domain (x) can    be anything.
    '''
    y = N.cos(x)
    return y

  def gen(self, low=0, high=1, size=1):
    samples = N.random.uniform(low = low, high= high,size = size)
    checkers = N.random.uniform(low=0, high=1, size=size)
    desired_samples = samples[checkers < self.my_pdf(samples)]
    return desired_samples



