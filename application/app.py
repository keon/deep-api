from __future__ import print_function

# webapp
from flask import request, render_template, jsonify, url_for, redirect, g
from .models import User
from index import app, db
from sqlalchemy.exc import IntegrityError
from .utils.auth import generate_token, requires_auth, verify_token


#################3
# restore trained data
import tensorflow as tf
import numpy as np

import sys
import os

from algorithms.mnist import model

x = tf.placeholder("float", [None, 784])
sess = tf.Session()

MNIST_FOLDER = os.path.join(app.config['ALGORITHM_FOLDER'],'mnist')

with tf.variable_scope("simple"):
    y1, variables = model.simple(x)
saver = tf.train.Saver(variables)
saver.restore(sess, os.path.join(MNIST_FOLDER,"data/simple.ckpt"))
def simple(input):
    return sess.run(y1, feed_dict={x: input}).flatten().tolist()

with tf.variable_scope("convolutional"):
    keep_prob = tf.placeholder("float")
    y2, variables = model.convolutional(x, keep_prob)
saver = tf.train.Saver(variables)
saver.restore(sess, os.path.join(MNIST_FOLDER,"data/convolutional.ckpt"))
def convolutional(input):
    return sess.run(y2, feed_dict={x: input, keep_prob: 1.0}).flatten().tolist()

from algorithms.char_rnn.models.model import Char_RNN_Model


import time
from six.moves import cPickle

from algorithms.char_rnn.utils import TextLoader

from six import text_type



def sample(args):
    SAVE_DIR = os.path.join(app.config['ALGORITHM_FOLDER'],'char_rnn/save')
    with open(os.path.join(SAVE_DIR, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(SAVE_DIR, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    model = Char_RNN_Model(saved_args, True)
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(SAVE_DIR)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            return model.sample(sess, chars, vocab, 500, " ", 1)

##################


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/mnist', methods=['POST'])
def mnist_api():
    input = ((255 - np.array(request.json, dtype=np.uint8)) / 255.0).reshape(1, 784)
    output1 = simple(input)
    output2 = convolutional(input)
    return jsonify(results=[output1, output2])

@app.route('/api/char-rnn', methods=['POST'])
def char_rnn_api():
    args = {
            "save_dir" : "save",
            "n" : 500,
            "prime" : ' ',
            "sample" : 1
            }
    return sample(args)

# @app.route('/mnist')
# def mnist():
    # return render_template('mnist.html')

@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')


@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )


@app.route("/api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403
