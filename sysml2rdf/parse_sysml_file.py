import logging
import xml.etree.ElementTree as ET
from .sysml_collector import SysMLCollector

logger = logging.getLogger(__name__)


def search_nested_requirements(clazz, clazz_id, collector: SysMLCollector):
    for child in clazz:
        child_type = child.get("{http://www.omg.org/spec/XMI/20131001}type")  # Typ des Child-Elements
        child_id = child.get("{http://www.omg.org/spec/XMI/20131001}id")
        print(f"  Child Element: {child.tag}, Type: {child_type} ID: {child_id}")
        if child_type == "uml:Class":
            if child_id in collector.dict_requirements:
                client_clazz_name = child.get("name")
                collector.dict_requirements[child_id]["name"] = client_clazz_name
                collector.dict_requirements[child_id]["nested"] = []

                collector.dict_requirements[clazz_id]["nested"].append(child_id)

                search_nested_requirements(child, child_id, collector)


def print_collected_data(collector: SysMLCollector):
    print("\nActors:")
    for actor_id, actor in collector.dict_actors.items():
        print(f"ID: {actor_id}, {actor}")
    print("\nUse Cases:")
    for use_case_id, use_case in collector.dict_use_cases.items():
        print(f"ID: {use_case_id}, {use_case}")
    print("\nSubjects:")
    for subject_id, subject in collector.dict_subjects.items():
        print(f"ID: {subject_id}, {subject}")
    print("\nAssociations:")
    for association_id, association in collector.dict_associations.items():
        print(f"ID: {association_id}, {association}")
    print("\nRequirements:")
    for requirement_id, requirement in collector.dict_requirements.items():
        print(f"ID: {requirement_id}, {requirement}")


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

    # define namespaces for XML parsing
    # depending on the UML version in your file

    XMI_NAMESPACE = "http://www.omg.org/spec/XMI/20131001"
    UML_NAMESPACE = "http://www.eclipse.org/uml2/5.0.0/UML"
    REQ_NAMESPACE = "http://www.eclipse.org/papyrus/sysml/1.6/SysML/Requirements"

    ns = {
        "xmi": XMI_NAMESPACE,
        "uml": UML_NAMESPACE,
        "req": REQ_NAMESPACE
    }

    collector = SysMLCollector()

    # Alle Actors im Modell suchen
    for actor in root.findall(".//packagedElement[@xmi:type='uml:Actor']", ns):
        name = actor.get("name")  # Namen des Actors auslesen
        actor_id = actor.get(f"{{{XMI_NAMESPACE}}}id")  # XMI-ID mit Namespace

        # print(f"Actor: {name}, ID: {actor_id}")
        collector.dict_actors[actor_id] = {"name": name}

    # Alle Use Cases im Modell suchen
    for use_case in root.findall(".//packagedElement[@xmi:type='uml:UseCase']", ns):
        name = use_case.get("name")  # Namen des Use Cases auslesen
        use_case_id = use_case.get("{http://www.omg.org/spec/XMI/20131001}id")  # XMI-ID mit Namespace

        # print(f"Use Case: {name}, ID: {use_case_id}")
        collector.dict_use_cases[use_case_id] = {"name": name}

    # Alle Subjects im Modell suchen
    for subject in root.findall(".//packagedElement[@xmi:type='uml:Component']", ns):
        name = subject.get("name")  # Namen des Subjects auslesen
        subject_id = subject.get("{http://www.omg.org/spec/XMI/20131001}id")  # XMI-ID mit Namespace
        use_cases = subject.get("useCase", "").strip().split(" ")
        # print(f"Subject: {name}, ID: {subject_id} UseCases: {use_cases}")
        collector.dict_subjects[subject_id] = {"name": name, "use_cases": use_cases}

        for child in subject:
            child_type = child.get("{http://www.omg.org/spec/XMI/20131001}type")  # Typ des Child-Elements
            child_id = child.get("{http://www.omg.org/spec/XMI/20131001}id")      
            # print(f"  Child Element: {child.tag}, Type: {type} ID: {child_id}")
            if child_type == "uml:UseCase":
                use_case_name = child.get("name")
                collector.dict_use_cases[child_id] = {"name": use_case_name}

    # Alle Associations im Modell suchen
    for association in root.findall(".//packagedElement[@xmi:type='uml:Association']", ns):
        association_id = association.get("{http://www.omg.org/spec/XMI/20131001}id")  # XMI-ID mit Namespace

        # print(f"Association: ID: {association_id}")
        association_data = {}
        for child in association:
            child_type = child.get("{http://www.omg.org/spec/XMI/20131001}type")  # Typ des Child-Elements
            child_id = child.get("{http://www.omg.org/spec/XMI/20131001}id")
            # print(f"  Child Element: {child.tag}, Type: {child_type} ID: {child_id}")
            if child_type == "uml:Property":
                child_id = child.get("type")
                if child_id in collector.dict_use_cases:
                    association_data["use_case"] = child_id
                elif child_id in collector.dict_actors:
                    association_data["actor"] = child_id
                else:
                    print(f"Warning: Use Case ID {use_case_id} not found in dict_use_cases or dict_actors")

        if association_data:
            collector.dict_associations[association_id] = association_data


    # Requirements

    # Alle Requirement-Elemente finden
    for requirement in root.findall(".//req:Requirement", ns):
        requirement_id = requirement.get("id")
        requirement_text = requirement.get("text")
        requirement_base_Class = requirement.get("base_Class")
        print(f"Requirement: Id: {requirement_id}, requirement_base_Class: {requirement_base_Class} text: {requirement_text}")
        collector.dict_requirements[requirement_base_Class] = {"requirement_id": requirement_id, "text": requirement_text}

    for clazz in root.findall(".//packagedElement[@xmi:type='uml:Class']", ns):
        clazz_id = clazz.get("{http://www.omg.org/spec/XMI/20131001}id")
        clazz_name = clazz.get("name")
        print(f"Class: {clazz_name}, ID: {clazz_id}")

        if clazz_id in collector.dict_requirements:
            collector.dict_requirements[clazz_id]["name"] = clazz_name
            collector.dict_requirements[clazz_id]["nested"] = []
            search_nested_requirements(clazz, clazz_id, collector)

    return collector