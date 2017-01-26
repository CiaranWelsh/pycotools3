<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="16" versionDevel="104" copasiSourcesModified="0">
  <ListOfFunctions>
    <Function key="Function_40" name="Function for transcription of PER" type="UserDefined" reversible="unspecified">
      <Expression>
        default*Vs*KI^n/(KI^n+Pn^n)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_265" name="KI" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_266" name="Pn" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_267" name="Vs" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_268" name="default" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_269" name="n" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_41" name="Function for translation of PER" type="UserDefined" reversible="unspecified">
      <Expression>
        ks*M*default
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_258" name="M" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_254" name="default" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_275" name="ks" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_42" name="Function for first phosphorylation of PER" type="UserDefined" reversible="false">
      <Expression>
        V1*P0/(K1+P0)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_279" name="K1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_280" name="P0" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_281" name="V1" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_43" name="Function for removal of the first PER phosphate" type="UserDefined" reversible="false">
      <Expression>
        V2*P1/(K2+P1)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_285" name="K2" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_286" name="P1" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_287" name="V2" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="Function for second phosphorylation of PER" type="UserDefined" reversible="false">
      <Expression>
        V3*P1/(K3+P1)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_291" name="K3" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_292" name="P1" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_293" name="V3" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="Function for removal of the second PER phosphate" type="UserDefined" reversible="false">
      <Expression>
        V4*P2/(K4+P2)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_297" name="K4" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_298" name="P2" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_299" name="V4" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_46" name="Function for translocation of PER to the nucleus" type="UserDefined" reversible="false">
      <Expression>
        k1*P2*CYTOPLASM
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_303" name="CYTOPLASM" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_304" name="P2" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_305" name="k1" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="Function for translocation of PER to the cytoplasm" type="UserDefined" reversible="false">
      <Expression>
        k2*Pn*compartment_0000004
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_309" name="Pn" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_310" name="compartment_0000004" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_311" name="k2" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="Function for degradation of PER mRNA" type="UserDefined" reversible="false">
      <Expression>
        Vm*M*CYTOPLASM/(Km+M)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_316" name="CYTOPLASM" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_317" name="Km" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_318" name="M" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_319" name="Vm" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="Function for degradation of PER" type="UserDefined" reversible="false">
      <Expression>
        CYTOPLASM*Vd*P2/(Kd+P2)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_324" name="CYTOPLASM" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_325" name="Kd" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_326" name="P2" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_327" name="Vd" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_4" name="Goldbeter1995_CircClock" simulationType="time" timeUnit="h" volumeUnit="l" areaUnit="m&#178;" lengthUnit="m" quantityUnit="&#181;mol" type="deterministic" avogadroConstant="6.02214179e+023">
    <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_4">
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
      <Metabolite key="Metabolite_13" name="total PER" simulationType="assignment" compartment="Compartment_3">
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
    <p>initial concentration for Pt is not used becuase Pt is determined by an Assigment Rule</p>
  </body>

        </Comment>
        <Expression>
          &lt;CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration&gt;+&lt;CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration&gt;+&lt;CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration&gt;+&lt;CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration&gt;
        </Expression>
      </Metabolite>
      <Metabolite key="Metabolite_11" name="nuclear PER" simulationType="reactions" compartment="Compartment_5">
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
  </body>

        </Comment>
      </Metabolite>
    </ListOfMetabolites>
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
          <Modifier metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4407" name="Vs" value="0.76"/>
          <Constant key="Parameter_4408" name="KI" value="1"/>
          <Constant key="Parameter_4409" name="n" value="4"/>
        </ListOfConstants>
        <KineticLaw function="Function_40">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Parameter_4408"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Parameter_4407"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="Parameter_4409"/>
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
          <Constant key="Parameter_4410" name="ks" value="0.38"/>
        </ListOfConstants>
        <KineticLaw function="Function_41">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Parameter_4410"/>
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
          <Constant key="Parameter_4411" name="V1" value="3.2"/>
          <Constant key="Parameter_4412" name="K1" value="2"/>
        </ListOfConstants>
        <KineticLaw function="Function_42">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Parameter_4412"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="Metabolite_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Parameter_4411"/>
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
          <Constant key="Parameter_4413" name="V2" value="1.58"/>
          <Constant key="Parameter_4414" name="K2" value="2"/>
        </ListOfConstants>
        <KineticLaw function="Function_43">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Parameter_4414"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_286">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Parameter_4413"/>
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
          <Constant key="Parameter_4415" name="V3" value="5"/>
          <Constant key="Parameter_4416" name="K3" value="2"/>
        </ListOfConstants>
        <KineticLaw function="Function_44">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_291">
              <SourceParameter reference="Parameter_4416"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Parameter_4415"/>
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
          <Constant key="Parameter_4417" name="V4" value="2.5"/>
          <Constant key="Parameter_4418" name="K4" value="2"/>
        </ListOfConstants>
        <KineticLaw function="Function_45">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_297">
              <SourceParameter reference="Parameter_4418"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_298">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_299">
              <SourceParameter reference="Parameter_4417"/>
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
          <Product metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4419" name="k1" value="1.9"/>
        </ListOfConstants>
        <KineticLaw function="Function_46">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_303">
              <SourceParameter reference="Compartment_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_304">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_305">
              <SourceParameter reference="Parameter_4419"/>
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
          <Substrate metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4420" name="k2" value="1.3"/>
        </ListOfConstants>
        <KineticLaw function="Function_47">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_309">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_310">
              <SourceParameter reference="Compartment_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_311">
              <SourceParameter reference="Parameter_4420"/>
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
          <Constant key="Parameter_4421" name="Km" value="0.5"/>
          <Constant key="Parameter_4422" name="Vm" value="0.65"/>
        </ListOfConstants>
        <KineticLaw function="Function_48">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_316">
              <SourceParameter reference="Compartment_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_317">
              <SourceParameter reference="Parameter_4421"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_318">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_319">
              <SourceParameter reference="Parameter_4422"/>
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
          <Constant key="Parameter_4423" name="Vd" value="0.95"/>
          <Constant key="Parameter_4424" name="Kd" value="0.2"/>
        </ListOfConstants>
        <KineticLaw function="Function_49">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_324">
              <SourceParameter reference="Compartment_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_325">
              <SourceParameter reference="Parameter_4424"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_326">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_327">
              <SourceParameter reference="Parameter_4423"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_0">
      <ModelParameterSet key="ModelParameterSet_0" name="Initial State">
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
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA]" value="60.22141790000001" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER]" value="150.55354475" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER]" value="150.55354475" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER]" value="150.55354475" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER]" value="602.2141790000001" type="Species" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER]" value="150.55354475" type="Species" simulationType="reactions"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=Vs" value="0.76" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=KI" value="1" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=n" value="4" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER],ParameterGroup=Parameters,Parameter=ks" value="0.38" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=V1" value="3.2" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=K1" value="2" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=V2" value="1.58" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=K2" value="2" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=V3" value="5" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=K3" value="2" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=V4" value="2.5" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=K4" value="2" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus],ParameterGroup=Parameters,Parameter=k1" value="1.9" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm],ParameterGroup=Parameters,Parameter=k2" value="1.3" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Km" value="0.5" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Vm" value="0.65" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Vd" value="0.95" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Kd" value="0.2" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
        </ModelParameterGroup>
      </ModelParameterSet>
    </ListOfModelParameterSets>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_4"/>
      <StateTemplateVariable objectReference="Metabolite_9"/>
      <StateTemplateVariable objectReference="Metabolite_7"/>
      <StateTemplateVariable objectReference="Metabolite_3"/>
      <StateTemplateVariable objectReference="Metabolite_5"/>
      <StateTemplateVariable objectReference="Metabolite_11"/>
      <StateTemplateVariable objectReference="Metabolite_13"/>
      <StateTemplateVariable objectReference="Metabolite_1"/>
      <StateTemplateVariable objectReference="Compartment_1"/>
      <StateTemplateVariable objectReference="Compartment_3"/>
      <StateTemplateVariable objectReference="Compartment_5"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 150.55354475 150.55354475 60.22141790000001 150.55354475 150.55354475 602.2141790000001 0 1e-015 1e-015 1e-015 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_12" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_8" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_11" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Report append="false" confirmOverwrite="false" reference="Report_87" target="" type="Deterministic(LSODA)" name="Deterministic (LSODA)"/><Problem type="Deterministic(LSODA)" name="Deterministic (LSODA)">
        <Parameter name="StepNumber" type="unsignedInteger" value="50"/>
        <Parameter name="StepSize" type="float" value="20"/>
        <Parameter name="Duration" type="float" value="1000"/>
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
    <Task key="Task_10" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report append="false" confirmOverwrite="false" reference="Report_32" target="D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\GoldbetterExample\PEData.txt"/><Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="5"/>
        <ParameterGroup name="ScanItems">
        <ParameterGroup name="ScanItem"><Parameter name="Number of steps" type="unsignedInteger" value="4000"/><Parameter name="Type" type="unsignedInteger" value="0"/><Parameter name="Object" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=InitialConcentration"/></ParameterGroup></ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="0"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_9" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_7" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_8" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_6" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_7" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_62" target="" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="true"/>
        <Parameter name="Calculate Statistics" type="bool" value="0"/>
        <ParameterGroup name="OptimizationItemList">
        <ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.2"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Kd,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.65"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Vm,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="2.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=K1,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="1.58"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=V2,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="1.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=KI,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.76"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=Vs,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="2.5"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=V4,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="5.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=V3,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="4.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=n,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="2.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=K4,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="2.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=K2,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="1.3"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm],ParameterGroup=Parameters,Parameter=k2,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="3.2"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=V1,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.38"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER],ParameterGroup=Parameters,Parameter=ks,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="2.0"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=K3,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="1.9"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus],ParameterGroup=Parameters,Parameter=k1,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.95"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Vd,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.5"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Km,Reference=Value"/></ParameterGroup></ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
        <ParameterGroup name="Experiment_0"><Parameter name="Data is Row Oriented" type="bool" value="1"/><Parameter name="Experiment Type" type="unsignedInteger" value="1"/><Parameter name="File Name" type="file" value="NoisyTimeCourseOutput.txt"/><Parameter name="First Row" type="unsignedInteger" value="1"/><Parameter name="Key" type="key" value="Experiment_0"/><Parameter name="Last Row" type="unsignedInteger" value="52"/><Parameter name="Normalize Weights per Experiment" type="bool" value="1"/><Parameter name="Number of Columns" type="unsignedInteger" value="8"/><ParameterGroup name="Object Map"><ParameterGroup name="0"><Parameter name="Role" type="unsignedInteger" value="3"/></ParameterGroup><ParameterGroup name="1"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="2"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="3"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="4"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="5"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="6"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="7"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup></ParameterGroup><Parameter name="Row containing Names" type="unsignedInteger" value="1"/><Parameter name="Separator" type="string" value=","/><Parameter name="Weight Method" type="unsignedInteger" value="1"/></ParameterGroup></ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
        </ParameterGroup>
      </Problem>
      <Method name="Hooke &amp;amp; Jeeves" type="HookeJeeves"><Parameter name="Iteration Limit" type="unsignedInteger" value="10"/><Parameter name="Tolerance" type="float" value="1e-05"/><Parameter name="Rho" type="float" value="0.2"/></Method></Task>
    <Task key="Task_6" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_4" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_12"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-009"/>
        <Parameter name="Use Reeder" type="bool" value="1"/>
        <Parameter name="Use Smallbone" type="bool" value="1"/>
      </Method>
    </Task>
    <Task key="Task_5" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_3" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_4" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_2" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_3" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_1" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_2" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
    <Task key="Task_1" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
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
    <Task key="Task_13" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_0" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_12"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_8" name="Steady-State" taskType="steadyState" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_7" name="Elementary Flux Modes" taskType="fluxMode" separator="&#9;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_6" name="Optimization" taskType="optimization" separator="&#9;" precision="6">
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
    <Report key="Report_5" name="Parameter Estimation" taskType="parameterFitting" separator="&#9;" precision="6">
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
    <Report key="Report_4" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#9;" precision="6">
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
    <Report key="Report_3" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#9;" precision="6">
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
    <Report key="Report_2" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#9;" precision="6">
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
    <Report key="Report_1" name="Sensitivities" taskType="sensitivities" separator="&#9;" precision="6">
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
    <Report key="Report_0" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#9;" precision="6">
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
  <Report taskType="Time-Course" separator="&#9;" precision="6" key="Report_87" name="Time-Course"><Comment/><Table printTitle="1"><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration"/></Table></Report><Report taskType="parameterFitting" separator="&#9;" precision="6" key="Report_32" name="parameter_estimation"><Comment/><Table printTitle="1"><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Kd,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Vm,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=K1,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=V2,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=KI,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=Vs,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=V4,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=V3,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=n,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=K4,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=K2,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm],ParameterGroup=Parameters,Parameter=k2,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=V1,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER],ParameterGroup=Parameters,Parameter=ks,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=K3,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus],ParameterGroup=Parameters,Parameter=k1,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Vd,Reference=Value"/><Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Km,Reference=Value"/><Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/></Table></Report></ListOfReports>
  <GUI>
  </GUI>
  <SBMLReference file="Goldbeter1995_CircClock.xml">
    <SBMLMap SBMLid="CYTOPLASM" COPASIkey="Compartment_3"/>
    <SBMLMap SBMLid="EmptySet" COPASIkey="Metabolite_1"/>
    <SBMLMap SBMLid="M" COPASIkey="Metabolite_3"/>
    <SBMLMap SBMLid="P0" COPASIkey="Metabolite_5"/>
    <SBMLMap SBMLid="P1" COPASIkey="Metabolite_7"/>
    <SBMLMap SBMLid="P2" COPASIkey="Metabolite_9"/>
    <SBMLMap SBMLid="Pn" COPASIkey="Metabolite_11"/>
    <SBMLMap SBMLid="Pt" COPASIkey="Metabolite_13"/>
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
