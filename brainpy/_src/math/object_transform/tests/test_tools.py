import brainpy as bp
import brainpy.math as bm
import jax
from brainpy._src.math.object_transform._tools import evaluate_dyn_vars


class TestTool(bp.testing.UnitTestCase):
  def test1(self):
    neu = bp.neurons.HH((5,))
    call_num = [0]

    def f():
      bp.share.save(t=0., dt=0.1)
      neu.update()
      call_num[0] += 1

    vars1 = evaluate_dyn_vars(f)
    self.assertTrue(len(vars1) == len(neu.vars().unique()))
    self.assertTrue(call_num[0] == 1)
    for k, v in vars1.items():
      self.assertTrue(isinstance(v, bm.Variable))
      self.assertTrue(isinstance(v.value, jax.Array))

  def test_cache1(self):
    neu = bp.neurons.HH((5,))
    call_num = [0]

    def f():
      bp.share.save(t=0., dt=0.1)
      neu.update()
      call_num[0] += 1

    vars1 = evaluate_dyn_vars(f)
    self.assertTrue(len(vars1) == len(neu.vars().unique()))
    self.assertTrue(call_num[0] == 1)
    for k, v in vars1.items():
      self.assertTrue(isinstance(v, bm.Variable))
      self.assertTrue(isinstance(v.value, jax.Array))

    vars2 = evaluate_dyn_vars(f)  # using cache, do not call ``f`` again
    self.assertTrue(call_num[0] == 1)
    for k, v in vars2.items():
      self.assertTrue(isinstance(v, bm.Variable))
      self.assertTrue(isinstance(v.value, jax.Array))

  def test_nested_evaluate(self):
    neu = bp.neurons.HH((5,))
    a = bm.Variable(bm.ones(1))

    def f():
      bp.share.save(t=0., dt=0.1)
      neu.update()

    def f2():
      a[:] = 0.
      evaluate_dyn_vars(f)

    vars2 = evaluate_dyn_vars(f2)
    self.assertTrue(len(vars2) == len(neu.vars().unique()) + 1)
    for k, v in vars2.items():
      self.assertTrue(isinstance(v, bm.Variable))
      self.assertTrue(isinstance(v.value, jax.Array))
    self.assertTrue(isinstance(a, bm.Variable))
    self.assertTrue(isinstance(a.value, jax.Array))

  def test_cache2(self):
    neu = bp.neurons.HH((5,))
    a = bm.Variable(bm.ones(1))
    call_num = [0]

    def f():
      bp.share.save(t=0., dt=0.1)
      neu.update()
      call_num[0] += 1

    def f2():
      a[:] = 0.
      evaluate_dyn_vars(f)

    vars1 = evaluate_dyn_vars(f2)  # cache
    self.assertTrue(len(vars1) == len(neu.vars().unique()) + 1)
    for k, v in vars1.items():
      self.assertTrue(isinstance(v, bm.Variable))
      self.assertTrue(isinstance(v.value, jax.Array))
    self.assertTrue(isinstance(a, bm.Variable))
    self.assertTrue(isinstance(a.value, jax.Array))
    self.assertTrue(call_num[0] == 1)

    vars2 = evaluate_dyn_vars(f2)  # cache too
    self.assertTrue(call_num[0] == 1)

  def test_cache3(self):
    call_num = [0]

    class Model(bp.DynamicalSystemNS):
      def __init__(self):
        super().__init__()
        self.a = bm.Variable(bm.ones(1))

      def update(self, *args, **kwargs):
        self.a.value += 1
        call_num[0] += 1

    model = Model()
    evaluate_dyn_vars(model.update)
    self.assertTrue(call_num[0] == 1)

    evaluate_dyn_vars(model.update)  # cache
    self.assertTrue(call_num[0] == 1)

    evaluate_dyn_vars(Model().update)  # no cache
    self.assertTrue(call_num[0] == 2)




