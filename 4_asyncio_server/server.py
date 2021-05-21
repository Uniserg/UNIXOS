import asyncio

HOST = 'localhost'
PORT = 9095


async def handle_echo(reader, writer):
    while True:
        try:
            data = await reader.read(100)
            message = data.decode()
            addr = writer.get_extra_info('peername')

            print(f"Received {message!r} from {addr!r}")

            print(f"Send: {message!r}")
            writer.write(data)
            await writer.drain()
        except ConnectionResetError:
            print("Пользователь отключился")
            break


async def main():
    server = await asyncio.start_server(handle_echo, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()
asyncio.run(main())
