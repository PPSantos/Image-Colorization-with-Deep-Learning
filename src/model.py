import numpy as np
import tensorflow as tf
import datetime

from models.MLP import MLP

class Model:

    def __init__(self, sess, seed):

        # TODO: put these parameters as arguments or something.

        # Training settings.
        self.learning_rate = 0.001
        self.num_epochs = 200
        self.batch_size = 100

        self.compiled = False

        # Verbose/logs/checkpoints options.
        self.verbose = True
        self.log = True
        self.save = False
        self.save_interval = 50
    
        self.sess = sess
        self.seed = seed

    def compile(self):

        if self.compiled:
            print('Model already compiled.')
            return
        self.compiled = True

        # Placeholders.
        self.X = tf.placeholder(tf.float32, shape=(None, 3072), name='X')
        self.Y = tf.placeholder(tf.float32, shape=(None, 10), name='Y')

        # Model.
        mlp = MLP(self.X, self.seed)
        logits = mlp.forward()

        # Loss and metrics.
        self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.Y, logits=logits))

        # Optimizer.
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)

        # Tensorboard.
        tf.summary.scalar('loss', self.loss)

        self.saver = tf.train.Saver()

    def train(self, X_train, Y_train, X_val, Y_val):

        if not self.compiled:
            print('Compile model first.')
            return

        N = X_train.shape[0]
        num_batches = int(N / self.batch_size)
        
        self.sess.run(tf.global_variables_initializer())

        # Tensorboard.
        merged = tf.summary.merge_all()
        date = str(datetime.datetime.now()).replace(" ", "_")[:19]
        train_writer = tf.summary.FileWriter('logs/' + date + '/train', self.sess.graph)
        val_writer = tf.summary.FileWriter('logs/' + date + '/val')

        try:
            for epoch in range(self.num_epochs):
                epoch_loss = 0.0

                for b in range(num_batches):

                    start = b * self.batch_size
                    end   = min(b * self.batch_size + self.batch_size, N)
                    batch_x = X_train[start:end, :]
                    batch_y = Y_train[start:end, :]

                    _, l = self.sess.run([self.optimizer, self.loss], feed_dict={self.X: batch_x, self.Y: batch_y})

                    epoch_loss += l / num_batches

                if self.verbose:
                    print('Epoch:', (epoch +1), 'loss =', epoch_loss)

                if self.log:
                    # Add training epoch loss to train log.
                    summary = tf.Summary()
                    summary.value.add(tag='loss', simple_value=epoch_loss)
                    train_writer.add_summary(summary, epoch)
                    train_writer.flush()

                    # Add validation loss to val log.
                    summary = self.sess.run(merged, feed_dict={self.X: X_val, self.Y: Y_val})
                    val_writer.add_summary(summary, epoch)

                # Save model.
                if self.save and epoch % self.save_interval == 0:
                    self.saver.save(self.sess, 'checkpoints/' + date + '/model', global_step=epoch)

        except KeyboardInterrupt:
            print("\nInterrupted")


    def evaluate(self, X, Y):

        if not self.compiled:
            print('Compile model first.')
            return

        loss = self.sess.run(self.loss, feed_dict={self.X: X, self.Y: Y})

        return loss


    def predict(self, X):

        if not self.compiled:
            print('Compile model first.')
            return

        raise ValueError("Not defined.")
