from rdflib import Namespace, URIRef, Graph, Literal, BNode
from rdflib.namespace import  RDF, OWL, RDFS, XSD
from rdflib import URIRef, RDFS, RDF, BNode

## Om de ontologie in WebVowl te kunnen visualiseren is het nodig dat elke relatie tussen classes zijn eigen property krijgt
## Dit script voegt de 'expliciete' properties toe voor elk statement waar datalab:komt_voor_in gebruikt wordt


g= Graph()

g.parse('..\ontologie\datalab.noord-holland.ttl', format='turtle')

namespaces = {'datalab': 'http://datalab.noord-holland.nl#',
                  'owl': 'http://www.w3.org/2002/07/owl#', 'skos':'http://www.w3.org/2004/02/skos/core#'}

for ns in namespaces:
    g.bind(ns,namespaces.get(ns))

qres = g.query(
    """
    PREFIX datalab: <http://datalab.noord-holland.nl#>

    SELECT DISTINCT ?s ?p
        WHERE
        {
           ?s datalab:komt_voor_in ?p .
        }""")

rt = URIRef(namespaces['datalab'] + 'relatieType')
g.add((rt, RDF.type, OWL.DatatypeProperty))

num = 1
for row in qres:
    print("%s komt voor in %s" % row)
    po = URIRef(namespaces['datalab']+ 'komt_voor_in_' + str(num))
    g.add((po, RDF.type, OWL.ObjectProperty))
    g.add((po, RDFS.label, Literal(row[0].split('#')[1]+'_komt_voor_in_'+row[1].split('#')[1])))
    g.add((po, RDFS.subPropertyOf, URIRef(namespaces['datalab']+ 'komt_voor_in')))
    g.add((po, RDFS.domain, row[0]))
    g.add((po, RDFS.range, row[1]))
    #bn = BNode()
    #g.add((bn, RDF.type, OWL.Restriction))
    #g.add((bn, OWL.onProperty, po))
    #g.add((bn, OWL.someValuesFrom, row[1]))
    #g.add((row[0], RDFS.subClassOf, bn))
    g.add((row[0], po, row[1]))

    #g.add((row[0],rt,Literal('partOf',datatype=XSD.string)))
    num +=1

g.serialize(destination=r'..\visualisatie\datalab_plus.noord-holland.ttl',format='turtle')

