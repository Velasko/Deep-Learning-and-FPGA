import numpy as np
import matplotlib.pyplot as plt
import pickle

#erased line:
#"fixed acidity";"volatile acidity";"citric acid";"residual sugar";"chlorides";"free sulfur dioxide";"total sulfur dioxide";"density";"pH";"sulphates";"alcohol";"quality"

if False:
	wine_data = np.loadtxt(data_path + "winequality.csv", delimiter=";")

	with open(data_path + "wine.pickle", 'wb') as file:
		pickle.dump(train_data, file)

	print('Train pickled')


with open("./ML/data/wine.pickle", 'rb') as file:
	wine_data_raw = pickle.load(file)

wine_data = [line for line in wine_data_raw if line[-1] in (3, 4, 5, 6, 7, 8)]
test_size = int(len(wine_data)/10)
print("wine size:", len(wine_data), test_size)

x_train = []
y_train = []
for line in wine_data[:-test_size]:
	x_train.append(line[:-1])
	y_train.append(line[-1])

x_test = []
y_test = []
for line in wine_data[-test_size:]:
	x_test.append(line[:-1])
	y_test.append(line[-1])


from sklearn.linear_model import LinearRegression

regressor = LinearRegression()  
regressor.fit(x_train, y_train)

x = [e for e in range(len(x_test))]

y_pred = regressor.predict(x_test)

d = [((value - y_pred[n])/value)**2 for n, value in enumerate(y_test)]

var = sum(d)**0.5/len(y_test)

print(var)
print(regressor.coef_)
print(regressor.intercept_)

print("acurracy:", sum([y_test[n] ==  round(y_pred[n]) for n in range(test_size)])/test_size)

#d.sort()
plt.plot(x, d)
#plt.plot(x, y_pred, 'ro', markersize=2)
#plt.show()