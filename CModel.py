import json
import os
import numpy as np
import tensorflow as tf
import model, sample, encoder

class CModel:
    def __init__(self, 
    model_name = '117M', 
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=40,
    top_p=0,
    models_dir='models',
    sentences=None,):
        self.model_name = model_name
        self.seed = seed
        self.nsamples = nsamples
        self.batch_size = batch_size
        self.length = length
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.models_dir = models_dir
        self.sentences = sentences
        self.enc = encoder.get_encoder(model_name)
        self.hparams = model.default_hparams()
        if self.batch_size is None:
            self.batch_size = 1
        assert self.nsamples % self.batch_size == 0
        if self.length is None:
            self.length = self.hparams.n_ctx // 2
        elif self.length > self.hparams.n_ctx:
            raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)
        with open(os.path.join('models', self.model_name, 'hparams.json')) as f:
            self.hparams.override_from_dict(json.load(f))
        test = tf.Session(graph=tf.Graph())
        self.sess = test.__enter__()
        self.context = tf.placeholder(tf.int32, [self.batch_size, None])
        np.random.seed(self.seed)
        tf.set_random_seed(self.seed)
        self.output = sample.sample_sequence(
            hparams=self.hparams, length=self.length,
            context=self.context,
            batch_size=self.batch_size,
            temperature=self.temperature, top_k=self.top_k, top_p=self.top_p
        )

        saver = tf.train.Saver()
        self.ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
        saver.restore(self.sess, self.ckpt)

    def runModel(self, sentences, seed):
        if sentences == None:
            raise ValueError('Sentences cannot be None')
            
        listy = []
        n = 0
        
        if isinstance(sentences, list):
            for i in sentences:
                context_tokens = self.enc.encode(i)
                for _ in range(self.nsamples // self.batch_size):
                    out = self.sess.run(self.output, feed_dict={
                        self.context: [context_tokens for _ in range(self.batch_size)]
                    })[:, len(context_tokens):]
                text = i + self.enc.decode(out[0])
                listy.append(text)
                n += 1
                print(n)
            return dict(zip(sentences,listy))
        else:
            context_tokens = self.enc.encode(sentences)
            for _ in range(self.nsamples // self.batch_size):
                out = self.sess.run(self.output, feed_dict={
                    self.context: [context_tokens for _ in range(self.batch_size)]
                })[:, len(context_tokens):]
            text = sentences + self.enc.decode(out[0])
            
            return {sentences: text}


