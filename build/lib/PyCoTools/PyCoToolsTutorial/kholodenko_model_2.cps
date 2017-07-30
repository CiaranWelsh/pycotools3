<!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-07-26 23:00:08 UTC --><?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?><COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="19" versionDevel="140" copasiSourcesModified="0">
  <ListOfFunctions>
    <Function key="Function_40" name="Function for MAPKKK activation" type="UserDefined" reversible="false">
      <Expression>
        V1*MKKK/((1+(MAPK_PP/Ki)^n)*(K1+MKKK))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_270" name="K1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_266" name="Ki" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_258" name="MAPK_PP" order="2" role="modifier"/>
        <ParameterDescription key="FunctionParameter_254" name="MKKK" order="3" role="substrate"/>
        <ParameterDescription key="FunctionParameter_264" name="V1" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_268" name="n" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_41" name="Function for MAPKKK inactivation" type="UserDefined" reversible="false">
      <Expression>
        V2*MKKK_P/(KK2+MKKK_P)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_246" name="KK2" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_267" name="MKKK_P" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_271" name="V2" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_42" name="Function for phosphorylation of MAPKK" type="UserDefined" reversible="false">
      <Expression>
        k3*MKKK_P*MKK/(KK3+MKK)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_275" name="KK3" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_273" name="MKK" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_269" name="MKKK_P" order="2" role="modifier"/>
        <ParameterDescription key="FunctionParameter_262" name="k3" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_43" name="Function for dephosphorylation of MAPKK-P" type="UserDefined" reversible="false">
      <Expression>
        V6*MKK_P/(KK6+MKK_P)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_277" name="KK6" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_272" name="MKK_P" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_276" name="V6" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="Function for phosphorylation of MAPK" type="UserDefined" reversible="false">
      <Expression>
        k7*MKK_PP*MAPK/(KK7+MAPK)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_282" name="KK7" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_280" name="MAPK" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_274" name="MKK_PP" order="2" role="modifier"/>
        <ParameterDescription key="FunctionParameter_278" name="k7" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="Function for dephosphorylation of MAPK-P" type="UserDefined" reversible="false">
      <Expression>
        V10*MAPK_P/(KK10+MAPK_P)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_284" name="KK10" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_279" name="MAPK_P" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_283" name="V10" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_46" name="Function for phosphorylation of MAPKK-P" type="UserDefined" reversible="false">
      <Expression>
        k4*MKKK_P*MKK_P/(KK4+MKK_P)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_316" name="KK4" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_310" name="MKKK_P" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_315" name="MKK_P" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_314" name="k4" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="Function for dephosphorylation of MAPKK-PP" type="UserDefined" reversible="false">
      <Expression>
        V5*MKK_PP/(KK5+MKK_PP)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_313" name="KK5" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_317" name="MKK_PP" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_308" name="V5" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="Function for phosphorylation of MAPK-P" type="UserDefined" reversible="false">
      <Expression>
        k8*MKK_PP*MAPK_P/(KK8+MAPK_P)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_318" name="KK8" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_320" name="MAPK_P" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_309" name="MKK_PP" order="2" role="modifier"/>
        <ParameterDescription key="FunctionParameter_311" name="k8" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="Function for dephosphorylation of MAPK-PP" type="UserDefined" reversible="false">
      <Expression>
        V9*MAPK_PP/(KK9+MAPK_PP)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_321" name="KK9" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_319" name="MAPK_PP" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_306" name="V9" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_7" name="Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade" simulationType="time" timeUnit="s" volumeUnit="l" areaUnit="m&#178;" lengthUnit="m" quantityUnit="nmol" type="deterministic" avogadroConstant="6.022140857e+23">
    <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_7">
    <bqbiol:hasTaxon>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/taxonomy/8355"/>
      </rdf:Bag>
    </bqbiol:hasTaxon>
    <dcterms:bibliographicCitation>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <CopasiMT:isDescribedBy rdf:resource="http://identifiers.org/pubmed/10712587"/>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:bibliographicCitation>
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2005-02-12T00:18:12Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <dcterms:creator>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>Herbert_Sauro@kgi.edu</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Sauro</vCard:Family>
                <vCard:Given>Herbert</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Keck Graduate Institute</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:creator>
    <dcterms:modified>
      <rdf:Description>
        <dcterms:W3CDTF>2015-06-02T12:04:33Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:modified>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/MODEL6615119181"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/BIOMD0000000010"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_634"/>
      </rdf:Bag>
    </CopasiMT:isHomologTo>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0000165"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      <body xmlns="http://www.w3.org/1999/xhtml">
    <div class="dc:title">Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade</div>
    <div class="dc:description">
      <p>The combination of ultrasensitivity and negative feedback bring sustained oscillations in the mitogen-activated protein kinase cascades.</p>
    </div>
    <div class="dc:bibliographicCitation">
      <p>This model is described in the article:</p>
      <div class="bibo:title">
        <a href="http://identifiers.org/pubmed/10712587" title="Access to this publication">Negative feedback and ultrasensitivity can bring about oscillations in the mitogen-activated protein kinase cascades.</a>
      </div>
      <div class="bibo:authorList">Kholodenko BN</div>
      <div class="bibo:Journal">Eur. J. Biochem. 2000; 267(6):1583-8</div>
      <p>Abstract:</p>
      <div class="bibo:abstract">
        <p>Functional organization of signal transduction into protein phosphorylation cascades, such as the mitogen-activated protein kinase (MAPK) cascades, greatly enhances the sensitivity of cellular targets to external stimuli. The sensitivity increases multiplicatively with the number of cascade levels, so that a tiny change in a stimulus results in a large change in the response, the phenomenon referred to as ultrasensitivity. In a variety of cell types, the MAPK cascades are imbedded in long feedback loops, positive or negative, depending on whether the terminal kinase stimulates or inhibits the activation of the initial level. Here we demonstrate that a negative feedback loop combined with intrinsic ultrasensitivity of the MAPK cascade can bring about sustained oscillations in MAPK phosphorylation. Based on recent kinetic data on the MAPK cascades, we predict that the period of oscillations can range from minutes to hours. The phosphorylation level can vary between the base level and almost 100% of the total protein. The oscillations of the phosphorylation cascades and slow protein diffusion in the cytoplasm can lead to intracellular waves of phospho-proteins.</p>
      </div>
    </div>
    <div class="dc:publisher">
      <p>This model is hosted on        <a href="http://www.ebi.ac.uk/biomodels/">BioModels Database</a>
            and identified by:        <a href="http://identifiers.org/biomodels.db/BIOMD0000000010">BIOMD0000000010</a>
            .        </p>
    <p>To cite BioModels Database, please use:        <a href="http://identifiers.org/pubmed/20587024" title="Latest BioModels Database publication">BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models</a>
            .        </p>
</div><div class="dc:license">
  <p>To the extent possible under law, all copyright and related or neighbouring rights to this encoded model have been dedicated to the public domain worldwide. Please refer to        <a href="http://creativecommons.org/publicdomain/zero/1.0/" title="Access to: CC0 1.0 Universal (CC0 1.0), Public Domain Dedication">CC0 Public Domain Dedication</a>
            for more information.        </p>
</div>
</body>
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_6" name="uVol" simulationType="fixed" dimensionality="3">
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_33" name="Mos" simulationType="reactions" compartment="Compartment_6">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_33">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P09560"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_1" name="Mos-P" simulationType="reactions" compartment="Compartment_6">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_1">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P09560"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_11" name="Mek1" simulationType="reactions" compartment="Compartment_6">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_11">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q05116"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_45" name="Mek1-P" simulationType="reactions" compartment="Compartment_6">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_45">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q05116"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_47" name="Mek1-PP" simulationType="reactions" compartment="Compartment_6">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_47">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q05116"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_49" name="Erk2" simulationType="reactions" compartment="Compartment_6">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_49">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P26696"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_51" name="Erk2-P" simulationType="reactions" compartment="Compartment_6">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_51">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P26696"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_53" name="Erk2-PP" simulationType="reactions" compartment="Compartment_6">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_53">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P26696"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_11" name="Mos_tot" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_11">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-07-26T23:40:17Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos],Reference=Concentration&gt;+&lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos-P],Reference=Concentration&gt;
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_10" name="Mos-P_tot" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_10">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-07-26T23:39:53Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos-P],Reference=Concentration&gt;
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_9" name="Mek_tot" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_9">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-07-26T23:38:52Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-P],Reference=Concentration&gt;+&lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-PP],Reference=Concentration&gt;+&lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1],Reference=Concentration&gt;
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_8" name="Mek-P_tot" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_8">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-07-26T23:38:19Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-P],Reference=Concentration&gt;+&lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-PP],Reference=Concentration&gt;
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_7" name="Erk_tot" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_7">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-07-26T23:37:52Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-P],Reference=Concentration&gt;+&lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-PP],Reference=Concentration&gt;+&lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2],Reference=Concentration&gt;
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_6" name="Erk-P_tot" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_6">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-07-26T23:37:04Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-P],Reference=Concentration&gt;+&lt;CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-PP],Reference=Concentration&gt;
        </Expression>
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_0" name="MAPKKK activation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_0">
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_525"/>
      </rdf:Bag>
    </CopasiMT:isHomologTo>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.11.1"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0000185"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0008349"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_33" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_53" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4372" name="V1" value="2.5"/>
          <Constant key="Parameter_4353" name="Ki" value="9"/>
          <Constant key="Parameter_4352" name="n" value="1"/>
          <Constant key="Parameter_4351" name="K1" value="10"/>
        </ListOfConstants>
        <KineticLaw function="Function_40" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Parameter_4351"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="Parameter_4353"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="Metabolite_33"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Parameter_4372"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Parameter_4352"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1" name="MAPKKK inactivation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_1">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/3.1.3.16"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006470"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0051390"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_33" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4350" name="V2" value="0.25"/>
          <Constant key="Parameter_4347" name="KK2" value="8"/>
        </ListOfConstants>
        <KineticLaw function="Function_41" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="Parameter_4347"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Parameter_4350"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_2" name="phosphorylation of MAPKK" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_2">
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_614"/>
      </rdf:Bag>
    </CopasiMT:isHomologTo>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.11.25"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0004709"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006468"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_45" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4346" name="k3" value="0.025"/>
          <Constant key="Parameter_4348" name="KK3" value="15"/>
        </ListOfConstants>
        <KineticLaw function="Function_42" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Parameter_4348"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="Parameter_4346"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_3" name="phosphorylation of MAPKK-P" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_3">
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_614"/>
      </rdf:Bag>
    </CopasiMT:isHomologTo>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.11.25"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0000186"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0004709"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006468"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_45" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4349" name="k4" value="0.025"/>
          <Constant key="Parameter_4358" name="KK4" value="15"/>
        </ListOfConstants>
        <KineticLaw function="Function_46" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_316">
              <SourceParameter reference="Parameter_4358"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_310">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_315">
              <SourceParameter reference="Metabolite_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_314">
              <SourceParameter reference="Parameter_4349"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_4" name="dephosphorylation of MAPKK-PP" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_4">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/3.1.3.16"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006470"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0051389"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_45" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4357" name="V5" value="0.75"/>
          <Constant key="Parameter_4356" name="KK5" value="15"/>
        </ListOfConstants>
        <KineticLaw function="Function_47" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_313">
              <SourceParameter reference="Parameter_4356"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_317">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_308">
              <SourceParameter reference="Parameter_4357"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_5" name="dephosphorylation of MAPKK-P" reversible="false" fast="false">
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
          <Substrate metabolite="Metabolite_45" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4355" name="V6" value="0.75"/>
          <Constant key="Parameter_4354" name="KK6" value="15"/>
        </ListOfConstants>
        <KineticLaw function="Function_43" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Parameter_4354"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="Metabolite_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Parameter_4355"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_16" name="phosphorylation of MAPK" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_16">
    <CopasiMT:hasVersion>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_136"/>
        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_2247"/>
      </rdf:Bag>
    </CopasiMT:hasVersion>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.12.2"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0004708"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006468"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_51" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4371" name="k7" value="0.025"/>
          <Constant key="Parameter_4370" name="KK7" value="15"/>
        </ListOfConstants>
        <KineticLaw function="Function_44" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="Parameter_4370"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="Metabolite_49"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Parameter_4371"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_17" name="phosphorylation of MAPK-P" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_17">
    <CopasiMT:hasVersion>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_136"/>
        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_2247"/>
      </rdf:Bag>
    </CopasiMT:hasVersion>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.12.2"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0000187"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0004708"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006468"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_51" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_53" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4252" name="k8" value="0.025"/>
          <Constant key="Parameter_4251" name="KK8" value="15"/>
        </ListOfConstants>
        <KineticLaw function="Function_48" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_318">
              <SourceParameter reference="Parameter_4251"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_320">
              <SourceParameter reference="Metabolite_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_309">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_311">
              <SourceParameter reference="Parameter_4252"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_18" name="dephosphorylation of MAPK-PP" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_18">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/ec-code/3.1.3.16"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0000188"/>
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006470"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_53" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_51" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4250" name="V9" value="0.5"/>
          <Constant key="Parameter_4249" name="KK9" value="15"/>
        </ListOfConstants>
        <KineticLaw function="Function_49" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_321">
              <SourceParameter reference="Parameter_4249"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_319">
              <SourceParameter reference="Metabolite_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_306">
              <SourceParameter reference="Parameter_4250"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_19" name="dephosphorylation of MAPK-P" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_19">
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
          <Substrate metabolite="Metabolite_51" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4248" name="V10" value="0.5"/>
          <Constant key="Parameter_4247" name="KK10" value="15"/>
        </ListOfConstants>
        <KineticLaw function="Function_45" unitType="Default" scalingCompartment="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Parameter_4247"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Parameter_4248"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_1">
      <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
        <ModelParameterGroup cn="String=Initial Time" type="Group">
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade" value="0" type="Model" simulationType="time"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol]" value="1" type="Compartment" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Species Values" type="Group">
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos]" value="5.419926771299998e+16" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos-P]" value="6022140856999998" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1]" value="1.68619943996e+17" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-P]" value="6022140856999998" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-PP]" value="6022140856999998" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2]" value="1.68619943996e+17" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-P]" value="6022140856999998" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-PP]" value="6022140856999998" type="Species" simulationType="reactions"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Mos_tot]" value="99.99999999999996" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Mos-P_tot]" value="9.999999999999996" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Mek_tot]" value="299.9999999999999" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Mek-P_tot]" value="19.99999999999999" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Erk_tot]" value="299.9999999999999" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Erk-P_tot]" value="19.99999999999999" type="ModelValue" simulationType="assignment"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation],ParameterGroup=Parameters,Parameter=V1" value="2.5" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation],ParameterGroup=Parameters,Parameter=Ki" value="9" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation],ParameterGroup=Parameters,Parameter=n" value="1" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation],ParameterGroup=Parameters,Parameter=K1" value="10" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK inactivation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK inactivation],ParameterGroup=Parameters,Parameter=V2" value="0.25" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK inactivation],ParameterGroup=Parameters,Parameter=KK2" value="8" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK],ParameterGroup=Parameters,Parameter=k3" value="0.025" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK],ParameterGroup=Parameters,Parameter=KK3" value="15" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK-P]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK-P],ParameterGroup=Parameters,Parameter=k4" value="0.025" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK-P],ParameterGroup=Parameters,Parameter=KK4" value="15" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-PP]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-PP],ParameterGroup=Parameters,Parameter=V5" value="0.75" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-PP],ParameterGroup=Parameters,Parameter=KK5" value="15" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-P]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-P],ParameterGroup=Parameters,Parameter=V6" value="0.75" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-P],ParameterGroup=Parameters,Parameter=KK6" value="15" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK],ParameterGroup=Parameters,Parameter=k7" value="0.025" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK],ParameterGroup=Parameters,Parameter=KK7" value="15" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK-P]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK-P],ParameterGroup=Parameters,Parameter=k8" value="0.025" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK-P],ParameterGroup=Parameters,Parameter=KK8" value="15" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-PP]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-PP],ParameterGroup=Parameters,Parameter=V9" value="0.5" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-PP],ParameterGroup=Parameters,Parameter=KK9" value="15" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-P]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-P],ParameterGroup=Parameters,Parameter=V10" value="0.5" type="ReactionParameter" simulationType="fixed"/>
            <ModelParameter cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-P],ParameterGroup=Parameters,Parameter=KK10" value="15" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
        </ModelParameterGroup>
      </ModelParameterSet>
    </ListOfModelParameterSets>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_7"/>
      <StateTemplateVariable objectReference="Metabolite_45"/>
      <StateTemplateVariable objectReference="Metabolite_51"/>
      <StateTemplateVariable objectReference="Metabolite_33"/>
      <StateTemplateVariable objectReference="Metabolite_11"/>
      <StateTemplateVariable objectReference="Metabolite_49"/>
      <StateTemplateVariable objectReference="Metabolite_47"/>
      <StateTemplateVariable objectReference="Metabolite_1"/>
      <StateTemplateVariable objectReference="Metabolite_53"/>
      <StateTemplateVariable objectReference="ModelValue_11"/>
      <StateTemplateVariable objectReference="ModelValue_10"/>
      <StateTemplateVariable objectReference="ModelValue_9"/>
      <StateTemplateVariable objectReference="ModelValue_8"/>
      <StateTemplateVariable objectReference="ModelValue_7"/>
      <StateTemplateVariable objectReference="ModelValue_6"/>
      <StateTemplateVariable objectReference="Compartment_6"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 6022140856999998 6022140856999998 5.419926771299998e+16 1.68619943996e+17 1.68619943996e+17 6022140856999998 6022140856999998 6022140856999998 99.99999999999996 9.999999999999996 299.9999999999999 19.99999999999999 299.9999999999999 19.99999999999999 1 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_27" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_9" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="JacobianRequested" type="bool" value="1"/>
        <Parameter name="StabilityAnalysisRequested" type="bool" value="1"/>
      </Problem>
      <Method name="Enhanced Newton" type="EnhancedNewton">
        <Parameter name="Resolution" type="unsignedFloat" value="1e-09"/>
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
      <Report append="false" confirmOverwrite="false" reference="Report_30" target="" type="Deterministic(LSODA)" name="Deterministic (LSODA)"/><Problem type="Deterministic(LSODA)" name="Deterministic (LSODA)">
        <Parameter name="AutomaticStepSize" type="bool" value="0"/>
        <Parameter name="StepNumber" type="unsignedInteger" value="10"/>
        <Parameter name="StepSize" type="float" value="100"/>
        <Parameter name="Duration" type="float" value="1000"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0.0"/>
        <Parameter name="Output Event" type="bool" value="false"/>
        <Parameter name="Start in Steady State" type="bool" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-6"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
        <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
      </Method>
    </Task>
    <Task key="Task_16" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report append="false" confirmOverwrite="false" reference="Report_82" target="/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/MultipleParameterEstimationResults/parameter_estimation_data22.txt"/><Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="5"/>
        <ParameterGroup name="ScanItems">
        <ParameterGroup name="ScanItem"><Parameter name="Number of steps" type="unsignedInteger" value="100"/><Parameter name="Type" type="unsignedInteger" value="0"/><Parameter name="Object" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-PP],Reference=InitialConcentration"/></ParameterGroup></ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="false"/>
        <Parameter name="Adjust initial conditions" type="bool" value="false"/>
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
      <Report reference="Report_32" target="" append="false" confirmOverwrite="false"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="true"/>
        <Parameter name="Calculate Statistics" type="bool" value="0"/>
        <ParameterGroup name="OptimizationItemList">
        <ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK],ParameterGroup=Parameters,Parameter=KK3,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation],ParameterGroup=Parameters,Parameter=K1,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-PP],ParameterGroup=Parameters,Parameter=V9,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK],ParameterGroup=Parameters,Parameter=k7,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK-P],ParameterGroup=Parameters,Parameter=k8,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK inactivation],ParameterGroup=Parameters,Parameter=KK2,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK inactivation],ParameterGroup=Parameters,Parameter=V2,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK],ParameterGroup=Parameters,Parameter=k3,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK-P],ParameterGroup=Parameters,Parameter=k4,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-PP],ParameterGroup=Parameters,Parameter=KK5,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-PP],ParameterGroup=Parameters,Parameter=KK9,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-P],ParameterGroup=Parameters,Parameter=KK6,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPKK-P],ParameterGroup=Parameters,Parameter=KK4,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation],ParameterGroup=Parameters,Parameter=V1,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation],ParameterGroup=Parameters,Parameter=Ki,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK],ParameterGroup=Parameters,Parameter=KK7,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-P],ParameterGroup=Parameters,Parameter=KK10,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[phosphorylation of MAPK-P],ParameterGroup=Parameters,Parameter=KK8,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-PP],ParameterGroup=Parameters,Parameter=V5,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPK-P],ParameterGroup=Parameters,Parameter=V10,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[dephosphorylation of MAPKK-P],ParameterGroup=Parameters,Parameter=V6,Reference=Value"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="0.1"/><Parameter name="UpperBound" type="cn" value="100"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Reactions[MAPKKK activation],ParameterGroup=Parameters,Parameter=n,Reference=Value"/></ParameterGroup></ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
        <ParameterGroup name="Experiment_0"><Parameter name="Data is Row Oriented" type="bool" value="1"/><Parameter name="Experiment Type" type="unsignedInteger" value="1"/><Parameter name="File Name" type="file" value="parameter_estimation_synthetic_data.txt"/><Parameter name="First Row" type="unsignedInteger" value="1"/><Parameter name="Key" type="key" value="Experiment_0"/><Parameter name="Last Row" type="unsignedInteger" value="12"/><Parameter name="Normalize Weights per Experiment" type="bool" value="1"/><Parameter name="Number of Columns" type="unsignedInteger" value="9"/><ParameterGroup name="Object Map"><ParameterGroup name="0"><Parameter name="Role" type="unsignedInteger" value="3"/></ParameterGroup><ParameterGroup name="1"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-PP],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="2"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="3"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="4"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-P],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="5"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-PP],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="6"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos-P],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="7"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="8"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-P],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup></ParameterGroup><Parameter name="Row containing Names" type="unsignedInteger" value="1"/><Parameter name="separator" type="string" value="&#9;"/><Parameter name="Weight Method" type="unsignedInteger" value="2"/></ParameterGroup></ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
        </ParameterGroup>
      </Problem>
      <Method name="Particle Swarm" type="ParticleSwarm"><Parameter name="Iteration Limit" type="unsignedInteger" value="2000"/><Parameter name="Swarm Size" type="unsignedInteger" value="100"/><Parameter name="Std. Deviation" type="unsignedFloat" value="1e-06"/><Parameter name="Random Number Generator" type="unsignedInteger" value="1"/><Parameter name="Seed" type="unsignedInteger" value="0"/></Method></Task>
    <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_27"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Use Reder" type="bool" value="1"/>
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
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
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
        <Parameter name="Deuflhard Tolerance" type="unsignedFloat" value="1e-06"/>
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
          <ParameterGroup name="Variables">
            <Parameter name="SingleObject" type="cn" value=""/>
            <Parameter name="ObjectListType" type="unsignedInteger" value="0"/>
          </ParameterGroup>
        </ParameterGroup>
      </Problem>
      <Method name="Sensitivities Method" type="SensitivitiesMethod">
        <Parameter name="Delta factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Delta minimum" type="unsignedFloat" value="1e-12"/>
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
        <Parameter name="AutomaticStepSize" type="bool" value="0"/>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Start in Steady State" type="bool" value="0"/>
        <Parameter name="LimitCrossings" type="bool" value="0"/>
        <Parameter name="NumCrossingsLimit" type="unsignedInteger" value="0"/>
        <Parameter name="LimitOutTime" type="bool" value="0"/>
        <Parameter name="LimitOutCrossings" type="bool" value="0"/>
        <Parameter name="PositiveDirection" type="bool" value="1"/>
        <Parameter name="NumOutCrossingsLimit" type="unsignedInteger" value="0"/>
        <Parameter name="LimitUntilConvergence" type="bool" value="0"/>
        <Parameter name="ConvergenceTolerance" type="float" value="1e-06"/>
        <Parameter name="Threshold" type="float" value="0"/>
        <Parameter name="DelayOutputUntilConvergence" type="bool" value="0"/>
        <Parameter name="OutputConvergenceTolerance" type="float" value="1e-06"/>
        <ParameterText name="TriggerExpression" type="expression">
          
        </ParameterText>
        <Parameter name="SingleVariable" type="cn" value=""/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
        <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
      </Method>
    </Task>
    <Task key="Task_14" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_17" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_27"/>
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
  <Report taskType="Time-Course" separator="&#9;" precision="6" key="Report_30" name="Time-Course"><Comment/><Table printTitle="1"><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-PP],Reference=Concentration"/><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2],Reference=Concentration"/><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos],Reference=Concentration"/><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-P],Reference=Concentration"/><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-PP],Reference=Concentration"/><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos-P],Reference=Concentration"/><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1],Reference=Concentration"/><Object cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-P],Reference=Concentration"/></Table></Report><Report taskType="parameterFitting" separator="&#9;" precision="6" key="Report_32" name="parameter_estimation"><Comment/><Footer><Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/><Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/></Footer></Report><Report taskType="parameterFitting" separator="&#9;" precision="6" key="Report_82" name="multi_parameter_estimation"><Comment/><Table printTitle="1"><Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/><Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/></Table></Report></ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[Mos]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Mos-P]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mos-P],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Mek1]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Mek1-P]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-P],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Mek1-PP]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Mek1-PP],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Erk2]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Erk2-P]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-P],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Erk2-PP]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Compartments[uVol],Vector=Metabolites[Erk2-PP],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Mos_tot]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Mos_tot],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Mos-P_tot]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Mos-P_tot],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Mek_tot]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Mek_tot],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Mek-P_tot]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Mek-P_tot],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Erk_tot]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Erk_tot],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Erk-P_tot]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Kholodenko2000 - Ultrasensitivity and negative feedback bring oscillations in MAPK cascade,Vector=Values[Erk-P_tot],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <SBMLReference file="Kholodenko2000.xml">
    <SBMLMap SBMLid="J0" COPASIkey="Reaction_0"/>
    <SBMLMap SBMLid="J1" COPASIkey="Reaction_1"/>
    <SBMLMap SBMLid="J2" COPASIkey="Reaction_2"/>
    <SBMLMap SBMLid="J3" COPASIkey="Reaction_3"/>
    <SBMLMap SBMLid="J4" COPASIkey="Reaction_4"/>
    <SBMLMap SBMLid="J5" COPASIkey="Reaction_5"/>
    <SBMLMap SBMLid="J6" COPASIkey="Reaction_16"/>
    <SBMLMap SBMLid="J7" COPASIkey="Reaction_17"/>
    <SBMLMap SBMLid="J8" COPASIkey="Reaction_18"/>
    <SBMLMap SBMLid="J9" COPASIkey="Reaction_19"/>
    <SBMLMap SBMLid="MAPK" COPASIkey="Metabolite_49"/>
    <SBMLMap SBMLid="MAPK_P" COPASIkey="Metabolite_51"/>
    <SBMLMap SBMLid="MAPK_PP" COPASIkey="Metabolite_53"/>
    <SBMLMap SBMLid="MKK" COPASIkey="Metabolite_11"/>
    <SBMLMap SBMLid="MKKK" COPASIkey="Metabolite_33"/>
    <SBMLMap SBMLid="MKKK_P" COPASIkey="Metabolite_1"/>
    <SBMLMap SBMLid="MKK_P" COPASIkey="Metabolite_45"/>
    <SBMLMap SBMLid="MKK_PP" COPASIkey="Metabolite_47"/>
    <SBMLMap SBMLid="uVol" COPASIkey="Compartment_6"/>
  </SBMLReference>
  <ListOfUnitDefinitions>
    <UnitDefinition key="Unit_0" name="meter" symbol="m">
      <Expression>
        m
      </Expression>
    </UnitDefinition>
    <UnitDefinition key="Unit_2" name="second" symbol="s">
      <Expression>
        s
      </Expression>
    </UnitDefinition>
  </ListOfUnitDefinitions>
</COPASI>