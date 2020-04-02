from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

dataset = loadtxt("C:\\Users\\Andrew Swaim\\Documents\\ANNE Homework\\trainingSet.txt", delimiter=',')
X = dataset[:, 0:37]
Y = dataset[:, 38]

model = Sequential()
model.add(Dense(input_dim=38, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=20, batch_size=400)
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))
