import asyncio
from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters
from typing import Any, List, Optional, Tuple, Callable

from .msgs import *
from .spec import TopicSpecs, CommandTopicSpecs


class BotCommands(Node):
    def __init__(self,
                 bot_id: str,
                 host: str = 'localhost',
                 port: int = 1883,
                 username: str = '',
                 password: str = '',
                 namespace: str = 'hbot',
                 **kwargs
                 ):
        self._bot_id = bot_id
        self._ns = namespace

        topic_prefix = TopicSpecs.PREFIX.format(
            namespace=self._ns,
            instance_id=self._bot_id
        )
        self._start_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.START}'
        self._stop_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.STOP}'
        self._import_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.IMPORT}'
        self._config_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.CONFIG}'
        self._status_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.STATUS}'
        self._history_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.HISTORY}'
        self._full_report_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.FULL_REPORT}'
        self._balance_limit_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.BALANCE_LIMIT}'
        self._balance_paper_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.BALANCE_PAPER}'
        self._command_shortcut_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.COMMAND_SHORTCUT}'
        self._cancel_orders_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.ORDERS_CANCEL}'
        self._place_limit_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.PLACE_LIMIT}'
        self._trading_pairs_uri = f'{topic_prefix}{TopicSpecs.COMMANDS.TRADING_PAIRS}'

        conn_params = ConnectionParameters(
            host=host,
            port=int(port),
            username=username,
            password=password
        )

        super().__init__(
            node_name=f'{self._ns}.{self._bot_id}',
            connection_params=conn_params,
            heartbeats=False,
            debug=True,
            **kwargs
        )
        self._init_clients()
        self.run()

    def _init_clients(self):
        self._start_cmd = self.create_rpc_client(
            msg_type=StartCommandMessage,
            rpc_name=self._start_uri
        )
        # print(f'[*] Created RPC client for start command @ {self._start_uri}')
        self._stop_cmd = self.create_rpc_client(
            msg_type=StopCommandMessage,
            rpc_name=self._stop_uri
        )
        # print(f'[*] Created RPC client for stop command @ {self._stop_uri}')
        self._import_cmd = self.create_rpc_client(
            msg_type=ImportCommandMessage,
            rpc_name=self._import_uri
        )
        # print(f'[*] Created RPC client for import command @ {self._import_uri}')
        self._config_cmd = self.create_rpc_client(
            msg_type=ConfigCommandMessage,
            rpc_name=self._config_uri
        )
        # print(f'[*] Created RPC client for config command @ {self._config_uri}')
        self._status_cmd = self.create_rpc_client(
            msg_type=StatusCommandMessage,
            rpc_name=self._status_uri
        )
        # print(f'[*] Created RPC client for status command @ {self._status_uri}')
        self._history_cmd = self.create_rpc_client(
            msg_type=HistoryCommandMessage,
            rpc_name=self._history_uri
        )
        self._full_report_cmd = self.create_rpc_client(
            msg_type=FullReportCommandMessage,
            rpc_name=self._full_report_uri
        )
        # print(f'[*] Created RPC client for history command @ {self._history_uri}')
        self._balance_limit_cmd = self.create_rpc_client(
            msg_type=BalanceLimitCommandMessage,
            rpc_name=self._balance_limit_uri
        )
        # print(f'[*] Created RPC client for balance limit command @ {self._balance_limit_uri}')
        self._balance_paper_cmd = self.create_rpc_client(
            msg_type=BalancePaperCommandMessage,
            rpc_name=self._balance_paper_uri
        )
        # print(f'[*] Created RPC client for balance limit command @ {self._balance_limit_uri}')
        self._command_shortcut_cmd = self.create_rpc_client(
            msg_type=CommandShortcutMessage,
            rpc_name=self._command_shortcut_uri
        )
        # print(f'[*] Created RPC client for command shortcuts @ {self._command_shortcut_uri}')
        self._cancel_orders_cmd = self.create_rpc_client(
            msg_type=CancelOrdersCommandMessage, rpc_name=self._cancel_orders_uri
        )
        # print(f'[*] Created RPC client for cancel orders command @ {self._cancel_orders_uri}')
        self._place_limit_cmd = self.create_rpc_client(
            msg_type=PlaceLimitCommandMessage, rpc_name=self._place_limit_uri
        )
        # print(f'[*] Created RPC client for place limit command @ {self._place_limit_uri}')
        self._trading_pairs_cmd = self.create_rpc_client(
            msg_type=TradingPairsCommandMessage, rpc_name=self._trading_pairs_uri
        )
        # print(f'[*] Created RPC client for trading pairs command @ {self._trading_pairs_uri}')

    def start(self,
              log_level: str = None,
              script: str = None,
              conf: str = None,
              async_backend: bool = False,
              timeout: int = 5
              ):
        resp = self._start_cmd.call(
            msg=StartCommandMessage.Request(
                log_level=log_level,
                script=script,
                conf=conf,
                async_backend=async_backend
            ),
            timeout=timeout
        )
        return resp

    def stop(self,
             skip_order_cancellation: bool = False,
             async_backend: bool = False,
             timeout: int = 5
             ):
        resp = self._stop_cmd.call(
            msg=StopCommandMessage.Request(
                skip_order_cancellation=skip_order_cancellation,
                async_backend=async_backend
            ),
            timeout=timeout
        )
        return resp

    def import_strategy(self,
                        strategy: str,
                        timeout: int = 5
                        ):
        resp = self._import_cmd.call(
            msg=ImportCommandMessage.Request(strategy=strategy),
            timeout=timeout
        )
        return resp

    def config(self,
               params: List[Tuple[str, Any]],
               timeout: int = 5
               ):
        resp = self._config_cmd.call(
            msg=ConfigCommandMessage.Request(params=params),
            timeout=timeout
        )
        return resp

    def status(self,
               async_backend: bool = False,
               timeout: int = 5
               ):
        resp = self._status_cmd.call(
            msg=StatusCommandMessage.Request(async_backend=async_backend),
            timeout=timeout
        )
        return resp

    def history(self,
                async_backend: bool = False,
                timeout: int = 5
                ):
        resp = self._history_cmd.call(
            msg=HistoryCommandMessage.Request(async_backend=async_backend),
            timeout=timeout
        )
        return resp

    def full_report(self,
                async_backend: bool = False,
                timeout: int = 20,
                days: int = 10,
                ):
        resp = (self._full_report_cmd.call(
            msg=FullReportCommandMessage.Request(async_backend=async_backend, days=days),
            timeout=timeout
        ))

        return resp

    def balance_limit(self,
                      exchange: str,
                      asset: str,
                      amount: float,
                      timeout: int = 5
                      ):
        resp = self._balance_limit_cmd.call(
            msg=BalanceLimitCommandMessage.Request(
                exchange=exchange,
                asset=asset,
                amount=amount
            ),
            timeout=timeout
        )
        return resp

    def balance_paper(self,
                      asset: str,
                      amount: float,
                      timeout: int = 5
                      ):
        resp = self._balance_paper_cmd.call(
            msg=BalancePaperCommandMessage.Request(
                asset=asset,
                amount=amount
            ),
            timeout=timeout
        )
        return resp

    def shortcut(self,
                 params=List[List[Any]],
                 timeout: int = 5
                 ):
        resp = self._command_shortcut_uri.call(
            msg=CommandShortcutMessage.Request(
                params=params
            ),
            timeout=timeout
        )
        return resp

    def cancel_orders(self, timeout: int = 5):
        resp = self._cancel_orders_cmd.call(
            msg=CancelOrdersCommandMessage.Request(), timeout=timeout
        )
        return resp

    def place_limit_order(
        self,
        exchange: str,
        trading_pair: str,
        amount: Decimal,
        price: Decimal,
        side: TradeType,
        timeout: int = 5,
    ):
        resp = self._place_limit_cmd.call(
            msg=PlaceLimitCommandMessage.Request(
                exchange=exchange,
                trading_pair=trading_pair,
                amount=amount,
                price=price,
                side=side.value,
            ),
            timeout=timeout,
        )
        return resp

    def trading_pairs(self, exchanges: List[str], timeout: int = 5):
        resp = self._trading_pairs_cmd.call(
            msg=TradingPairsCommandMessage.Request(exchanges=exchanges), timeout=timeout
        )
        return resp
