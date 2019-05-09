import numpy as np
import tensorflow as tf

from model import Model

from helpers import *

SEED = 24

X_train, Y_train, X_val, Y_val, X_test, Y_test = load_CIFAR(SEED)

X_train = X_train[0:1000,:,:,:]
Y_train = Y_train[0:1000,:,:,:]

X_val = X_val[0:100,:,:,:]
Y_val = Y_val[0:100,:,:,:]

X_test = X_test[0:100,:,:,:]
Y_test = Y_test[0:100,:,:,:]

print('Train:')
print('X_train:', X_train.shape)
print('Y_train:', Y_train.shape)

print('Validation:')
print('X_val:', X_val.shape)
print('Y_val:', Y_val.shape)

print('Test:')
print('X_test:', X_test.shape)
print('Y_test:', Y_test.shape)

save_gray_images(X_train[0:10,:,:,:], filename="images/train_before_gray_{}.png")
save_lab_images(Y_train[0:10,:,:,:], filename="images/train_before_color_{}.png")

save_gray_images(X_val[0:10,:,:,:], filename="images/val_before_gray_{}.png")
save_lab_images(Y_val[0:10,:,:,:], filename="images/val_before_color_{}.png")

save_gray_images(X_test[0:10,:,:,:], filename="images/test_before_gray_{}.png")
save_lab_images(Y_test[0:10,:,:,:], filename="images/test_before_color_{}.png")

np.random.seed(SEED)
tf.random.set_random_seed(SEED)

with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    
    UNET = Model(sess, SEED)

    UNET.compile()
    
    print('Training...')
    UNET.train(X_train, Y_train, X_val, Y_val)

    print('Predicting training set...')
    pred = UNET.predict(X_train)
    save_lab_images(pred[0:10,:,:,:], filename="images/after_train_{}.png")

    print('Predicting validation set...')
    pred = UNET.predict(X_val)
    save_lab_images(pred[0:10,:,:,:], filename="images/after_val_{}.png")

    print('Predicting test set...')
    pred = UNET.predict(X_test)
    save_lab_images(pred[0:10,:,:,:], filename="images/after_test_{}.png")
