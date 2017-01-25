<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="16" versionDevel="104" copasiSourcesModified="0">
  <ListOfFunctions>
    <Function key="Function_40" name="Function for transcription of PER" type="UserDefined" reversible="unspecified">
      <Expression>
        default*Vs*KI^n/(KI^n+Pn^n)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_258" name="KI" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_268" name="Pn" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_254" name="Vs" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_264" name="default" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_266" name="n" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_41" name="Function for translation of PER" type="UserDefined" reversible="unspecified">
      <Expression>
        ks*M*default
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_265" name="M" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_262" name="default" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_269" name="ks" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_42" name="Function for first phosphorylation of PER" type="UserDefined" reversible="false">
      <Expression>
        V1*P0/(K1+P0)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_272" name="K1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_267" name="P0" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_270" name="V1" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_43" name="Function for removal of the first PER phosphate" type="UserDefined" reversible="false">
      <Expression>
        V2*P1/(K2+P1)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_275" name="K2" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_246" name="P1" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_273" name="V2" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="Function for second phosphorylation of PER" type="UserDefined" reversible="false">
      <Expression>
        V3*P1/(K3+P1)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_278" name="K3" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_271" name="P1" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_276" name="V3" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="Function for removal of the second PER phosphate" type="UserDefined" reversible="false">
      <Expression>
        V4*P2/(K4+P2)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_281" name="K4" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_274" name="P2" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_279" name="V4" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_46" name="Function for translocation of PER to the nucleus" type="UserDefined" reversible="false">
      <Expression>
        k1*P2*CYTOPLASM
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_284" name="CYTOPLASM" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_277" name="P2" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_282" name="k1" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="Function for translocation of PER to the cytoplasm" type="UserDefined" reversible="false">
      <Expression>
        k2*Pn*compartment_0000004
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_280" name="Pn" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_287" name="compartment_0000004" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_285" name="k2" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="Function for degradation of PER mRNA" type="UserDefined" reversible="false">
      <Expression>
        Vm*M*CYTOPLASM/(Km+M)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_290" name="CYTOPLASM" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_292" name="Km" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_283" name="M" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_288" name="Vm" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="Function for degradation of PER" type="UserDefined" reversible="false">
      <Expression>
        CYTOPLASM*Vd*P2/(Kd+P2)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_293" name="CYTOPLASM" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_296" name="Kd" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_294" name="P2" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_289" name="Vd" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_3" name="Goldbeter1995_CircClock" simulationType="time" timeUnit="h" volumeUnit="pl" areaUnit="m&#178;" lengthUnit="m" quantityUnit="&#181;mol" type="deterministic" avogadroConstant="6.02214179e+023">
    <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_3">
    <bqbiol:hasTaxon>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/taxonomy/7227"/>
      </rdf:Bag>
    </bqbiol:hasTaxon>
    <dcterms:bibliographicCitation>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <CopasiMT:isDescribedBy rdf:resource="http://identifiers.org/pubmed/8587874"/>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:bibliographicCitation>
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2005-06-29T10:17:21Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <dcterms:creator>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>lenov@ebi.ac.uk</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Le Nov&#232;re</vCard:Family>
                <vCard:Given>Nicolas</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>EMBL-EBI</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>bshapiro@jpl.nasa.gov</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Shapiro</vCard:Family>
                <vCard:Given>Bruce</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>NASA Jet Propulsion Laboratory</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:creator>
    <dcterms:modified>
      <rdf:Description>
        <dcterms:W3CDTF>2015-02-25T13:08:26Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:modified>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/MODEL6617161845"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/BIOMD0000000016"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/kegg.pathway/dme04711"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0042752"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      <body xmlns="http://www.w3.org/1999/xhtml">
    <p>To the extent possible under law, all copyright and related or neighbouring rights to this encoded model have been dedicated to the public domain worldwide. Please refer to      <a href="http://creativecommons.org/publicdomain/zero/1.0/" title="Creative Commons CC0">CC0 Public Domain Dedication</a>
          for more information.      </p>
  <p>In summary, you are entitled to use this encoded model in absolutely any manner you deem suitable, verbatim, or with modification, alone or embedded it in a larger context, redistribute it, commercially or not, in a restricted way or not.</p>
  <br/>
  <p>To cite BioModels Database, please use:      <a href="http://www.ncbi.nlm.nih.gov/pubmed/20587024" target="_blank">Li C, Donizelli M, Rodriguez N, Dharuri H, Endler L, Chelliah V, Li L, He E, Henry A, Stefan MI, Snoep JL, Hucka M, Le Nov&#232;re N, Laibe C (2010) BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models. BMC Syst Biol., 4:92.</a>
</p>
</body>
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_1" name="default" simulationType="fixed" dimensionality="3">
      </Compartment>
      <Compartment key="Compartment_3" name="CYTOPLASM" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_3">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0005737"/>
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_5" name="NUCLEUS" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_5">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0005634"/>
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_1" name="EmptySet" simulationType="fixed" compartment="Compartment_1">
        <Comment>
          <body xmlns="http://www.w3.org/1999/xhtml">
    <p>boundaryCondition changed from default (i.e. false) to true, because EmptySet acts as a reactant. Nicolas Le Novere</p>
  </body>
        </Comment>
      </Metabolite>
      <Metabolite key="Metabolite_3" name="PER mRNA" simulationType="reactions" compartment="Compartment_3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_3">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/chebi/CHEBI:33699"/>
        <rdf:li rdf:resource="http://identifiers.org/kegg.compound/C00046"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Comment>
          <body xmlns="http://www.w3.org/1999/xhtml">
    <p>Initial condition changed from amount to concentration as per article. Bruce Shapiro</p>
  </body>
        </Comment>
      </Metabolite>
      <Metabolite key="Metabolite_5" name="unphosphorylated PER" simulationType="reactions" compartment="Compartment_3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_5">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Comment>
          <body xmlns="http://www.w3.org/1999/xhtml">
    <p>Initial condition changed from amount to concentration as per article. Bruce Shapiro</p>
  </body>
        </Comment>
      </Metabolite>
      <Metabolite key="Metabolite_7" name="monophosphorylated PER" simulationType="reactions" compartment="Compartment_3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_7">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Comment>
          <body xmlns="http://www.w3.org/1999/xhtml">
    <p>Initial condition changed from amount to concentration as per article. Bruce Shapiro</p>
  </body>
        </Comment>
      </Metabolite>
      <Metabolite key="Metabolite_9" name="biphosphorylated PER" simulationType="reactions" compartment="Compartment_3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_9">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Comment>
          <body xmlns="http://www.w3.org/1999/xhtml">
    <p>Initial condition changed from amount to concentration as per article. Bruce Shapiro</p>
  </body>
        </Comment>
      </Metabolite>
      <Metabolite key="Metabolite_11" name="total PER" simulationType="assignment" compartment="Compartment_3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_11">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663"/>
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Comment>
          <body xmlns="http://www.w3.org/1999/xhtml">
    <p>Initial condition changed from amount to concentration as per article. Bruce Shapiro</p>
    <p>initial concentration for Pt is not used becuase Pt is determined by an Assigment Rule</p>
  </body>
        </Comment>
        <Expression>
          &lt;CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration&gt;+&lt;CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration&gt;+&lt;CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration&gt;+&lt;CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_13" name="nuclear PER" simulationType="reactions" compartment="Compartment_5">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_13">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663"/>
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Comment>
          <body xmlns="http://www.w3.org/1999/xhtml">
    <p>Initial condition changed from amount to concentration as per article. Bruce Shapiro</p>
  </body>
        </Comment>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_0" name="quantity_1" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_0" name="transcription of PER" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_0">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006355"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0009299"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4393" name="Vs" value="0.00297438"/>
          <Constant key="Parameter_4392" name="KI" value="0.000286224"/>
          <Constant key="Parameter_4391" name="n" value="0.0145912"/>
        </ListOfConstants>
        <KineticLaw function="Function_40">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Parameter_4392"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Metabolite_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="Parameter_4393"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="Parameter_4391"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1" name="translation of PER" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_1">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006412"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4390" name="ks" value="12.2604"/>
        </ListOfConstants>
        <KineticLaw function="Function_41">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="Parameter_4390"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_2" name="first phosphorylation of PER" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_2">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.11.1"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006468"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4389" name="V1" value="93.0415"/>
          <Constant key="Parameter_4388" name="K1" value="1.38621e-006"/>
        </ListOfConstants>
        <KineticLaw function="Function_42">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="Parameter_4388"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Parameter_4389"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_3" name="removal of the first PER phosphate" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_3">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/3.1.3.16"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006470"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4387" name="V2" value="19.8721"/>
          <Constant key="Parameter_4386" name="K2" value="0.000226111"/>
        </ListOfConstants>
        <KineticLaw function="Function_43">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Parameter_4386"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Parameter_4387"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_4" name="second phosphorylation of PER" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_4">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.11.1"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006468"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4385" name="V3" value="0.0137514"/>
          <Constant key="Parameter_4384" name="K3" value="354984"/>
        </ListOfConstants>
        <KineticLaw function="Function_44">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Parameter_4384"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Parameter_4385"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_5" name="removal of the second PER phosphate" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_5">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/3.1.3.16"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006470"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4383" name="V4" value="0.20815"/>
          <Constant key="Parameter_4382" name="K4" value="0.0072364"/>
        </ListOfConstants>
        <KineticLaw function="Function_45">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Parameter_4382"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Parameter_4383"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_6" name="translocation of PER to the nucleus" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_6">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006606"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4381" name="k1" value="2.02091"/>
        </ListOfConstants>
        <KineticLaw function="Function_46">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Compartment_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="Parameter_4381"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_7" name="translocation of PER to the cytoplasm" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_7">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006611"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4380" name="k2" value="6.73469e-005"/>
        </ListOfConstants>
        <KineticLaw function="Function_47">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="Metabolite_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Compartment_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Parameter_4380"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_8" name="degradation of PER mRNA" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_8">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006402"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4379" name="Km" value="6646.32"/>
          <Constant key="Parameter_4378" name="Vm" value="128708"/>
        </ListOfConstants>
        <KineticLaw function="Function_48">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Compartment_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Parameter_4379"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="Parameter_4378"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_9" name="degradation of PER" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_9">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006402"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4377" name="Vd" value="0.900553"/>
          <Constant key="Parameter_4376" name="Kd" value="20813"/>
        </ListOfConstants>
        <KineticLaw function="Function_49">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Compartment_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_296">
              <SourceParameter reference="Parameter_4376"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="Parameter_4377"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_1">
      <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
        <ModelParameterGroup cn="String=Initial Time" type="Group">
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock" value="0" type="Model" simulationType="time"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default]" value="1e-015" type="Compartment" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM]" value="1e-015" type="Compartment" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS]" value="1e-015" type="Compartment" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Species Values" type="Group">
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet]" value="0" type="Species" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA]" value="77327.31165449999" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER]" value="0.004575876261999999" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER]" value="56118291.8128" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER]" value="128.590191428" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER]" value="365428269.2395673" type="Species" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER]" value="309309848.832" type="Species" simulationType="reactions"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Values[quantity_1]" value="0" type="ModelValue" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=Vs" value="0.00297438" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=KI" value="0.000286224" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=n" value="0.0145912" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER],ParameterGroup=Parameters,Parameter=ks" value="12.2604" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=V1" value="93.0415" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=K1" value="1.38621e-006" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=V2" value="19.8721" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=K2" value="0.000226111" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=V3" value="0.0137514" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=K3" value="354984" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=V4" value="0.20815" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=K4" value="0.0072364" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus],ParameterGroup=Parameters,Parameter=k1" value="2.02091" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm],ParameterGroup=Parameters,Parameter=k2" value="6.73469e-005" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Km" value="6646.32" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Vm" value="128708" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Vd" value="0.9005530000000001" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Kd" value="20813" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
        </ModelParameterGroup>
      </ModelParameterSet>
    </ListOfModelParameterSets>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_3"/>
      <StateTemplateVariable objectReference="Metabolite_9"/>
      <StateTemplateVariable objectReference="Metabolite_7"/>
      <StateTemplateVariable objectReference="Metabolite_3"/>
      <StateTemplateVariable objectReference="Metabolite_5"/>
      <StateTemplateVariable objectReference="Metabolite_13"/>
      <StateTemplateVariable objectReference="Metabolite_11"/>
      <StateTemplateVariable objectReference="Metabolite_1"/>
      <StateTemplateVariable objectReference="Compartment_1"/>
      <StateTemplateVariable objectReference="Compartment_3"/>
      <StateTemplateVariable objectReference="Compartment_5"/>
      <StateTemplateVariable objectReference="ModelValue_0"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 128.590191428 56118291.8128 77327.31165449999 0.004575876261999999 309309848.832 365428269.2395673 0 1e-015 1e-015 1e-015 0 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_14" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_9" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="JacobianRequested" type="bool" value="1"/>
        <Parameter name="StabilityAnalysisRequested" type="bool" value="1"/>
      </Problem>
      <Method name="Enhanced Newton" type="EnhancedNewton">
        <Parameter name="Resolution" type="unsignedFloat" value="1e-009"/>
        <Parameter name="Derivation Factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Use Newton" type="bool" value="1"/>
        <Parameter name="Use Integration" type="bool" value="1"/>
        <Parameter name="Use Back Integration" type="bool" value="1"/>
        <Parameter name="Accept Negative Concentrations" type="bool" value="0"/>
        <Parameter name="Iteration Limit" type="unsignedInteger" value="50"/>
        <Parameter name="Maximum duration for forward integration" type="unsignedFloat" value="1000000000"/>
        <Parameter name="Maximum duration for backward integration" type="unsignedFloat" value="1000000"/>
      </Method>
    </Task>
    <Task key="Task_15" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Report reference="Report_65" target="" append="false" confirmOverwrite="false" type="Deterministic(LSODA)" name="Deterministic (LSODA)"/>
      <Problem type="Deterministic(LSODA)" name="Deterministic (LSODA)">
        <Parameter name="StepNumber" type="unsignedInteger" value="50"/>
        <Parameter name="StepSize" type="float" value="100"/>
        <Parameter name="Duration" type="float" value="5000"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0.0"/>
        <Parameter name="Output Event" type="bool" value="false"/>
        <Parameter name="Continue on Simultaneous Events" type="bool" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-6"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_16" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report reference="Report_83" target="D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Tests\VilarPEData.txt" append="false" confirmOverwrite="false"/>
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="5"/>
        <ParameterGroup name="ScanItems">
          <ParameterGroup name="ScanItem"><Parameter name="Number of steps" type="unsignedInteger" value="2"/><Parameter name="Type" type="unsignedInteger" value="0"/><Parameter name="Object" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=InitialConcentration"/></ParameterGroup></ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="0"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_17" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_10" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_18" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_11" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Subtask" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <ParameterText name="ObjectiveExpression" type="expression">
          
        </ParameterText>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
      </Problem>
      <Method name="Random Search" type="RandomSearch">
        <Parameter name="Number of Iterations" type="unsignedInteger" value="100000"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_19" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_32" target="" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="true"/>
        <Parameter name="Calculate Statistics" type="bool" value="0"/>
        <ParameterGroup name="OptimizationItemList">
          <ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="20813.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Kd,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="128708.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Vm,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="1.38621e-06"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=K1,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="19.8721"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=V2,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.000286224"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=KI,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.00297438"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=Vs,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.20815"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=V4,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.0137514"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=V3,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.0145912"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=n,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.0072364"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=K4,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.000226111"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=K2,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="6.73469e-05"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm],ParameterGroup=Parameters,Parameter=k2,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="93.0415"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=V1,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="12.2604"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER],ParameterGroup=Parameters,Parameter=ks,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="354984.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=K3,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="2.02091"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus],ParameterGroup=Parameters,Parameter=k1,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.900553"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Vd,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="6646.32"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Km,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Values[quantity_1],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="93186.6"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="128.405"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="513621.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="7.59842e-06"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.213529000001"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=InitialConcentration"/></ParameterGroup></ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
          <ParameterGroup name="Experiment_0"><Parameter name="Data is Row Oriented" type="bool" value="1"/><Parameter name="Experiment Type" type="unsignedInteger" value="1"/><Parameter name="File Name" type="file" value="vilarTimeCourse.txt"/><Parameter name="First Row" type="unsignedInteger" value="1"/><Parameter name="Key" type="key" value="Experiment_0"/><Parameter name="Last Row" type="unsignedInteger" value="51"/><Parameter name="Normalize Weights per Experiment" type="bool" value="1"/><Parameter name="Number of Columns" type="unsignedInteger" value="8"/><ParameterGroup name="Object Map"><ParameterGroup name="0"><Parameter name="Role" type="unsignedInteger" value="3"/></ParameterGroup><ParameterGroup name="1"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="2"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="3"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="4"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="5"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="6"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="7"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup></ParameterGroup><Parameter name="Row containing Names" type="unsignedInteger" value="1"/><Parameter name="Separator" type="string" value="&#9;"/><Parameter name="Weight Method" type="unsignedInteger" value="1"/></ParameterGroup></ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
        </ParameterGroup>
      </Problem>
      <Method name="Genetic Algorithm" type="GeneticAlgorithm"><Parameter name="Number of Generations" type="unsignedInteger" value="5"/><Parameter name="Population Size" type="unsignedInteger" value="5"/><Parameter name="Random Number Generator" type="unsignedInteger" value="1"/><Parameter name="Seed" type="unsignedInteger" value="0"/></Method></Task>
    <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_14"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-009"/>
        <Parameter name="Use Reeder" type="bool" value="1"/>
        <Parameter name="Use Smallbone" type="bool" value="1"/>
      </Method>
    </Task>
    <Task key="Task_21" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_14" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="ExponentNumber" type="unsignedInteger" value="3"/>
        <Parameter name="DivergenceRequested" type="bool" value="1"/>
        <Parameter name="TransientTime" type="float" value="0"/>
      </Problem>
      <Method name="Wolf Method" type="WolfMethod">
        <Parameter name="Orthonormalization Interval" type="unsignedFloat" value="1"/>
        <Parameter name="Overall time" type="unsignedFloat" value="1000"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_22" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_15" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
      </Problem>
      <Method name="ILDM (LSODA,Deuflhard)" type="TimeScaleSeparation(ILDM,Deuflhard)">
        <Parameter name="Deuflhard Tolerance" type="unsignedFloat" value="1e-006"/>
      </Method>
    </Task>
    <Task key="Task_23" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_16" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="SubtaskType" type="unsignedInteger" value="1"/>
        <ParameterGroup name="TargetFunctions">
          <Parameter name="SingleObject" type="cn" value=""/>
          <Parameter name="ObjectListType" type="unsignedInteger" value="7"/>
        </ParameterGroup>
        <ParameterGroup name="ListOfVariables">
          <ParameterGroup name="Variables">
            <Parameter name="SingleObject" type="cn" value=""/>
            <Parameter name="ObjectListType" type="unsignedInteger" value="41"/>
          </ParameterGroup>
        </ParameterGroup>
      </Problem>
      <Method name="Sensitivities Method" type="SensitivitiesMethod">
        <Parameter name="Delta factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Delta minimum" type="unsignedFloat" value="1e-012"/>
      </Method>
    </Task>
    <Task key="Task_24" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
    <Task key="Task_25" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Continue on Simultaneous Events" type="bool" value="0"/>
        <Parameter name="LimitCrossings" type="bool" value="0"/>
        <Parameter name="NumCrossingsLimit" type="unsignedInteger" value="0"/>
        <Parameter name="LimitOutTime" type="bool" value="0"/>
        <Parameter name="LimitOutCrossings" type="bool" value="0"/>
        <Parameter name="PositiveDirection" type="bool" value="1"/>
        <Parameter name="NumOutCrossingsLimit" type="unsignedInteger" value="0"/>
        <Parameter name="LimitUntilConvergence" type="bool" value="0"/>
        <Parameter name="ConvergenceTolerance" type="float" value="1e-006"/>
        <Parameter name="Threshold" type="float" value="0"/>
        <Parameter name="DelayOutputUntilConvergence" type="bool" value="0"/>
        <Parameter name="OutputConvergenceTolerance" type="float" value="1e-006"/>
        <ParameterText name="TriggerExpression" type="expression">
          
        </ParameterText>
        <Parameter name="SingleVariable" type="cn" value=""/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_26" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_17" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_14"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_9" name="Steady-State" taskType="steadyState" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_10" name="Elementary Flux Modes" taskType="fluxMode" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_11" name="Optimization" taskType="optimization" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#9;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#9;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#9;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#9;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#10;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_12" name="Parameter Estimation" taskType="parameterFitting" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#9;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#9;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#9;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#9;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#10;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_13" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#10;"/>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_14" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#10;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_15" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#10;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_16" name="Sensitivities" taskType="sensitivities" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#10;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_17" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#10;"/>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Result"/>
      </Footer>
    </Report>
    <Report taskType="Time-Course" separator="&#9;" precision="6" key="Report_65" name="Time-Course"><Comment/><Table printTitle="1"><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration"/></Table></Report><Report taskType="parameterFitting" separator="&#9;" precision="6" key="Report_83" name="parameter_estimation"><Comment/><Table printTitle="1"><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Values[quantity_1],Reference=InitialValue"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Kd,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Vm,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=K1,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=V2,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=KI,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=Vs,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=V4,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=V3,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=n,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=K4,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=K2,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm],ParameterGroup=Parameters,Parameter=k2,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=V1,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER],ParameterGroup=Parameters,Parameter=ks,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=K3,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus],ParameterGroup=Parameters,Parameter=k1,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Vd,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Km,Reference=Value"/><Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/></Table></Report></ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[PER mRNA]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[unphosphorylated PER]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[monophosphorylated PER]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[biphosphorylated PER]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[total PER]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[nuclear PER]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <SBMLReference file="Goldbeter1995_CircClock.xml">
    <SBMLMap SBMLid="CYTOPLASM" COPASIkey="Compartment_3"/>
    <SBMLMap SBMLid="EmptySet" COPASIkey="Metabolite_1"/>
    <SBMLMap SBMLid="M" COPASIkey="Metabolite_3"/>
    <SBMLMap SBMLid="P0" COPASIkey="Metabolite_5"/>
    <SBMLMap SBMLid="P1" COPASIkey="Metabolite_7"/>
    <SBMLMap SBMLid="P2" COPASIkey="Metabolite_9"/>
    <SBMLMap SBMLid="Pn" COPASIkey="Metabolite_13"/>
    <SBMLMap SBMLid="Pt" COPASIkey="Metabolite_11"/>
    <SBMLMap SBMLid="compartment_0000004" COPASIkey="Compartment_5"/>
    <SBMLMap SBMLid="default" COPASIkey="Compartment_1"/>
    <SBMLMap SBMLid="rM" COPASIkey="Reaction_0"/>
    <SBMLMap SBMLid="rP01" COPASIkey="Reaction_2"/>
    <SBMLMap SBMLid="rP10" COPASIkey="Reaction_3"/>
    <SBMLMap SBMLid="rP12" COPASIkey="Reaction_4"/>
    <SBMLMap SBMLid="rP21" COPASIkey="Reaction_5"/>
    <SBMLMap SBMLid="rP2n" COPASIkey="Reaction_6"/>
    <SBMLMap SBMLid="rPn2" COPASIkey="Reaction_7"/>
    <SBMLMap SBMLid="rTL" COPASIkey="Reaction_1"/>
    <SBMLMap SBMLid="rVd" COPASIkey="Reaction_9"/>
    <SBMLMap SBMLid="rmRNAd" COPASIkey="Reaction_8"/>
  </SBMLReference>
</COPASI>
