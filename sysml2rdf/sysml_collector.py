from typing import Dict


class SysMLCollector:
    def __init__(self):
        self.dict_elements = dict()  # Dictionary for all elements

    def set(self, xmi_id: str, name: str, value: any):
        """
        Set an element in the collector.
        Args:
            xmi_id (str): The XMI ID of the element.
            name (str): The name of the element.
            xmi_type (str): The XMI type of the element.
        """
        if xmi_id not in self.dict_elements:
            self.dict_elements[xmi_id] = {}
        self.dict_elements[xmi_id][name] = value

    def append(self, xmi_id: str, name: str, value: any):
        """
        Append a value to a list in the collector.
        Args:
            xmi_id (str): The XMI ID of the element.
            name (str): The name of the element.
            value (any): The value to append.
        """
        if xmi_id not in self.dict_elements:
            self.dict_elements[xmi_id] = {}
        if name not in self.dict_elements[xmi_id]:
            self.dict_elements[xmi_id][name] = []
        self.dict_elements[xmi_id][name].append(value)

    def __select_elements(self, xmi_type) -> Dict[str, dict]:
        """
        Select elements of a specific type from the collected elements.
        Args:
            xmi_type (str): The XMI type to filter elements by.
        Returns:
            Dict[str, dict]: A dictionary of elements of the specified type.
        """
        return {k: v for k, v in self.dict_elements.items() if "type" in v and v["type"] == xmi_type}

    def actors(self) -> Dict[str, dict]:
        """
        Get all actors.
        Returns:
            Dict[str, dict]: A dictionary of actors.
        """
        return self.__select_elements("uml:Actor")

    def use_cases(self) -> Dict[str, dict]:
        """
        Get all use cases.
        Returns:
            Dict[str, dict]: A dictionary of use cases.
        """
        return self.__select_elements("uml:UseCase")

    def associations(self) -> Dict[str, dict]:
        """
        Get all associations.
        Returns:
            Dict[str, dict]: A dictionary of associations.
        """
        return self.__select_elements("uml:Association")

    def clazzes(self) -> Dict[str, dict]:
        """
        Get all classes.
        Returns:
            Dict[str, dict]: A dictionary of classes.
        """
        return self.__select_elements("uml:Class")

    def dependencies(self) -> Dict[str, dict]:
        """
        Get all dependencies.
        Returns:
            Dict[str, dict]: A dictionary of dependencies.
        """
        return self.__select_elements("uml:Dependency")

    def get_pair_nodes(self, element, node1_type, node2_type):
        nodes = {}

        if "nodes" in element:
            for node_id in element["nodes"]:
                node = self.dict_elements.get(node_id)
                node_type = node.get("type")
                if node_type not in nodes:
                    nodes[node_type] = []
                nodes[node["type"]].append(node_id)

        if node1_type == node2_type:
            if node1_type in nodes and len(nodes[node1_type]) == 2:
                return nodes[node1_type][0], nodes[node1_type][1]
            return None, None

        if node1_type in nodes and len(nodes[node1_type]) == 1 and node2_type in nodes and len(nodes[node2_type]) == 1:
            return nodes[node1_type][0], nodes[node2_type][0]

        return None, None
