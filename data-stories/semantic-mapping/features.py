import numpy as np
import cPickle
import tables
import os

from text.story.util.dsutils import make_word_ds, make_phoneme_ds, histogram_phonemes, cstates_to_bigrams, DataSequence, makelsa, catmats, histogram_phonemes2, sliding_chunk_sum, modulate

from text.models.semtax.Semtax import Semtax
from text.movie.util.SemanticModel import SemanticModel


mapdict = lambda d, fun: dict(zip(d.keys(), map(fun, d.values())))

class Features(object):
    def __init__(self, grids, trfiles, interp="rect", **kwargs):
        """Initializes a Features object that can be used to create feature-space
        representations of the stimulus with the given [grids] and [trfiles].

        [interp] can be "rect" or "sinc".
        [kwargs] are passed to the interpolation function.
        """
        self.grids = grids
        self.trfiles = trfiles

        self.interp = interp
        self.interpargs = kwargs

        ## Precache word sequences and phoneme sequences for later use
        self.wordseqs = make_word_ds(grids, trfiles)
        self.phonseqs = make_phoneme_ds(grids, trfiles)

    def downsample(self, dsdict):
        """Downsamples each DataSequence in [dsdict] using the settings specified in the
        initializer.
        """
        return mapdict(dsdict, lambda h: h.chunksums(self.interp,
                                                     **self.interpargs))

    def perstory(self):
        """Simple model: a separate intercept regressor for each story.
        """
        nstories = len(self.grids)
        storymats = dict()
        for ii,st in enumerate(sorted(self.grids.keys())):
            smat = np.zeros((len(self.wordseqs[st].tr_times), nstories))
            smat[:,ii] = 1
            storymats[st] = smat
        return storymats
        
    def numwords(self):
        """Simple model: the number of words per TR.
        """
        return mapdict(self.wordseqs, lambda s: np.atleast_2d(map(len, s.chunks())).T.astype(float))

    def numphonemes(self):
        """Simple model: the number of phonemes per TR.
        """
        return mapdict(self.phonseqs, lambda s: np.atleast_2d(map(len, s.chunks())).T.astype(float))

    def phonemecounts(self, debug=False):
        """Number of times each phoneme appears per TR.
        """
        phonhists = mapdict(self.phonseqs, histogram_phonemes2)
        if debug:
            return phonhists
        return self.downsample(phonhists)
        #return mapdict(phonhists, lambda h: h.chunksums())
        
    def markov(self, log=False, modeldir="/auto/k8/huth/storydata/stories-semtax-wbooks-3+20_100", num=10, nC=20, debug=False):
        """Markov syntactic model. The [modeldir] and [num] will be passed to the
        function Semtax.load_from_dir.
        This function assumes that the first [nC] features are syntactic.
        """
        stmodel = Semtax.load_from_dir(modeldir, num)
        stmodel.cphi[0] = stmodel.cphi[-1] ## Fix vocab * bug
        stmodel.zphi[0] = stmodel.zphi[-1]

        sm = stmodel.to_SemanticModel(True)
        sm.data = sm.data[:nC] ## Limit to only syntactic part

        makecs = lambda ds: DataSequence(stmodel.infer_word_cstates(ds.data)[:,:nC],
                                         ds.split_inds,
                                         ds.data_times,
                                         ds.tr_times)
        rstimseqs = mapdict(self.wordseqs, makecs)
        if log:
            rstimseqs = mapdict(rstimseqs, lambda ds: DataSequence(np.log(ds.data+1e-10),
                                                                   ds.split_inds,
                                                                   ds.data_times,
                                                                   ds.tr_times))

        if debug:
            return rstimseqs
        #return mapdict(rstimseqs, lambda s: s.chunksums())
        return self.downsample(rstimseqs)

    def markov_bigrams(self, log=False, modeldir="/auto/k8/huth/storydata/stories-semtax-wbooks-3+20_100",
                       num=10, nC=20):
        """Markov bigram syntactic model. The [modeldir] and [num] will be passed to the
        function Semtax.load_from_dir.
        This function assumes that the first [nC] features are syntactic.
        """
        stmodel = Semtax.load_from_dir(modeldir, num)
        stmodel.cphi[0] = stmodel.cphi[-1] ## Fix vocab * bug
        stmodel.zphi[0] = stmodel.zphi[-1]

        sm = stmodel.to_SemanticModel(True)
        sm.data = sm.data[:nC] ## Limit to only syntactic part

        makecs = lambda ds: DataSequence(stmodel.infer_word_cstates(ds.data)[:,:nC],
                                         ds.split_inds,
                                         ds.data_times,
                                         ds.tr_times)
        rstimseqs = mapdict(self.wordseqs, makecs)
        bigramseqs = mapdict(rstimseqs, cstates_to_bigrams)
        if log:
            bigramseqs = mapdict(bigramseqs, lambda ds: DataSequence(np.log(ds.data+1e-10),
                                                                     ds.split_inds,
                                                                     ds.data_times,
                                                                     ds.tr_times))

        #return mapdict(bigramseqs, lambda s: s.chunksums())
        return self.downsample(bigramseqs)

    def markov_bigram_ics(self, modeldir="/auto/k8/huth/storydata/stories-semtax-wbooks-3+20_100",
                       num=10, nC=20, icfile="/auto/k8/huth/storydata/transmat-ics-150-wbooks-2.hf5"):
        """Markov bigram IC syntactic model. The [modeldir] and [num] will be passed to the
        function Semtax.load_from_dir.
        This function assumes that the first [nC] features are syntactic.
        """
        stmodel = Semtax.load_from_dir(modeldir, num)
        stmodel.cphi[0] = stmodel.cphi[-1] ## Fix vocab * bug
        stmodel.zphi[0] = stmodel.zphi[-1]

        sm = stmodel.to_SemanticModel(True)
        sm.data = sm.data[:nC] ## Limit to only syntactic part

        makecs = lambda ds: DataSequence(stmodel.infer_word_cstates(ds.data)[:,:nC],
                                         ds.split_inds,
                                         ds.data_times,
                                         ds.tr_times)
        rstimseqs = mapdict(self.wordseqs, makecs)
        bigramseqs = mapdict(rstimseqs, cstates_to_bigrams)
        logbigramseqs = mapdict(bigramseqs, lambda ds: DataSequence(np.log(ds.data+1e-10),
                                                                    ds.split_inds,
                                                                    ds.data_times,
                                                                    ds.tr_times))

        bgics = tables.openFile(icfile).root.ics.read()
        projics = lambda ds: DataSequence(np.dot(bgics, sliding_chunk_sum(ds.data, 7).T).T,
                                          ds.split_inds,
                                          ds.data_times,
                                          ds.tr_times)
        bgicseqs = mapdict(logbigramseqs, projics)

        #return mapdict(bgicseqs, lambda s: s.chunksums())
        return self.downsample(bgicseqs)

    def lsa(self, ndim, rectify, zsaxes=(1,), basepath="/auto/k8/huth/storydata/stories-wbooks-lsa-2", debug=False):
        """LSA semantic model.
        """
        vocab = cPickle.load(open(basepath+"-vocab"))
        lsasm = SemanticModel(None, None)
        lsasm.load_ascii_root(basepath+"-Vt", vocab)
        lsasm.data = lsasm.data[:ndim]

        for axis in zsaxes:
            lsasm.zscore(axis)

        if rectify:
            lsasm.rectify()

        lsastimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, lsasm))
        #return mapdict(lsastimseqs, lambda s: s.chunksums())
        if debug:
            return lsastimseqs
        return self.downsample(lsastimseqs)

    @staticmethod
    def get_newlsa_model(ndim, rectify, entweight, entcutoff=5, basepath="/auto/k6/huth/lsamats6/"):
        """Returns a new LSA semantic model.
        """
        entropyfilename = os.path.join(basepath, "globnorm_lsa1_1.npy")
        modelfilename = os.path.join(basepath, "evd1.hf5")

        entropy = np.load(entropyfilename)
        lsafile = tables.openFile(modelfilename)

        Q = lsafile.root.Q.read()
        vocab = lsafile.root.vocab.read()

        if entweight:
            lsasm = SemanticModel(Q[:,-ndim:].T * (np.clip(entropy, entcutoff, np.inf)**-1), vocab)
        else:
            lsasm = SemanticModel(Q[:,-ndim:].T, vocab)

        if rectify:
            lsasm.rectify()

        ## Store entropies in there as well
        lsasm.wordentropy = entropy

        lsafile.close()
        
        return lsasm

    def newlsa(self, ndim, rectify, entweight, entcutoff=5, basepath="/auto/k6/huth/lsamats6/", debug=False):
        """New LSA semantic model.
        """
        lsasm = self.get_newlsa_model(ndim, rectify, entweight, entcutoff, basepath)
        lsastimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, lsasm))

        if debug:
            return lsastimseqs
        return self.downsample(lsastimseqs)

    def hal(self, wordset="verbs", zsaxes=(0,1), rectify=False,
            basepath="/auto/k8/huth/storydata/story+books+wiki+15w-densehal-mat", debug=False):
        """HAL semantic model (without dimensionality reduction).
        """
        from text.story.util.HalModel import make_hal_wordset_model, verb_set, make_hal_sm, english1000
        haltf = tables.openFile(basepath+".hf5")
        halmat = np.array(haltf.root.halmat.read())
        halvocab = cPickle.load(open(basepath+"-vocab"))

        ## Choose a wordset
        if wordset=="verbs":
            wordset = verb_set
        elif wordset=="cmuverbs":
            wordset = verb_set[:23]
        elif wordset=="english1000":
            wordset = english1000
        
        halsm = make_hal_sm(halmat, halvocab, wordset)

        for axis in zsaxes:
            halsm.zscore(axis)

        if rectify:
            halsm.rectify()

        halstimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, halsm))
        #return mapdict(halstimseqs, lambda s: s.chunksums())
        if debug:
            return halstimseqs
        return self.downsample(halstimseqs)

    @staticmethod
    def get_co_model(wordset="english1000", zsaxes=(0,1), rectify=False,
                     basepath="/auto/k8/huth/storydata/comodels/complete2-15w-denseco-mat"):
        """Co-occurence-based semantic model (without dimensionality reduction).
        """
        from text.story.util.HalModel import make_hal_wordset_model, verb_set, make_hal_sm, english1000
        cotf = tables.openFile(basepath+".hf5")
        comat = np.array(cotf.root.mat.read())
        covocab = cPickle.load(open(basepath+"-vocab"))

        ## Choose a wordset
        if wordset=="verbs":
            wordset = verb_set
        elif wordset=="cmuverbs":
            wordset = verb_set[:23]
        elif wordset=="english1000":
            wordset = english1000
        elif wordset=="story":
            wordset = [[w] for w in cPickle.load(open("/auto/k1/huth/text/story/storyvocab_2013.pickle"))]
        
        cosm = make_hal_sm(comat, covocab, wordset)

        for axis in zsaxes:
            cosm.zscore(axis)

        if rectify:
            cosm.rectify()

        return cosm
        

    def co(self, wordset="english1000", zsaxes=(0,1), rectify=False,
           basepath="/auto/k8/huth/storydata/comodels/complete2-15w-denseco-mat", debug=False):
        """Co-occurence-based semantic model (without dimensionality reduction).
        """
        cosm = self.get_co_model(wordset, zsaxes, rectify, basepath)
        costimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, cosm))
        #return mapdict(halstimseqs, lambda s: s.chunksums())
        if debug:
            return costimseqs
        return self.downsample(costimseqs)

    @staticmethod
    def get_orthogonal_co_model(wordset="english1000", zsaxes=(0,1), rectify=False,
                                basepath="/auto/k8/huth/storydata/comodels/complete2-15w-denseco-mat",
                                debug=False):
        """Co-occurence-based semantic model with pre-whitening.
        """
        cosm = Features.get_co_model(wordset, zsaxes, rectify, basepath)
        ## Orthogonalize cosm data
        from text.movie.util.util import make_delayed, save_table_file, eigprincomp
        coc, col = eigprincomp(cosm.data.T)
        ## Flip so that first value on each component is positive (makes result deterministic)
        fcoc = (coc.T * np.sign(coc[:,0])).T
        ## Make new orthogonal cosm
        ocosm = cosm.copy()
        ocosm.data = np.dot(fcoc, cosm.data)
        return ocosm

    def orthogonal_co(self, wordset="english1000", zsaxes=(0,1), rectify=False,
                      basepath="/auto/k8/huth/storydata/comodels/complete2-15w-denseco-mat",
                      debug=False):
        """Co-occurence-based semantic model with pre-whitening.
        """
        ocosm = self.get_orthogonal_co_model(wordset, zsaxes, rectify, basepath)
        costimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, ocosm))
        #return mapdict(halstimseqs, lambda s: s.chunksums())
        if debug:
            return costimseqs
        return self.downsample(costimseqs)

    def commonwords(self, num=100, basepath="/auto/k8/huth/storydata/stories-wbooks-lsa-2-vocab"):
        """Common word indicator model. Based on old LSA model fitting, used less data.
        """
        vocab = cPickle.load(open(basepath))
        counts = cPickle.load(open(basepath+"-Rcounts"))
        selwords = np.argsort(counts)[-num:]
        wmodel = SemanticModel(np.eye(num), list(np.array(vocab)[selwords]))

        wordstimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, wmodel))
        #return mapdict(wordstimseqs, lambda s: s.chunksums())
        return self.downsample(wordstimseqs)

    def commonwords2(self, num=100, basepath="/auto/k8/huth/storydata/comodels/complete2-15w-denseco-mat"):
        """Common word indicator model. Base on newer co model fitting, using more data.
        """
        cotf = tables.openFile(basepath+".hf5")
        counts = cotf.root.wordcounts.read()
        covocab = cPickle.load(open(basepath+"-vocab"))
        selwords = np.argsort(counts)[-num:]
        wmodel = SemanticModel(np.eye(num), list(np.array(covocab)[selwords]))

        wordstimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, wmodel))
        return self.downsample(wordstimseqs)

    def allwords(self):
        """All word indicator model.
        """
        from text.textcore import Corpus
        corpus_file = "/auto/k5/huth/corpora/story/raw-transcripts/stories1.tar.gz"
        corpus = Corpus(corpus_file, split_documents=200)
        corpus_file1 = "/auto/k5/huth/corpora/story/raw-transcripts/stories2.tar.gz"
        corpus.append_corpus(corpus_file1)

        storyvocab = sorted(list(set(corpus.get_vocabulary())))
        num = len(storyvocab)
        wmodel = SemanticModel(np.eye(num), list(np.array(storyvocab)))

        wordstimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, wmodel))
        #return mapdict(wordstimseqs, lambda s: s.chunksums())
        return self.downsample(wordstimseqs)

    def nmflsa(self):
        """NMF LSA model based on newLSA.
        """
        tf = tables.openFile("/auto/k6/huth/nmf-lsa.hf5")
        vocab = tf.root.vocab.read()
        data = tf.root.data.read()
        nmodel = SemanticModel(data, vocab)
        wordstimseqs = mapdict(self.wordseqs, lambda ds: makelsa(ds, nmodel))
        #return mapdict(wordstimseqs, lambda s: s.chunksums())
        return self.downsample(wordstimseqs)

    def surprisal(self, template="/auto/k5/huth/story-surprisal/%s.npy", prob=False, debug=False):
        """Word surprisal model.
        """
        ## Load surprisal for each story
        sseqs = dict()
        for story,wseq in self.wordseqs.iteritems():
            surprisal = np.load(template%story)
            if prob:
                d = 1-np.atleast_2d(surprisal).T
            else:
                d = -np.log2(np.atleast_2d(surprisal).T)
                d[np.isinf(d)] = 100
            sseq = DataSequence(d,
                                wseq.split_inds,
                                wseq.data_times,
                                wseq.tr_times)
            sseqs[story] = sseq

        if debug:
            return sseqs
        else:
            return self.downsample(sseqs)

    def sphal(self, halargs, spargs, debug=False):
        """HAL model modulated by surprisal.
        """
        halargs["debug"] = True
        halseqs = self.hal(**halargs)
        spargs["debug"] = True
        spargs["prob"] = True
        spseqs = self.surprisal(**spargs)

        modhal = dict([(st, modulate(ds, spseqs[st].data[:,0])) for (st,ds) in halseqs.items()])
        
        if debug:
            return modhal
        return self.downsample(modhal)

    @classmethod
    def _get_word2vec_model(cls, modelfile="/auto/k8/huth/GoogleNews-vectors-negative300.bin",
                            norm=False):
        from gensim.models.word2vec import Word2Vec
        model = Word2Vec.load_word2vec_format(modelfile, binary=True)
        usevocab = set(cPickle.load(open("/auto/k8/huth/storydata/comodels/complete2-15w-denseco-mat-vocab")))
        vocab, vocinds = zip(*[(w, model.vocab[w].index) for w in usevocab if w in model.vocab])
        #w2v_usevocab = [(w,val.index) for w,val in w2v.vocab.items() if w in usevocab]
        #srtvocab = [w for w,voc in sorted(w2v.vocab.items(), key=lambda item:item[1].index)]
        #srtvocab,srtinds = zip(*sorted(w2v_usevocab, key=lambda item:item[1]))
        if norm:
            data = model.syn0norm[list(vocinds)]
        else:
            data = model.syn0[list(vocinds)]

        w2vsm = SemanticModel(data.T, vocab)
        return w2vsm

    @classmethod
    def get_word2vec_model(cls, *args, **kwargs):
        if "_w2v_cache" not in dir(cls):
            cls._w2v_cache = cls._get_word2vec_model(*args, **kwargs)
        return cls._w2v_cache
    
    def word2vec(self, modelfile="/auto/k8/huth/GoogleNews-vectors-negative300.bin", norm=False):
        """GenSim / word2vec model.
        """
        model = self.get_word2vec_model(modelfile, norm)
        #modeldims = model["test"].shape[0]
        #model.data = np.zeros((modeldims,))
        w2vstims = mapdict(self.wordseqs, lambda ds: makelsa(ds, model))
        return self.downsample(w2vstims)

    def emoratings(self, subjects=("ah", "ds", "jg", "wh", "ml"), smoothing=1.0):
        from text.story.emotions import util
        storyemolevels = util.load_story_ratings(subjects, self.grids)
        return util.story_interp_grids(subjects, self.grids, self.trfiles,
                                       storyemolevels, [smoothing])
