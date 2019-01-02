import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
### Script for performing experiment 2 ###

results = []
ranges = [4,8,12,18,24,30]
for i in ranges:

	f1 = open("responses/initiatorTime" + str(5) + "poisson" + str(i) + ".txt","r")

	f2 = open("responses/leaftime" + str(5) + "poisson" + str(i) +".txt","r")

	arr1 = np.array([])

	arr2 = np.array([])

	for line1 in f1:

		arr1 = np.append(arr1, float(line1[:-1]))

	for line2 in f2:
	
		arr2 = np.append(arr2, float(line2[:-1]))

	results.append((arr1+arr2))
	
means = []

stds = []

linspaces = []


for i in range(len(results)):

	means.append(results[i].mean(axis = 0))

	stds.append(results[i].std())

	linspaces.append(np.linspace(means[i] - 3*stds[i], means[i] + 3*stds[i], 100))

x_axis = ranges


plt.suptitle('Lambda vs Stable Delivery Time', fontsize=15)

# exp1_rdt_loss

#plt.subplot(1, 2, 1)
plt.xlabel('Lambda (packets/sec)')
plt.ylabel('Stable Delivery Time(sec)')
rdt = plt.boxplot(linspaces, labels=x_axis)
plt.plot(x_axis, means)
plt.show()

