#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2022-11-30
# @Filename: server.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import asyncio


async def server_handler(reader, writer):

    filter_pos = 0

    while True:
        data_bytes = await reader.readline()
        data_str = data_bytes.decode().strip()

        if data_str == "":
            continue
        try:
            if data_str.startswith("home"):
                await asyncio.sleep(10)
                writer.write(b"Filter Wheel has homed\n")
                filter_pos = 0
            elif data_str.startswith("move"):
                if len(data_str.split()) >= 2:
                    try:
                        if int(data_str.split()[1]) not in range(0, 6):
                            raise Exception('Invalid position number. Position numbers range from 0 to 5.\n')
                        filter_pos = int(data_str.split()[1])
                        message = f"moved to filter position {data_str.split()[1]}\n"
                        writer.write(message.encode('utf-8'))
                    except ValueError:
                        writer.write(b"""Invalid position character. 
                                        Position character must be a number range from 0 to 5.\n""")
                else:
                    writer.write(b'Error while moving filter wheel.\n')
            elif data_str.startswith('getFilter'):
                message = f"moved to filter position {filter_pos}\n"
                writer.write(message.encode('utf-8'))
                
            else:
                writer.write(b"Invalid\n")
        except Exception as err:
            writer.write(str(err).encode() + b'\n')
        writer.drain()


async def main():
    server = await asyncio.start_server(server_handler, host="0.0.0", port=5503)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
