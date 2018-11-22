import unittest
from process_csv import NormalizeCSV

class MyTest(unittest.TestCase):
  def testZipCodes(self):
    self.assertEqual(NormalizeCSV.prefixZipCode(None, "436"), "00436")

  def testTimestampPSTtoEST(self):
    self.assertEqual(NormalizeCSV.timestampPSTtoEST(None, "10/2/04 8:44:11 AM"), "2004-10-02T11:44:11")

  def testUnicodeValidation(self):
    self.assertEqual(NormalizeCSV.getDeltaTime(None, "21:23:32.123").total_seconds(), .123 + 32 + (23 * 60) + (21 * 60 * 60))

if __name__ == '__main__':
  unittest.main()
