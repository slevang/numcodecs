# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import numpy as np
from numpy.testing import assert_array_equal
from nose.tools import eq_ as eq, assert_is_instance


from numcodecs.delta import Delta
from numcodecs.tests.common import check_encode_decode
from numcodecs.registry import get_codec
from numcodecs.abc import Codec


# mix of dtypes: integer, float
# mix of shapes: 1D, 2D, 3D
# mix of orders: C, F
arrays = [
    np.arange(1000, dtype='i4'),
    np.linspace(1000, 1001, 1000, dtype='f8').reshape(100, 10),
    np.random.normal(loc=1000, scale=1, size=(10, 10, 10)),
    np.random.randint(0, 200, size=1000, dtype='u2').reshape(100, 10,
                                                             order='F'),
]


def test_encode_decode():
    for arr in arrays:
        codec = Delta(dtype=arr.dtype)
        check_encode_decode(arr, codec)


def test_encode():
    dtype = 'i8'
    astype = 'i4'
    codec = Delta(dtype=dtype, astype=astype)
    arr = np.arange(10, 20, 1, dtype=dtype)
    expect = np.array([10] + ([1] * 9), dtype=astype)
    actual = codec.encode(arr)
    assert_array_equal(expect, actual)
    eq(np.dtype(astype), actual.dtype)


def test_get_config():
    codec = Delta(dtype='<i4', astype='<i2')
    config = codec.get_config()
    eq(codec, get_codec(config))


def test_repr():
    expect = "Delta(dtype='<i4', astype='<i2')"
    codec = eval(expect)
    actual = repr(codec)
    eq(expect, actual)