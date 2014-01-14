#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import swehockey 

class TestTeamStats(unittest.TestCase):

    def test_teamstats_3905(self):
        # make sure skaters get read
        s = list(swehockey.playerstats(3905))
        self.assertTrue(s)


    def test_rosters_3905(self):
        # make sure goalies get read
        s = list(swehockey.rosters(3905))
        self.assertTrue(s)


    def test_teamstats_3906(self):
        # make sure skaters get read
        s = list(swehockey.playerstats(3906))
        self.assertTrue(s)


    def test_rosters_3906(self):
        # make sure goalies get read
        s = list(swehockey.rosters(3906))
        self.assertTrue(s)


if __name__ == '__main__':
    unittest.main()