import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.generate_certs import CertificatePaths, generate_localhost_certificates


class GenerateCertificatesTest(unittest.TestCase):
    def test_generates_ca_server_certificate_and_key(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = generate_localhost_certificates(Path(temp_dir))

            self.assertIsInstance(paths, CertificatePaths)
            self.assertTrue(paths.ca_key.exists())
            self.assertTrue(paths.ca_cert.exists())
            self.assertTrue(paths.server_key.exists())
            self.assertTrue(paths.server_csr.exists())
            self.assertTrue(paths.server_cert.exists())
            self.assertTrue(paths.server_ext.exists())

    def test_server_certificate_contains_localhost_san(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = generate_localhost_certificates(Path(temp_dir))

            result = subprocess.run(
                ["openssl", "x509", "-in", str(paths.server_cert), "-noout", "-text"],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("DNS:localhost", result.stdout)
            self.assertIn("IP Address:127.0.0.1", result.stdout)


if __name__ == "__main__":
    unittest.main()
