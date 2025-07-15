from rdflib import Graph, URIRef, RDFS
from py_sysml_rdf import SYSML
from obse.graphwrapper import GraphWrapper, create_ref
from .sysml_collector import SysMLCollector


def create_rdf_model(collector: SysMLCollector):
    # Create RDF model
    graph = Graph()

    # Bind a user-declared namespace to a prefix
    graph.bind("sysml", SYSML)

    wrapper = GraphWrapper(graph)

    # Create SysML Micro Model
    for actor_id, actor in collector.dict_actors.items():
        wrapper.add_labeled_instance(SYSML.Actor, actor["name"], actor_id)

    for use_case_id, use_case in collector.dict_use_cases.items():
        wrapper.add_labeled_instance(SYSML.UseCase, use_case["name"], use_case_id)

    for subject_id, subject in collector.dict_subjects.items():
        subject_rdf = wrapper.add_labeled_instance(SYSML.Subject, subject["name"], subject_id)
        for use_case_id in subject["use_cases"]:
            wrapper.add_reference(SYSML.hasSubject, create_ref(SYSML.UseCase, use_case_id), subject_rdf)

    for _, association in collector.dict_associations.items():
        if "use_case" in association and "actor" in association:
            use_case_rdf = create_ref(SYSML.UseCase, association["use_case"])
            actor_rdf = create_ref(SYSML.Actor, association["actor"])
            wrapper.add_reference(SYSML.association, use_case_rdf, actor_rdf)

    for requirement_id, requirement in collector.dict_requirements.items():
        requirement_rdf = wrapper.add_labeled_instance(SYSML.Requirement, requirement["name"], requirement_id)
        wrapper.add_str_property(SYSML.requirementText, requirement_rdf, requirement["text"])
        wrapper.add_str_property(SYSML.requirementId, requirement_rdf, requirement["requirement_id"])
        if "nested" in requirement:
            for nested_id in requirement["nested"]:
                nested_rdf = create_ref(SYSML.Requirement, nested_id)
                wrapper.add_reference(SYSML.nestedRequirement, requirement_rdf, nested_rdf)

    return graph
