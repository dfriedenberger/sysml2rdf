from rdflib import Graph, URIRef, RDFS
from py_sysml_rdf import SYSML
from obse.graphwrapper import GraphWrapper, create_ref
from .sysml_collector import SysMLCollector


def create_instance(wrapper: GraphWrapper, rdf_type, obj_id, obj):
    rdf = wrapper.add_labeled_instance(rdf_type, obj["name"], obj_id)

    if "comment" in obj:
        wrapper.add_comment(rdf, "\n".join(obj["comment"]))


def create_reference(wrapper: GraphWrapper, rdf1, rdf2, association):
    association_name = association.get("name")

    if "aggregation" in association:
        aggregation = association["aggregation"]
        if aggregation == "composite":
            wrapper.add_reference(SYSML.composition, rdf1, rdf2)
        elif aggregation == "shared":
            wrapper.add_reference(SYSML.shared, rdf1, rdf2)
    elif association_name:  # TODO define in ontology, create subproperty for association
        xxx = create_ref(SYSML.association, association_name)
        wrapper.add_reference(xxx, rdf1, rdf2)
    else:
        wrapper.add_reference(SYSML.association, rdf1, rdf2)


def create_rdf_model(collector: SysMLCollector):
    # Create RDF model
    graph = Graph()

    # Bind a user-declared namespace to a prefix
    graph.bind("sysml", SYSML)

    wrapper = GraphWrapper(graph)

    # Create SysML Micro Model
    for actor_id, actor in collector.actors().items():
        create_instance(wrapper, SYSML.Actor, actor_id, actor)

    for use_case_id, use_case in collector.use_cases().items():
        create_instance(wrapper, SYSML.UseCase, use_case_id, use_case)

    for clazz_id, clazz in collector.clazzes().items():
        create_instance(wrapper, SYSML.Block, clazz_id, clazz)

    for association in collector.associations().values():
        # Actor -> UseCase
        actor_id, usecase_id = collector.get_pair_nodes(association, "uml:Actor", "uml:UseCase")
        if actor_id and usecase_id:
            use_case_rdf = create_ref(SYSML.UseCase, usecase_id)
            actor_rdf = create_ref(SYSML.Actor, actor_id)
            create_reference(wrapper, use_case_rdf, actor_rdf, association)

        actor_id, clazz_id = collector.get_pair_nodes(association, "uml:Actor", "uml:Class")
        if actor_id and clazz_id:
            clazz_rdf = create_ref(SYSML.Block, clazz_id)
            actor_rdf = create_ref(SYSML.Actor, actor_id)
            create_reference(wrapper, actor_rdf, clazz_rdf, association)

        # Clazz -> Clazz
        clazz1_id, clazz2_id = collector.get_pair_nodes(association, "uml:Class", "uml:Class")
        if clazz1_id and clazz2_id:
            clazz1_rdf = create_ref(SYSML.Block, clazz1_id)
            clazz2_rdf = create_ref(SYSML.Block, clazz2_id)

            create_reference(wrapper, clazz1_rdf, clazz2_rdf, association)

           
    return graph
