import pytest
from ip_subnet_trie import IPv6SubnetTrie, IPSubnetJsonSerializer, IPSubnetProtobufSerializer
def test_trie_ipv6_subnet():
    trie = IPv6SubnetTrie(serializer=IPSubnetProtobufSerializer())
    trie.insert('2001:db8::/32')
    trie.insert('2001:db8:abcd::/48')
    trie.insert('2001:db8:abcd:12::/64')
    trie.insert('2001:db8:abcd:12:ffff::/80')
    trie.insert('2001:db8:abcd:12:ffff:ffff::/96')
    trie.insert('2001:db8:abcd:12:ffff:ffff:ffff::/112')
    trie.insert('2001:db8:abcd:12:ffff:ffff:ffff:ffff/128')
    assert trie.search('2001:db8::/32') == '2001:db8::/32'
    assert trie.search('2001:db8:abcd::/48') == '2001:db8:abcd::/48'
    assert trie.search('2001:db8:abcd:12::/64') == '2001:db8:abcd:12::/64'
    assert trie.search('2001:db8:abcd:12:ffff::/80') == '2001:db8:abcd:12:ffff::/80'
    assert trie.search('2001:db8:abcd:12:ffff:ffff::/96') == '2001:db8:abcd:12:ffff:ffff::/96'
    assert trie.search('2001:db8:abcd:12:ffff:ffff:ffff::/112') == '2001:db8:abcd:12:ffff:ffff:ffff::/112'
    assert trie.search('2001:db8:abcd:12:ffff:ffff:ffff:ffff/128') == '2001:db8:abcd:12:ffff:ffff:ffff:ffff/128'
    assert trie.search('2001:db8:abcd:12:ffff:ffff:ffff:fffe') is False
    with pytest.raises(ValueError):
        trie.search('2001:db8:abcd:12:ffff:ffff:ffff:ffff:ffff')
    with pytest.raises(ValueError):
        trie.search('2001:db8:abcd:12:ffff:ffff:ffff:ffff:ffff:ffff')
    trie.delete('2001:db8:abcd:12:ffff:ffff:ffff:ffff/128')
    assert trie.search('2001:db8:abcd:12:ffff:ffff:ffff:ffff/128') is False

def test_get_parent():
    trie = IPv6SubnetTrie(serializer=IPSubnetProtobufSerializer())
    trie.insert('2001:db8::/32')
    # trie.insert('::')
    # trie.insert('::/0')
    trie.insert('2001:db8::')
    trie.insert('2001:db8:abcd::/48')
    trie.insert('2001:db8:abcd::')
    trie.insert('2001:db8:abcd::1')
    trie.insert('2001:db8:abcd:12::')
    trie.insert('2001:db8:abcd:12::128')
    trie.insert('2001:db8:abcd:12::/64')
    trie.insert('2001:db8:abcd:12:ffff::')
    trie.insert('2001:db8:abcd:12:ffff::/80')
    trie.insert('2001:db8:abcd:12:ffff:ffff::')
    trie.insert('2001:db8:abcd:12:ffff:ffff::/96')
    trie.insert('2001:db8:abcd:12:ffff:ffff:ffff::/112')
    trie.insert('2001:db8:abcd:12:ffff:ffff:ffff::')
    trie.insert('2001:db8:abcd:12:ffff:ffff:ffff:ffff/128')
    # assert trie.get_parent('::') == '::/0'
    assert trie.get_parent('2001:db8::') == '2001:db8::/32'
    assert trie.get_parent('2001:db8:abcd::') == '2001:db8:abcd::/48'
    assert trie.get_parent('2001:db8:abcd::1') == '2001:db8:abcd::/48'
    assert trie.get_parent('2001:db8:abcd:12::') == '2001:db8:abcd:12::/64'
    assert trie.get_parent('2001:db8:abcd:12::128') == '2001:db8:abcd:12::/64'
    assert trie.get_parent('2001:db8:abcd:12:ffff::') == '2001:db8:abcd:12:ffff::/80'
    assert trie.get_parent('2001:db8:abcd:12:ffff:ffff::') == '2001:db8:abcd:12:ffff:ffff::/96'
    assert trie.get_parent('2001:db8:abcd:12:ffff:ffff::192') == None
    assert trie.get_parent('2001:db8:abcd:12:ffff:ffff:ffff::') == '2001:db8:abcd:12:ffff:ffff:ffff::/112'
    assert trie.get_parent('2001:db8:abcd:12:ffff:ffff:ffff:ffff') == '2001:db8:abcd:12:ffff:ffff:ffff::/112'
    assert trie.get_parent('2001:db8:abcd:12:ffff:ffff:ffff:fffe') is None
    assert trie.get_parent('2001:db8:abcd:12:ffff:ffff:ffff:ffff/128') == '2001:db8:abcd:12:ffff:ffff:ffff::/112'
    with pytest.raises(ValueError):
        trie.get_parent('2001:db8:abcd:12:ffff:ffff:ffff:ffff:ffff')
