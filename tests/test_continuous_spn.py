import tensorflow as tf
from tensorflow import test as tftest

from tests.utils import get_continuous_data
from tests.utils import get_continuous_model
from tests.utils import normal_leafs
from tests.utils import product0_out
from tests.utils import product1_out
from tests.utils import root_out
from tests.utils import sum0_out

tf.config.experimental_run_functions_eagerly(True)


class TestContinuousSPN(tftest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spn = get_continuous_model()
        cls.data = get_continuous_data()

    def _compute_until(self, x, name):
        for layer in self.spn.layers:
            x = layer(x)
            if layer.name == name:
                return tf.exp(x)

    def test_normal_leafs(self):
        got = self._compute_until(self.data, "normal_leaf")
        expected = normal_leafs(self.data)
        self.assertAllClose(got, expected)

    def test_prod0(self):
        got = self._compute_until(self.data, "dense_product")
        expected = product0_out(normal_leafs(self.data))
        self.assertAllClose(got, expected)

    def test_sum0(self):
        got = self._compute_until(self.data, "dense_sum")
        expected = sum0_out(product0_out(normal_leafs(self.data)))
        self.assertAllClose(got, expected)

    def test_product1(self):
        got = self._compute_until(self.data, "dense_product_1")
        expected = product1_out(sum0_out(product0_out(normal_leafs(self.data))))
        self.assertAllClose(got, expected)

    def test_root(self):
        got = tf.exp(self.spn(self.data))
        expected = root_out(
            product1_out(sum0_out(product0_out(normal_leafs(self.data))))
        )
        self.assertAllClose(got, expected)
