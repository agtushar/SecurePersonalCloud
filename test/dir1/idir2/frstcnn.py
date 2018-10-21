import tensorflow as tf
from tensorflow import keras

import numpy as np
from sklearn.utils import shuffle

mnist = tf.contrib.learn.datasets.load_dataset("mnist")
trii = mnist.train.images # Returns np.array
tril = np.asarray(mnist.train.labels, dtype=np.int32)
tsi = mnist.test.images # Returns np.array
tsl = np.asarray(mnist.test.labels, dtype=np.int32)

#dataset = keras.datasets.fashion_mnist

#(trii, tril), (tsi, tsl) = dataset.load_data();

#trii = trii/255.000

trii, tril = shuffle(trii, tril);
#trill = []
#for i in tril:
#    temp = [0,0,0,0,0,0,0,0,0,0]
#    temp[i] = 1
#    trill.append(temp)
#tril = trill

tri, trl = trii[0:int(0.75*len(trii))], tril[0:int(0.75*len(trii))];
vli, vll = (trii[int(0.75*len(trii)):len(trii)], tril[int(0.75*len(trii)):len(trii)]);


tri = tri.reshape(len(tri),28,28,1);
vli = vli.reshape(len(vli),28,28,1);
tsi = tsi.reshape(len(tsi), 28,28,1);
model = keras.Sequential([keras.layers.Conv2D(filters=32, input_shape=(28, 28, 1), kernel_initializer='he_normal', kernel_size=3, activation=tf.nn.relu),
                          keras.layers.MaxPool2D(pool_size=[2,2]),
                          #keras.layers.Dropout(0.25),
                          keras.layers.Conv2D(filters=64, kernel_size=3, activation=tf.nn.relu),
                          keras.layers.MaxPool2D(pool_size=[2,2]),
                          #keras.layers.Dropout(0.4),
                          #keras.layers.Conv2D(filters=128, kernel_size=3, activation=tf.nn.relu),
                          #keras.layers.MaxPool2D(pool_size=[2,2], strides=2),
                          keras.layers.Flatten(),
                          keras.layers.Dense(units=128, activation=tf.nn.relu),
                          #keras.layers.Dropout(0.3),
                          #keras.layers.Dense(units=320, activation=tf.nn.relu),
                          keras.layers.Dense(units=10, activation=tf.nn.softmax)
                         ]);

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

test_accp = 0;
model.fit(tri, trl, epochs=3);
test_accc = model.evaluate(vli, vll)[1];
print(model.evaluate(tsi, tsl)[1])
count = 0;

while test_accc > test_accp:
    model.fit(tri, trl, epochs=2)
    test_accp = test_accc
    test_accc = model.evaluate(vli, vll)[1]
    count = count + 1
    print("=================================================")
    print(count)
    print(test_accc)
    print("kabali "+str(model.evaluate(tsi, tsl)[1]))
    print("=================================================")

print(model.evaluate(tsi, tsl)[1])
