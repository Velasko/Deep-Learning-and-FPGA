import random
import pickle

#this file shows the chance of getting the wines correctly using only a random guess

# wine distribution:
# 3.0 0.006253908692933083
# 4.0 0.03314571607254534
# 5.0 0.425891181988743
# 6.0 0.3989993746091307
# 7.0 0.12445278298936835
# 8.0 0.01125703564727955
with open("./ML/data/wine.pickle", 'rb') as file:
	wine_data = pickle.load(file)

types = [line[-1] for line in wine_data]

dist = {}
for data in types:
	if not data in dist: dist[data] = 0
	dist[data] += 1

for key, value in dist.items():
	dist[key] /= len(types)

#uniform distribution function
f = lambda: random.randrange(3, 9)

#function with the same distribution of the wines
def r():
	while True:
		a = f()
		if dist[a] >= random.random(): return a

uniform = 0
not_uniform = 0
for data in types:
	if f() == data: uniform += 1
	if r() == data: not_uniform += 1

print("Uniform distribution got: %.2f %% correct" % (uniform/15.99))
print("Non uniform distribution got: %.2f %% correct" % (not_uniform/15.99))