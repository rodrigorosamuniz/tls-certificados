import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.generate_certs import generate_localhost_certificates
from scripts.inspect_cert import inspect_certificate


class InspectCertificateTest(unittest.TestCase):
    def test_extracts_subject_issuer_san_and_dates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = generate_localhost_certificates(Path(temp_dir))

            details = inspect_certificate(paths.server_cert)

            self.assertIn("localhost", details["subject"])
            self.assertIn("IP Address:127.0.0.1", details["subject_alternative_name"])
            self.assertIn("not_before", details)
            self.assertIn("not_after", details)
            self.assertIn("issuer", details)


if __name__ == "__main__":
    unittest.main()
