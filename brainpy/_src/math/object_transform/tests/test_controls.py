# -*- coding: utf-8 -*-

import unittest
from functools import partial

import jax
from absl.testing import parameterized
from jax._src import test_util as jtu

import brainpy as bp
import brainpy.math as bm


class TestLoop(parameterized.TestCase):
  def test_make_loop(self):
    def make_node(v1, v2):
      def update(x):
        v1.value = v1 * x
        return (v1 + v2) * x

      return update

    bp.math.random.seed()
    _v1 = bm.Variable(bm.random.normal(size=10))
    _v2 = bm.Variable(bm.random.random(size=10))
    _xs = bm.random.uniform(size=(4, 10))

    scan_f = bm.make_loop(make_node(_v1, _v2),
                          dyn_vars=(_v1, _v2),
                          out_vars=(_v1,),
                          has_return=True)
    outs, returns = scan_f(_xs)
    for out in outs:
      print(out.shape)
    print(outs)
    print(returns.shape)
    print(returns)

    print('-' * 20)
    scan_f = bm.make_loop(make_node(_v1, _v2),
                          dyn_vars=(_v1, _v2),
                          out_vars=_v1,
                          has_return=True)
    outs, returns = scan_f(_xs)
    print(outs.shape)
    print(outs)
    print(returns.shape)
    print(returns)

    print('-' * 20)
    scan_f = bm.make_loop(make_node(_v1, _v2),
                          dyn_vars=(_v1, _v2),
                          has_return=True)
    outs, returns = scan_f(_xs)
    print(outs)
    print(returns.shape)
    print(returns)

  def test_make_loop_jaxarray(self):
    def make_node(v1, v2):
      def update(x):
        v1.value = v1 * x
        return (v1 + v2) * x

      return update

    bp.math.random.seed()
    _v1 = bm.Variable(bm.random.normal(size=10))
    _v2 = bm.as_variable(bm.random.random(size=10))
    _xs = bm.random.uniform(size=(4, 10))

    scan_f = bm.make_loop(make_node(_v1, _v2),
                          dyn_vars=(_v1, _v2),
                          out_vars=(_v1,),
                          has_return=True)
    # with self.assertRaises(bp.errors.MathError):
    outs, returns = scan_f(_xs)

  @parameterized.named_parameters(
    {"testcase_name": "_jit_scan={}_jit_f={}_unroll={}".format(jit_scan, jit_f, unroll),
     "jit_scan": jit_scan,
     "jit_f": jit_f,
     "unroll": unroll}
    for jit_scan in [False, True]
    for jit_f in [False, True]
    for unroll in [1, 2]
  )
  def test_for_loop(self, jit_scan, jit_f, unroll):
    rng = bm.random.RandomState(123)

    c = bm.Variable(rng.randn(4))
    d = rng.randn(2)
    all_a = rng.randn(5, 3)

    def f(a):
      assert a.shape == (3,)
      assert c.shape == (4,)
      b = bm.cos(bm.sum(bm.sin(a)) + bm.sum(bm.cos(c)) + bm.sum(bm.tan(d)))
      c.value = bm.sin(c * b)
      assert b.shape == ()
      return b

    if jit_f:
      f = bm.jit(f)
    scan = partial(bm.for_loop, f, unroll=unroll, )
    if jit_scan:
      scan = bm.jit(scan)
    ans = scan(operands=all_a)
    print(ans)
    print(c)


class TestIfElse(unittest.TestCase):
  def test1(self):
    def f(a):
      return bm.ifelse(conditions=[a > 10, a > 5, a > 2, a > 0],
                       branches=[lambda _: 1,
                                 lambda _: 2,
                                 lambda _: 3,
                                 lambda _: 4,
                                 lambda _: 5])

    self.assertTrue(f(3) == 3)
    self.assertTrue(f(1) == 4)
    self.assertTrue(f(-1) == 5)

  def test2(self):
    def f(a):
      return bm.ifelse(conditions=[a > 10, a > 5, a > 2, a > 0],
                       branches=[1, 2, 3, 4, 5])

    self.assertTrue(f(3) == 3)
    self.assertTrue(f(1) == 4)
    self.assertTrue(f(-1) == 5)

  def test_dyn_vars1(self):
    var_a = bm.Variable(bm.zeros(1))

    def f(a):
      def f1(_):
        var_a.value += 1
        return 1

      return bm.ifelse(conditions=[a > 10, a > 5, a > 2, a > 0],
                       branches=[f1,
                                 lambda _: 2, lambda _: 3,
                                 lambda _: 4, lambda _: 5],
                       dyn_vars=var_a,
                       show_code=True)

    self.assertTrue(f(11) == 1)
    print(var_a)
    self.assertTrue(bm.all(var_a == 1))
    self.assertTrue(f(1) == 4)
    self.assertTrue(f(-1) == 5)

  def test_vmap(self):
    from jax import vmap

    def f(operands):
      f = lambda a: bm.ifelse(conditions=[a > 10, a > 5, a > 2, a > 0],
                              branches=[lambda _: 1,
                                        lambda _: 2,
                                        lambda _: 3,
                                        lambda _: 4,
                                        lambda _: 5, ],
                              operands=a,
                              show_code=True)
      return vmap(f)(operands)

    r = f(bm.random.randint(-20, 20, 200))
    self.assertTrue(r.size == 200)

  def test_vmap2(self):
    from jax import vmap

    def f2():
      f = lambda a: bm.ifelse(conditions=[a > 10, a > 5, a > 2, a > 0],
                              branches=[1, 2, 3, 4, lambda _: 5],
                              operands=a,
                              show_code=True)
      return vmap(f)(bm.random.randint(-20, 20, 200))

    self.assertTrue(f2().size == 200)


class TestWhile(bp.testing.UnitTestCase):
  def test1(self):
    a = bm.Variable(bm.zeros(1))
    b = bm.Variable(bm.ones(1))

    def cond(x, y):
      return x < 6.

    def body(x, y):
      a.value += x
      b.value *= y
      return x + b[0], y + 1.

    res = bm.while_loop(body, cond, operands=(1., 1.))
    print()
    print(res)

  def test2(self):
    a = bm.Variable(bm.zeros(1))
    b = bm.Variable(bm.ones(1))

    def cond(x, y):
      return x < 6.

    def body(x, y):
      a.value += x
      b.value *= y
      return x + b[0], y + 1.

    res = bm.while_loop(body, cond, operands=(1., 1.))
    print()
    print(res)

    with jax.disable_jit():
      a = bm.Variable(bm.zeros(1))
      b = bm.Variable(bm.ones(1))

      res2 = bm.while_loop(body, cond, operands=(1., 1.))
      self.assertTrue(bm.array_equal(res2[0], res[0]))
      self.assertTrue(bm.array_equal(res2[1], res[1]))

