import logging
import xml.etree.ElementTree as ET
from .sysml_collector import SysMLCollector

logger = logging.getLogger(__name__)


# Define namespaces for XML parsing
# depending on the UML version in your file
XMI_NAMESPACE = "http://www.omg.org/spec/XMI/20131001"
UML_NAMESPACE = "http://www.eclipse.org/uml2/5.0.0/UML"
REQ_NAMESPACE = "http://www.eclipse.org/papyrus/sysml/1.6/SysML/Requirements"

ns = {
    "xmi": XMI_NAMESPACE,
    "uml": UML_NAMESPACE,
    "req": REQ_NAMESPACE
}


def handle_association_property(packaged_element, child, collector: SysMLCollector):
    # <ownedEnd xmi:type="uml:Property" xmi:id="_hhw8gFKJEfCGt4EH7VyqHw" name="exchange data securely" type="_VxOtsFKJEfCGt4EH7VyqHw" association="_hhsEAFKJEfCGt4EH7VyqHw"/>
    #  <ownedAttribute xmi:type="uml:Property" xmi:id="_IExws17-EfC7zM_i7orNRw" name="kme-2" type="_2xU90F77EfC7zM_i7orNRw" association="_IExwsF7-EfC7zM_i7orNRw">
    xmi_id = child.get("association")
    node = child.get("type")

    aggregation = child.get("aggregation")
    if aggregation:
        collector.set(xmi_id, "aggregation", aggregation)

    collector.append(xmi_id, "nodes", node)


# Define injections for child elements
injections = {
    "uml:Association": {
        "uml:Property": handle_association_property
    },
    "uml:Class": {
        "uml:Property": handle_association_property
    }
}


def parse_sysml_file(file_path) -> SysMLCollector:
    """    Parses a SysML file and collects data about actors, use cases, subjects, associations, and requirements.
    Args:
        file_path (str): The path to the SysML file to be parsed.
    Returns:
        SysMLCollector: An instance of SysMLCollector containing the collected data.
    """
    logger.info(f"Parsing SysML file: {file_path}")

    tree = ET.parse(file_path)
    root = tree.getroot()

    collector = SysMLCollector()

    # PackedElement ist das Root-Element für UML-Modelle
    for packaged_element in root.findall(".//packagedElement", ns):
        xmi_id = packaged_element.get(f"{{{XMI_NAMESPACE}}}id")  # XMI-ID mit Namespace
        xmi_type = packaged_element.get(f"{{{XMI_NAMESPACE}}}type")  # XMI-Typ mit Namespace
        name = packaged_element.get("name")  # Namen des Actors auslesen
        print(f"Packaged Element: {name}, ID: {xmi_id}, Type: {xmi_type}")
        collector.set(xmi_id, "name", name)
        collector.set(xmi_id, "type", xmi_type)

        for child in packaged_element:
            child_type = child.get(f"{{{XMI_NAMESPACE}}}type")
            child_id = child.get(f"{{{XMI_NAMESPACE}}}id")
            print(f"  Child Element: {child.tag}, Type: {child_type} ID: {child_id}")

            if xmi_type in injections and child_type in injections[xmi_type]:
                injections[xmi_type][child_type](packaged_element, child, collector)

    # find all comments (xmi:type="uml:Comment")
    for comment in root.findall(".//*[@xmi:type='uml:Comment']", namespaces=ns):
        comment_for_id = comment.get("annotatedElement")
        comment_body = comment.find("body").text
        print(f"  Comment ID: {comment_for_id}, Body: {comment_body}")
        collector.append(comment_for_id, "comment", comment_body)

    return collector
