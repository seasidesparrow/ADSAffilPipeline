#!/usr/bin/env python

import unittest
import run as r
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from pandas.util.testing import assert_frame_equal

from adsmsg import AugmentAffiliationRequestRecord, AugmentAffiliationRequestRecordList, AugmentAffiliationResponseRecord, AugmentAffiliationResponseRecordList

class TestReadData(unittest.TestCase):

    def test_normal(self):
        infile = "test/test_dict.txt"
        incols = ['A','B']
        outdf = pd.DataFrame({'A':pd.Series(['1000','2000'], index=[0,1]),
                              'B':pd.Series(['hello nice day goodbye',
                                             'yes no maybe definitely'],
                                            index=[0,1])})
        indf = r.read_data(infile, incols)
        assert_frame_equal(indf, outdf)

    def test_nocolumns(self):
        infile="test/test_dict.txt"
        with self.assertRaises(NameError):
            indf = r.read_data(infile, incols)


    def test_nofile(self):
        incols = ['A','B']
        infile = "no_such_file"
        with self.assertRaises(IOError):
            r.read_data(infile, incols)
            

    def test_lockedfile(self):
        incols = ['A','B']
        infile = "test/locked_file.txt"
        with self.assertRaises(IOError):
            r.read_data(infile, incols)


class TestColToList(unittest.TestCase):

    def test_normal(self):
        inlist=['1000', '2000']
        testdf=pd.DataFrame({'A':pd.Series(['1000','2000'], index=[0,1]),
                             'B':pd.Series(['hello nice day goodbye',
                                            'yes no maybe definitely'],
                                           index=[0,1])})
        outlist = r.column_to_list(testdf, 'A')
        self.assertEqual(inlist, outlist)

        
    def test_wrongtype(self):
        inlist = ['1000', '2000']
        testdf = 0
        with self.assertRaises(TypeError):
            outlist = r.column_to_list(testdf, 'A')
        
    def test_badcolumn(self):
        inlist = ['1000', '2000']
        testdf = pd.DataFrame({'A':pd.Series(['1000','2000'], index=[0,1]),
                             'B':pd.Series(['hello nice day goodbye',
                                            'yes no maybe definitely'],
                                           index=[0,1])})
        with self.assertRaises(KeyError):
            outlist = r.column_to_list(testdf, 'C')
        

class TestLearningModel(unittest.TestCase):

    def test_returntypes(self):
        infile = "test/tiny_learner.txt"
        incols = ['Affcode','Affil']
        df = r.read_data(infile, incols)
        a,b,c,d = r.learning_model(df)
        self.assertEqual(type(d), list)
        self.assertEqual(type(c), SGDClassifier)
        self.assertEqual(type(b), TfidfTransformer)
        self.assertEqual(type(a), CountVectorizer)


class TestParentsChildren(unittest.TestCase):

    def test_getparent(self):
        infile = "test/tiny_pc.txt"
        a,b,c = r.parents_children(infile)
        affil = '61814'
        self.assertEqual(r.get_parent(affil,b), '0001')


class TestGetParent(unittest.TestCase):

    def test_badaffil(self):
        affil = '999999'
        parents = {'1234':'test 1', '2345':'test 2'}
        with self.assertRaises(KeyError):
            out = r.get_parent(parents[affil], parents)

    def test_nodict(self):
        affil = '123'
        with self.assertRaises(NameError):
            out = r.get_parent(parents[affil], parents)

    def test_baddict(self):
        affil = '123'
        parents = 0
        with self.assertRaises(TypeError):
            out = r.get_parent(parents[affil], parents)

    def test_emptycall(self):
        with self.assertRaises(TypeError):
            out = r.get_parent()
