import unittest
from advanced_crm import AdvancedCRMAgent

class TestAdvancedCRMAgent(unittest.TestCase):

    def setUp(self):
        self.agent = AdvancedCRMAgent()

    def test_run_lead_scoring(self):
        result = self.agent.run_lead_scoring()
        self.assertEqual(result['status'], 'success')
        self.assertIn('Lead scoring completed successfully', result['message'])

    def test_predict_churn(self):
        result = self.agent.predict_churn()
        self.assertEqual(result['status'], 'success')
        self.assertIn('Customer churn prediction completed successfully', result['message'])

if __name__ == '__main__':
    unittest.main()
