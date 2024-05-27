import unittest
import requests

from time import sleep
from rate_limiter import INTERVAL, RATE_LIMIT


class TestRateLimiter(unittest.TestCase):
    def test_configure(self):
        data = {INTERVAL: 30, RATE_LIMIT: 2}
        response = requests.post('http://127.0.0.1:5000/api/configure', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Interval and Rate limit configured successfully')

    def test_is_rate_limited(self):
        # Configure rate limit
        self.test_configure()

        # Make requests
        response1 = requests.get('http://127.0.0.1:5000/api/is_rate_limited/abc')
        self.assertEqual(response1.status_code, 200)
        self.assertFalse(response1.json()['is_rate_limited'])

        response2 = requests.get('http://127.0.0.1:5000/api/is_rate_limited/abc')
        self.assertEqual(response2.status_code, 200)
        self.assertFalse(response2.json()['is_rate_limited'])

        response3 = requests.get('http://127.0.0.1:5000/api/is_rate_limited/abc')
        self.assertEqual(response3.status_code, 200)
        self.assertTrue(response3.json()['is_rate_limited'])

        response4 = requests.get('http://127.0.0.1:5000/api/is_rate_limited/def')
        self.assertEqual(response4.status_code, 200)
        self.assertFalse(response4.json()['is_rate_limited'])

        response5 = requests.get('http://127.0.0.1:5000/api/is_rate_limited/def')
        self.assertEqual(response5.status_code, 200)
        self.assertFalse(response5.json()['is_rate_limited'])

        response6 = requests.get('http://127.0.0.1:5000/api/is_rate_limited/def')
        self.assertEqual(response6.status_code, 200)
        self.assertTrue(response6.json()['is_rate_limited'])

        # Wait until next interval before sending requests
        sleep(30)
        response7 = requests.get('http://127.0.0.1:5000/api/is_rate_limited/def')
        self.assertEqual(response7.status_code, 200)
        self.assertFalse(response4.json()['is_rate_limited'])

        response8 = requests.get('http://127.0.0.1:5000/api/is_rate_limited/def')
        self.assertEqual(response8.status_code, 200)
        self.assertFalse(response5.json()['is_rate_limited'])


if __name__ == '__main__':
    unittest.main()
