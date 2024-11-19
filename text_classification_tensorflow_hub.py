# -*- coding: utf-8 -*-
"""text_classification_tensorflow_hub.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NpW4Yd-1-eFTBhV_cNtvBhwiwC_UTG41
"""

import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
import tensorflow_hub as hub
import tf_keras

import tensorflow as tf

print("Version : ", tf.__version__)
print("Eager mode : ", tf.executing_eagerly())
print("Hub version : ", hub.__version__)
print("GPU is", "available." if tf.config.list_physical_devices(
    "GPU") else "NOT AVAILABLE.")

train_data, test_data = tfds.load(
    name="imdb_reviews",
    split=["train", "test"],
    batch_size=-1,
    as_supervised=True)

train_examples, train_labels = tfds.as_numpy(train_data)
test_examples, test_labels = tfds.as_numpy(test_data)

print(
    f"Training entries : {len(train_examples)}, Testing entries : {len(test_examples)}")

print(train_examples[:3])
print(train_labels[:3])

HANDLE = "https://www.kaggle.com/models/google/nnlm/TensorFlow2/en-dim128-with-normalization/1"
hub_layer = hub.KerasLayer(
    handle=HANDLE, input_shape=[], dtype=tf.string, trainable=True)
hub_layer(train_examples[:3])

model = tf_keras.Sequential()
model.add(hub_layer)
model.add(tf_keras.layers.Dense(16, activation="relu"))
model.add(tf_keras.layers.Dense(1, activation="sigmoid"))
model.summary()

x_val = train_examples[:10000]
y_val = train_labels[:10000]

partial_x_train = train_examples[10000:]
partial_y_train = train_labels[10000:]

model.compile(
    optimizer="adam",
    loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    metrics=["accuracy"])
HISTORY = model.fit(
    partial_x_train,
    partial_y_train,
    epochs=10,
    batch_size=512,
    validation_data=(x_val, y_val))

results = model.evaluate(test_examples, test_labels)

history_dict = HISTORY.history
history_dict.keys()

acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, label="Training Accuracy")
plt.plot(epochs, val_acc, label="Validation Accuracy")
plt.title("Training and Validation Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

plt.plot(epochs, loss, label="Training Loss")
plt.plot(epochs, val_loss, label="Validation Loss")
plt.title("Training and Validation Loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()
