from unittest import TestCase

from hummingbot.connector.exchange.lambdaplex import lambdaplex_constants as CONSTANTS


class LambdaplexConstantsTests(TestCase):
    def test_private_rate_limit_pools_match_lambdaplex_defaults(self):
        rate_limits = {rate_limit.limit_id: rate_limit for rate_limit in CONSTANTS.RATE_LIMITS}

        self.assertEqual(12_000, rate_limits[CONSTANTS.REQUEST_WEIGHT].limit)
        self.assertEqual(12_000, rate_limits[CONSTANTS.API_KEY_REQUESTS_WEIGHT].limit)
        self.assertEqual(2_000, rate_limits[CONSTANTS.ORDERS_WEIGHT].limit)
        self.assertEqual(
            {
                CONSTANTS.REQUEST_WEIGHT,
                CONSTANTS.API_KEY_REQUESTS_WEIGHT,
                CONSTANTS.ORDERS_WEIGHT,
            },
            {linked_limit.limit_id for linked_limit in rate_limits[CONSTANTS.ORDER_PATH_URL].linked_limits},
        )
