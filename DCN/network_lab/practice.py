import ipaddress
def submet(network_addr,subnet_addr):
    network=ipaddress.IPv4Network(f'{network_addr}/{subnet_addr}',strict=False)

    subnet_info={
        'net address':network.network_address,
        'boradcast':network.broadcast_address,
        'subnet count':2**(32-network.prefixlen),
        'usable_address':network.num_addresses-2,
        'first_host':list(network.hosts())[0],
        'last host':list(network.hosts())[-1],
        'subnet mask':network.netmask
    }

    return subnet_info

network_addr=input()
subnet_addr=input()
if '/' not in subnet_addr:
    subnet_mask=ipaddress.IPv4Address(subnet_addr).max_prefixlen-ipaddress.IPv4Address(subnet_addr).packed.count(b'\xff')