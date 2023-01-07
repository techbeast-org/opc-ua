#Simple Python OPC-UA Client
#code repository at https://github.com/techbeast-org/opc-ua
#LGPL-3.0 License

import asyncio
import logging
from asyncua import Client, Node, ua
logger = logging.getLogger('asyncua')
logging.disable(logging.WARNING)

data_variables = ["temperature","pressure","pumpsetting"]


async def dict_format(keys, values):
  return dict(zip(keys, values))

async def main():
    while True:
        url = "opc.tcp://<OPC-SERVER-IP-ADDRESS>:4840/opcua/"
        async with Client(url=url) as client:
            data_list = []
            namespace = "mynamespace"
            idx = await client.get_namespace_index(namespace)
            for i in range(len(data_variables)):
                myvar = await client.nodes.root.get_child(["0:Objects", "{}:vPLC".format(idx), "{}:{}".format(idx,data_variables[i])])
                val = await myvar.get_value()
                data_list.append(val)
            # _list = data_list
            print(await dict_format(data_variables,data_list))
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())