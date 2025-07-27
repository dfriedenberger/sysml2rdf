



python main.py --input-sysml ../../../workspace-papyrus/SQuIRRL/SQuIRRL.uml --output-rdf ../../../rdf2visjs/app/data/sysml-squirrl.ttl 

# sysml_2_rdf("../../xmi-codegen/cleaned.xmi", "eulynx-test.ttl")
# sysml_2_rdf("../../xmi-codegen/EULYNX System BL4 v23 - BL4.xmi", "eulynx-test.ttl")
#python main.py --input-sysml ../../../xmi-codegen/cleaned.xmi --output-rdf ../../../rdf2visjs/app/data/sysml-eulynx.ttl


## Build docker image

```
docker build -t frittenburger/sysml2rdf:dev .
```