def parse_ip_subnet(ip_subnet):
    """
    Parse the given IP subnet string and return the IP address and subnet mask.

    Args:
        ip_subnet (str): The IP subnet string in the format 'ip_address/subnet_mask'.

    Returns:
        tuple: A tuple containing the IP address (str) and subnet mask (int).

    """
    if '/' in ip_subnet:
        ip, netmask = ip_subnet.split('/')
        netmask = int(netmask)
    else:
        ip = ip_subnet
        netmask = 32  # If no subnet mask is provided, assume it's a single IP address
    return ip, netmask