import argparse

from sysml2rdf.create_rdf_model import create_rdf_model
from sysml2rdf.parse_sysml_file import parse_sysml_file


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SysMP to RDF Transformation.')
    parser.add_argument("--input-sysml", required=True, help="Inputfile in SysML Format")
    parser.add_argument("--output-rdf", required=True, help="Outputfile in RDF Format")
    args = parser.parse_args()

    return args.input_sysml, args.output_rdf


input_sysml, output_rdf = parse_args()
sysml_collector = parse_sysml_file(input_sysml)

graph = create_rdf_model(sysml_collector)
graph.serialize(destination=output_rdf, format='turtle')
