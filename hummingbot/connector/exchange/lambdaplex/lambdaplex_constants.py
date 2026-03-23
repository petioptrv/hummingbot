import os
import sys

from hummingbot.core.api_throttler.data_types import LinkedLimitWeightPair, RateLimit
from hummingbot.core.data_type.in_flight_order import OrderState

DEFAULT_DOMAIN = "com"

EXCHANGE_NAME = "lambdaplex"

REST_URL = os.getenv("LAMBDAPLEX_REST_URL", "https://api.lambdaplex.io/api/")
WSS_URL = os.getenv("LAMBDAPLEX_WSS_URL", "wss://api.lambdaplex.io/api/{}/ws")
API_VERSION = os.getenv("LAMBDAPLEX_API_VERSION", "v1")

ORDER_ID_MAX_LEN = 32
HBOT_ORDER_ID_PREFIX = ""

RECEIVE_WINDOW = 5000

# Public API endpoints
EXCHANGE_INFO_PATH_URL = "/exchangeInfo"
LAST_PRICE_URL = "/ticker/price"
SNAPSHOT_PATH_URL = "/depth"
SERVER_TIME_PATH_URL = "/time"
SERVER_AVAILABILITY_URL = "/ping"

LAST_PRICE_SINGLE_LIMIT = "LAST_PRICE_SINGLE"
LAST_PRICE_MULTI_LIMIT = "LAST_PRICE_MULTI"

SNAPSHOT_HUNDRED_LIMIT = "SNAPSHOT_100"
SNAPSHOT_FIVE_HUNDRED_LIMIT = "SNAPSHOT_500"
SNAPSHOT_THOUSAND_LIMIT = "SNAPSHOT_1_000"
SNAPSHOT_FIVE_THOUSAND_LIMIT = "SNAPSHOT_5_000"

# Private API endpoints
ACCOUNTS_PATH_URL = "/account"
MY_TRADES_PATH_URL = "/myTrades"
ORDER_PATH_URL = "/order"
USER_FEES_PATH_URL = "/account/commission"

# Rate limit IDs (non-path) for endpoints with variant weights
ORDER_QUERY_LIMIT = "ORDER_QUERY"

# Order States
ORDER_STATE = {
    "ACTIVE": OrderState.OPEN,
    "OPEN": OrderState.OPEN,
    "PARTIALLY_FILLED": OrderState.PARTIALLY_FILLED,
    "FILLED": OrderState.FILLED,
    "CANCELED": OrderState.CANCELED,
    "EXPIRED": OrderState.FAILED,
    "FAILED": OrderState.FAILED,
}

WS_HEARTBEAT_TIME_INTERVAL = 30

# WebSocket methods
WS_SESSION_LOGON_METHOD = "session.logon"
WS_SESSION_SUBSCRIBE_METHOD = "session.subscribe"

# WebSocket event types
DIFF_EVENT_TYPE = "depthUpdate"
TRADE_EVENT_TYPE = "trade"

# Rate Limit Type
REQUEST_WEIGHT = "REQUEST_WEIGHT"
API_KEY_REQUESTS_WEIGHT = "API_KEY_REQUESTS"
ORDERS_WEIGHT = "ORDERS"

# Rate Limit time intervals
ONE_MINUTE = 60
ONE_SECOND = 1

MAX_REQUEST = sys.maxsize


def _read_limit_from_env(var_name: str, default: int) -> int:
    raw_value = os.getenv(var_name)
    return default if raw_value is None else int(raw_value)


# Lambdaplex supports materially higher private order throughput than the generic exchange defaults
# this connector started from. Keep these buckets configurable for containerized/headless deployments.
REQUEST_WEIGHT_LIMIT_PER_MINUTE = _read_limit_from_env(
    "LAMBDAPLEX_REQUEST_WEIGHT_LIMIT_PER_MINUTE",
    12_000,
)
API_KEY_REQUESTS_LIMIT_PER_MINUTE = _read_limit_from_env(
    "LAMBDAPLEX_API_KEY_REQUESTS_LIMIT_PER_MINUTE",
    12_000,
)
ORDERS_LIMIT_PER_10_SECONDS = _read_limit_from_env(
    "LAMBDAPLEX_ORDERS_LIMIT_PER_10S",
    2_000,
)

RATE_LIMITS = [
    # Pools
    RateLimit(
        limit_id=REQUEST_WEIGHT,
        limit=REQUEST_WEIGHT_LIMIT_PER_MINUTE,
        time_interval=ONE_MINUTE,
    ),
    RateLimit(
        limit_id=API_KEY_REQUESTS_WEIGHT,
        limit=API_KEY_REQUESTS_LIMIT_PER_MINUTE,
        time_interval=ONE_MINUTE,
    ),
    RateLimit(
        limit_id=ORDERS_WEIGHT,
        limit=ORDERS_LIMIT_PER_10_SECONDS,
        time_interval=10 * ONE_SECOND,
    ),
    # Weighted Limits
    RateLimit(
        limit_id=EXCHANGE_INFO_PATH_URL,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 20),
        ],
    ),
    RateLimit(
        limit_id=LAST_PRICE_SINGLE_LIMIT,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 2),
        ],
    ),
    RateLimit(
        limit_id=LAST_PRICE_MULTI_LIMIT,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 4),
        ],
    ),
    RateLimit(
        limit_id=SNAPSHOT_HUNDRED_LIMIT,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 5),
        ],
    ),
    RateLimit(
        limit_id=SNAPSHOT_FIVE_HUNDRED_LIMIT,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 25),
        ],
    ),
    RateLimit(
        limit_id=SNAPSHOT_THOUSAND_LIMIT,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 50),
        ],
    ),
    RateLimit(
        limit_id=SNAPSHOT_FIVE_THOUSAND_LIMIT,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 250),
        ],
    ),
    RateLimit(
        limit_id=SERVER_TIME_PATH_URL,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 1),
        ],
    ),
    RateLimit(
        limit_id=SERVER_AVAILABILITY_URL,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 1),
        ],
    ),
    RateLimit(
        limit_id=ACCOUNTS_PATH_URL,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 20),
            LinkedLimitWeightPair(API_KEY_REQUESTS_WEIGHT, 20),
        ],
    ),
    RateLimit(
        limit_id=MY_TRADES_PATH_URL,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 20),
            LinkedLimitWeightPair(API_KEY_REQUESTS_WEIGHT, 20),
        ],
    ),
    RateLimit(
        limit_id=ORDER_PATH_URL,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 1),
            LinkedLimitWeightPair(API_KEY_REQUESTS_WEIGHT, 1),
            LinkedLimitWeightPair(ORDERS_WEIGHT, 1),
        ],
    ),
    # GET /order: query single order status (weight 4) but does not count against the orders bucket.
    RateLimit(
        limit_id=ORDER_QUERY_LIMIT,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 4),
            LinkedLimitWeightPair(API_KEY_REQUESTS_WEIGHT, 4),
        ],
    ),
    RateLimit(
        limit_id=USER_FEES_PATH_URL,
        limit=MAX_REQUEST,
        time_interval=ONE_MINUTE,
        linked_limits=[
            LinkedLimitWeightPair(REQUEST_WEIGHT, 20),
            LinkedLimitWeightPair(API_KEY_REQUESTS_WEIGHT, 20),
        ],
    ),
]
