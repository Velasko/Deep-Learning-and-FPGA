import numpy as np
import matplotlib.pyplot as plt
import pickle

if __name__ == '__main__':
#https://www.python-course.eu/neural_network_mnist.php

	image_size = 28 # width and length
	no_of_different_labels = 10 #  i.e. 0, 1, 2, 3, ..., 9
	image_pixels = image_size * image_size
	# data_path = "../mnist/"
	# train_data = np.loadtxt(data_path + "mnist_train.csv", 
	#                         delimiter=",")

	# print("train data loaded")

	# with open("train.pickle", 'wb') as file:
	# 	pickle.dump(train_data, file)

	# print('Train pickled')

	# test_data = np.loadtxt(data_path + "mnist_test.csv", 
	#                        delimiter=",") 

	# print('test loaded')

	# with open("test.pickle", 'wb') as file:
	# 	pickle.dump(test_data, file)

	# print('test pickled')

	with open("train.pickle", 'rb') as file:
		train_data = pickle.load(file)

	with open("test.pickle", 'rb') as file:
		test_data = pickle.load(file)


	fac = 0.99 / 255
	train_imgs = np.asfarray(train_data[:, 1:]) * fac + 0.01
	test_imgs = np.asfarray(test_data[:, 1:]) * fac + 0.01

	train_labels = np.asfarray(train_data[:, :1])
	test_labels = np.asfarray(test_data[:, :1])


	lr = np.arange(10)

	for label in range(10):
		one_hot = (lr==label).astype(np.int)
		print("label: ", label, " in one-hot representation: ", one_hot)

	lr = np.arange(no_of_different_labels)

	# transform labels into one hot representation
	train_labels_one_hot = (lr==train_labels).astype(np.float)
	test_labels_one_hot = (lr==test_labels).astype(np.float)

	# we don't want zeroes and ones in the labels neither:
	train_labels_one_hot[train_labels_one_hot==0] = 0.01
	train_labels_one_hot[train_labels_one_hot==1] = 0.99
	test_labels_one_hot[test_labels_one_hot==0] = 0.01
	test_labels_one_hot[test_labels_one_hot==1] = 0.99


	for i in range(10):
		img = train_imgs[i].reshape((28,28))
		plt.imshow(img, cmap="Greys")
#		plt.show()

	with open("pickled_mnist.pkl", "wb") as fh:
		data = (train_imgs, 
				test_imgs, 
				train_labels,
				test_labels,
				train_labels_one_hot,
				test_labels_one_hot)
		pickle.dump(data, fh)

with open("pickled_mnist.pkl", "br") as fh:
    data = pickle.load(fh)

train_imgs = data[0]
test_imgs = data[1]
train_labels = data[2]
test_labels = data[3]
train_labels_one_hot = data[4]
test_labels_one_hot = data[5]

image_size = 28 # width and length
no_of_different_labels = 10 #  i.e. 0, 1, 2, 3, ..., 9
image_pixels = image_size * image_size

