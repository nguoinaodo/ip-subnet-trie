# Design Decisions

## Decision 1: Using a Trie for IPv4 and IPv6 Subnet Storage

We decided to use a trie data structure for storing both IPv4 and IPv6 subnets. This decision was made because:

- Tries allow for efficient insertion and lookup of subnets.
- Tries can be serialized and deserialized, which allows for easy storage and retrieval of the trie.

This design decision affects the `insert`, `search`, `get_parent`, `get_children`, and `delete` methods in the `Trie` class, which are used to manipulate and query IPv4 and IPv6 subnets in the trie.

## Decision 2: Serializing the Trie Level by Level when using Protobuf Serializer

We decided to serialize the trie level by level, rather than using a depth-first or breadth-first approach. This decision was made because:

- Protocol Buffers, the serialization format we are using, has a recursion limit. If the trie is too deep, serialization or deserialization might fail due to this limit. We haven't encountered this limit when using JSON for serialization.
- By serializing the trie level by level, we ensure that the depth of the recursion does not exceed the Protocol Buffers recursion limit.

This design decision affects the `serialize` and `deserialize` methods in the `Trie` class, which are used to convert the trie to and from a string.

## Decision 3: Applying the Template Method Design Pattern to Refactor IPv4 and IPv6 Tries

We decided to apply the Template Method design pattern to refactor the `IPv4SubnetTrie` and `IPv6SubnetTrie` classes into a common base `BaseIPSubnetTrie` class. This decision was made because:

- Both `IPv4SubnetTrie` and `IPv6SubnetTrie` classes share common methods such as `insert` and `search`, but the implementation details of these methods differ based on whether the subnet is IPv4 or IPv6.
- The Template Method design pattern allows us to define the "skeleton" of these common methods in the base `BaseIPSubnetTrie` class, while deferring the implementation of the details to the `IPv4SubnetTrie` and `IPv6SubnetTrie` subclasses.
- This approach reduces code duplication and improves code maintainability, as changes to the common methods only need to be made in one place.

This design decision affects the `insert` and `search` methods in the `IPSubnetTrie` class, as well as the `_parse_subnet` method in the `IPv4SubnetTrie` and `IPv6SubnetTrie` subclasses, which are used to handle the specifics of parsing IPv4 and IPv6 subnets.

## Decision 4: Applying the Strategy Design Pattern for Serialization

We decided to apply the Strategy design pattern for serialization in the `IPSubnetTrie` class. This decision was made because:

- We want to be able to switch between different serialization methods (like JSON, Protocol Buffers, etc.) without modifying the `IPSubnetTrie` class.
- The Strategy design pattern allows us to define a common interface for different serialization strategies, which can be used interchangeably within the `IPSubnetTrie` class.
- This approach increases the flexibility of our code and makes it easier to add new serialization methods in the future.

This design decision affects the `serialize` and `deserialize` methods in the `IPSubnetTrie` class, which use the selected serialization strategy to convert the trie to and from a string.