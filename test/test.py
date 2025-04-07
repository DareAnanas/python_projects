def nextFit(weight, capacity):
	bins = [0]
	for weight in weights:
		if bins[-1] + weight <= capacity:
			bins[-1] += weight
		else:
			bins.append(weight)
	return len(bins)


def firstFit(weights, capacity):
	bins = []
	for weight in weights:
		placed = False
		for i in range(len(bins)):
			if (bins[i] + weights <= capacity):
				bins[i] += weight
				placed = True
				break
		if not placed:
			bins.append(weight)
	return len(bins)
	
def worstFit(weights, capacity):
	bins = []
	for weight in weights:
		