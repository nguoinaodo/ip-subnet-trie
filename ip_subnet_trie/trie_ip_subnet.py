from .base import *
from .utils import parse_ip_subnet

class IPSubnetNode(TrieNode):
    def __init__(self, depth=0):
        super().__init__()
        self.children = [None, None]
        self.depth = depth

class IPSubnetTrie(Trie):
    """
    A trie data structure for storing and searching IP subnets.

    Attributes:
        serializer (TrieSerializer): The serializer used for serializing and deserializing the trie.

    Methods:
        insert(ip_subnet): Inserts an IP subnet into the trie.
        search(ip_subnet): Searches for an IP subnet in the trie.
        get_children(ip_subnet): Returns the children of an IP subnet in the trie.
        delete(ip_subnet): Deletes an IP subnet from the trie.
        serialize(): Serializes the trie using the specified serializer.
        deserialize(s): Deserializes the trie using the specified serialized string.
    """

    def __init__(self, serializer: TrieSerializer):
        self.serializer = serializer
        self.__root = IPSubnetNode()

    def _get_root(self) -> IPSubnetNode:
        return self.__root
    
    def insert(self, ip_subnet):
        """
        Inserts an IP subnet into the trie.

        Args:
            ip_subnet (str): The IP subnet to be inserted.

        Returns:
            None
        """
        ip, netmask = parse_ip_subnet(ip_subnet)        
        node = self.__root
        depth = 0
        for part in map(int, ip.split('.')):
            for i in range(7, -1, -1):  # For each bit in the part
                if depth >= netmask:
                    break
                bit = (part >> i) & 1
                if node.children[bit] is None:
                    node.children[bit] = IPSubnetNode(depth + 1)
                node = node.children[bit]
                depth += 1
                
        node.is_end = True
        node.depth = netmask
        print(f'inserted {self.__get_node_representation(node)}')

    def __get_node_representation(self, node):
        """
        Returns the string representation of a node in the trie.

        Args:
            node (IPSubnetNode): The node to get the representation of.

        Returns:
            str: The string representation of the node.
        """
        def traverse(current_node, path, depth):
            if current_node is node:
                # Pad the path with zeros until it has 32 bits
                path += [0] * (32 - len(path))
                ip_parts = [str(int(''.join(map(str, path[i:i+8])), 2)) for i in range(0, len(path), 8)]
                return '.'.join(ip_parts) + '/' + str(depth)
            if current_node.children[0] is not None:
                result = traverse(current_node.children[0], path + [0], depth + 1)
                if result is not None:
                    return result
            if current_node.children[1] is not None:
                result = traverse(current_node.children[1], path + [1], depth + 1)
                if result is not None:
                    return result
            return None

        return traverse(self.__root, [], 0)

    def search(self, ip_subnet):
        """
        Searches for an IP subnet in the trie.

        Args:
            ip_subnet (str): The IP subnet to search for.

        Returns:
            str or False: The string representation of the found IP subnet if found, False otherwise.
        """
        ip, netmask = parse_ip_subnet(ip_subnet)        
        _, node = self.__traverse_node(ip, netmask)
        
        return self.__get_node_representation(node) if node and node.is_end else False

    def __traverse_node(self, ip, netmask):
        """
        Traverses the trie to find the node corresponding to the given IP subnet.

        Args:
            ip (str): The IP address of the subnet.
            netmask (int): The netmask of the subnet.

        Returns:
            tuple: A tuple containing the list of parent-child pairs and the node found.
        """
        parents = []  # Keep track of the path to the node
        node = self.__root
        depth = 0

        for part in map(int, ip.split('.')):
            for i in range(7, -1, -1):  # For each bit in the part
                if depth >= netmask:
                    return parents, node
                bit = (part >> i) & 1
                if node.children[bit] is None:
                    return parents, None  # IP/subnet not found
                parents.append((node, bit))
                node = node.children[bit]
                depth += 1
        
        node = node if depth == netmask else None
        return parents, node

    def get_children(self, ip_subnet):
        """
        Returns the children of an IP subnet in the trie.

        Args:
            ip_subnet (str): The IP subnet to get the children of.

        Returns:
            list: A list of string representations of the children.
        """
        ip, netmask = parse_ip_subnet(ip_subnet)
        _, node = self.__traverse_node(ip, netmask)
        if node is None:
            return []
        return self.__dfs(node, include_self=False)

    def __dfs(self, node, include_self=True):
        """
        Performs a depth-first search starting from the given node.

        Args:
            node (IPSubnetNode): The starting node of the search.
            include_self (bool): Whether to include the starting node in the result.

        Returns:
            list: A list of string representations of the nodes visited during the search.
        """
        result = [self.__get_node_representation(node)] if (node.is_end and include_self) else []
        for child in node.children:
            if child is not None:
                result.extend(self.__dfs(child))
        return result

    def get_parent(self, ip_subnet: str):
        """
        Retrieves the parent node of the given IP subnet.

        Args:
            ip_subnet (str): The IP subnet to find the parent for.

        Returns:
            str: The representation of the nearest parent node, or None if no parent found.
        """
        
        ip, netmask = parse_ip_subnet(ip_subnet)

        parents, _ = self.__traverse_node(ip, netmask)
        if not parents:
            return None
        nearest_parent = self.__get_nearest_parent(parents)
        if not nearest_parent:
            return None

        return self.__get_node_representation(nearest_parent)
    
    def __get_nearest_parent(self, parents: list[TrieNode]):
        for parent, _ in reversed(parents):
            if parent.is_end:
                return parent
        return None
    
    def delete(self, ip_subnet):
        """
        Deletes an IP subnet from the trie.

        Args:
            ip_subnet (str): The IP subnet to be deleted.

        Returns:
            None
        """
        ip, netmask = parse_ip_subnet(ip_subnet)
        parents, node = self.__traverse_node(ip, netmask)
        if node:
            self.__remove_node(parents, node)

    def __remove_node(self, parents, node):
        """
        Removes a node from the trie.

        Args:
            parents (list): The list of parent-child pairs leading to the node.
            node (IPSubnetNode): The node to be removed.

        Returns:
            None
        """
        node.is_end = False  # Remove the IP/subnet

        # If the node has no children and is not an end node, remove it
        if not any(node.children) and not node.is_end:
            for parent, bit in reversed(parents):
                if not any(parent.children[bit].children) and not parent.children[bit].is_end:
                    parent.children[bit] = None
                else:
                    break

    def serialize(self):
        """
        Serializes the trie using the specified serializer.

        Returns:
            str: The serialized string representation of the trie.
        """
        return self.serializer.serialize(self)

    def deserialize(self, s):
        """
        Deserializes the trie using the specified serialized string.

        Args:
            s (str): The serialized string representation of the trie.

        Returns:
            None
        """
        self.__root = self.serializer.deserialize(s)
