import ipaddress

def subnet(network_address,subnet_mask):
	network=ipaddress.IPv4Network(f'{network_address}/{subnet_mask}',strict=False)
	
	subnet_info={
		'Net Address':network.network_address,
		'Broadcast Address':network.broadcast_address,
		'Number of subnets':2**(32-network.prefixlen),
		'number of usable hosts':network.num_addresses-2,
		'first host':list(network.hosts())[0],
		'last host':list(network.hosts())[-1],
		'subnet mask':network.netmask }
	return subnet_info
def main():
	network_address=input()
	subnet_mask=input()
	if '/' not in subnet_mask:
		subnet_mask=ipaddress.IPv4Address(subnet_mask).max_prefixlen - ipaddress.IPv4Address(subnet_mask).packed.count(b'\xff')
	subnet_info=subnet(network_address,subnet_mask)
	for key,values in subnet_info.items():
		print(f'{key}:{values}')
		
main()