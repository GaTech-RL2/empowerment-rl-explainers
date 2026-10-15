import math,unittest
from empowerment_lab import *

class InformationTests(unittest.TestCase):
    def test_binary_symmetric_capacity(self):
        for e in [0.,.1,.5,.9,1.]:
            W=[[1-e,e],[e,1-e]]
            self.assertAlmostEqual(capacity(W)['value'],math.log(2)-entropy([e,1-e]),places=9)
    def test_duplicates_and_no_control(self):
        self.assertAlmostEqual(capacity([[1,0],[0,1],[1,0]])['value'],math.log(2),places=8)
        self.assertAlmostEqual(capacity([[.2,.8]]*4)['value'],0)
    def test_asymmetric_channel_gap(self):
        W=[[1,0],[.5,.5]];result=capacity(W)
        # This Z-channel's exact capacity is ln(1 + 1/4).
        self.assertAlmostEqual(result['value'],math.log(1.25),places=8)
        self.assertLess(result['gap'],1e-9)
        self.assertLessEqual(mutual_information(W,[.1,.9]),result['upper']+1e-12)
    def test_variational_bound(self):
        W=symmetric(4,.3);p=[.1,.2,.3,.4];I=mutual_information(W,p)
        for q in [0,.2,.7,1.]:self.assertLessEqual(variational_bound(W,p,q),I+1e-12)
        self.assertAlmostEqual(variational_bound(W,p,1),I)
    def test_nuisance_cancels(self):
        W=symmetric(3,.23);p=[.2,.3,.5];I=mutual_information(W,p)
        for q in [[0,1],[.3,.7],[.5,.5]]:
            joint=nuisance_channel(W,q)
            self.assertAlmostEqual(mutual_information(joint,p),I)
    def test_takeover(self):
        self.assertAlmostEqual(capacity(assistance_channel(1,1))['value'],0)
        self.assertAlmostEqual(capacity(assistance_channel(1,0))['value'],math.log(3))
        self.assertAlmostEqual(mutual_information(assistance_channel(1,0),[1,0,0]),0)
    def test_threshold_and_strict_boundary(self):
        self.assertEqual(threshold_prefix([1,1],0)['accepted'],0)
        self.assertEqual(threshold_prefix([.9,.8,.1],1)['accepted'],2)
        result=threshold_prefix([.5],math.log(2))
        self.assertEqual(result['accepted'],0)
        self.assertAlmostEqual(result['sequence_floor'],.5)

if __name__=='__main__':unittest.main()
