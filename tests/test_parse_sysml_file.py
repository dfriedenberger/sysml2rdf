from pathlib import Path
from sysml2rdf.parse_sysml_file import parse_sysml_file
from sysml2rdf.sysml_collector import SysMLCollector


def test_parse_sysml_file():
    # Test parsing of a SysML file
    sysml_file = Path(__file__).parent / "data" / "test_uml.xmi"
    sys_ml_collector: SysMLCollector = parse_sysml_file(sysml_file)
    assert sys_ml_collector is not None

    assert len(sys_ml_collector.dict_elements) == 36, "Expected 36 elements, found {}".format(len(sys_ml_collector.dict_elements))
    assert len(sys_ml_collector.actors()) == 5, "Expected 5 actors, found {}".format(len(sys_ml_collector.actors()))
    assert len(sys_ml_collector.use_cases()) == 2, "Expected 2 use cases, found {}".format(len(sys_ml_collector.use_cases()))
    assert len(sys_ml_collector.clazzes()) == 8, "Expected 8 classes, found {}".format(len(sys_ml_collector.clazzes()))
    assert len(sys_ml_collector.associations()) == 20, "Expected 20 associations, found {}".format(len(sys_ml_collector.associations()))
