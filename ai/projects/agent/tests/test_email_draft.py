import inspect
import os
import unittest

from mock_email_tool import MockEmailAgent, MockEmailToolSpec, sequence_dict
from pi_log import getLogger

from qai.agent import ROOT_DIR

log = getLogger(__name__, level="INFO", init_basic_config=True)

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(ROOT_DIR)))


class TestEmail(unittest.TestCase):

    def test_emailagent(self):
        sequence_id = f"seq_{inspect.stack()[0][3]}"
        from_person = {
            "name": "Maya",
            "email": "jane.doe@example.com",
            "title": "VP of Engineering",
        }
        from_company = {
            "name": "Example Corp",
            "url": "https://example.com",
            "industry": "Software and Consulting",
        }
        to_persons = [
            {
                "name": "Zachary",
                "email": "zach.doe@example.com",
                "title": "Software Engineer",
            }
        ]

        ets = MockEmailToolSpec(from_person, from_company)
        ea: MockEmailAgent = MockEmailAgent.create(
            tools=ets.to_tool_list(), email_tool_spec_cls=MockEmailToolSpec
        )
        ## convert list of dict to dict of dict
        to_people = {to_person["name"]: to_person for to_person in to_persons}
        emails = ea.create_emails(
            sequence_id=sequence_id,
            from_person=from_person,
            from_company=from_company,
            to_people=to_people,
            use_async_on=None,
        )
        log.debug(f"emails = {emails}")
        self.assertEqual(len(emails), 1)
        self.assertTrue(sequence_id in sequence_dict)
        self.assertTrue("on_email_complete" in sequence_dict[sequence_id])
        self.assertTrue("on_all_emails_complete" in sequence_dict[sequence_id])


if __name__ == "__main__":
    testmethod = ""
    if testmethod:
        suite = unittest.TestSuite()
        suite.addTest(TestEmail(testmethod))
        runner = unittest.TextTestRunner().run(suite)
    else:
        unittest.main()
