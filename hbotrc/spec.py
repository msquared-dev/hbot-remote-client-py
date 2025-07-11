from enum import Enum


class CommandTopicSpecs:
    START: str = '/start'
    STOP: str = '/stop'
    CONFIG: str = '/config'
    IMPORT: str = '/import'
    STATUS: str = '/status'
    HISTORY: str = '/history'
    FULL_REPORT: str = '/full_report'
    BALANCE_LIMIT: str = '/balance/limit'
    BALANCE_PAPER: str = '/balance/paper'
    COMMAND_SHORTCUT: str = '/command_shortcuts'
    ORDERS_CANCEL: str = "/orders/cancel_all"
    PLACE_LIMIT: str = "/orders/place_limit"
    TRADING_PAIRS: str = "/trading_pairs"


class TopicSpecs:
    PREFIX: str = '{namespace}/{instance_id}'
    COMMANDS: CommandTopicSpecs = CommandTopicSpecs()
    LOGS: str = '/log'
    MARKET_EVENTS: str = '/events'
    NOTIFICATIONS: str = '/notify'
    HEARTBEATS: str = '/hb'
    EXTERNAL_EVENTS: str = '/external/event/*'

class TradeType(Enum):
    BUY = 1
    SELL = 2
    RANGE = 3
