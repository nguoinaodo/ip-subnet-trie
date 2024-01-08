import json

from . import binary_trie_pb2
from .base import *
from .trie_ip_subnet import IPSubnetNode

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

    def serialize(self, trie: Trie) -> bytes:
        """
        Serialize the Trie object to Protobuf format.

        Args:
            trie (Trie): The Trie object to be serialized.

        Returns:
            bytes: The serialized Trie object in Protobuf format.
        """
        def node_to_proto(node: TrieNode):
            node_proto = binary_trie_pb2.BinaryTrieNode()
            node_proto.is_end = node.is_end
            if node.children[0] is not None:
                node_proto.children.zero.CopyFrom(node_to_proto(node.get_child(0)))
            if node.children[1] is not None:
                node_proto.children.one.CopyFrom(node_to_proto(node.get_child(1)))
            return node_proto
        return node_to_proto(trie._get_root()).SerializeToString()

    def deserialize(self, s) -> IPSubnetNode:
        """
        Deserialize the Protobuf data to an IPSubnetNode object.

        Args:
            s (bytes): The serialized Protobuf data.

        Returns:
            IPSubnetNode: The deserialized IPSubnetNode object.
        """
        def proto_to_node(node_proto: binary_trie_pb2.BinaryTrieNode):
            node = IPSubnetNode()
            node.is_end = node_proto.is_end
            node.children = [
                proto_to_node(node_proto.children.zero) if node_proto.children.HasField('zero') else None,
                proto_to_node(node_proto.children.one) if node_proto.children.HasField('one') else None
            ]
            return node
        return proto_to_node(binary_trie_pb2.BinaryTrieNode().FromString(s))
