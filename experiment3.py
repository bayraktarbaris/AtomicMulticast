import numpy as np
import scipy.stats
import matplotlib.pyplot as plt


results = []
ranges = range(5,25,2)
for i in ranges:

	f1 = open("experiments/counter" + str(i) + ".txt","r")

	arr1 = np.array([])

	for line in f1:
		tmp = 0
		if line == '\n':
			tmp = 0
		else:
			tmp = sum(list(map(lambda x: int(x), line[:-1].split())))

		arr1 = np.append(arr1, tmp)

	results.append(576*arr1[:50]/i)
	
means = []

stds = []

linspaces = []


for i in range(len(results)):

	means.append(results[i].mean(axis = 0))

	stds.append(results[i].std())
	lin1 = means[i] - 3*stds[i] if means[i] - 3*stds[i] >= 0 else 0
	lin2 = means[i] + 3*stds[i] if means[i] + 3*stds[i] >= 0 else 0

	linspaces.append(np.linspace(lin1, lin2, 50))

x_axis = ranges


plt.suptitle('Group size vs Efficiency', fontsize=15)

# exp1_rdt_loss

#plt.subplot(1, 2, 1)
plt.xlabel('Group Size')
plt.ylabel('Efficiency(total number of bits per useful bit)')
rdt = plt.boxplot(linspaces, labels=x_axis)
plt.plot(x_axis, means)
plt.show()

