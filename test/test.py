#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from io import StringIO
from wik import info


class FetchTest(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_getSummary(self, mock_stdout):
        exp_result = """-----------------------------------------------------KISS_principle-----------------------------------------------------


KISS, an acronym for "Keep it simple, stupid!", is a design principle first noted by the U.S. Navy in 1960. First seen partly in American English by at least 1938, the KISS principle states that most systems work best if they are kept simple rather than made complicated; therefore, simplicity should be a key goal in design, and unnecessary complexity should be avoided. The phrase has been associated with aircraft engineer Kelly Johnson. The term "KISS principle" was in popular use by 1970. Variations on the phrase (usually as some euphemism for the more churlish "stupid") include "keep it super simple", "keep it simple, silly", "keep it short and simple", "keep it short and sweet", "keep it simple and straightforward", "keep it small and simple", "keep it simple, soldier", "keep it simple, sailor", "keep it simple, sweetie", "keep it stupidly simple", or "keep it sweet and simple".


The acronym was reportedly coined by Kelly Johnson, lead engineer at the Lockheed Skunk Works (creators of the Lockheed U-2 and SR-71 Blackbird spy planes, among many others). However, the variant "Keep it Short and Simple" is attested from a 1938 issue of the Minneapolis Star.


While popular usage has transcribed it for decades as "Keep it simple, stupid", Johnson transcribed it simply as "Keep it simple stupid" (no comma), and this reading is still used by many authors."""

        info.getSummary("KISS_principle")
        output = mock_stdout.getvalue()

        import re
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        cleaned_output = ansi_escape.sub('', output)
        cleaned_output = re.sub(r'\n+', '\n', cleaned_output).strip()
        self.assertEqual(cleaned_output, re.sub(r'\n+', '\n', exp_result).strip())

if __name__ == '__main__':
    unittest.main()
