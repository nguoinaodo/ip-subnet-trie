from ip_subnet_trie import IPSubnetTrie, IPSubnetJsonSerializer, IPSubnetProtobufSerializer

def test_trie_ip_subnet():
    trie = IPSubnetTrie(serializer=IPSubnetProtobufSerializer())

    trie.insert('192.168.0.1')
    trie.insert('192.168.0.2')
    trie.insert('192.168.0.6')
    trie.insert('192.168.0.5')

    assert trie.search('192.168.0.0/24') is False
    trie.insert('192.168.0.0/24')
    assert trie.search('192.168.0.0/24') == '192.168.0.0/24'

    assert trie.search('192.168.0.1') == '192.168.0.1/32'
    assert trie.search('192.168.0.3') is False
    assert trie.search('192.168.0') is False

    assert set(trie.get_children('192.168.0.0/24')) == {'192.168.0.1/32', '192.168.0.2/32', '192.168.0.6/32', '192.168.0.5/32'}

    trie.delete('192.168.0.2')
    assert set(trie.get_children('192.168.0.0/24')) == {'192.168.0.1/32', '192.168.0.6/32', '192.168.0.5/32'}

    with open('ip_subnet_trie.pb', 'wb') as f:
        f.write(trie.serialize())

    trie.serializer = IPSubnetJsonSerializer()
    with open('ip_subnet_trie.json', 'w') as f:
        f.write(trie.serialize())

    trie.deserialize(open('ip_subnet_trie.json', 'r').read())
    assert set(trie.get_children('192.168.0.0/24')) == {'192.168.0.1/32', '192.168.0.6/32', '192.168.0.5/32'}

    trie.serializer = IPSubnetProtobufSerializer()
    trie.deserialize(open('ip_subnet_trie.pb', 'rb').read())
    assert set(trie.get_children('192.168.0.0/24')) == {'192.168.0.1/32', '192.168.0.6/32', '192.168.0.5/32'}

def test_get_parent():
    trie = IPSubnetTrie(serializer=IPSubnetProtobufSerializer())

    trie.insert('10.255.249.105')
    trie.insert('10.255.249.104')
    trie.insert('10.255.249.0/24')
    trie.insert('10.255.249.64/26')
    trie.insert('10.255.249.0/26')
    assert set(trie.get_children('10.255.249.0/24')) == {
        '10.255.249.105/32', '10.255.249.104/32',
        '10.255.249.0/26', '10.255.249.64/26',
    }
    assert set(trie.get_children('10.255.249.64/26')) == {
        '10.255.249.105/32', '10.255.249.104/32',
    }
    assert trie.get_parent('10.255.249.104') == '10.255.249.64/26'
    assert trie.get_parent('10.255.249.105') == '10.255.249.64/26'
    assert trie.get_parent('10.255.249.0/26') == '10.255.249.0/24'
    assert trie.get_parent('10.255.249.64/26') == '10.255.249.0/24'
