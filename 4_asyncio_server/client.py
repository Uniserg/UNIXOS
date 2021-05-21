import asyncio

HOST = 'localhost'
PORT = 9095


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    while True:
        try:
            message = input('Введите сообщение:')
            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(100)
            print(f'Получено: {data.decode()!r}')
        except ConnectionResetError:
            writer.close()
            break

asyncio.run(tcp_echo_client())

