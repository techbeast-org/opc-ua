#Simple Python OPC-UA Server
#Sending out 2 data values
#code repository at https://github.com/techbeast-org/opc-ua
#LGPL-3.0 License

import asyncio
import random
from asyncua import ua, Server
from asyncua.common.methods import uamethod
import logging

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


# class SubHandler(object):

#     """
#     Subscription Handler. To receive events from server for a subscription
#     """

#     def datachange_notification(self, node, val, data):
#         _logger.warn("Python: New data change event %s %s", node, val)

#     def event_notification(self, event):
#         _logger.warn("Python: New event %s", event)

async def main():
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://<IP-ADDRESS>:4840/opcua/')    # put your Raspberry pi IP if you are running it in a raspberry pi
    server.set_server_name("DevNet OPC-UA Test Server")

    # setup our own namespace, not really necessary but should as spec
    idx = await server.register_namespace("mynamespace")

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    obj_vplc = await server.nodes.objects.add_object(idx, 'vPLC')
    var_temperature = await obj_vplc.add_variable(idx, 'temperature', 0)
    var_pressure = await obj_vplc.add_variable(idx, 'pressure', 0)
    var_pumpsetting = await obj_vplc.add_variable(idx, 'pumpsetting', 0)
    _logger.info("starting server...")
    # handler = SubHandler()
    # sub = await server.create_subscription(500, handler)   
    # await sub.subscribe_data_change(var_temperature)

    async with server:
        # run forever every 5 secs
        while True:
                # Writing Variables
                await var_temperature.write_value(random.randint(25,35))
                await var_pressure.write_value(random.randint(55,75))
                await var_pumpsetting.write_value(random.randint(0,1))
                await asyncio.sleep(5)

if __name__ == '__main__':
    #python 3.6 or lower
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    #python 3.7 onwards (comment lines above)
    asyncio.run(main())