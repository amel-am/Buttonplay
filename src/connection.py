from anyio import connect_tcp
from anyio.streams.buffered import BufferedByteReceiveStream
from loguru import logger


class Connection(object):
    def __init__(self, ip):
        self.ip = ip
        self.port = 6000

    async def send(self, send: str):
        """Args: send (str): The command to send to sysbotbase!"""
        try:
            async with await connect_tcp(remote_host=self.ip, remote_port=self.port) as client:
                await client.send(f"{send}\n".encode("utf-8"))
        except OSError as e:
            logger.error(f"Something didnt work out quite right:{e}")

    async def receive(self, send: str):
        """
        Receives and decodes the bytes.

        Sends a command to sysbotbase and then receives the bytes returned from sysbotbase, which get decoded along with returned.

        Parameters:
        send (str): The command to send to sysbotbase.

        Returns:
        str: Returns the decoded bytes.

        """
        try:
            async with await connect_tcp(remote_host=self.ip, remote_port=self.port) as client:
                await client.send(f"{send}\n".encode("utf-8"))
                Receive = bytes.decode(await BufferedByteReceiveStream(client).receive_until(b"\n", max_bytes=1000000), "utf-8")
                return Receive
        except OSError as e:
            logger.error(f"Something didnt work out quite right:{e}")
