from twitter_stats import *
stats_obj = TweetCount()


followers_mock_dict = {"ids": [465638, 65884878, 848743]}

import unittest

from mock import Mock, patch

class UtilsTestCase(unittest.TestCase):
    def test_get_followers_id(self):
        user = self.user = Mock()
        user.email = 'user@example.com'
        with patch('twitter_stats.requests') as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = followers_mock_dict
            results = stats_obj.get_followers_ids()
            self.assertEqual(results['ids'], followers_mock_dict['ids'])

if __name__ == '__main__':
    unittest.main()