import os
import unittest
from unittest.mock import patch, Mock

from src import post_to_patreon


class TestCampaignDiscovery(unittest.TestCase):

    def setUp(self):
        # ensure we run in network mode (so code tries to discover campaign)
        os.environ['PATREON_API_KEY'] = 'fake-token'
        os.environ.pop('CAMPAIGN_ID', None)

    def tearDown(self):
        os.environ.pop('PATREON_API_KEY', None)
        os.environ.pop('CAMPAIGN_ID', None)

    @patch('src.post_to_patreon.requests.post')
    @patch('src.post_to_patreon.requests.get')
    def test_discover_campaign_in_relationships(self, mock_get, mock_post):
        # identity response that references campaign under data.relationships
        identity = {
            'data': {
                'id': 'user1',
                'type': 'user',
                'relationships': {
                    'campaigns': {'data': [{'type': 'campaign', 'id': '98765'}]}
                }
            },
            'included': []
        }

        mock_get.return_value = Mock(status_code=200, json=lambda: identity)
        mock_post.return_value = Mock(status_code=201, json=lambda: {'data': {'id': 'post1'}})

        result = post_to_patreon.post_audio('test.mp3', 'Test', 'Desc')

        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('status'), 201)
        # debug should show discovery path
        self.assertIn('campaign_discovery', result.get('debug', {}))
        self.assertEqual(result['debug']['campaign_discovery'].get('from_relationships'), '98765')


if __name__ == '__main__':
    unittest.main()
