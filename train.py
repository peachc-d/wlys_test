# -- coding: utf-8 --

# 环境配置：
# linux
# tensorflow 2.0.0
# keras 2.3.1

import tensorflow as tf

from keras.models import Sequential

from keras.layers import Dense, Dropout, Activation, Flatten

from keras.layers import Conv2D, MaxPooling2D

import keras

from keras.datasets import cifar10


from keras import backend as K

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from keras.preprocessing.image import ImageDataGenerator


classes_num = 10

batch_size = 50

epochs_num = 200


# 定义卷积神经网络模型
def quality_classify_model():
    model = Sequential()

    # 卷积->激活（使用ReLU）->池化（使用最大池化）重复三次
    model.add(Conv2D(32, (3, 3), padding="same", input_shape=(32, 32, 3)))

    model.add(Activation("relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))

    model.add(Activation("relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), padding="same"))

    model.add(Activation("relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    # 展开到一个全连接层
    model.add(Flatten())

    model.add(Dense(64))  # 64个神经元

    model.add(Activation("relu"))  # 激活函数使用ReLU

    model.add(Dropout(0.5))  # 抛弃50%，防止过拟合

    model.add(Dense(classes_num))

    model.add(Activation("softmax"))  # 最后的激活函数选择适合多分类任务的softmax

    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

    model.compile(
        loss="categorical_crossentropy",
        optimizer=opt,
        metrics=["accuracy", f1_m, recall_m, precision_m],
    )
    # 模型编译，配置优化器、损失函数（此处使用多分类损失函数）和准确度测评指标

    return model


# 定义recall值的计算
def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))

    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))

    recall = true_positives / (possible_positives + K.epsilon())

    return recall


# 定义precision值的计算
def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))

    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))

    precision = true_positives / (predicted_positives + K.epsilon())

    return precision


# 定义f1值的计算
def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)

    recall = recall_m(y_true, y_pred)

    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


def train():
    # 数据载入

    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # 多分类标签生成

    y_train = keras.utils.to_categorical(y_train, classes_num)

    y_test = keras.utils.to_categorical(y_test, classes_num)

    # 生成训练数据

    x_train = x_train.astype("float32")

    x_test = x_test.astype("float32")

    # x_train /= 255

    x_test /= 255

    # 用ImageDataGenerator类返回了一个train_datagan ，用来增强数据
    train_datagan = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=15,
        width_shift_range=0.15,
        height_shift_range=0.15,
        fill_mode="wrap",
    )

    model = quality_classify_model()

    hist = model.fit_generator(
        train_datagan.flow(x_train, y_train, batch_size=batch_size),
        steps_per_epoch=x_train.shape[0] // batch_size,
        epochs=epochs_num,
        validation_data=(x_test, y_test),
        shuffle=True,
    )

    model.save("./cifar10_model.hdf5")

    model.save_weights("./cifar10_model_weight.hdf5")

    hist_dict = hist.history

    print("train acc:")

    print(hist_dict["accuracy"])

    print("validation acc:")

    print(hist_dict["val_accuracy"])

    train_acc = hist.history["accuracy"]

    val_acc = hist.history["val_accuracy"]

    train_loss = hist.history["loss"]

    val_loss = hist.history["val_loss"]

    train_f1 = hist.history["f1_m"]

    val_f1 = hist.history["val_f1_m"]

    train_pre = hist.history["precision_m"]

    val_pre = hist.history["val_precision_m"]

    train_re = hist.history["recall_m"]

    val_re = hist.history["val_recall_m"]

    # 绘图

    epochs = range(1, len(train_acc) + 1)

    plt.plot(epochs, train_acc, "bo", label="Training acc")

    plt.plot(epochs, val_acc, "r", label="Validation acc")

    plt.title("Training and validation accuracy")

    plt.legend()

    plt.savefig("accuracy.png")

    plt.figure()  # 新建一个图

    plt.plot(epochs, train_loss, "bo", label="Training loss")

    plt.plot(epochs, val_loss, "r", label="Validation loss")

    plt.title("Training and validation loss")

    plt.legend()

    plt.savefig("loss.png")

    plt.figure()

    plt.plot(epochs, train_f1, "bo", label="Training f1")

    plt.plot(epochs, val_f1, "r", label="Validation f1")

    plt.title("Training and validation f1")

    plt.legend()

    plt.savefig("f1.png")

    plt.figure()

    plt.plot(epochs, train_pre, "bo", label="Training precision")

    plt.plot(epochs, val_pre, "r", label="Validation precision")

    plt.title("Training and validation precision")

    plt.legend()

    plt.savefig("precision.png")

    plt.figure()

    plt.plot(epochs, train_re, "bo", label="Training recall")

    plt.plot(epochs, val_re, "r", label="Validation recall")

    plt.title("Training and validation recall")

    plt.legend()

    plt.savefig("recall.png")
