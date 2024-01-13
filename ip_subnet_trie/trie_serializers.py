import json

from . import binary_trie_pb2
from .base import *

class IPSubnetJsonSerializer(TrieJsonSerializer):
    """
    Serializer class for converting IPSubnet trie to JSON format and vice versa.
    """

    def serialize(self, trie: Trie) -> str:
        """
        Serialize the given trie into a JSON string.

        Args:
            trie (Trie): The trie to be serialized.

        Returns:
            str: The JSON string representation of the trie.
        """
        def node_to_dict(node: TrieNode):
            return {
                'is_end': node.is_end,
                'children': [node_to_dict(child) if child else None for child in node.get_children()]
            }
        return json.dumps(node_to_dict(trie._get_root()))

    def deserialize(self, s) -> IPSubnetNode:
        """
        Deserialize the given JSON string into an IPSubnetNode.

        Args:
            s (str): The JSON string to be deserialized.

        Returns:
            IPSubnetNode: The deserialized IPSubnetNode.
        """
        def dict_to_node(node_dict: dict):
            node = IPSubnetNode()
            node.is_end = node_dict['is_end']
            node.children = [dict_to_node(child) if child else None for child in node_dict['children']]
            return node
        return dict_to_node(json.loads(s))

class IPSubnetProtobufSerializer(TrieProtobufSerializer):
    """
    Serializer class for converting Trie objects to and from Protobuf format.

    This serializer specifically handles IP subnet data and provides methods
    for serializing and deserializing Trie objects to and from Protobuf format.
    """

    def serialize(self, trie: IPSubnetTrie):
        """
        Serialize the IPSubnetTrie object into a binary format.

        Args:
            trie (IPSubnetTrie): The IPSubnetTrie object to be serialized.

        Returns:
            bytes: The serialized binary data representing the IPSubnetTrie.
        """
        nodes_proto = binary_trie_pb2.BinaryTrieNodes()

        root = trie._get_root()
        if root is None:
            return nodes_proto.SerializeToString()

        queue = [root]

        while queue:
            node = queue.pop(0)
            node_proto = nodes_proto.nodes.add()
            node_proto.is_end = node.is_end
            if node.children[0] is not None:
                queue.append(node.children[0])
                node_proto.has_zero_child = True
            if node.children[1] is not None:
                queue.append(node.children[1])
                node_proto.has_one_child = True

        return nodes_proto.SerializeToString()

    def deserialize(self, s):
        """
        Deserialize a binary trie from a string representation.

        Args:
            s (str): The string representation of the binary trie.

        Returns:
            IPSubnetNode: The root node of the deserialized binary trie.
        """
        nodes_proto = binary_trie_pb2.BinaryTrieNodes()
        nodes_proto.ParseFromString(s)

        if not nodes_proto.nodes:
            return None

        nodes = [None] * len(nodes_proto.nodes)
        queue = [(0, None, False)]  # (node index, parent node, is right child)
        next_index = 1  # The index of the next node to add to nodes_proto.nodes

        while queue:
            node_index, parent_node, is_right_child = queue.pop(0)
            node_proto = nodes_proto.nodes[node_index]

            node = IPSubnetNode()  # Replace with your actual Node class
            node.is_end = node_proto.is_end
            nodes[node_index] = node

            if parent_node is not None:
                parent_node.children[is_right_child] = node

            if node_proto.has_zero_child:
                queue.append((next_index, node, False))
                next_index += 1
            if node_proto.has_one_child:
                queue.append((next_index, node, True))
                next_index += 1

        return nodes[0]  # The root of the trie
