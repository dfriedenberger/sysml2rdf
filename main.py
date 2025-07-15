import argparse

from sysml2rdf.create_rdf_model import create_rdf_model
from sysml2rdf.parse_sysml_file import parse_sysml_file, print_collected_data


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SysMP to RDF Transformation.')
    parser.add_argument("--input-sysml", required=True, help="Inputfile in SysML Format")
    parser.add_argument("--output-rdf", required=True, help="Outputfile in RDF Format")
    parser.add_argument("--verbose", action='store_true', help="Enable verbose output")
    args = parser.parse_args()

    return args.input_sysml, args.output_rdf, args.verbose


input_sysml, output_rdf, verbose = parse_args()
sysml_collector = parse_sysml_file(input_sysml)
if verbose:
    print_collected_data(sysml_collector)

graph = create_rdf_model(sysml_collector)
graph.serialize(destination=output_rdf, format='turtle')
