import json
import subprocess
import time
import unittest
import urllib.request
import urllib.error


class TestMyApp(unittest.TestCase):
    process = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.process = subprocess.Popen(["python3", "main.py"], stdout=subprocess.PIPE)
        retries = 0
        while retries < 10:
            result = cls.process.stdout.readline().decode().strip()
            if result == 'Ready':
                break
            else:
                retries += 1
                time.sleep(1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.process.kill()
        cls.process.wait()

    def test_100_usd(self):
        s = type(self).process.stdout
        print(s)
        with urllib.request.urlopen("http://localhost:5000/?usd_amount=100") as response:
            result = json.loads(response.read())
            self.assertEqual(response.status, 200)
            self.assertIn('usd_rur_rate', result)
            self.assertIn('usd_amount', result)
            self.assertIn('rur_amount', result)

    def test_errors(self):
        s = type(self).process.stdout
        print(s)
        with urllib.request.urlopen("http://localhost:5000/?usd_amount=string") as response:
            result = json.loads(response.read())
            self.assertDictEqual({
                "error": "usd_amount must be a number"
            }, result)

        with urllib.request.urlopen("http://localhost:5000/") as response:
            result = json.loads(response.read())
            self.assertDictEqual({
                "error": "usd_amount is required"
            }, result)

    def test_404(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            with urllib.request.urlopen("http://localhost:5000/not_exist"):
                pass
        self.assertEqual(cm.exception.code, 404)


if __name__ == '__main__':
    unittest.main()
