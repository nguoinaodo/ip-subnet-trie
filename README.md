# ip-subnet-trie
An efficient data structure for handling a large number of IP addresses/subnets in a hierarchy. 

### Run tests
```
pytest -s tests
```

### Generate Python protobuf classes from proto file.
```
cd ip_subnet_trie
protoc --python_out=. trie.proto
```

