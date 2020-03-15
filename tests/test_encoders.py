from unittest import TestCase

from urls.encoders import SequentialEncoder


class TestSequentialEncoder(TestCase):
    def test_encode_uses_seed_to_create_the_encoded_representation(self):
        representation_1 = SequentialEncoder().encode(1)
        representation_2 = SequentialEncoder().encode(1)
        representation_3 = SequentialEncoder().encode(2)
        self.assertEqual(representation_1, representation_2)
        self.assertNotEqual(representation_1, representation_3)

    def test_decode_obtains_seed_correctly(self):
        for seed in range(0, 10):
            representation = SequentialEncoder().encode(seed)
            decoded_seed = SequentialEncoder().decode(representation)
            self.assertEqual(seed, decoded_seed)
