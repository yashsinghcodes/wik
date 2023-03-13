#!/usr/bin/env python3
import unittest

from wik import info


class FetchTest(unittest.TestCase):
    def getSummary(self):
        result = info.getSummary("Linux")
        self.assertEqual(
            result,
            """-------------------------------------------------------Linux--------------------------------------------------------

Linux (/ˈlinʊks/ (listen) LEEN-uuks or /ˈlɪnʊks/ LIN-uuks) is a family of open-source Unix-like operating systems based on the Linux kernel, an operating system kernel first released on September 17, 1991, by Linus Torvalds. Linux is typically packaged in a Linux distribution.


Distributions include the Linux kernel and supporting system software and libraries, many of which are provided by the GNU Project. Many Linux distributions use the word "Linux" in their name, but the Free Software Foundation uses the name "GNU/Linux" to emphasize the importance of GNU software, causing some controversy.""",
        )
