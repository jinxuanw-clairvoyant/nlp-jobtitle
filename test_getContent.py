from unittest import TestCase

from _pytest import unittest

from getContent import getContent


class TestGetContent(TestCase):
    def test_getContent(self):
        print getContent([(1,
                           'http://www.onetonline.org/link/result/11-1021.00?c=tk&n_tk=0&e_tk=1&c_tk=50&s_tk=IM&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_cx=10&c_cx=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go')])

    def test_getContent2(self):
        print getContent([(2,
                           'http://www.onetonline.org/link/result/11-1031.00?c=ta&n_ta=0&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_wc=10&c_wc=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go')]
                         )

    def test_getContent3(self):
        print getContent([(1, u'http://www.onetonline.org/link/result/11-3071.01?c=tk&n_tk=0&e_tk=1&c_tk=50&s_tk=IM&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_cx=10&c_cx=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go'), (1, u'http://www.onetonline.org/link/result/11-3071.02?c=tk&n_tk=0&e_tk=1&c_tk=50&s_tk=IM&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_cx=10&c_cx=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go'), (1, u'http://www.onetonline.org/link/result/11-3071.03?c=tk&n_tk=0&e_tk=1&c_tk=50&s_tk=IM&n_tt=20&s_tt=s&e_tt=L&e_tt=C&n_kn=10&c_kn=50&s_kn=IM&n_sk=10&c_sk=50&s_sk=IM&n_ab=10&c_ab=50&s_ab=IM&n_wa=10&c_wa=50&s_wa=IM&n_dw=10&a_iw=g&a_iw=i&a_iw=d&a_iw=t&n_cx=10&c_cx=50&c_in=50&n_ws=10&c_ws=50&c_wv=50&n_wn=10&c_wn=50&n_cw=10&s_cw=CIP&g=Go')]
)


if __name__ == '__main__':
    unittest.main()