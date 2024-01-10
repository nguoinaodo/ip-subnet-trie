def parse_ip_subnet_v4(ip_subnet):
    """
    Parse an IPv4 subnet string into its IP address and subnet mask components.

    Args:
        ip_subnet (str): The IPv4 subnet string in the format 'ip_address/subnet_mask'.

    Returns:
        tuple: A tuple containing the IP address (str) and subnet mask (int) components.

    """
    if '/' in ip_subnet:
        ip, netmask = ip_subnet.split('/')
        netmask = int(netmask)
    else:
        ip = ip_subnet
        netmask = 32  # If no subnet mask is provided, assume it's a single IP address
    return ip, netmask

def parse_ip_subnet_v6(ip_subnet):
    """
    Parses an IPv6 subnet string and returns the IP address and subnet mask.

    Args:
        ip_subnet (str): The IPv6 subnet string in the format 'ip_address/netmask'.

    Returns:
        tuple: A tuple containing the IP address (list of ints) and subnet mask (int).

    Raises:
        ValueError: If the IPv6 address is invalid.

    Examples:
        >>> parse_ip_subnet_v6('2001:db8::1/64')
        ([8193, 3512, 0, 0, 0, 0, 0, 1], 64)

        >>> parse_ip_subnet_v6('2001:db8::1')
        ([8193, 3512, 0, 0, 0, 0, 0, 1], 128)

    """
    if '/' not in ip_subnet:
        ip_subnet += '/128'  # If no subnet mask is provided, assume it's a single IP address
    ip, netmask = ip_subnet.split('/')
    ip_parts = ip.split(':')

    # Expand ::
    if '' in ip_parts:
        index = ip_parts.index('')
        ip_parts = ip_parts[:index] + ['0'] * (8 - len(ip_parts) + 1) + ip_parts[index+1:]

    # Ensure all parts are valid hexadecimal numbers
    ip_parts = [part if part != '' else '0' for part in ip_parts]

    ip = [int(part, 16) for part in ip_parts]
    if len(ip) > 8:
        raise ValueError('Invalid IPv6 address')
    
    return ip, int(netmask)