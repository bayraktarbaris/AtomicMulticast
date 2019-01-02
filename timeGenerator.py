import math
import random

## Simple function that returns the time needs to pass before next transmission

def nextInterval(poissonVariable):

	return -math.log(1.0 - random.random()) / poissonVariable	