# -*- coding: utf-8 -*-



class Models(object):

    @property
    def published_zi(self):
        """
        This is the published zi2012 model
        of TGFb signalling
        :return:
        """
        return """<?xml version="1.0" encoding="UTF-8"?>
    <!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-09-27 17:55:10 UTC -->
    <?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
    <COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="19" versionDevel="140" copasiSourcesModified="0">
      <ListOfFunctions>
        <Function key="Function_6" name="Constant flux (irreversible)" type="PreDefined" reversible="false">
          <Expression>
            v
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_49" name="v" order="0" role="constant"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_13" name="Mass action (irreversible)" type="MassAction" reversible="false">
          <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
       <rdf:Description rdf:about="#Function_13">
       <CopasiMT:is rdf:resource="urn:miriam:obo.sbo:SBO:0000041" />
       </rdf:Description>
       </rdf:RDF>
          </MiriamAnnotation>
          <Comment>
            <body xmlns="http://www.w3.org/1999/xhtml">
    <b>Mass action rate law for first order irreversible reactions</b>
    <p>
    Reaction scheme where the products are created from the reactants and the change of a product quantity is proportional to the product of reactant activities. The reaction scheme does not include any reverse process that creates the reactants from the products. The change of a product quantity is proportional to the quantity of one reactant.
    </p>
    </body>
          </Comment>
          <Expression>
            k1*PRODUCT&lt;substrate_i>
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_81" name="k1" order="0" role="constant"/>
            <ParameterDescription key="FunctionParameter_79" name="substrate" order="1" role="substrate"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_40" name="Function for R1_Smad2_import" type="UserDefined" reversible="false">
          <MiriamAnnotation>
    <rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Function_40">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T14:07:29Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
      </rdf:Description>
    </rdf:RDF>
          </MiriamAnnotation>
          <Expression>
            V_cyt*Kimp_Smad2c*Smad2c
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_254" name="Kimp_Smad2c" order="0" role="constant"/>
            <ParameterDescription key="FunctionParameter_258" name="Smad2c" order="1" role="substrate"/>
            <ParameterDescription key="FunctionParameter_264" name="V_cyt" order="2" role="volume"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_41" name="Function for R2_Smad2_export" type="UserDefined" reversible="false">
          <Expression>
            V_nuc*Kexp_Smad2n*Smad2n
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_262" name="Kexp_Smad2n" order="0" role="constant"/>
            <ParameterDescription key="FunctionParameter_267" name="Smad2n" order="1" role="substrate"/>
            <ParameterDescription key="FunctionParameter_265" name="V_nuc" order="2" role="volume"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_42" name="Function for R3_Smad4_import" type="UserDefined" reversible="false">
          <Expression>
            V_cyt*Kimp_Smad4c*Smad4c
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_246" name="Kimp_Smad4c" order="0" role="constant"/>
            <ParameterDescription key="FunctionParameter_270" name="Smad4c" order="1" role="substrate"/>
            <ParameterDescription key="FunctionParameter_268" name="V_cyt" order="2" role="volume"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_43" name="Function for R4_Smad4_export" type="UserDefined" reversible="false">
          <Expression>
            V_nuc*Kexp_Smad4n*Smad4n
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_266" name="Kexp_Smad4n" order="0" role="constant"/>
            <ParameterDescription key="FunctionParameter_273" name="Smad4n" order="1" role="substrate"/>
            <ParameterDescription key="FunctionParameter_271" name="V_nuc" order="2" role="volume"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_44" name="Function for R15_T2R_EE_recycling" type="UserDefined" reversible="false">
          <Expression>
            V_cyt*kr_EE*T2R_EE
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_276" name="T2R_EE" order="0" role="substrate"/>
            <ParameterDescription key="FunctionParameter_274" name="V_cyt" order="1" role="volume"/>
            <ParameterDescription key="FunctionParameter_269" name="kr_EE" order="2" role="constant"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_45" name="Function for R17_LRC_formation" type="UserDefined" reversible="false">
          <Expression>
            V_cyt*k_LRC*TGF_beta*T2R_Surf*T1R_Surf
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_283" name="T1R_Surf" order="0" role="substrate"/>
            <ParameterDescription key="FunctionParameter_281" name="T2R_Surf" order="1" role="substrate"/>
            <ParameterDescription key="FunctionParameter_279" name="TGF_beta" order="2" role="substrate"/>
            <ParameterDescription key="FunctionParameter_277" name="V_cyt" order="3" role="volume"/>
            <ParameterDescription key="FunctionParameter_272" name="k_LRC" order="4" role="constant"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_46" name="Function for R19_LRC_Cave_recycling" type="UserDefined" reversible="false">
          <Expression>
            V_cyt*kr_Cave*LRC_Cave
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_275" name="LRC_Cave" order="0" role="substrate"/>
            <ParameterDescription key="FunctionParameter_284" name="V_cyt" order="1" role="volume"/>
            <ParameterDescription key="FunctionParameter_280" name="kr_Cave" order="2" role="constant"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_47" name="Function for R21_LRC_EE_recycling" type="UserDefined" reversible="false">
          <Expression>
            V_cyt*kr_EE*LRC_EE
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_287" name="LRC_EE" order="0" role="substrate"/>
            <ParameterDescription key="FunctionParameter_285" name="V_cyt" order="1" role="volume"/>
            <ParameterDescription key="FunctionParameter_282" name="kr_EE" order="2" role="constant"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_48" name="Function for R23_Smads_Complex_formation" type="UserDefined" reversible="false">
          <MiriamAnnotation>
    <rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Function_48">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-22T12:24:54Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
      </rdf:Description>
    </rdf:RDF>
          </MiriamAnnotation>
          <Expression>
            k_Smads_Complex_c*Smad2c*Smad4c*LRC_EE
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_292" name="LRC_EE" order="0" role="modifier"/>
            <ParameterDescription key="FunctionParameter_278" name="Smad2c" order="1" role="substrate"/>
            <ParameterDescription key="FunctionParameter_290" name="Smad4c" order="2" role="substrate"/>
            <ParameterDescription key="FunctionParameter_288" name="k_Smads_Complex_c" order="3" role="constant"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_49" name="Function for R24_Smads_Complex_import" type="UserDefined" reversible="false">
          <Expression>
            V_cyt*Kimp_Smads_Complex_c*Smads_Complex_c
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_289" name="Kimp_Smads_Complex_c" order="0" role="constant"/>
            <ParameterDescription key="FunctionParameter_294" name="Smads_Complex_c" order="1" role="substrate"/>
            <ParameterDescription key="FunctionParameter_293" name="V_cyt" order="2" role="volume"/>
          </ListOfParameterDescriptions>
        </Function>
        <Function key="Function_50" name="Function for R26_LRC_Cave_degradation" type="UserDefined" reversible="false">
          <Expression>
            Klid*LRC_Cave*Smads_Complex_n
          </Expression>
          <ListOfParameterDescriptions>
            <ParameterDescription key="FunctionParameter_295" name="Klid" order="0" role="constant"/>
            <ParameterDescription key="FunctionParameter_291" name="LRC_Cave" order="1" role="substrate"/>
            <ParameterDescription key="FunctionParameter_297" name="Smads_Complex_n" order="2" role="modifier"/>
          </ListOfParameterDescriptions>
        </Function>
      </ListOfFunctions>
      <Model key="Model_3" name="Zi2007_TGFbeta_signaling" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="nmol" type="deterministic" avogadroConstant="6.022140857e+23">
        <MiriamAnnotation>
    <rdf:RDF
       xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
       xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
       xmlns:dcterms="http://purl.org/dc/terms/"
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
       xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
      <rdf:Description rdf:about="#Model_3">
        <bqbiol:hasTaxon>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/taxonomy/131567"/>
          </rdf:Bag>
        </bqbiol:hasTaxon>
        <dcterms:bibliographicCitation>
          <rdf:Bag>
            <rdf:li>
              <rdf:Description>
                <CopasiMT:isDescribedBy rdf:resource="http://identifiers.org/pubmed/17895977"/>
              </rdf:Description>
            </rdf:li>
          </rdf:Bag>
        </dcterms:bibliographicCitation>
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2008-02-14T09:21:13Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <dcterms:creator>
          <rdf:Bag>
            <rdf:li>
              <rdf:Description>
                <vCard:EMAIL>hdharuri@cds.caltech.edu</vCard:EMAIL>
                <vCard:N>
                  <rdf:Description>
                    <vCard:Family>Dharuri</vCard:Family>
                    <vCard:Given>Harish</vCard:Given>
                  </rdf:Description>
                </vCard:N>
                <vCard:ORG>
                  <rdf:Description>
                    <vCard:Orgname>California Institute of Technology</vCard:Orgname>
                  </rdf:Description>
                </vCard:ORG>
              </rdf:Description>
            </rdf:li>
            <rdf:li>
              <rdf:Description>
                <vCard:N>
                  <rdf:Description>
                    <vCard:Family>Yang</vCard:Family>
                    <vCard:Given>Kun</vCard:Given>
                  </rdf:Description>
                </vCard:N>
                <vCard:ORG>
                  <rdf:Description>
                    <vCard:Orgname>Beijing National Laboratory for Molecular Sciences</vCard:Orgname>
                  </rdf:Description>
                </vCard:ORG>
              </rdf:Description>
            </rdf:li>
            <rdf:li>
              <rdf:Description>
                <vCard:EMAIL>klipp@molgen.mpg.de</vCard:EMAIL>
                <vCard:N>
                  <rdf:Description>
                    <vCard:Family>Klipp</vCard:Family>
                    <vCard:Given>Edda</vCard:Given>
                  </rdf:Description>
                </vCard:N>
                <vCard:ORG>
                  <rdf:Description>
                    <vCard:Orgname>Max Planck Institute for molecular genetics</vCard:Orgname>
                  </rdf:Description>
                </vCard:ORG>
              </rdf:Description>
            </rdf:li>
          </rdf:Bag>
        </dcterms:creator>
        <dcterms:modified>
          <rdf:Description>
            <dcterms:W3CDTF>2012-07-05T16:45:46Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:modified>
        <CopasiMT:is>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/biomodels.db/MODEL3388742457"/>
          </rdf:Bag>
        </CopasiMT:is>
        <CopasiMT:is>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/biomodels.db/BIOMD0000000163"/>
          </rdf:Bag>
        </CopasiMT:is>
        <CopasiMT:isPartOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/kegg.pathway/hsa04350"/>
          </rdf:Bag>
        </CopasiMT:isPartOf>
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015"/>
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>

        </MiriamAnnotation>
        <Comment>
          <body xmlns="http://www.w3.org/1999/xhtml">
        <p>The model reproduces the time profiles of Total Smad2 in the nucleus as well as the cytoplasm as depicted in 2D and also the other time profiles as depicted in Fig 2.  Two parameters that are not present in the paper are introduced here for illustration purposes and they are Total Smad2n and Total Smad2c. The term kr_EE*LRC_EE has not been included in the ODE's for T1R_surf, T2R_surf and TGFbeta in the paper but is included in this model. MathSBML was used to reproduce the simulation result.</p>
        <br />
        <p>To the extent possible under law, all copyright and related or neighbouring rights to this encoded model have been dedicated to the public domain worldwide. Please refer to      <a href="http://creativecommons.org/publicdomain/zero/1.0/" title="Creative Commons CC0">CC0 Public Domain Dedication</a>
              for more information.      </p>
      <p>In summary, you are entitled to use this encoded model in absolutely any manner you deem suitable, verbatim, or with modification, alone or embedded it in a larger context, redistribute it, commercially or not, in a restricted way or not.</p>
      <br />
      <p>To cite BioModels Database, please use:      <a href="http://www.ncbi.nlm.nih.gov/pubmed/20587024" target="_blank">Li C, Donizelli M, Rodriguez N, Dharuri H, Endler L, Chelliah V, Li L, He E, Henry A, Stefan MI, Snoep JL, Hucka M, Le Novère N, Laibe C (2010) BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models. BMC Syst Biol., 4:92.</a>
    </p>
    </body>
        </Comment>
        <ListOfCompartments>
          <Compartment key="Compartment_1" name="Medium" simulationType="fixed" dimensionality="3">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Compartment_1">
        <CopasiMT:is>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005576" />
          </rdf:Bag>
        </CopasiMT:is>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Compartment>
          <Compartment key="Compartment_3" name="Nucleus" simulationType="fixed" dimensionality="3">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Compartment_3">
        <CopasiMT:is>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005634" />
          </rdf:Bag>
        </CopasiMT:is>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Compartment>
          <Compartment key="Compartment_5" name="Cytoplasm" simulationType="fixed" dimensionality="3">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Compartment_5">
        <CopasiMT:is>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005737" />
          </rdf:Bag>
        </CopasiMT:is>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Compartment>
        </ListOfCompartments>
        <ListOfMetabolites>
          <Metabolite key="Metabolite_1" name="Smad3c" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_1">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_3" name="Smad3n" simulationType="reactions" compartment="Compartment_3">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_3">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_5" name="Smad4c" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_5">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_7" name="Smad4n" simulationType="reactions" compartment="Compartment_3">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_7">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_9" name="T1R_Surf" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_9">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_11" name="T1R_Cave" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_11">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_13" name="T1R_EE" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_13">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_15" name="T2R_Surf" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_15">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_17" name="T2R_Cave" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_17">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_19" name="T2R_EE" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_19">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_21" name="LRC_Surf" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_21">
        <CopasiMT:hasPart>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
          </rdf:Bag>
        </CopasiMT:hasPart>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_23" name="LRC_Cave" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_23">
        <CopasiMT:hasPart>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
          </rdf:Bag>
        </CopasiMT:hasPart>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_25" name="LRC_EE" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_25">
        <CopasiMT:hasPart>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
          </rdf:Bag>
        </CopasiMT:hasPart>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_27" name="Smads_Complex_c" simulationType="reactions" compartment="Compartment_5">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_27">
        <CopasiMT:hasPart>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
          </rdf:Bag>
        </CopasiMT:hasPart>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_29" name="Smads_Complex_n" simulationType="reactions" compartment="Compartment_3">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_29">
        <CopasiMT:hasPart>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
            <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
          </rdf:Bag>
        </CopasiMT:hasPart>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
          <Metabolite key="Metabolite_31" name="TGF_beta" simulationType="reactions" compartment="Compartment_1">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Metabolite_31">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
          </Metabolite>
        </ListOfMetabolites>
        <ListOfModelValues>
          <ModelValue key="ModelValue_0" name="v_T1R" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_1" name="v_T2R" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_2" name="ki_EE" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_3" name="kr_EE" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_4" name="ki_Cave" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_5" name="kr_Cave" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_6" name="Kcd" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_7" name="k_LRC" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_8" name="Klid" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_9" name="Kdeg_T1R_EE" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_10" name="Kdeg_T2R_EE" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_11" name="Kimp_Smad2c" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_12" name="Kexp_Smad2n" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_13" name="Kimp_Smad4c" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_14" name="Kexp_Smad4n" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_15" name="k_Smads_Complex_c" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_16" name="Kimp_Smads_Complex_c" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_17" name="Kdiss_Smads_Complex_n" simulationType="fixed">
          </ModelValue>
          <ModelValue key="ModelValue_18" name="Total_Smad2n" simulationType="assignment">
            <Expression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration>
            </Expression>
          </ModelValue>
          <ModelValue key="ModelValue_19" name="Total_Smad2c" simulationType="assignment">
            <Expression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration>
            </Expression>
          </ModelValue>
        </ListOfModelValues>
        <ListOfReactions>
          <Reaction key="Reaction_0" name="R1_Smad2_import" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_0">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T10:41:56Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:is>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
          </rdf:Bag>
        </CopasiMT:is>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_3" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4385" name="Kimp_Smad2c" value="0.16"/>
            </ListOfConstants>
            <KineticLaw function="Function_40" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_254">
                  <SourceParameter reference="ModelValue_11"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_258">
                  <SourceParameter reference="Metabolite_1"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_264">
                  <SourceParameter reference="Compartment_5"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_1" name="R2_Smad2_export" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_1">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T14:06:48Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006886" />
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
              <Constant key="Parameter_4384" name="Kexp_Smad2n" value="1"/>
            </ListOfConstants>
            <KineticLaw function="Function_41" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_262">
                  <SourceParameter reference="ModelValue_12"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_267">
                  <SourceParameter reference="Metabolite_3"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_265">
                  <SourceParameter reference="Compartment_3"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_2" name="R3_Smad4_import" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_2">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T14:06:52Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:is>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
          </rdf:Bag>
        </CopasiMT:is>
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
              <Constant key="Parameter_4383" name="Kimp_Smad4c" value="0.08"/>
            </ListOfConstants>
            <KineticLaw function="Function_42" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_246">
                  <SourceParameter reference="ModelValue_13"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_270">
                  <SourceParameter reference="Metabolite_5"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_268">
                  <SourceParameter reference="Compartment_5"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_3" name="R4_Smad4_export" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_3">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T14:06:56Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006886" />
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
              <Constant key="Parameter_4382" name="Kexp_Smad4n" value="0.5"/>
            </ListOfConstants>
            <KineticLaw function="Function_43" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_266">
                  <SourceParameter reference="ModelValue_14"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_273">
                  <SourceParameter reference="Metabolite_7"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_271">
                  <SourceParameter reference="Compartment_3"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_4" name="R5_T1R_production" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_4">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T10:47:37Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032905" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfProducts>
              <Product metabolite="Metabolite_9" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4381" name="v" value="0.0103"/>
            </ListOfConstants>
            <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_49">
                  <SourceParameter reference="ModelValue_0"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_5" name="R6_T1R_Cave_formation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_5">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
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
              <Constant key="Parameter_4380" name="k1" value="0.33"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_4"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_9"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_6" name="R7_T1R_Cave_recycling" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_6">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-22T12:31:08Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
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
              <Constant key="Parameter_4379" name="k1" value="0.03742"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_5"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_11"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_7" name="R8_T1R_EE_formation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_7">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
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
              <Constant key="Parameter_4378" name="k1" value="0.33"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_2"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_9"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_8" name="R9_T1R_EE_recycling" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_8">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
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
              <Constant key="Parameter_4377" name="k1" value="0.033"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_3"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_13"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_9" name="R10_T1R_EE_degradation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_9">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T10:49:31Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_13" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfConstants>
              <Constant key="Parameter_4376" name="k1" value="0.005"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_9"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_13"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_10" name="R11_T2R_production" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_10">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T10:51:21Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032906" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfProducts>
              <Product metabolite="Metabolite_15" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4375" name="v" value="0.02869"/>
            </ListOfConstants>
            <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_49">
                  <SourceParameter reference="ModelValue_1"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_11" name="R12_T2R_Cave_formation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_11">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_15" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_17" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4374" name="k1" value="0.33"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_4"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_15"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_12" name="R13_T2R_Cave_recycling" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_12">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_17" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_15" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4373" name="k1" value="0.03742"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_5"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_17"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_13" name="R14_T2R_EE_formation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_13">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_15" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_19" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4372" name="k1" value="0.33"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_2"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_15"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_14" name="R15_T2R_EE_recycling" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_14">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_19" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_15" stoichiometry="1"/>
              <Product metabolite="Metabolite_31" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4371" name="kr_EE" value="0.033"/>
            </ListOfConstants>
            <KineticLaw function="Function_44" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_276">
                  <SourceParameter reference="Metabolite_19"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_274">
                  <SourceParameter reference="Compartment_5"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_269">
                  <SourceParameter reference="ModelValue_3"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_15" name="R16_T2R_EE_degradation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_15">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_19" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfConstants>
              <Constant key="Parameter_4370" name="k1" value="0.025"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_10"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_19"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_16" name="R17_LRC_formation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_16">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005160" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_31" stoichiometry="1"/>
              <Substrate metabolite="Metabolite_15" stoichiometry="1"/>
              <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_21" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4369" name="k_LRC" value="2197"/>
            </ListOfConstants>
            <KineticLaw function="Function_45" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_283">
                  <SourceParameter reference="Metabolite_9"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_281">
                  <SourceParameter reference="Metabolite_15"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_279">
                  <SourceParameter reference="Metabolite_31"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_277">
                  <SourceParameter reference="Compartment_5"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_272">
                  <SourceParameter reference="ModelValue_7"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_17" name="R18_LRC_Cave_formation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_17">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_23" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4368" name="k1" value="0.33"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_4"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_21"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_18" name="R19_LRC_Cave_recycling" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_18">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_23" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_9" stoichiometry="1"/>
              <Product metabolite="Metabolite_31" stoichiometry="1"/>
              <Product metabolite="Metabolite_15" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4367" name="kr_Cave" value="0.03742"/>
            </ListOfConstants>
            <KineticLaw function="Function_46" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_275">
                  <SourceParameter reference="Metabolite_23"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_284">
                  <SourceParameter reference="Compartment_5"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_280">
                  <SourceParameter reference="ModelValue_5"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_19" name="R20_LRC_EE_formation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_19">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_25" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4366" name="k1" value="0.33"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_2"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_21"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_20" name="R21_LRC_EE_recycling" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_20">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_25" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_9" stoichiometry="1"/>
              <Product metabolite="Metabolite_15" stoichiometry="1"/>
              <Product metabolite="Metabolite_31" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4365" name="kr_EE" value="0.033"/>
            </ListOfConstants>
            <KineticLaw function="Function_47" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_287">
                  <SourceParameter reference="Metabolite_25"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_285">
                  <SourceParameter reference="Compartment_5"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_282">
                  <SourceParameter reference="ModelValue_3"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_21" name="R22_LRC_EE_degradation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_21">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_25" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfConstants>
              <Constant key="Parameter_4364" name="k1" value="0.005"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_6"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_25"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_22" name="R23_Smads_Complex_formation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_22">
        <dcterms:created>
          <rdf:Description>
            <dcterms:W3CDTF>2017-08-17T14:06:11Z</dcterms:W3CDTF>
          </rdf:Description>
        </dcterms:created>
        <CopasiMT:is>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
          </rdf:Bag>
        </CopasiMT:is>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
              <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_27" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfModifiers>
              <Modifier metabolite="Metabolite_25" stoichiometry="1"/>
            </ListOfModifiers>
            <ListOfConstants>
              <Constant key="Parameter_4363" name="k_Smads_Complex_c" value="6.85e-05"/>
            </ListOfConstants>
            <KineticLaw function="Function_48" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_292">
                  <SourceParameter reference="Metabolite_25"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_278">
                  <SourceParameter reference="Metabolite_1"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_290">
                  <SourceParameter reference="Metabolite_5"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_288">
                  <SourceParameter reference="ModelValue_15"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_23" name="R24_Smads_Complex_import" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_23">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_27" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_29" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4362" name="Kimp_Smads_Complex_c" value="0.16"/>
            </ListOfConstants>
            <KineticLaw function="Function_49" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_289">
                  <SourceParameter reference="ModelValue_16"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_294">
                  <SourceParameter reference="Metabolite_27"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_293">
                  <SourceParameter reference="Compartment_5"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_24" name="R25_Smads_Complex_Dissociation" reversible="false" fast="false">
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_29" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfProducts>
              <Product metabolite="Metabolite_7" stoichiometry="1"/>
              <Product metabolite="Metabolite_3" stoichiometry="1"/>
            </ListOfProducts>
            <ListOfConstants>
              <Constant key="Parameter_4361" name="k1" value="0.1174"/>
            </ListOfConstants>
            <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_81">
                  <SourceParameter reference="ModelValue_17"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_79">
                  <SourceParameter reference="Metabolite_29"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
          <Reaction key="Reaction_25" name="R26_LRC_Cave_degradation" reversible="false" fast="false">
            <MiriamAnnotation>
    <rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about="#Reaction_25">
        <CopasiMT:isVersionOf>
          <rdf:Bag>
            <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0030163" />
          </rdf:Bag>
        </CopasiMT:isVersionOf>
      </rdf:Description>
    </rdf:RDF>
            </MiriamAnnotation>
            <ListOfSubstrates>
              <Substrate metabolite="Metabolite_23" stoichiometry="1"/>
            </ListOfSubstrates>
            <ListOfModifiers>
              <Modifier metabolite="Metabolite_29" stoichiometry="1"/>
            </ListOfModifiers>
            <ListOfConstants>
              <Constant key="Parameter_4360" name="Klid" value="0.02609"/>
            </ListOfConstants>
            <KineticLaw function="Function_50" unitType="Default">
              <ListOfCallParameters>
                <CallParameter functionParameter="FunctionParameter_295">
                  <SourceParameter reference="ModelValue_8"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_291">
                  <SourceParameter reference="Metabolite_23"/>
                </CallParameter>
                <CallParameter functionParameter="FunctionParameter_297">
                  <SourceParameter reference="Metabolite_29"/>
                </CallParameter>
              </ListOfCallParameters>
            </KineticLaw>
          </Reaction>
        </ListOfReactions>
        <ListOfModelParameterSets activeSet="ModelParameterSet_1">
          <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
            <ModelParameterGroup cn="String=Initial Time" type="Group">
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling" value="0" type="Model" simulationType="time"/>
            </ModelParameterGroup>
            <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium]" value="1" type="Compartment" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]" value="0.00035" type="Compartment" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]" value="0.00105" type="Compartment" simulationType="fixed"/>
            </ModelParameterGroup>
            <ModelParameterGroup cn="String=Initial Species Values" type="Group">
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c]" value="311489514794510.7" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n]" value="49837732197317.75" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c]" value="726794113608758.9" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n]" value="116288744376841.4" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf]" value="149860975226.4449" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave]" value="1322823460648.618" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE]" value="1302589067369.099" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf]" value="127729607576.9699" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave]" value="1124273476593.329" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE]" value="725908858902.7791" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf]" value="0" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave]" value="0" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE]" value="0" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c]" value="0" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n]" value="0" type="Species" simulationType="reactions"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta]" value="48177126855999.97" type="Species" simulationType="reactions"/>
            </ModelParameterGroup>
            <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R]" value="0.0103" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R]" value="0.02869" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE]" value="0.33" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE]" value="0.033" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave]" value="0.33" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave]" value="0.03742" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd]" value="0.005" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC]" value="2197" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid]" value="0.02609" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE]" value="0.005" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE]" value="0.025" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c]" value="0.16" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n]" value="1" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c]" value="0.08" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n]" value="0.5" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c]" value="6.85e-05" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c]" value="0.16" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n]" value="0.1174" type="ModelValue" simulationType="fixed"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n]" value="236.45" type="ModelValue" simulationType="assignment"/>
              <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c]" value="492.6099999999997" type="ModelValue" simulationType="assignment"/>
            </ModelParameterGroup>
            <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R1_Smad2_import]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R1_Smad2_import],ParameterGroup=Parameters,Parameter=Kimp_Smad2c" value="0.16" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R2_Smad2_export]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R2_Smad2_export],ParameterGroup=Parameters,Parameter=Kexp_Smad2n" value="1" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R3_Smad4_import]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R3_Smad4_import],ParameterGroup=Parameters,Parameter=Kimp_Smad4c" value="0.08" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R4_Smad4_export]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R4_Smad4_export],ParameterGroup=Parameters,Parameter=Kexp_Smad4n" value="0.5" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R5_T1R_production]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R5_T1R_production],ParameterGroup=Parameters,Parameter=v" value="0.0103" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R6_T1R_Cave_formation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R6_T1R_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R7_T1R_Cave_recycling]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R7_T1R_Cave_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.03742" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R8_T1R_EE_formation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R8_T1R_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R9_T1R_EE_recycling]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R9_T1R_EE_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.033" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R10_T1R_EE_degradation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R10_T1R_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.005" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R11_T2R_production]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R11_T2R_production],ParameterGroup=Parameters,Parameter=v" value="0.02869" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R12_T2R_Cave_formation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R12_T2R_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R13_T2R_Cave_recycling]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R13_T2R_Cave_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.03742" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R14_T2R_EE_formation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R14_T2R_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R15_T2R_EE_recycling]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R15_T2R_EE_recycling],ParameterGroup=Parameters,Parameter=kr_EE" value="0.033" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R16_T2R_EE_degradation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R16_T2R_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.025" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R17_LRC_formation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R17_LRC_formation],ParameterGroup=Parameters,Parameter=k_LRC" value="2197" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R18_LRC_Cave_formation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R18_LRC_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R19_LRC_Cave_recycling]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R19_LRC_Cave_recycling],ParameterGroup=Parameters,Parameter=kr_Cave" value="0.03742" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R20_LRC_EE_formation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R20_LRC_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R21_LRC_EE_recycling]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R21_LRC_EE_recycling],ParameterGroup=Parameters,Parameter=kr_EE" value="0.033" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R22_LRC_EE_degradation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R22_LRC_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.005" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R23_Smads_Complex_formation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R23_Smads_Complex_formation],ParameterGroup=Parameters,Parameter=k_Smads_Complex_c" value="6.85e-05" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R24_Smads_Complex_import]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R24_Smads_Complex_import],ParameterGroup=Parameters,Parameter=Kimp_Smads_Complex_c" value="0.16" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R25_Smads_Complex_Dissociation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R25_Smads_Complex_Dissociation],ParameterGroup=Parameters,Parameter=k1" value="0.1174" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
              <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R26_LRC_Cave_degradation]" type="Reaction">
                <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R26_LRC_Cave_degradation],ParameterGroup=Parameters,Parameter=Klid" value="0.02609" type="ReactionParameter" simulationType="assignment">
                  <InitialExpression>
                    &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid],Reference=InitialValue>
                  </InitialExpression>
                </ModelParameter>
              </ModelParameterGroup>
            </ModelParameterGroup>
          </ModelParameterSet>
        </ListOfModelParameterSets>
        <StateTemplate>
          <StateTemplateVariable objectReference="Model_3"/>
          <StateTemplateVariable objectReference="Metabolite_9"/>
          <StateTemplateVariable objectReference="Metabolite_15"/>
          <StateTemplateVariable objectReference="Metabolite_7"/>
          <StateTemplateVariable objectReference="Metabolite_1"/>
          <StateTemplateVariable objectReference="Metabolite_21"/>
          <StateTemplateVariable objectReference="Metabolite_13"/>
          <StateTemplateVariable objectReference="Metabolite_19"/>
          <StateTemplateVariable objectReference="Metabolite_23"/>
          <StateTemplateVariable objectReference="Metabolite_25"/>
          <StateTemplateVariable objectReference="Metabolite_29"/>
          <StateTemplateVariable objectReference="Metabolite_31"/>
          <StateTemplateVariable objectReference="Metabolite_27"/>
          <StateTemplateVariable objectReference="Metabolite_11"/>
          <StateTemplateVariable objectReference="Metabolite_17"/>
          <StateTemplateVariable objectReference="Metabolite_3"/>
          <StateTemplateVariable objectReference="Metabolite_5"/>
          <StateTemplateVariable objectReference="ModelValue_18"/>
          <StateTemplateVariable objectReference="ModelValue_19"/>
          <StateTemplateVariable objectReference="Compartment_1"/>
          <StateTemplateVariable objectReference="Compartment_3"/>
          <StateTemplateVariable objectReference="Compartment_5"/>
          <StateTemplateVariable objectReference="ModelValue_0"/>
          <StateTemplateVariable objectReference="ModelValue_1"/>
          <StateTemplateVariable objectReference="ModelValue_2"/>
          <StateTemplateVariable objectReference="ModelValue_3"/>
          <StateTemplateVariable objectReference="ModelValue_4"/>
          <StateTemplateVariable objectReference="ModelValue_5"/>
          <StateTemplateVariable objectReference="ModelValue_6"/>
          <StateTemplateVariable objectReference="ModelValue_7"/>
          <StateTemplateVariable objectReference="ModelValue_8"/>
          <StateTemplateVariable objectReference="ModelValue_9"/>
          <StateTemplateVariable objectReference="ModelValue_10"/>
          <StateTemplateVariable objectReference="ModelValue_11"/>
          <StateTemplateVariable objectReference="ModelValue_12"/>
          <StateTemplateVariable objectReference="ModelValue_13"/>
          <StateTemplateVariable objectReference="ModelValue_14"/>
          <StateTemplateVariable objectReference="ModelValue_15"/>
          <StateTemplateVariable objectReference="ModelValue_16"/>
          <StateTemplateVariable objectReference="ModelValue_17"/>
        </StateTemplate>
        <InitialState type="initialState">
          0 149860975226.4449 127729607576.9699 116288744376841.4 311489514794510.7 0 1302589067369.099 725908858902.7791 0 0 0 48177126855999.97 0 1322823460648.618 1124273476593.329 49837732197317.75 726794113608758.9 236.45 492.6099999999997 1 0.00035 0.00105 0.0103 0.02869 0.33 0.033 0.33 0.03742 0.005 2197 0.02609 0.005 0.025 0.16 1 0.08 0.5 6.85e-05 0.16 0.1174 
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
          <Report reference="Report_18" target="../../Models/2017/09_Sept/zi_timecourse_simulation.csv" append="0" confirmOverwrite="0"/>
          <Problem>
            <Parameter name="AutomaticStepSize" type="bool" value="0"/>
            <Parameter name="StepNumber" type="unsignedInteger" value="1000"/>
            <Parameter name="StepSize" type="float" value="1"/>
            <Parameter name="Duration" type="float" value="1000"/>
            <Parameter name="TimeSeriesRequested" type="float" value="1"/>
            <Parameter name="OutputStartTime" type="float" value="0"/>
            <Parameter name="Output Event" type="bool" value="0"/>
            <Parameter name="Start in Steady State" type="bool" value="0"/>
          </Problem>
          <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
            <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
            <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
            <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
            <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
            <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
          </Method>
        </Task>
        <Task key="Task_16" name="Scan" type="scan" scheduled="true" updateModel="false">
          <Report reference="Report_19" target="zi_repeat.csv" append="0" confirmOverwrite="0"/>
          <Problem>
            <Parameter name="Subtask" type="unsignedInteger" value="1"/>
            <ParameterGroup name="ScanItems">
              <ParameterGroup name="ScanItem">
                <Parameter name="Number of steps" type="unsignedInteger" value="10"/>
                <Parameter name="Object" type="cn" value="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=InitialConcentration"/>
                <Parameter name="Type" type="unsignedInteger" value="0"/>
              </ParameterGroup>
            </ParameterGroup>
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
          <Report reference="Report_12" target="" append="1" confirmOverwrite="1"/>
          <Problem>
            <Parameter name="Maximize" type="bool" value="0"/>
            <Parameter name="Randomize Start Values" type="bool" value="0"/>
            <Parameter name="Calculate Statistics" type="bool" value="1"/>
            <ParameterGroup name="OptimizationItemList">
            </ParameterGroup>
            <ParameterGroup name="OptimizationConstraintList">
            </ParameterGroup>
            <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
            <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
            <Parameter name="Create Parameter Sets" type="bool" value="0"/>
            <ParameterGroup name="Experiment Set">
            </ParameterGroup>
            <ParameterGroup name="Validation Set">
              <Parameter name="Threshold" type="unsignedInteger" value="5"/>
              <Parameter name="Weight" type="unsignedFloat" value="1"/>
            </ParameterGroup>
          </Problem>
          <Method name="Evolutionary Programming" type="EvolutionaryProgram">
            <Parameter name="Number of Generations" type="unsignedInteger" value="200"/>
            <Parameter name="Population Size" type="unsignedInteger" value="20"/>
            <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
            <Parameter name="Seed" type="unsignedInteger" value="0"/>
          </Method>
        </Task>
        <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
          <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
          <Problem>
            <Parameter name="Steady-State" type="key" value="Task_14"/>
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
        <Report key="Report_9" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Footer>
            <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
          </Footer>
        </Report>
        <Report key="Report_10" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Footer>
            <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
          </Footer>
        </Report>
        <Report key="Report_11" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Header>
            <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
            <Object cn="String=\[Function Evaluations\]"/>
            <Object cn="Separator=&#x09;"/>
            <Object cn="String=\[Best Value\]"/>
            <Object cn="Separator=&#x09;"/>
            <Object cn="String=\[Best Parameters\]"/>
          </Header>
          <Body>
            <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
            <Object cn="Separator=&#x09;"/>
            <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
            <Object cn="Separator=&#x09;"/>
            <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
          </Body>
          <Footer>
            <Object cn="String=&#x0a;"/>
            <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
          </Footer>
        </Report>
        <Report key="Report_12" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Header>
            <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
            <Object cn="String=\[Function Evaluations\]"/>
            <Object cn="Separator=&#x09;"/>
            <Object cn="String=\[Best Value\]"/>
            <Object cn="Separator=&#x09;"/>
            <Object cn="String=\[Best Parameters\]"/>
          </Header>
          <Body>
            <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
            <Object cn="Separator=&#x09;"/>
            <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
            <Object cn="Separator=&#x09;"/>
            <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
          </Body>
          <Footer>
            <Object cn="String=&#x0a;"/>
            <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
          </Footer>
        </Report>
        <Report key="Report_13" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Header>
            <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
          </Header>
          <Footer>
            <Object cn="String=&#x0a;"/>
            <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
          </Footer>
        </Report>
        <Report key="Report_14" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Header>
            <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
          </Header>
          <Footer>
            <Object cn="String=&#x0a;"/>
            <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
          </Footer>
        </Report>
        <Report key="Report_15" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Header>
            <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
          </Header>
          <Footer>
            <Object cn="String=&#x0a;"/>
            <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
          </Footer>
        </Report>
        <Report key="Report_16" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Header>
            <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
          </Header>
          <Footer>
            <Object cn="String=&#x0a;"/>
            <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
          </Footer>
        </Report>
        <Report key="Report_17" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
          <Comment>
            Automatically generated report.
          </Comment>
          <Header>
            <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Description"/>
          </Header>
          <Footer>
            <Object cn="String=&#x0a;"/>
            <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Result"/>
          </Footer>
        </Report>
        <Report key="Report_18" name="Time-Course" taskType="unset" separator="&#x09;" precision="6">
          <Comment>
          </Comment>
          <Table printTitle="1">
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE],Reference=Concentration"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE],Reference=Value"/>
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c],Reference=Value"/>
          </Table>
        </Report>
        <Report key="Report_19" name="profilelikelihood" taskType="unset" separator="&#x09;" precision="6">
          <Comment>
          </Comment>
          <Table printTitle="1">
            <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Metabolites[Smad3n],Reference=InitialConcentration"/>
            <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
          </Table>
        </Report>
      </ListOfReports>
      <ListOfPlots>
        <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
          <Parameter name="log X" type="bool" value="0"/>
          <Parameter name="log Y" type="bool" value="0"/>
          <ListOfPlotItems>
            <PlotItem name="[Smad3c]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[Smad3n]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[Smad4c]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[Smad4n]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[T1R_Surf]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[T1R_Cave]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[T1R_EE]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[T2R_Surf]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[T2R_Cave]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[T2R_EE]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[LRC_Surf]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[LRC_Cave]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[LRC_EE]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[Smads_Complex_c]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[Smads_Complex_n]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[TGF_beta]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="[Smad7]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[Smad7],Reference=Concentration"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="Values[Total_Smad2n]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n],Reference=Value"/>
              </ListOfChannels>
            </PlotItem>
            <PlotItem name="Values[Total_Smad2c]" type="Curve2D">
              <Parameter name="Color" type="string" value="auto"/>
              <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
              <Parameter name="Line type" type="unsignedInteger" value="0"/>
              <Parameter name="Line width" type="unsignedFloat" value="1"/>
              <Parameter name="Recording Activity" type="string" value="during"/>
              <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
              <ListOfChannels>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
                <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c],Reference=Value"/>
              </ListOfChannels>
            </PlotItem>
          </ListOfPlotItems>
        </PlotSpecification>
      </ListOfPlots>
      <GUI>
      </GUI>
      <SBMLReference file="Zi2012.xml">
        <SBMLMap SBMLid="Kcd" COPASIkey="ModelValue_6"/>
        <SBMLMap SBMLid="Kdeg_T1R_EE" COPASIkey="ModelValue_9"/>
        <SBMLMap SBMLid="Kdeg_T2R_EE" COPASIkey="ModelValue_10"/>
        <SBMLMap SBMLid="Kdiss_Smads_Complex_n" COPASIkey="ModelValue_17"/>
        <SBMLMap SBMLid="Kexp_Smad2n" COPASIkey="ModelValue_12"/>
        <SBMLMap SBMLid="Kexp_Smad4n" COPASIkey="ModelValue_14"/>
        <SBMLMap SBMLid="Kimp_Smad2c" COPASIkey="ModelValue_11"/>
        <SBMLMap SBMLid="Kimp_Smad4c" COPASIkey="ModelValue_13"/>
        <SBMLMap SBMLid="Kimp_Smads_Complex_c" COPASIkey="ModelValue_16"/>
        <SBMLMap SBMLid="Klid" COPASIkey="ModelValue_8"/>
        <SBMLMap SBMLid="LRC_Cave" COPASIkey="Metabolite_23"/>
        <SBMLMap SBMLid="LRC_EE" COPASIkey="Metabolite_25"/>
        <SBMLMap SBMLid="LRC_Surf" COPASIkey="Metabolite_21"/>
        <SBMLMap SBMLid="R10_T1R_EE_degradation" COPASIkey="Reaction_9"/>
        <SBMLMap SBMLid="R11_T2R_production" COPASIkey="Reaction_10"/>
        <SBMLMap SBMLid="R12_T2R_Cave_formation" COPASIkey="Reaction_11"/>
        <SBMLMap SBMLid="R13_T2R_Cave_recycling" COPASIkey="Reaction_12"/>
        <SBMLMap SBMLid="R14_T2R_EE_formation" COPASIkey="Reaction_13"/>
        <SBMLMap SBMLid="R15_T2R_EE_recycling" COPASIkey="Reaction_14"/>
        <SBMLMap SBMLid="R16_T2R_EE_degradation" COPASIkey="Reaction_15"/>
        <SBMLMap SBMLid="R17_LRC_formation" COPASIkey="Reaction_16"/>
        <SBMLMap SBMLid="R18_LRC_Cave_formation" COPASIkey="Reaction_17"/>
        <SBMLMap SBMLid="R19_LRC_Cave_recycling" COPASIkey="Reaction_18"/>
        <SBMLMap SBMLid="R1_Smad2_import" COPASIkey="Reaction_0"/>
        <SBMLMap SBMLid="R20_LRC_EE_formation" COPASIkey="Reaction_19"/>
        <SBMLMap SBMLid="R21_LRC_EE_recycling" COPASIkey="Reaction_20"/>
        <SBMLMap SBMLid="R22_LRC_EE_degradation" COPASIkey="Reaction_21"/>
        <SBMLMap SBMLid="R23_Smads_Complex_formation" COPASIkey="Reaction_22"/>
        <SBMLMap SBMLid="R24_Smads_Complex_import" COPASIkey="Reaction_23"/>
        <SBMLMap SBMLid="R25_Smads_Complex_Dissociation" COPASIkey="Reaction_24"/>
        <SBMLMap SBMLid="R26_LRC_Cave_degradation" COPASIkey="Reaction_25"/>
        <SBMLMap SBMLid="R2_Smad2_export" COPASIkey="Reaction_1"/>
        <SBMLMap SBMLid="R3_Smad4_import" COPASIkey="Reaction_2"/>
        <SBMLMap SBMLid="R4_Smad4_export" COPASIkey="Reaction_3"/>
        <SBMLMap SBMLid="R5_T1R_production" COPASIkey="Reaction_4"/>
        <SBMLMap SBMLid="R6_T1R_Cave_formation" COPASIkey="Reaction_5"/>
        <SBMLMap SBMLid="R7_T1R_Cave_recycling" COPASIkey="Reaction_6"/>
        <SBMLMap SBMLid="R8_T1R_EE_formation" COPASIkey="Reaction_7"/>
        <SBMLMap SBMLid="R9_T1R_EE_recycling" COPASIkey="Reaction_8"/>
        <SBMLMap SBMLid="Smad2c" COPASIkey="Metabolite_1"/>
        <SBMLMap SBMLid="Smad2n" COPASIkey="Metabolite_3"/>
        <SBMLMap SBMLid="Smad4c" COPASIkey="Metabolite_5"/>
        <SBMLMap SBMLid="Smad4n" COPASIkey="Metabolite_7"/>
        <SBMLMap SBMLid="Smads_Complex_c" COPASIkey="Metabolite_27"/>
        <SBMLMap SBMLid="Smads_Complex_n" COPASIkey="Metabolite_29"/>
        <SBMLMap SBMLid="T1R_Cave" COPASIkey="Metabolite_11"/>
        <SBMLMap SBMLid="T1R_EE" COPASIkey="Metabolite_13"/>
        <SBMLMap SBMLid="T1R_Surf" COPASIkey="Metabolite_9"/>
        <SBMLMap SBMLid="T2R_Cave" COPASIkey="Metabolite_17"/>
        <SBMLMap SBMLid="T2R_EE" COPASIkey="Metabolite_19"/>
        <SBMLMap SBMLid="T2R_Surf" COPASIkey="Metabolite_15"/>
        <SBMLMap SBMLid="TGF_beta" COPASIkey="Metabolite_31"/>
        <SBMLMap SBMLid="Total_Smad2c" COPASIkey="ModelValue_19"/>
        <SBMLMap SBMLid="Total_Smad2n" COPASIkey="ModelValue_18"/>
        <SBMLMap SBMLid="V_cyt" COPASIkey="Compartment_5"/>
        <SBMLMap SBMLid="V_medium" COPASIkey="Compartment_1"/>
        <SBMLMap SBMLid="V_nuc" COPASIkey="Compartment_3"/>
        <SBMLMap SBMLid="k_LRC" COPASIkey="ModelValue_7"/>
        <SBMLMap SBMLid="k_Smads_Complex_c" COPASIkey="ModelValue_15"/>
        <SBMLMap SBMLid="ki_Cave" COPASIkey="ModelValue_4"/>
        <SBMLMap SBMLid="ki_EE" COPASIkey="ModelValue_2"/>
        <SBMLMap SBMLid="kr_Cave" COPASIkey="ModelValue_5"/>
        <SBMLMap SBMLid="kr_EE" COPASIkey="ModelValue_3"/>
        <SBMLMap SBMLid="v_T1R" COPASIkey="ModelValue_0"/>
        <SBMLMap SBMLid="v_T2R" COPASIkey="ModelValue_1"/>
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
    </COPASI>"""

    @property
    def smad7_reproduced(self):
        """

        :return:
        """
        return """<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-10-11 14:56:22 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="19" versionDevel="140" copasiSourcesModified="0">
  <ListOfFunctions>
    <Function key="Function_6" name="Constant flux (irreversible)" type="PreDefined" reversible="false">
      <Expression>
        v
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_49" name="v" order="0" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_13" name="Mass action (irreversible)" type="MassAction" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <rdf:Description rdf:about="#Function_13">
   <CopasiMT:is rdf:resource="urn:miriam:obo.sbo:SBO:0000041" />
   </rdf:Description>
   </rdf:RDF>
      </MiriamAnnotation>
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
<b>Mass action rate law for first order irreversible reactions</b>
<p>
Reaction scheme where the products are created from the reactants and the change of a product quantity is proportional to the product of reactant activities. The reaction scheme does not include any reverse process that creates the reactants from the products. The change of a product quantity is proportional to the quantity of one reactant.
</p>
</body>
      </Comment>
      <Expression>
        k1*PRODUCT&lt;substrate_i>
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_81" name="k1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_79" name="substrate" order="1" role="substrate"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_40" name="Function for R1_Smad2_import" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_40">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:07:29Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
      </MiriamAnnotation>
      <Expression>
        V_cyt*Kimp_Smad2c*Smad2c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_254" name="Kimp_Smad2c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_258" name="Smad2c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_264" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_41" name="Function for R2_Smad2_export" type="UserDefined" reversible="false">
      <Expression>
        V_nuc*Kexp_Smad2n*Smad2n
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_262" name="Kexp_Smad2n" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_267" name="Smad2n" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_265" name="V_nuc" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_42" name="Function for R3_Smad4_import" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*Kimp_Smad4c*Smad4c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_246" name="Kimp_Smad4c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_270" name="Smad4c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_268" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_43" name="Function for R4_Smad4_export" type="UserDefined" reversible="false">
      <Expression>
        V_nuc*Kexp_Smad4n*Smad4n
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_266" name="Kexp_Smad4n" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_273" name="Smad4n" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_271" name="V_nuc" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="Function for R15_T2R_EE_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_EE*T2R_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_276" name="T2R_EE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_274" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_269" name="kr_EE" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="Function for R17_LRC_formation" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_45">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:42:20Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        V_cyt*k_LRC*TGF_beta*T2R_Surf*T1R_Surf
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_283" name="T1R_Surf" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_281" name="T2R_Surf" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_279" name="TGF_beta" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_277" name="V_cyt" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_272" name="k_LRC" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_46" name="Function for R19_LRC_Cave_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_Cave*LRC_Cave
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_275" name="LRC_Cave" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_284" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_280" name="kr_Cave" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="Function for R21_LRC_EE_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_EE*LRC_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_287" name="LRC_EE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_285" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_282" name="kr_EE" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="Function for R23_Smads_Complex_formation" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_48">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-22T12:24:54Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
      </MiriamAnnotation>
      <Expression>
        k_Smads_Complex_c*Smad2c*Smad4c*LRC_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_292" name="LRC_EE" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_278" name="Smad2c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_290" name="Smad4c" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_288" name="k_Smads_Complex_c" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="Function for R24_Smads_Complex_import" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*Kimp_Smads_Complex_c*Smads_Complex_c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_289" name="Kimp_Smads_Complex_c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_294" name="Smads_Complex_c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_293" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_50" name="k*A/I" type="UserDefined" reversible="unspecified">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_50">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:42:22Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        k*(A/I)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_373" name="k" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_383" name="A" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_386" name="I" order="2" role="modifier"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_7" name="Zi2007_TGFbeta_signaling" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="nmol" type="deterministic" avogadroConstant="6.022140857e+23">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_7">
    <bqbiol:hasTaxon>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/taxonomy/131567"/>
      </rdf:Bag>
    </bqbiol:hasTaxon>
    <dcterms:bibliographicCitation>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <CopasiMT:isDescribedBy rdf:resource="http://identifiers.org/pubmed/17895977"/>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:bibliographicCitation>
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2008-02-14T09:21:13Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <dcterms:creator>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>klipp@molgen.mpg.de</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Klipp</vCard:Family>
                <vCard:Given>Edda</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Max Planck Institute for molecular genetics</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>hdharuri@cds.caltech.edu</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Dharuri</vCard:Family>
                <vCard:Given>Harish</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>California Institute of Technology</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Yang</vCard:Family>
                <vCard:Given>Kun</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Beijing National Laboratory for Molecular Sciences</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:creator>
    <dcterms:modified>
      <rdf:Description>
        <dcterms:W3CDTF>2012-07-05T16:45:46Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:modified>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/MODEL3388742457"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/BIOMD0000000163"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isPartOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/kegg.pathway/hsa04350"/>
      </rdf:Bag>
    </CopasiMT:isPartOf>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      <body xmlns="http://www.w3.org/1999/xhtml">
    <p>The model reproduces the time profiles of Total Smad2 in the nucleus as well as the cytoplasm as depicted in 2D and also the other time profiles as depicted in Fig 2.  Two parameters that are not present in the paper are introduced here for illustration purposes and they are Total Smad2n and Total Smad2c. The term kr_EE*LRC_EE has not been included in the ODE's for T1R_surf, T2R_surf and TGFbeta in the paper but is included in this model. MathSBML was used to reproduce the simulation result.</p>
    <br />
    <p>To the extent possible under law, all copyright and related or neighbouring rights to this encoded model have been dedicated to the public domain worldwide. Please refer to      <a href="http://creativecommons.org/publicdomain/zero/1.0/" title="Creative Commons CC0">CC0 Public Domain Dedication</a>
          for more information.      </p>
  <p>In summary, you are entitled to use this encoded model in absolutely any manner you deem suitable, verbatim, or with modification, alone or embedded it in a larger context, redistribute it, commercially or not, in a restricted way or not.</p>
  <br />
  <p>To cite BioModels Database, please use:      <a href="http://www.ncbi.nlm.nih.gov/pubmed/20587024" target="_blank">Li C, Donizelli M, Rodriguez N, Dharuri H, Endler L, Chelliah V, Li L, He E, Henry A, Stefan MI, Snoep JL, Hucka M, Le Novère N, Laibe C (2010) BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models. BMC Syst Biol., 4:92.</a>
</p>
</body>
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_9" name="Medium" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_9">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005576" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_15" name="Nucleus" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_15">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_17" name="Cytoplasm" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_17">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005737" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_77" name="Smad3c" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_77">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_73" name="Smad3n" simulationType="reactions" compartment="Compartment_15">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_73">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_65" name="Smad4c" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_65">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_61" name="Smad4n" simulationType="reactions" compartment="Compartment_15">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_61">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_57" name="T1R_Surf" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_57">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_53" name="T1R_Cave" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_53">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_49" name="T1R_EE" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_49">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_41" name="T2R_Surf" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_41">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_47" name="T2R_Cave" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_47">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_71" name="T2R_EE" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_71">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_101" name="LRC_Surf" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_101">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_103" name="LRC_Cave" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_103">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_105" name="LRC_EE" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_105">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_107" name="Smads_Complex_c" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_107">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_109" name="Smads_Complex_n" simulationType="reactions" compartment="Compartment_15">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_109">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_111" name="TGF_beta" simulationType="reactions" compartment="Compartment_9">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_111">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_113" name="Smad7" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_113">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:03:36Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_115" name="Ski" simulationType="reactions" compartment="Compartment_17">
      </Metabolite>
      <Metabolite key="Metabolite_117" name="Smad7_mRNA" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_117">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:06:01Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_119" name="Ski_mRNA" simulationType="reactions" compartment="Compartment_17">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_119">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:06:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_55" name="v_T1R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_54" name="v_T2R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_53" name="ki_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_52" name="kr_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_51" name="ki_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_50" name="kr_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_49" name="Kcd" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_48" name="k_LRC" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_47" name="Klid" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_46" name="Kdeg_T1R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_45" name="Kdeg_T2R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_44" name="Kimp_Smad2c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_43" name="Kexp_Smad2n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_42" name="Kimp_Smad4c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_41" name="Kexp_Smad4n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_40" name="k_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_39" name="Kimp_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_38" name="Kdiss_Smads_Complex_n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_37" name="Total_Smad2n" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_36" name="Total_Smad2c" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_35" name="SkiObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_35">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:11:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski_mRNA],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_34" name="Smad7Obs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_34">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:13Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_33" name="SkiSF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_33">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_32" name="Smad7SF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_32">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:45Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_31" name="Smad7mRNAObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_31">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:12:28Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7_mRNA],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_30" name="Smad7mRNAInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_29" name="SkiInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_28" name="Smad7ProteinInitial" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_67" name="R1_Smad2_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_67">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:41:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_77" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_73" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4021" name="Kimp_Smad2c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_40" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="ModelValue_44"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_77"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Compartment_17"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_66" name="R2_Smad2_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_66">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006886" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_73" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_77" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3960" name="Kexp_Smad2n" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_41" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="ModelValue_43"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_73"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Compartment_15"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_65" name="R3_Smad4_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_65">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:52Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_65" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3845" name="Kimp_Smad4c" value="0.08"/>
        </ListOfConstants>
        <KineticLaw function="Function_42" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="ModelValue_42"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Metabolite_65"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Compartment_17"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_64" name="R4_Smad4_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_64">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006886" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_65" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3846" name="Kexp_Smad4n" value="0.5"/>
        </ListOfConstants>
        <KineticLaw function="Function_43" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="ModelValue_41"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_61"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Compartment_15"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_63" name="R5_T1R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_63">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:47:37Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032905" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3847" name="v" value="0.0103"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_55"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_62" name="R6_T1R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_62">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_53" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3848" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_57"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_61" name="R7_T1R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_61">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-22T12:31:08Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_53" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3849" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_50"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_53"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_60" name="R8_T1R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_60">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3850" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_57"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_59" name="R9_T1R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_59">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3851" name="k1" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_52"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_49"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_58" name="R10_T1R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_58">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:49:31Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_3852" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_46"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_49"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_57" name="R11_T2R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_57">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:51:21Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032906" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_41" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3853" name="v" value="0.02869"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_54"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_56" name="R12_T2R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_56">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_41" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3854" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_41"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_55" name="R13_T2R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_55">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_41" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3855" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_50"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_54" name="R14_T2R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_54">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_41" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_71" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3856" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_41"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_53" name="R15_T2R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_53">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_71" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_41" stoichiometry="1"/>
          <Product metabolite="Metabolite_111" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3857" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_44" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Metabolite_71"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Compartment_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="ModelValue_52"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_52" name="R16_T2R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_52">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_71" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_3858" name="k1" value="0.025"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_71"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_51" name="R17_LRC_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_51">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005160" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_111" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_41" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_101" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3859" name="k_LRC" value="2197"/>
        </ListOfConstants>
        <KineticLaw function="Function_45" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Metabolite_57"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_41"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_111"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Compartment_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="ModelValue_48"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_50" name="R18_LRC_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_50">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_101" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_103" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3860" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_101"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_49" name="R19_LRC_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_49">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_103" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_57" stoichiometry="1"/>
          <Product metabolite="Metabolite_111" stoichiometry="1"/>
          <Product metabolite="Metabolite_41" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3861" name="kr_Cave" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_46" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Metabolite_103"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Compartment_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="ModelValue_50"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_48" name="R20_LRC_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_48">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_101" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_105" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3862" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_101"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_47" name="R21_LRC_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_47">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_105" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_57" stoichiometry="1"/>
          <Product metabolite="Metabolite_41" stoichiometry="1"/>
          <Product metabolite="Metabolite_111" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3863" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_47" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Metabolite_105"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Compartment_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="ModelValue_52"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_46" name="R22_LRC_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_46">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_105" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_3864" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_49"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_105"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_45" name="R23_Smads_Complex_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_45">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:11Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_77" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_65" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_107" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_105" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_3865" name="k_Smads_Complex_c" value="6.85e-05"/>
        </ListOfConstants>
        <KineticLaw function="Function_48" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Metabolite_105"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Metabolite_77"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Metabolite_65"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="ModelValue_40"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_44" name="R24_Smads_Complex_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_44">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_107" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_109" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3866" name="Kimp_Smads_Complex_c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_49" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="ModelValue_39"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Metabolite_107"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Compartment_17"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_43" name="R25_Smads_Complex_Dissociation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_109" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_61" stoichiometry="1"/>
          <Product metabolite="Metabolite_73" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3867" name="k1" value="0.1174"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_38"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_109"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_42" name="Smad7Transcription" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_42">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:56:04Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_109" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_109" stoichiometry="1"/>
          <Product metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_115" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4431" name="k" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_50" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_373">
              <SourceParameter reference="Parameter_4431"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_383">
              <SourceParameter reference="Metabolite_109"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_386">
              <SourceParameter reference="Metabolite_115"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_41" name="SkiTranscription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_109" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_109" stoichiometry="1"/>
          <Product metabolite="Metabolite_119" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3869" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_3869"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_109"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_40" name="Smad7mRNADeg" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_40">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:56:08Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_3870" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_3870"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_117"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_39" name="SkimRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_119" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_3871" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_3871"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_119"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_38" name="Smad7Translation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_117" stoichiometry="1"/>
          <Product metabolite="Metabolite_113" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3872" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_3872"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_117"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_37" name="SkiTranslation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_119" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_119" stoichiometry="1"/>
          <Product metabolite="Metabolite_115" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3873" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_3873"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_119"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_36" name="SkiDeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_115" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_3874" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_3874"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_115"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_35" name="Smad7Feedback" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_113" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_103" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_113" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3875" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_3875"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_113"/>
              <SourceParameter reference="Metabolite_103"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_34" name="Smad7Deg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_113" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_3876" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_3876"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_113"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_1">
      <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
        <ModelParameterGroup cn="String=Initial Time" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling" value="0" type="Model" simulationType="time"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium]" value="1" type="Compartment" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]" value="0.00035" type="Compartment" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]" value="0.00105" type="Compartment" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Species Values" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c]" value="311489514795000" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n]" value="49837732197299.99" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c]" value="726794113608999.8" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n]" value="116288744376999.9" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf]" value="149860975226" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave]" value="1322823460650" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE]" value="1302589067370" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf]" value="127729607577" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave]" value="1124273476590" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE]" value="725908858903.0001" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta]" value="48177126855999.98" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7]" value="463707204823.9352" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski]" value="6323247899850" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7_mRNA]" value="6182762730.987911" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski_mRNA]" value="41388964352.41602" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R]" value="0.0103" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R]" value="0.02869" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE]" value="0.33" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE]" value="0.033" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave]" value="0.33" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave]" value="0.03742" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd]" value="0.005" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC]" value="2197" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid]" value="0.02609" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE]" value="0.005" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE]" value="0.025" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c]" value="0.16" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c]" value="0.08" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n]" value="0.5" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c]" value="6.85e-05" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c]" value="0.16" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n]" value="0.1174" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n]" value="236.4499999999157" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c]" value="492.6100000007736" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiObs]" value="0.0654552296667" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7Obs]" value="0.73333706375" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAObs]" value="0.00977782751667" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial]" value="0.00977782751667" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial]" value="0.0654552296667" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial]" value="0.73333706375" type="ModelValue" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R1_Smad2_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R1_Smad2_import],ParameterGroup=Parameters,Parameter=Kimp_Smad2c" value="0.16" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R2_Smad2_export]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R2_Smad2_export],ParameterGroup=Parameters,Parameter=Kexp_Smad2n" value="1" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R3_Smad4_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R3_Smad4_import],ParameterGroup=Parameters,Parameter=Kimp_Smad4c" value="0.08" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R4_Smad4_export]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R4_Smad4_export],ParameterGroup=Parameters,Parameter=Kexp_Smad4n" value="0.5" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R5_T1R_production]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R5_T1R_production],ParameterGroup=Parameters,Parameter=v" value="0.0103" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R6_T1R_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R6_T1R_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R7_T1R_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R7_T1R_Cave_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R8_T1R_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R8_T1R_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R9_T1R_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R9_T1R_EE_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R10_T1R_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R10_T1R_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.005" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R11_T2R_production]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R11_T2R_production],ParameterGroup=Parameters,Parameter=v" value="0.02869" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R12_T2R_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R12_T2R_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R13_T2R_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R13_T2R_Cave_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R14_T2R_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R14_T2R_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R15_T2R_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R15_T2R_EE_recycling],ParameterGroup=Parameters,Parameter=kr_EE" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R16_T2R_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R16_T2R_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.025" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R17_LRC_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R17_LRC_formation],ParameterGroup=Parameters,Parameter=k_LRC" value="2197" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R18_LRC_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R18_LRC_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R19_LRC_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R19_LRC_Cave_recycling],ParameterGroup=Parameters,Parameter=kr_Cave" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R20_LRC_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R20_LRC_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R21_LRC_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R21_LRC_EE_recycling],ParameterGroup=Parameters,Parameter=kr_EE" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R22_LRC_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R22_LRC_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.005" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R23_Smads_Complex_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R23_Smads_Complex_formation],ParameterGroup=Parameters,Parameter=k_Smads_Complex_c" value="6.85e-05" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R24_Smads_Complex_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R24_Smads_Complex_import],ParameterGroup=Parameters,Parameter=Kimp_Smads_Complex_c" value="0.16" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R25_Smads_Complex_Dissociation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R25_Smads_Complex_Dissociation],ParameterGroup=Parameters,Parameter=k1" value="0.1174" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Transcription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Transcription],ParameterGroup=Parameters,Parameter=k" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranscription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranscription],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7mRNADeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7mRNADeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkimRNADeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkimRNADeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Translation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Translation],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranslation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranslation],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiDeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiDeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Feedback]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Feedback],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Deg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Deg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
        </ModelParameterGroup>
      </ModelParameterSet>
    </ListOfModelParameterSets>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_7"/>
      <StateTemplateVariable objectReference="Metabolite_57"/>
      <StateTemplateVariable objectReference="Metabolite_41"/>
      <StateTemplateVariable objectReference="Metabolite_61"/>
      <StateTemplateVariable objectReference="Metabolite_77"/>
      <StateTemplateVariable objectReference="Metabolite_101"/>
      <StateTemplateVariable objectReference="Metabolite_49"/>
      <StateTemplateVariable objectReference="Metabolite_71"/>
      <StateTemplateVariable objectReference="Metabolite_103"/>
      <StateTemplateVariable objectReference="Metabolite_105"/>
      <StateTemplateVariable objectReference="Metabolite_113"/>
      <StateTemplateVariable objectReference="Metabolite_115"/>
      <StateTemplateVariable objectReference="Metabolite_117"/>
      <StateTemplateVariable objectReference="Metabolite_119"/>
      <StateTemplateVariable objectReference="Metabolite_107"/>
      <StateTemplateVariable objectReference="Metabolite_111"/>
      <StateTemplateVariable objectReference="Metabolite_109"/>
      <StateTemplateVariable objectReference="Metabolite_53"/>
      <StateTemplateVariable objectReference="Metabolite_47"/>
      <StateTemplateVariable objectReference="Metabolite_65"/>
      <StateTemplateVariable objectReference="Metabolite_73"/>
      <StateTemplateVariable objectReference="ModelValue_37"/>
      <StateTemplateVariable objectReference="ModelValue_36"/>
      <StateTemplateVariable objectReference="ModelValue_35"/>
      <StateTemplateVariable objectReference="ModelValue_34"/>
      <StateTemplateVariable objectReference="ModelValue_31"/>
      <StateTemplateVariable objectReference="Compartment_9"/>
      <StateTemplateVariable objectReference="Compartment_15"/>
      <StateTemplateVariable objectReference="Compartment_17"/>
      <StateTemplateVariable objectReference="ModelValue_55"/>
      <StateTemplateVariable objectReference="ModelValue_54"/>
      <StateTemplateVariable objectReference="ModelValue_53"/>
      <StateTemplateVariable objectReference="ModelValue_52"/>
      <StateTemplateVariable objectReference="ModelValue_51"/>
      <StateTemplateVariable objectReference="ModelValue_50"/>
      <StateTemplateVariable objectReference="ModelValue_49"/>
      <StateTemplateVariable objectReference="ModelValue_48"/>
      <StateTemplateVariable objectReference="ModelValue_47"/>
      <StateTemplateVariable objectReference="ModelValue_46"/>
      <StateTemplateVariable objectReference="ModelValue_45"/>
      <StateTemplateVariable objectReference="ModelValue_44"/>
      <StateTemplateVariable objectReference="ModelValue_43"/>
      <StateTemplateVariable objectReference="ModelValue_42"/>
      <StateTemplateVariable objectReference="ModelValue_41"/>
      <StateTemplateVariable objectReference="ModelValue_40"/>
      <StateTemplateVariable objectReference="ModelValue_39"/>
      <StateTemplateVariable objectReference="ModelValue_38"/>
      <StateTemplateVariable objectReference="ModelValue_33"/>
      <StateTemplateVariable objectReference="ModelValue_32"/>
      <StateTemplateVariable objectReference="ModelValue_30"/>
      <StateTemplateVariable objectReference="ModelValue_29"/>
      <StateTemplateVariable objectReference="ModelValue_28"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 149860975226 127729607577 116288744376999.9 311489514795000 0 1302589067370 725908858903.0001 0 0 463707204823.9352 6323247899850 6182762730.987911 41388964352.41602 0 48177126855999.98 0 1322823460650 1124273476590 726794113608999.8 49837732197299.99 236.4499999999157 492.6100000007736 0.0654552296667 0.73333706375 0.00977782751667 1 0.00035 0.00105 0.0103 0.02869 0.33 0.033 0.33 0.03742 0.005 2197 0.02609 0.005 0.025 0.16 1 0.08 0.5 6.85e-05 0.16 0.1174 1 1 0.00977782751667 0.0654552296667 0.73333706375 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_27" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_21" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_16" target="../../Models/2017/09_Sept/zi_timecourse_simulation.csv" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="AutomaticStepSize" type="bool" value="0"/>
        <Parameter name="StepNumber" type="unsignedInteger" value="1000"/>
        <Parameter name="StepSize" type="float" value="1"/>
        <Parameter name="Duration" type="float" value="1000"/>
        <Parameter name="TimeSeriesRequested" type="float" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Start in Steady State" type="bool" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
        <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
      </Method>
    </Task>
    <Task key="Task_16" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report reference="Report_17" target="zi_repeat.csv" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="1"/>
        <ParameterGroup name="ScanItems">
          <ParameterGroup name="ScanItem">
            <Parameter name="Number of steps" type="unsignedInteger" value="10"/>
            <Parameter name="Object" type="cn" value="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=InitialConcentration"/>
            <Parameter name="Type" type="unsignedInteger" value="0"/>
          </ParameterGroup>
        </ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="0"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_17" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_20" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_18" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_9" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_10" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
        </ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
        </ParameterGroup>
      </Problem>
      <Method name="Evolutionary Programming" type="EvolutionaryProgram">
        <Parameter name="Number of Generations" type="unsignedInteger" value="200"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_11" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_12" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_14" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_15" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_27"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_21" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_20" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_9" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_10" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_11" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_12" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_13" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_14" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_15" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_16" name="Time-Course" taskType="unset" separator="&#x09;" precision="6">
      <Comment>
      </Comment>
      <Table printTitle="1">
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c],Reference=Value"/>
      </Table>
    </Report>
    <Report key="Report_17" name="profilelikelihood" taskType="unset" separator="&#x09;" precision="6">
      <Comment>
      </Comment>
      <Table printTitle="1">
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Metabolites[Smad3n],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
      </Table>
    </Report>
  </ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[Smad3c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad3n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad4c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad4n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smads_Complex_c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smads_Complex_n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[TGF_beta]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad7]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Total_Smad2n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Total_Smad2c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <SBMLReference file="Zi2012.xml">
    <SBMLMap SBMLid="Kcd" COPASIkey="ModelValue_49"/>
    <SBMLMap SBMLid="Kdeg_T1R_EE" COPASIkey="ModelValue_46"/>
    <SBMLMap SBMLid="Kdeg_T2R_EE" COPASIkey="ModelValue_45"/>
    <SBMLMap SBMLid="Kdiss_Smads_Complex_n" COPASIkey="ModelValue_38"/>
    <SBMLMap SBMLid="Kexp_Smad2n" COPASIkey="ModelValue_43"/>
    <SBMLMap SBMLid="Kexp_Smad4n" COPASIkey="ModelValue_41"/>
    <SBMLMap SBMLid="Kimp_Smad2c" COPASIkey="ModelValue_44"/>
    <SBMLMap SBMLid="Kimp_Smad4c" COPASIkey="ModelValue_42"/>
    <SBMLMap SBMLid="Kimp_Smads_Complex_c" COPASIkey="ModelValue_39"/>
    <SBMLMap SBMLid="Klid" COPASIkey="ModelValue_47"/>
    <SBMLMap SBMLid="LRC_Cave" COPASIkey="Metabolite_103"/>
    <SBMLMap SBMLid="LRC_EE" COPASIkey="Metabolite_105"/>
    <SBMLMap SBMLid="LRC_Surf" COPASIkey="Metabolite_101"/>
    <SBMLMap SBMLid="R10_T1R_EE_degradation" COPASIkey="Reaction_58"/>
    <SBMLMap SBMLid="R11_T2R_production" COPASIkey="Reaction_57"/>
    <SBMLMap SBMLid="R12_T2R_Cave_formation" COPASIkey="Reaction_56"/>
    <SBMLMap SBMLid="R13_T2R_Cave_recycling" COPASIkey="Reaction_55"/>
    <SBMLMap SBMLid="R14_T2R_EE_formation" COPASIkey="Reaction_54"/>
    <SBMLMap SBMLid="R15_T2R_EE_recycling" COPASIkey="Reaction_53"/>
    <SBMLMap SBMLid="R16_T2R_EE_degradation" COPASIkey="Reaction_52"/>
    <SBMLMap SBMLid="R17_LRC_formation" COPASIkey="Reaction_51"/>
    <SBMLMap SBMLid="R18_LRC_Cave_formation" COPASIkey="Reaction_50"/>
    <SBMLMap SBMLid="R19_LRC_Cave_recycling" COPASIkey="Reaction_49"/>
    <SBMLMap SBMLid="R1_Smad2_import" COPASIkey="Reaction_67"/>
    <SBMLMap SBMLid="R20_LRC_EE_formation" COPASIkey="Reaction_48"/>
    <SBMLMap SBMLid="R21_LRC_EE_recycling" COPASIkey="Reaction_47"/>
    <SBMLMap SBMLid="R22_LRC_EE_degradation" COPASIkey="Reaction_46"/>
    <SBMLMap SBMLid="R23_Smads_Complex_formation" COPASIkey="Reaction_45"/>
    <SBMLMap SBMLid="R24_Smads_Complex_import" COPASIkey="Reaction_44"/>
    <SBMLMap SBMLid="R25_Smads_Complex_Dissociation" COPASIkey="Reaction_43"/>
    <SBMLMap SBMLid="R2_Smad2_export" COPASIkey="Reaction_66"/>
    <SBMLMap SBMLid="R3_Smad4_import" COPASIkey="Reaction_65"/>
    <SBMLMap SBMLid="R4_Smad4_export" COPASIkey="Reaction_64"/>
    <SBMLMap SBMLid="R5_T1R_production" COPASIkey="Reaction_63"/>
    <SBMLMap SBMLid="R6_T1R_Cave_formation" COPASIkey="Reaction_62"/>
    <SBMLMap SBMLid="R7_T1R_Cave_recycling" COPASIkey="Reaction_61"/>
    <SBMLMap SBMLid="R8_T1R_EE_formation" COPASIkey="Reaction_60"/>
    <SBMLMap SBMLid="R9_T1R_EE_recycling" COPASIkey="Reaction_59"/>
    <SBMLMap SBMLid="Smad2c" COPASIkey="Metabolite_77"/>
    <SBMLMap SBMLid="Smad2n" COPASIkey="Metabolite_73"/>
    <SBMLMap SBMLid="Smad4c" COPASIkey="Metabolite_65"/>
    <SBMLMap SBMLid="Smad4n" COPASIkey="Metabolite_61"/>
    <SBMLMap SBMLid="Smads_Complex_c" COPASIkey="Metabolite_107"/>
    <SBMLMap SBMLid="Smads_Complex_n" COPASIkey="Metabolite_109"/>
    <SBMLMap SBMLid="T1R_Cave" COPASIkey="Metabolite_53"/>
    <SBMLMap SBMLid="T1R_EE" COPASIkey="Metabolite_49"/>
    <SBMLMap SBMLid="T1R_Surf" COPASIkey="Metabolite_57"/>
    <SBMLMap SBMLid="T2R_Cave" COPASIkey="Metabolite_47"/>
    <SBMLMap SBMLid="T2R_EE" COPASIkey="Metabolite_71"/>
    <SBMLMap SBMLid="T2R_Surf" COPASIkey="Metabolite_41"/>
    <SBMLMap SBMLid="TGF_beta" COPASIkey="Metabolite_111"/>
    <SBMLMap SBMLid="Total_Smad2c" COPASIkey="ModelValue_36"/>
    <SBMLMap SBMLid="Total_Smad2n" COPASIkey="ModelValue_37"/>
    <SBMLMap SBMLid="V_cyt" COPASIkey="Compartment_17"/>
    <SBMLMap SBMLid="V_medium" COPASIkey="Compartment_9"/>
    <SBMLMap SBMLid="V_nuc" COPASIkey="Compartment_15"/>
    <SBMLMap SBMLid="k_LRC" COPASIkey="ModelValue_48"/>
    <SBMLMap SBMLid="k_Smads_Complex_c" COPASIkey="ModelValue_40"/>
    <SBMLMap SBMLid="ki_Cave" COPASIkey="ModelValue_51"/>
    <SBMLMap SBMLid="ki_EE" COPASIkey="ModelValue_53"/>
    <SBMLMap SBMLid="kr_Cave" COPASIkey="ModelValue_50"/>
    <SBMLMap SBMLid="kr_EE" COPASIkey="ModelValue_52"/>
    <SBMLMap SBMLid="v_T1R" COPASIkey="ModelValue_55"/>
    <SBMLMap SBMLid="v_T2R" COPASIkey="ModelValue_54"/>
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
</COPASI>"""


    @property
    def smad7_not_reproduced(self):
        """

        :return:
        """
        return """<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-10-11 14:57:38 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="19" versionDevel="140" copasiSourcesModified="0">
  <ListOfFunctions>
    <Function key="Function_6" name="Constant flux (irreversible)" type="PreDefined" reversible="false">
      <Expression>
        v
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_49" name="v" order="0" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_13" name="Mass action (irreversible)" type="MassAction" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <rdf:Description rdf:about="#Function_13">
   <CopasiMT:is rdf:resource="urn:miriam:obo.sbo:SBO:0000041" />
   </rdf:Description>
   </rdf:RDF>
      </MiriamAnnotation>
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
<b>Mass action rate law for first order irreversible reactions</b>
<p>
Reaction scheme where the products are created from the reactants and the change of a product quantity is proportional to the product of reactant activities. The reaction scheme does not include any reverse process that creates the reactants from the products. The change of a product quantity is proportional to the quantity of one reactant.
</p>
</body>
      </Comment>
      <Expression>
        k1*PRODUCT&lt;substrate_i>
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_81" name="k1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_79" name="substrate" order="1" role="substrate"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_40" name="Function for R1_Smad2_import" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_40">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:07:29Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
      </MiriamAnnotation>
      <Expression>
        V_cyt*Kimp_Smad2c*Smad2c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_254" name="Kimp_Smad2c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_258" name="Smad2c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_264" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_41" name="Function for R2_Smad2_export" type="UserDefined" reversible="false">
      <Expression>
        V_nuc*Kexp_Smad2n*Smad2n
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_262" name="Kexp_Smad2n" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_267" name="Smad2n" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_265" name="V_nuc" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_42" name="Function for R3_Smad4_import" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*Kimp_Smad4c*Smad4c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_246" name="Kimp_Smad4c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_270" name="Smad4c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_268" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_43" name="Function for R4_Smad4_export" type="UserDefined" reversible="false">
      <Expression>
        V_nuc*Kexp_Smad4n*Smad4n
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_266" name="Kexp_Smad4n" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_273" name="Smad4n" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_271" name="V_nuc" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="Function for R15_T2R_EE_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_EE*T2R_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_276" name="T2R_EE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_274" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_269" name="kr_EE" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="Function for R17_LRC_formation" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_45">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:42:20Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        V_cyt*k_LRC*TGF_beta*T2R_Surf*T1R_Surf
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_283" name="T1R_Surf" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_281" name="T2R_Surf" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_279" name="TGF_beta" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_277" name="V_cyt" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_272" name="k_LRC" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_46" name="Function for R19_LRC_Cave_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_Cave*LRC_Cave
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_275" name="LRC_Cave" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_284" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_280" name="kr_Cave" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="Function for R21_LRC_EE_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_EE*LRC_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_287" name="LRC_EE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_285" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_282" name="kr_EE" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="Function for R23_Smads_Complex_formation" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_48">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-22T12:24:54Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
      </MiriamAnnotation>
      <Expression>
        k_Smads_Complex_c*Smad2c*Smad4c*LRC_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_292" name="LRC_EE" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_278" name="Smad2c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_290" name="Smad4c" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_288" name="k_Smads_Complex_c" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="Function for R24_Smads_Complex_import" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*Kimp_Smads_Complex_c*Smads_Complex_c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_289" name="Kimp_Smads_Complex_c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_294" name="Smads_Complex_c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_293" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_50" name="k*A/I" type="UserDefined" reversible="unspecified">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_50">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:42:22Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        k*(A/I)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_373" name="k" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_383" name="A" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_386" name="I" order="2" role="modifier"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_9" name="Zi2007_TGFbeta_signaling" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="nmol" type="deterministic" avogadroConstant="6.022140857e+23">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_9">
    <bqbiol:hasTaxon>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/taxonomy/131567"/>
      </rdf:Bag>
    </bqbiol:hasTaxon>
    <dcterms:bibliographicCitation>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <CopasiMT:isDescribedBy rdf:resource="http://identifiers.org/pubmed/17895977"/>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:bibliographicCitation>
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2008-02-14T09:21:13Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <dcterms:creator>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>hdharuri@cds.caltech.edu</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Dharuri</vCard:Family>
                <vCard:Given>Harish</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>California Institute of Technology</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Yang</vCard:Family>
                <vCard:Given>Kun</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Beijing National Laboratory for Molecular Sciences</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>klipp@molgen.mpg.de</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Klipp</vCard:Family>
                <vCard:Given>Edda</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Max Planck Institute for molecular genetics</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:creator>
    <dcterms:modified>
      <rdf:Description>
        <dcterms:W3CDTF>2012-07-05T16:45:46Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:modified>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/MODEL3388742457"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/BIOMD0000000163"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isPartOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/kegg.pathway/hsa04350"/>
      </rdf:Bag>
    </CopasiMT:isPartOf>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      <body xmlns="http://www.w3.org/1999/xhtml">
    <p>The model reproduces the time profiles of Total Smad2 in the nucleus as well as the cytoplasm as depicted in 2D and also the other time profiles as depicted in Fig 2.  Two parameters that are not present in the paper are introduced here for illustration purposes and they are Total Smad2n and Total Smad2c. The term kr_EE*LRC_EE has not been included in the ODE's for T1R_surf, T2R_surf and TGFbeta in the paper but is included in this model. MathSBML was used to reproduce the simulation result.</p>
    <br />
    <p>To the extent possible under law, all copyright and related or neighbouring rights to this encoded model have been dedicated to the public domain worldwide. Please refer to      <a href="http://creativecommons.org/publicdomain/zero/1.0/" title="Creative Commons CC0">CC0 Public Domain Dedication</a>
          for more information.      </p>
  <p>In summary, you are entitled to use this encoded model in absolutely any manner you deem suitable, verbatim, or with modification, alone or embedded it in a larger context, redistribute it, commercially or not, in a restricted way or not.</p>
  <br />
  <p>To cite BioModels Database, please use:      <a href="http://www.ncbi.nlm.nih.gov/pubmed/20587024" target="_blank">Li C, Donizelli M, Rodriguez N, Dharuri H, Endler L, Chelliah V, Li L, He E, Henry A, Stefan MI, Snoep JL, Hucka M, Le Novère N, Laibe C (2010) BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models. BMC Syst Biol., 4:92.</a>
</p>
</body>
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_15" name="Medium" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_15">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005576" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_21" name="Nucleus" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_21">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_23" name="Cytoplasm" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_23">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005737" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_117" name="Smad3c" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_117">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_113" name="Smad3n" simulationType="reactions" compartment="Compartment_21">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_113">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_105" name="Smad4c" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_105">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_101" name="Smad4n" simulationType="reactions" compartment="Compartment_21">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_101">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_47" name="T1R_Surf" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_47">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_49" name="T1R_Cave" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_49">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_57" name="T1R_EE" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_57">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_77" name="T2R_Surf" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_77">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_61" name="T2R_Cave" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_61">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_111" name="T2R_EE" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_111">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_141" name="LRC_Surf" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_141">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_143" name="LRC_Cave" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_143">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_145" name="LRC_EE" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_145">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_147" name="Smads_Complex_c" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_147">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_149" name="Smads_Complex_n" simulationType="reactions" compartment="Compartment_21">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_149">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_151" name="TGF_beta" simulationType="reactions" compartment="Compartment_15">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_151">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_153" name="Smad7" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_153">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:03:36Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_155" name="Ski" simulationType="reactions" compartment="Compartment_23">
      </Metabolite>
      <Metabolite key="Metabolite_157" name="Smad7_mRNA" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_157">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:06:01Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_159" name="Ski_mRNA" simulationType="reactions" compartment="Compartment_23">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_159">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:06:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_28" name="v_T1R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_29" name="v_T2R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_30" name="ki_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_31" name="kr_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_32" name="ki_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_33" name="kr_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_34" name="Kcd" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_35" name="k_LRC" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_36" name="Klid" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_37" name="Kdeg_T1R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_38" name="Kdeg_T2R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_39" name="Kimp_Smad2c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_40" name="Kexp_Smad2n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_41" name="Kimp_Smad4c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_42" name="Kexp_Smad4n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_43" name="k_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_44" name="Kimp_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_45" name="Kdiss_Smads_Complex_n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_46" name="Total_Smad2n" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_47" name="Total_Smad2c" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_48" name="SkiObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_48">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:11:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski_mRNA],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_49" name="Smad7Obs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_49">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:13Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_50" name="SkiSF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_50">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_51" name="Smad7SF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_51">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:45Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_52" name="Smad7mRNAObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_52">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:12:28Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7_mRNA],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_53" name="Smad7mRNAInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_54" name="SkiInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_55" name="Smad7ProteinInitial" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_34" name="R1_Smad2_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_34">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:41:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_113" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4297" name="Kimp_Smad2c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_40" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="ModelValue_39"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_117"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Compartment_23"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_35" name="R2_Smad2_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_35">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006886" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_113" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4298" name="Kexp_Smad2n" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_41" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="ModelValue_40"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_113"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Compartment_21"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_36" name="R3_Smad4_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_36">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:52Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_105" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_101" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_74" name="Kimp_Smad4c" value="0.08"/>
        </ListOfConstants>
        <KineticLaw function="Function_42" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="ModelValue_41"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Metabolite_105"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Compartment_23"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_37" name="R4_Smad4_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_37">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006886" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_101" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_105" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_73" name="Kexp_Smad4n" value="0.5"/>
        </ListOfConstants>
        <KineticLaw function="Function_43" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="ModelValue_42"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_101"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Compartment_21"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_38" name="R5_T1R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_38">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:47:37Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032905" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_72" name="v" value="0.0103"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_28"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_39" name="R6_T1R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_39">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_71" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_32"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_40" name="R7_T1R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_40">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-22T12:31:08Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_49" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_70" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_33"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_49"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_41" name="R8_T1R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_41">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_69" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_30"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_42" name="R9_T1R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_42">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_68" name="k1" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_31"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_57"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_43" name="R10_T1R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_43">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:49:31Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_67" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_37"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_57"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_44" name="R11_T2R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_44">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:51:21Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032906" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_77" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_66" name="v" value="0.02869"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_29"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_45" name="R12_T2R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_45">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_77" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_65" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_32"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_77"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_46" name="R13_T2R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_46">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_77" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_64" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_33"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_61"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_47" name="R14_T2R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_47">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_77" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_111" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_63" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_30"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_77"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_48" name="R15_T2R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_48">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_111" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_77" stoichiometry="1"/>
          <Product metabolite="Metabolite_151" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_62" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_44" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Metabolite_111"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Compartment_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="ModelValue_31"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_49" name="R16_T2R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_49">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_111" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_52" name="k1" value="0.025"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_38"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_111"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_50" name="R17_LRC_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_50">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005160" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_151" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_77" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_141" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_51" name="k_LRC" value="2197"/>
        </ListOfConstants>
        <KineticLaw function="Function_45" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_77"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_151"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Compartment_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="ModelValue_35"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_51" name="R18_LRC_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_51">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_141" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_143" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_61" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_32"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_141"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_52" name="R19_LRC_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_52">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_143" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
          <Product metabolite="Metabolite_151" stoichiometry="1"/>
          <Product metabolite="Metabolite_77" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_60" name="kr_Cave" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_46" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Metabolite_143"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Compartment_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="ModelValue_33"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_53" name="R20_LRC_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_53">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_141" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_145" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_59" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_30"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_141"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_54" name="R21_LRC_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_54">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_145" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
          <Product metabolite="Metabolite_77" stoichiometry="1"/>
          <Product metabolite="Metabolite_151" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_58" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_47" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Metabolite_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Compartment_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="ModelValue_31"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_55" name="R22_LRC_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_55">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_145" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_57" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_34"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_145"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_56" name="R23_Smads_Complex_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_56">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:11Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_117" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_105" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_147" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_145" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_56" name="k_Smads_Complex_c" value="6.85e-05"/>
        </ListOfConstants>
        <KineticLaw function="Function_48" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Metabolite_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Metabolite_117"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Metabolite_105"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="ModelValue_43"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_57" name="R24_Smads_Complex_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_57">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_147" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_149" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_55" name="Kimp_Smads_Complex_c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_49" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="ModelValue_44"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Metabolite_147"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Compartment_23"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_58" name="R25_Smads_Complex_Dissociation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_149" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_101" stoichiometry="1"/>
          <Product metabolite="Metabolite_113" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_54" name="k1" value="0.1174"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_149"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_59" name="Smad7Transcription" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_59">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:57:12Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_149" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_149" stoichiometry="1"/>
          <Product metabolite="Metabolite_157" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_155" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4006" name="k" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_50" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_373">
              <SourceParameter reference="Parameter_4006"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_383">
              <SourceParameter reference="Metabolite_149"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_386">
              <SourceParameter reference="Metabolite_155"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_60" name="SkiTranscription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_149" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_149" stoichiometry="1"/>
          <Product metabolite="Metabolite_159" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4491" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4491"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_149"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_61" name="Smad7mRNADeg" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_61">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:57:35Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_157" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4490" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4490"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_157"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_62" name="SkimRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_159" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4489" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4489"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_159"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_63" name="Smad7Translation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_157" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_157" stoichiometry="1"/>
          <Product metabolite="Metabolite_153" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4488" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4488"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_157"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_64" name="SkiTranslation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_159" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_159" stoichiometry="1"/>
          <Product metabolite="Metabolite_155" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4487" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4487"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_159"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_65" name="SkiDeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_155" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4486" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4486"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_155"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_66" name="Smad7Feedback" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_153" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_143" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4485" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4485"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_153"/>
              <SourceParameter reference="Metabolite_143"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_67" name="Smad7Deg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_153" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4484" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4484"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_153"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_1">
      <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
        <ModelParameterGroup cn="String=Initial Time" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling" value="0" type="Model" simulationType="time"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium]" value="1" type="Compartment" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]" value="0.00035" type="Compartment" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]" value="0.00105" type="Compartment" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Species Values" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c]" value="311489514795000" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n]" value="49837732197299.99" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c]" value="726794113608999.8" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n]" value="116288744377000" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf]" value="149860975226" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave]" value="1322823460650" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE]" value="1302589067370" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf]" value="127729607577" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave]" value="1124273476590" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE]" value="725908858903.0001" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta]" value="48177126855999.98" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7]" value="463707204823.9352" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski]" value="6323247899850" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7_mRNA]" value="6182762730.987911" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski_mRNA]" value="41388964352.41602" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R]" value="0.0103" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R]" value="0.02869" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE]" value="0.33" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE]" value="0.033" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave]" value="0.33" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave]" value="0.03742" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd]" value="0.005" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC]" value="2197" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid]" value="0.02609" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE]" value="0.005" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE]" value="0.025" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c]" value="0.16" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c]" value="0.08" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n]" value="0.5" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c]" value="6.85e-05" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c]" value="0.16" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n]" value="0.1174" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n]" value="236.4499999999157" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c]" value="492.6100000007736" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiObs]" value="0.0654552296667" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7Obs]" value="0.73333706375" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAObs]" value="0.00977782751667" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial]" value="0.00977782751667" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial]" value="0.0654552296667" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial]" value="0.73333706375" type="ModelValue" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R1_Smad2_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R1_Smad2_import],ParameterGroup=Parameters,Parameter=Kimp_Smad2c" value="0.16" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R2_Smad2_export]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R2_Smad2_export],ParameterGroup=Parameters,Parameter=Kexp_Smad2n" value="1" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R3_Smad4_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R3_Smad4_import],ParameterGroup=Parameters,Parameter=Kimp_Smad4c" value="0.08" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R4_Smad4_export]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R4_Smad4_export],ParameterGroup=Parameters,Parameter=Kexp_Smad4n" value="0.5" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R5_T1R_production]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R5_T1R_production],ParameterGroup=Parameters,Parameter=v" value="0.0103" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R6_T1R_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R6_T1R_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R7_T1R_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R7_T1R_Cave_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R8_T1R_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R8_T1R_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R9_T1R_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R9_T1R_EE_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R10_T1R_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R10_T1R_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.005" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R11_T2R_production]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R11_T2R_production],ParameterGroup=Parameters,Parameter=v" value="0.02869" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R12_T2R_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R12_T2R_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R13_T2R_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R13_T2R_Cave_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R14_T2R_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R14_T2R_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R15_T2R_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R15_T2R_EE_recycling],ParameterGroup=Parameters,Parameter=kr_EE" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R16_T2R_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R16_T2R_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.025" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R17_LRC_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R17_LRC_formation],ParameterGroup=Parameters,Parameter=k_LRC" value="2197" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R18_LRC_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R18_LRC_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R19_LRC_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R19_LRC_Cave_recycling],ParameterGroup=Parameters,Parameter=kr_Cave" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R20_LRC_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R20_LRC_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R21_LRC_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R21_LRC_EE_recycling],ParameterGroup=Parameters,Parameter=kr_EE" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R22_LRC_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R22_LRC_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.005" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R23_Smads_Complex_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R23_Smads_Complex_formation],ParameterGroup=Parameters,Parameter=k_Smads_Complex_c" value="6.85e-05" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R24_Smads_Complex_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R24_Smads_Complex_import],ParameterGroup=Parameters,Parameter=Kimp_Smads_Complex_c" value="0.16" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R25_Smads_Complex_Dissociation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R25_Smads_Complex_Dissociation],ParameterGroup=Parameters,Parameter=k1" value="0.1174" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Transcription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Transcription],ParameterGroup=Parameters,Parameter=k" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranscription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranscription],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7mRNADeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7mRNADeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkimRNADeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkimRNADeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Translation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Translation],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranslation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranslation],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiDeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiDeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Feedback]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Feedback],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Deg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Deg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
        </ModelParameterGroup>
      </ModelParameterSet>
    </ListOfModelParameterSets>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_9"/>
      <StateTemplateVariable objectReference="Metabolite_47"/>
      <StateTemplateVariable objectReference="Metabolite_77"/>
      <StateTemplateVariable objectReference="Metabolite_101"/>
      <StateTemplateVariable objectReference="Metabolite_117"/>
      <StateTemplateVariable objectReference="Metabolite_153"/>
      <StateTemplateVariable objectReference="Metabolite_141"/>
      <StateTemplateVariable objectReference="Metabolite_57"/>
      <StateTemplateVariable objectReference="Metabolite_111"/>
      <StateTemplateVariable objectReference="Metabolite_145"/>
      <StateTemplateVariable objectReference="Metabolite_155"/>
      <StateTemplateVariable objectReference="Metabolite_157"/>
      <StateTemplateVariable objectReference="Metabolite_159"/>
      <StateTemplateVariable objectReference="Metabolite_143"/>
      <StateTemplateVariable objectReference="Metabolite_147"/>
      <StateTemplateVariable objectReference="Metabolite_151"/>
      <StateTemplateVariable objectReference="Metabolite_149"/>
      <StateTemplateVariable objectReference="Metabolite_49"/>
      <StateTemplateVariable objectReference="Metabolite_61"/>
      <StateTemplateVariable objectReference="Metabolite_113"/>
      <StateTemplateVariable objectReference="Metabolite_105"/>
      <StateTemplateVariable objectReference="ModelValue_46"/>
      <StateTemplateVariable objectReference="ModelValue_47"/>
      <StateTemplateVariable objectReference="ModelValue_48"/>
      <StateTemplateVariable objectReference="ModelValue_49"/>
      <StateTemplateVariable objectReference="ModelValue_52"/>
      <StateTemplateVariable objectReference="Compartment_15"/>
      <StateTemplateVariable objectReference="Compartment_21"/>
      <StateTemplateVariable objectReference="Compartment_23"/>
      <StateTemplateVariable objectReference="ModelValue_28"/>
      <StateTemplateVariable objectReference="ModelValue_29"/>
      <StateTemplateVariable objectReference="ModelValue_30"/>
      <StateTemplateVariable objectReference="ModelValue_31"/>
      <StateTemplateVariable objectReference="ModelValue_32"/>
      <StateTemplateVariable objectReference="ModelValue_33"/>
      <StateTemplateVariable objectReference="ModelValue_34"/>
      <StateTemplateVariable objectReference="ModelValue_35"/>
      <StateTemplateVariable objectReference="ModelValue_36"/>
      <StateTemplateVariable objectReference="ModelValue_37"/>
      <StateTemplateVariable objectReference="ModelValue_38"/>
      <StateTemplateVariable objectReference="ModelValue_39"/>
      <StateTemplateVariable objectReference="ModelValue_40"/>
      <StateTemplateVariable objectReference="ModelValue_41"/>
      <StateTemplateVariable objectReference="ModelValue_42"/>
      <StateTemplateVariable objectReference="ModelValue_43"/>
      <StateTemplateVariable objectReference="ModelValue_44"/>
      <StateTemplateVariable objectReference="ModelValue_45"/>
      <StateTemplateVariable objectReference="ModelValue_50"/>
      <StateTemplateVariable objectReference="ModelValue_51"/>
      <StateTemplateVariable objectReference="ModelValue_53"/>
      <StateTemplateVariable objectReference="ModelValue_54"/>
      <StateTemplateVariable objectReference="ModelValue_55"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 149860975226 127729607577 116288744377000 311489514795000 463707204823.9352 0 1302589067370 725908858903.0001 0 6323247899850 6182762730.987911 41388964352.41602 0 0 48177126855999.98 0 1322823460650 1124273476590 49837732197299.99 726794113608999.8 236.4499999999157 492.6100000007736 0.0654552296667 0.73333706375 0.00977782751667 1 0.00035 0.00105 0.0103 0.02869 0.33 0.033 0.33 0.03742 0.005 2197 0.02609 0.005 0.025 0.16 1 0.08 0.5 6.85e-05 0.16 0.1174 1 1 0.00977782751667 0.0654552296667 0.73333706375 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_14" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_17" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_25" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Report reference="Report_20" target="../../Models/2017/09_Sept/zi_timecourse_simulation.csv" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="AutomaticStepSize" type="bool" value="0"/>
        <Parameter name="StepNumber" type="unsignedInteger" value="1000"/>
        <Parameter name="StepSize" type="float" value="1"/>
        <Parameter name="Duration" type="float" value="1000"/>
        <Parameter name="TimeSeriesRequested" type="float" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Start in Steady State" type="bool" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
        <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
      </Method>
    </Task>
    <Task key="Task_24" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report reference="Report_21" target="zi_repeat.csv" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="1"/>
        <ParameterGroup name="ScanItems">
          <ParameterGroup name="ScanItem">
            <Parameter name="Number of steps" type="unsignedInteger" value="10"/>
            <Parameter name="Object" type="cn" value="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=InitialConcentration"/>
            <Parameter name="Type" type="unsignedInteger" value="0"/>
          </ParameterGroup>
        </ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="0"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_23" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_16" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_22" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_15" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_21" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_14" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
        </ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
        </ParameterGroup>
      </Problem>
      <Method name="Evolutionary Programming" type="EvolutionaryProgram">
        <Parameter name="Number of Generations" type="unsignedInteger" value="200"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_14"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Use Reder" type="bool" value="1"/>
        <Parameter name="Use Smallbone" type="bool" value="1"/>
      </Method>
    </Task>
    <Task key="Task_19" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_12" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_18" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_11" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_17" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_10" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_16" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
    <Task key="Task_15" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
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
    <Task key="Task_26" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_9" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_14"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_17" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_16" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_15" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_14" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_13" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_12" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_11" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_10" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_9" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_20" name="Time-Course" taskType="unset" separator="&#x09;" precision="6">
      <Comment>
      </Comment>
      <Table printTitle="1">
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c],Reference=Value"/>
      </Table>
    </Report>
    <Report key="Report_21" name="profilelikelihood" taskType="unset" separator="&#x09;" precision="6">
      <Comment>
      </Comment>
      <Table printTitle="1">
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Metabolites[Smad3n],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
      </Table>
    </Report>
  </ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[Smad3c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad3n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad4c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad4n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smads_Complex_c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smads_Complex_n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[TGF_beta]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad7]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Total_Smad2n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Total_Smad2c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <SBMLReference file="Zi2012.xml">
    <SBMLMap SBMLid="Kcd" COPASIkey="ModelValue_34"/>
    <SBMLMap SBMLid="Kdeg_T1R_EE" COPASIkey="ModelValue_37"/>
    <SBMLMap SBMLid="Kdeg_T2R_EE" COPASIkey="ModelValue_38"/>
    <SBMLMap SBMLid="Kdiss_Smads_Complex_n" COPASIkey="ModelValue_45"/>
    <SBMLMap SBMLid="Kexp_Smad2n" COPASIkey="ModelValue_40"/>
    <SBMLMap SBMLid="Kexp_Smad4n" COPASIkey="ModelValue_42"/>
    <SBMLMap SBMLid="Kimp_Smad2c" COPASIkey="ModelValue_39"/>
    <SBMLMap SBMLid="Kimp_Smad4c" COPASIkey="ModelValue_41"/>
    <SBMLMap SBMLid="Kimp_Smads_Complex_c" COPASIkey="ModelValue_44"/>
    <SBMLMap SBMLid="Klid" COPASIkey="ModelValue_36"/>
    <SBMLMap SBMLid="LRC_Cave" COPASIkey="Metabolite_143"/>
    <SBMLMap SBMLid="LRC_EE" COPASIkey="Metabolite_145"/>
    <SBMLMap SBMLid="LRC_Surf" COPASIkey="Metabolite_141"/>
    <SBMLMap SBMLid="R10_T1R_EE_degradation" COPASIkey="Reaction_43"/>
    <SBMLMap SBMLid="R11_T2R_production" COPASIkey="Reaction_44"/>
    <SBMLMap SBMLid="R12_T2R_Cave_formation" COPASIkey="Reaction_45"/>
    <SBMLMap SBMLid="R13_T2R_Cave_recycling" COPASIkey="Reaction_46"/>
    <SBMLMap SBMLid="R14_T2R_EE_formation" COPASIkey="Reaction_47"/>
    <SBMLMap SBMLid="R15_T2R_EE_recycling" COPASIkey="Reaction_48"/>
    <SBMLMap SBMLid="R16_T2R_EE_degradation" COPASIkey="Reaction_49"/>
    <SBMLMap SBMLid="R17_LRC_formation" COPASIkey="Reaction_50"/>
    <SBMLMap SBMLid="R18_LRC_Cave_formation" COPASIkey="Reaction_51"/>
    <SBMLMap SBMLid="R19_LRC_Cave_recycling" COPASIkey="Reaction_52"/>
    <SBMLMap SBMLid="R1_Smad2_import" COPASIkey="Reaction_34"/>
    <SBMLMap SBMLid="R20_LRC_EE_formation" COPASIkey="Reaction_53"/>
    <SBMLMap SBMLid="R21_LRC_EE_recycling" COPASIkey="Reaction_54"/>
    <SBMLMap SBMLid="R22_LRC_EE_degradation" COPASIkey="Reaction_55"/>
    <SBMLMap SBMLid="R23_Smads_Complex_formation" COPASIkey="Reaction_56"/>
    <SBMLMap SBMLid="R24_Smads_Complex_import" COPASIkey="Reaction_57"/>
    <SBMLMap SBMLid="R25_Smads_Complex_Dissociation" COPASIkey="Reaction_58"/>
    <SBMLMap SBMLid="R2_Smad2_export" COPASIkey="Reaction_35"/>
    <SBMLMap SBMLid="R3_Smad4_import" COPASIkey="Reaction_36"/>
    <SBMLMap SBMLid="R4_Smad4_export" COPASIkey="Reaction_37"/>
    <SBMLMap SBMLid="R5_T1R_production" COPASIkey="Reaction_38"/>
    <SBMLMap SBMLid="R6_T1R_Cave_formation" COPASIkey="Reaction_39"/>
    <SBMLMap SBMLid="R7_T1R_Cave_recycling" COPASIkey="Reaction_40"/>
    <SBMLMap SBMLid="R8_T1R_EE_formation" COPASIkey="Reaction_41"/>
    <SBMLMap SBMLid="R9_T1R_EE_recycling" COPASIkey="Reaction_42"/>
    <SBMLMap SBMLid="Smad2c" COPASIkey="Metabolite_117"/>
    <SBMLMap SBMLid="Smad2n" COPASIkey="Metabolite_113"/>
    <SBMLMap SBMLid="Smad4c" COPASIkey="Metabolite_105"/>
    <SBMLMap SBMLid="Smad4n" COPASIkey="Metabolite_101"/>
    <SBMLMap SBMLid="Smads_Complex_c" COPASIkey="Metabolite_147"/>
    <SBMLMap SBMLid="Smads_Complex_n" COPASIkey="Metabolite_149"/>
    <SBMLMap SBMLid="T1R_Cave" COPASIkey="Metabolite_49"/>
    <SBMLMap SBMLid="T1R_EE" COPASIkey="Metabolite_57"/>
    <SBMLMap SBMLid="T1R_Surf" COPASIkey="Metabolite_47"/>
    <SBMLMap SBMLid="T2R_Cave" COPASIkey="Metabolite_61"/>
    <SBMLMap SBMLid="T2R_EE" COPASIkey="Metabolite_111"/>
    <SBMLMap SBMLid="T2R_Surf" COPASIkey="Metabolite_77"/>
    <SBMLMap SBMLid="TGF_beta" COPASIkey="Metabolite_151"/>
    <SBMLMap SBMLid="Total_Smad2c" COPASIkey="ModelValue_47"/>
    <SBMLMap SBMLid="Total_Smad2n" COPASIkey="ModelValue_46"/>
    <SBMLMap SBMLid="V_cyt" COPASIkey="Compartment_23"/>
    <SBMLMap SBMLid="V_medium" COPASIkey="Compartment_15"/>
    <SBMLMap SBMLid="V_nuc" COPASIkey="Compartment_21"/>
    <SBMLMap SBMLid="k_LRC" COPASIkey="ModelValue_35"/>
    <SBMLMap SBMLid="k_Smads_Complex_c" COPASIkey="ModelValue_43"/>
    <SBMLMap SBMLid="ki_Cave" COPASIkey="ModelValue_32"/>
    <SBMLMap SBMLid="ki_EE" COPASIkey="ModelValue_30"/>
    <SBMLMap SBMLid="kr_Cave" COPASIkey="ModelValue_33"/>
    <SBMLMap SBMLid="kr_EE" COPASIkey="ModelValue_31"/>
    <SBMLMap SBMLid="v_T1R" COPASIkey="ModelValue_28"/>
    <SBMLMap SBMLid="v_T2R" COPASIkey="ModelValue_29"/>
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
</COPASI>"""

    @property
    def smad7_not_reproduced_alternative(self):
        """

        :return:
        """
        return """<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-10-11 14:58:33 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="19" versionDevel="140" copasiSourcesModified="0">
  <ListOfFunctions>
    <Function key="Function_6" name="Constant flux (irreversible)" type="PreDefined" reversible="false">
      <Expression>
        v
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_49" name="v" order="0" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_13" name="Mass action (irreversible)" type="MassAction" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <rdf:Description rdf:about="#Function_13">
   <CopasiMT:is rdf:resource="urn:miriam:obo.sbo:SBO:0000041" />
   </rdf:Description>
   </rdf:RDF>
      </MiriamAnnotation>
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
<b>Mass action rate law for first order irreversible reactions</b>
<p>
Reaction scheme where the products are created from the reactants and the change of a product quantity is proportional to the product of reactant activities. The reaction scheme does not include any reverse process that creates the reactants from the products. The change of a product quantity is proportional to the quantity of one reactant.
</p>
</body>
      </Comment>
      <Expression>
        k1*PRODUCT&lt;substrate_i>
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_81" name="k1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_79" name="substrate" order="1" role="substrate"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_40" name="Function for R1_Smad2_import" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_40">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:07:29Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
      </MiriamAnnotation>
      <Expression>
        V_cyt*Kimp_Smad2c*Smad2c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_254" name="Kimp_Smad2c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_258" name="Smad2c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_264" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_41" name="Function for R2_Smad2_export" type="UserDefined" reversible="false">
      <Expression>
        V_nuc*Kexp_Smad2n*Smad2n
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_262" name="Kexp_Smad2n" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_267" name="Smad2n" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_265" name="V_nuc" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_42" name="Function for R3_Smad4_import" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*Kimp_Smad4c*Smad4c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_246" name="Kimp_Smad4c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_270" name="Smad4c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_268" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_43" name="Function for R4_Smad4_export" type="UserDefined" reversible="false">
      <Expression>
        V_nuc*Kexp_Smad4n*Smad4n
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_266" name="Kexp_Smad4n" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_273" name="Smad4n" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_271" name="V_nuc" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="Function for R15_T2R_EE_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_EE*T2R_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_276" name="T2R_EE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_274" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_269" name="kr_EE" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="Function for R17_LRC_formation" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_45">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:42:20Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        V_cyt*k_LRC*TGF_beta*T2R_Surf*T1R_Surf
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_283" name="T1R_Surf" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_281" name="T2R_Surf" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_279" name="TGF_beta" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_277" name="V_cyt" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_272" name="k_LRC" order="4" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_46" name="Function for R19_LRC_Cave_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_Cave*LRC_Cave
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_275" name="LRC_Cave" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_284" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_280" name="kr_Cave" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="Function for R21_LRC_EE_recycling" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*kr_EE*LRC_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_287" name="LRC_EE" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_285" name="V_cyt" order="1" role="volume"/>
        <ParameterDescription key="FunctionParameter_282" name="kr_EE" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="Function for R23_Smads_Complex_formation" type="UserDefined" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_48">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-22T12:24:54Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
      </MiriamAnnotation>
      <Expression>
        k_Smads_Complex_c*Smad2c*Smad4c*LRC_EE
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_292" name="LRC_EE" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_278" name="Smad2c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_290" name="Smad4c" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_288" name="k_Smads_Complex_c" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="Function for R24_Smads_Complex_import" type="UserDefined" reversible="false">
      <Expression>
        V_cyt*Kimp_Smads_Complex_c*Smads_Complex_c
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_289" name="Kimp_Smads_Complex_c" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_294" name="Smads_Complex_c" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_293" name="V_cyt" order="2" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_50" name="k*A/I" type="UserDefined" reversible="unspecified">
      <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Function_50">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:42:22Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

      </MiriamAnnotation>
      <Expression>
        k*(A/I)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_373" name="k" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_383" name="A" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_386" name="I" order="2" role="modifier"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_11" name="Zi2007_TGFbeta_signaling" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="nmol" type="deterministic" avogadroConstant="6.022140857e+23">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_11">
    <bqbiol:hasTaxon>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/taxonomy/131567"/>
      </rdf:Bag>
    </bqbiol:hasTaxon>
    <dcterms:bibliographicCitation>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <CopasiMT:isDescribedBy rdf:resource="http://identifiers.org/pubmed/17895977"/>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:bibliographicCitation>
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2008-02-14T09:21:13Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <dcterms:creator>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Yang</vCard:Family>
                <vCard:Given>Kun</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Beijing National Laboratory for Molecular Sciences</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>klipp@molgen.mpg.de</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Klipp</vCard:Family>
                <vCard:Given>Edda</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Max Planck Institute for molecular genetics</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>hdharuri@cds.caltech.edu</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Dharuri</vCard:Family>
                <vCard:Given>Harish</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>California Institute of Technology</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:creator>
    <dcterms:modified>
      <rdf:Description>
        <dcterms:W3CDTF>2012-07-05T16:45:46Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:modified>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/MODEL3388742457"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/BIOMD0000000163"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isPartOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/kegg.pathway/hsa04350"/>
      </rdf:Bag>
    </CopasiMT:isPartOf>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      <body xmlns="http://www.w3.org/1999/xhtml">
    <p>The model reproduces the time profiles of Total Smad2 in the nucleus as well as the cytoplasm as depicted in 2D and also the other time profiles as depicted in Fig 2.  Two parameters that are not present in the paper are introduced here for illustration purposes and they are Total Smad2n and Total Smad2c. The term kr_EE*LRC_EE has not been included in the ODE's for T1R_surf, T2R_surf and TGFbeta in the paper but is included in this model. MathSBML was used to reproduce the simulation result.</p>
    <br />
    <p>To the extent possible under law, all copyright and related or neighbouring rights to this encoded model have been dedicated to the public domain worldwide. Please refer to      <a href="http://creativecommons.org/publicdomain/zero/1.0/" title="Creative Commons CC0">CC0 Public Domain Dedication</a>
          for more information.      </p>
  <p>In summary, you are entitled to use this encoded model in absolutely any manner you deem suitable, verbatim, or with modification, alone or embedded it in a larger context, redistribute it, commercially or not, in a restricted way or not.</p>
  <br />
  <p>To cite BioModels Database, please use:      <a href="http://www.ncbi.nlm.nih.gov/pubmed/20587024" target="_blank">Li C, Donizelli M, Rodriguez N, Dharuri H, Endler L, Chelliah V, Li L, He E, Henry A, Stefan MI, Snoep JL, Hucka M, Le Novère N, Laibe C (2010) BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models. BMC Syst Biol., 4:92.</a>
</p>
</body>
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_21" name="Medium" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_21">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005576" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_27" name="Nucleus" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_27">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_29" name="Cytoplasm" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_29">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005737" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_157" name="Smad3c" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_157">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_153" name="Smad3n" simulationType="reactions" compartment="Compartment_27">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_153">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_145" name="Smad4c" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_145">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_141" name="Smad4n" simulationType="reactions" compartment="Compartment_27">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_141">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_61" name="T1R_Surf" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_61">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_57" name="T1R_Cave" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_57">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_47" name="T1R_EE" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_47">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_117" name="T2R_Surf" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_117">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_101" name="T2R_Cave" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_101">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_151" name="T2R_EE" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_151">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_181" name="LRC_Surf" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_181">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_183" name="LRC_Cave" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_183">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_185" name="LRC_EE" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_185">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_187" name="Smads_Complex_c" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_187">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_189" name="Smads_Complex_n" simulationType="reactions" compartment="Compartment_27">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_189">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_191" name="TGF_beta" simulationType="reactions" compartment="Compartment_21">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_191">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_193" name="Smad7" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_193">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:03:36Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_195" name="Ski" simulationType="reactions" compartment="Compartment_29">
      </Metabolite>
      <Metabolite key="Metabolite_197" name="Smad7_mRNA" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_197">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:06:01Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_199" name="Ski_mRNA" simulationType="reactions" compartment="Compartment_29">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_199">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T18:06:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <InitialExpression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial],Reference=InitialValue>
        </InitialExpression>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_55" name="v_T1R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_54" name="v_T2R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_53" name="ki_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_52" name="kr_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_51" name="ki_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_50" name="kr_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_49" name="Kcd" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_48" name="k_LRC" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_47" name="Klid" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_46" name="Kdeg_T1R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_45" name="Kdeg_T2R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_44" name="Kimp_Smad2c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_43" name="Kexp_Smad2n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_42" name="Kimp_Smad4c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_41" name="Kexp_Smad4n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_40" name="k_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_39" name="Kimp_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_38" name="Kdiss_Smads_Complex_n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_37" name="Total_Smad2n" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_36" name="Total_Smad2c" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_35" name="SkiObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_35">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:11:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski_mRNA],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_34" name="Smad7Obs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_34">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:13Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_33" name="SkiSF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_33">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_32" name="Smad7SF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_32">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:45Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_31" name="Smad7mRNAObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_31">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:12:28Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7_mRNA],Reference=Concentration>/&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=Value>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_30" name="Smad7mRNAInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_29" name="SkiInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_28" name="Smad7ProteinInitial" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_67" name="R1_Smad2_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_67">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:41:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_157" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_153" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3854" name="Kimp_Smad2c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_40" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="ModelValue_44"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_157"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Compartment_29"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_66" name="R2_Smad2_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_66">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006886" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_153" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_157" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3855" name="Kexp_Smad2n" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_41" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="ModelValue_43"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_153"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Compartment_27"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_65" name="R3_Smad4_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_65">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:52Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_145" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_141" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4108" name="Kimp_Smad4c" value="0.08"/>
        </ListOfConstants>
        <KineticLaw function="Function_42" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="ModelValue_42"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Metabolite_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Compartment_29"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_64" name="R4_Smad4_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_64">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:56Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006886" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_141" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_145" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4107" name="Kexp_Smad4n" value="0.5"/>
        </ListOfConstants>
        <KineticLaw function="Function_43" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="ModelValue_41"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_141"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Compartment_27"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_63" name="R5_T1R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_63">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:47:37Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032905" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4106" name="v" value="0.0103"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_55"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_62" name="R6_T1R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_62">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4105" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_61"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_61" name="R7_T1R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_61">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-22T12:31:08Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_57" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4104" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_50"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_57"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_60" name="R8_T1R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_60">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4103" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_61"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_59" name="R9_T1R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_59">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4102" name="k1" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_52"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_58" name="R10_T1R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_58">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:49:31Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_47" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4101" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_46"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_47"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_57" name="R11_T2R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_57">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T10:51:21Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032906" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfProducts>
          <Product metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4100" name="v" value="0.02869"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_54"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_56" name="R12_T2R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_56">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_101" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4099" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_117"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_55" name="R13_T2R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_55">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_101" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4098" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_50"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_101"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_54" name="R14_T2R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_54">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_151" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4097" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_117"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_53" name="R15_T2R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_53">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_151" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_117" stoichiometry="1"/>
          <Product metabolite="Metabolite_191" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4096" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_44" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Metabolite_151"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Compartment_29"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="ModelValue_52"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_52" name="R16_T2R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_52">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_151" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4095" name="k1" value="0.025"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_45"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_151"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_51" name="R17_LRC_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_51">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005160" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_191" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_117" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_61" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_181" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4094" name="k_LRC" value="2197"/>
        </ListOfConstants>
        <KineticLaw function="Function_45" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Metabolite_61"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_117"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_191"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Compartment_29"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="ModelValue_48"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_50" name="R18_LRC_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_50">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_181" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_183" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4093" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_51"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_181"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_49" name="R19_LRC_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_49">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_183" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_61" stoichiometry="1"/>
          <Product metabolite="Metabolite_191" stoichiometry="1"/>
          <Product metabolite="Metabolite_117" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4092" name="kr_Cave" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_46" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Metabolite_183"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Compartment_29"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="ModelValue_50"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_48" name="R20_LRC_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_48">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_181" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_185" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4091" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_53"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_181"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_47" name="R21_LRC_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_47">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_185" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_61" stoichiometry="1"/>
          <Product metabolite="Metabolite_117" stoichiometry="1"/>
          <Product metabolite="Metabolite_191" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4090" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_47" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Metabolite_185"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Compartment_29"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="ModelValue_52"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_46" name="R22_LRC_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_46">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_185" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4089" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_49"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_185"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_45" name="R23_Smads_Complex_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_45">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-08-17T14:06:11Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_157" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_145" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_187" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_185" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4088" name="k_Smads_Complex_c" value="6.85e-05"/>
        </ListOfConstants>
        <KineticLaw function="Function_48" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Metabolite_185"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Metabolite_157"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Metabolite_145"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="ModelValue_40"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_44" name="R24_Smads_Complex_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_44">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_187" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_189" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4087" name="Kimp_Smads_Complex_c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_49" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="ModelValue_39"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Metabolite_187"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Compartment_29"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_43" name="R25_Smads_Complex_Dissociation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_189" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_141" stoichiometry="1"/>
          <Product metabolite="Metabolite_153" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4086" name="k1" value="0.1174"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_38"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_189"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_42" name="Smad7Transcription" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_42">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-11T15:58:24Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_189" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_189" stoichiometry="1"/>
          <Product metabolite="Metabolite_197" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_195" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4161" name="k" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_50" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_373">
              <SourceParameter reference="Parameter_4161"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_383">
              <SourceParameter reference="Metabolite_189"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_386">
              <SourceParameter reference="Metabolite_195"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_41" name="SkiTranscription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_189" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_189" stoichiometry="1"/>
          <Product metabolite="Metabolite_199" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4084" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4084"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_189"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_40" name="Smad7mRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_197" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4083" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4083"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_197"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_39" name="SkimRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_199" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4082" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4082"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_199"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_38" name="Smad7Translation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_197" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_197" stoichiometry="1"/>
          <Product metabolite="Metabolite_193" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4081" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4081"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_197"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_37" name="SkiTranslation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_199" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_199" stoichiometry="1"/>
          <Product metabolite="Metabolite_195" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4080" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4080"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_199"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_36" name="SkiDeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_195" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4079" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4079"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_195"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_35" name="Smad7Feedback" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_193" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_183" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4078" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4078"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_193"/>
              <SourceParameter reference="Metabolite_183"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_1">
      <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
        <ModelParameterGroup cn="String=Initial Time" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling" value="0" type="Model" simulationType="time"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium]" value="1" type="Compartment" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]" value="0.00035" type="Compartment" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]" value="0.00105" type="Compartment" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Species Values" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c]" value="311489514795000" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n]" value="49837732197299.99" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c]" value="726794113608999.8" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n]" value="116288744377000" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf]" value="149860975226" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave]" value="1322823460650" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE]" value="1302589067370" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf]" value="127729607577" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave]" value="1124273476590" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE]" value="725908858903.0001" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n]" value="0" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta]" value="48177126855999.98" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7]" value="463707204823.9352" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski]" value="6323247899850" type="Species" simulationType="reactions"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7_mRNA]" value="6182762730.987911" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Ski_mRNA]" value="41388964352.41602" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF],Reference=InitialValue>*&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial],Reference=InitialValue>
            </InitialExpression>
          </ModelParameter>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R]" value="0.0103" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R]" value="0.02869" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE]" value="0.33" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE]" value="0.033" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave]" value="0.33" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave]" value="0.03742" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd]" value="0.005" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC]" value="2197" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid]" value="0.02609" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE]" value="0.005" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE]" value="0.025" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c]" value="0.16" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c]" value="0.08" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n]" value="0.5" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c]" value="6.85e-05" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c]" value="0.16" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n]" value="0.1174" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n]" value="236.4499999999157" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c]" value="492.6100000007736" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiObs]" value="0.0654552296667" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7Obs]" value="0.73333706375" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiSF]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7SF]" value="1" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAObs]" value="0.00977782751667" type="ModelValue" simulationType="assignment"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7mRNAInitial]" value="0.00977782751667" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[SkiInitial]" value="0.0654552296667" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Smad7ProteinInitial]" value="0.73333706375" type="ModelValue" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R1_Smad2_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R1_Smad2_import],ParameterGroup=Parameters,Parameter=Kimp_Smad2c" value="0.16" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R2_Smad2_export]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R2_Smad2_export],ParameterGroup=Parameters,Parameter=Kexp_Smad2n" value="1" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R3_Smad4_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R3_Smad4_import],ParameterGroup=Parameters,Parameter=Kimp_Smad4c" value="0.08" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R4_Smad4_export]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R4_Smad4_export],ParameterGroup=Parameters,Parameter=Kexp_Smad4n" value="0.5" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R5_T1R_production]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R5_T1R_production],ParameterGroup=Parameters,Parameter=v" value="0.0103" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R6_T1R_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R6_T1R_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R7_T1R_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R7_T1R_Cave_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R8_T1R_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R8_T1R_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R9_T1R_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R9_T1R_EE_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R10_T1R_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R10_T1R_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.005" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R11_T2R_production]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R11_T2R_production],ParameterGroup=Parameters,Parameter=v" value="0.02869" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R12_T2R_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R12_T2R_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R13_T2R_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R13_T2R_Cave_recycling],ParameterGroup=Parameters,Parameter=k1" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R14_T2R_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R14_T2R_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R15_T2R_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R15_T2R_EE_recycling],ParameterGroup=Parameters,Parameter=kr_EE" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R16_T2R_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R16_T2R_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.025" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R17_LRC_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R17_LRC_formation],ParameterGroup=Parameters,Parameter=k_LRC" value="2197" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R18_LRC_Cave_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R18_LRC_Cave_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R19_LRC_Cave_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R19_LRC_Cave_recycling],ParameterGroup=Parameters,Parameter=kr_Cave" value="0.03742" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R20_LRC_EE_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R20_LRC_EE_formation],ParameterGroup=Parameters,Parameter=k1" value="0.33" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R21_LRC_EE_recycling]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R21_LRC_EE_recycling],ParameterGroup=Parameters,Parameter=kr_EE" value="0.033" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R22_LRC_EE_degradation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R22_LRC_EE_degradation],ParameterGroup=Parameters,Parameter=k1" value="0.005" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R23_Smads_Complex_formation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R23_Smads_Complex_formation],ParameterGroup=Parameters,Parameter=k_Smads_Complex_c" value="6.85e-05" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R24_Smads_Complex_import]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R24_Smads_Complex_import],ParameterGroup=Parameters,Parameter=Kimp_Smads_Complex_c" value="0.16" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R25_Smads_Complex_Dissociation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[R25_Smads_Complex_Dissociation],ParameterGroup=Parameters,Parameter=k1" value="0.1174" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n],Reference=InitialValue>
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Transcription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Transcription],ParameterGroup=Parameters,Parameter=k" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranscription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranscription],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7mRNADeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7mRNADeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkimRNADeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkimRNADeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Translation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Translation],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranslation]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiTranslation],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiDeg]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[SkiDeg],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Feedback]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Feedback],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
          </ModelParameterGroup>
        </ModelParameterGroup>
      </ModelParameterSet>
    </ListOfModelParameterSets>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_11"/>
      <StateTemplateVariable objectReference="Metabolite_61"/>
      <StateTemplateVariable objectReference="Metabolite_117"/>
      <StateTemplateVariable objectReference="Metabolite_141"/>
      <StateTemplateVariable objectReference="Metabolite_157"/>
      <StateTemplateVariable objectReference="Metabolite_181"/>
      <StateTemplateVariable objectReference="Metabolite_47"/>
      <StateTemplateVariable objectReference="Metabolite_151"/>
      <StateTemplateVariable objectReference="Metabolite_183"/>
      <StateTemplateVariable objectReference="Metabolite_185"/>
      <StateTemplateVariable objectReference="Metabolite_195"/>
      <StateTemplateVariable objectReference="Metabolite_197"/>
      <StateTemplateVariable objectReference="Metabolite_199"/>
      <StateTemplateVariable objectReference="Metabolite_189"/>
      <StateTemplateVariable objectReference="Metabolite_193"/>
      <StateTemplateVariable objectReference="Metabolite_191"/>
      <StateTemplateVariable objectReference="Metabolite_187"/>
      <StateTemplateVariable objectReference="Metabolite_57"/>
      <StateTemplateVariable objectReference="Metabolite_101"/>
      <StateTemplateVariable objectReference="Metabolite_153"/>
      <StateTemplateVariable objectReference="Metabolite_145"/>
      <StateTemplateVariable objectReference="ModelValue_37"/>
      <StateTemplateVariable objectReference="ModelValue_36"/>
      <StateTemplateVariable objectReference="ModelValue_35"/>
      <StateTemplateVariable objectReference="ModelValue_34"/>
      <StateTemplateVariable objectReference="ModelValue_31"/>
      <StateTemplateVariable objectReference="Compartment_21"/>
      <StateTemplateVariable objectReference="Compartment_27"/>
      <StateTemplateVariable objectReference="Compartment_29"/>
      <StateTemplateVariable objectReference="ModelValue_55"/>
      <StateTemplateVariable objectReference="ModelValue_54"/>
      <StateTemplateVariable objectReference="ModelValue_53"/>
      <StateTemplateVariable objectReference="ModelValue_52"/>
      <StateTemplateVariable objectReference="ModelValue_51"/>
      <StateTemplateVariable objectReference="ModelValue_50"/>
      <StateTemplateVariable objectReference="ModelValue_49"/>
      <StateTemplateVariable objectReference="ModelValue_48"/>
      <StateTemplateVariable objectReference="ModelValue_47"/>
      <StateTemplateVariable objectReference="ModelValue_46"/>
      <StateTemplateVariable objectReference="ModelValue_45"/>
      <StateTemplateVariable objectReference="ModelValue_44"/>
      <StateTemplateVariable objectReference="ModelValue_43"/>
      <StateTemplateVariable objectReference="ModelValue_42"/>
      <StateTemplateVariable objectReference="ModelValue_41"/>
      <StateTemplateVariable objectReference="ModelValue_40"/>
      <StateTemplateVariable objectReference="ModelValue_39"/>
      <StateTemplateVariable objectReference="ModelValue_38"/>
      <StateTemplateVariable objectReference="ModelValue_33"/>
      <StateTemplateVariable objectReference="ModelValue_32"/>
      <StateTemplateVariable objectReference="ModelValue_30"/>
      <StateTemplateVariable objectReference="ModelValue_29"/>
      <StateTemplateVariable objectReference="ModelValue_28"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 149860975226 127729607577 116288744377000 311489514795000 0 1302589067370 725908858903.0001 0 0 6323247899850 6182762730.987911 41388964352.41602 0 463707204823.9352 48177126855999.98 0 1322823460650 1124273476590 49837732197299.99 726794113608999.8 236.4499999999157 492.6100000007736 0.0654552296667 0.73333706375 0.00977782751667 1 0.00035 0.00105 0.0103 0.02869 0.33 0.033 0.33 0.03742 0.005 2197 0.02609 0.005 0.025 0.16 1 0.08 0.5 6.85e-05 0.16 0.1174 1 1 0.00977782751667 0.0654552296667 0.73333706375 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_26" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_21" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_16" target="../../Models/2017/09_Sept/zi_timecourse_simulation.csv" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="AutomaticStepSize" type="bool" value="0"/>
        <Parameter name="StepNumber" type="unsignedInteger" value="1000"/>
        <Parameter name="StepSize" type="float" value="1"/>
        <Parameter name="Duration" type="float" value="1000"/>
        <Parameter name="TimeSeriesRequested" type="float" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Start in Steady State" type="bool" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
        <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
      </Method>
    </Task>
    <Task key="Task_16" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report reference="Report_17" target="zi_repeat.csv" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="1"/>
        <ParameterGroup name="ScanItems">
          <ParameterGroup name="ScanItem">
            <Parameter name="Number of steps" type="unsignedInteger" value="10"/>
            <Parameter name="Object" type="cn" value="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=InitialConcentration"/>
            <Parameter name="Type" type="unsignedInteger" value="0"/>
          </ParameterGroup>
        </ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="0"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_17" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_20" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_18" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_9" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_10" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
        </ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
        </ParameterGroup>
      </Problem>
      <Method name="Evolutionary Programming" type="EvolutionaryProgram">
        <Parameter name="Number of Generations" type="unsignedInteger" value="200"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_11" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_26"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Use Reder" type="bool" value="1"/>
        <Parameter name="Use Smallbone" type="bool" value="1"/>
      </Method>
    </Task>
    <Task key="Task_21" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_12" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
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
      <Report reference="Report_14" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_27" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_15" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_26"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_21" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_20" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_9" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_10" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_11" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_12" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_13" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_14" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_15" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_16" name="Time-Course" taskType="unset" separator="&#x09;" precision="6">
      <Comment>
      </Comment>
      <Table printTitle="1">
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad2n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T1R_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Klid],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T2R],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[v_T1R],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_LRC],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kcd],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[kr_Cave],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[ki_Cave],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kexp_Smad4n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdiss_Smads_Complex_n],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad2c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smads_Complex_c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kimp_Smad4c],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Kdeg_T2R_EE],Reference=Value"/>
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[k_Smads_Complex_c],Reference=Value"/>
      </Table>
    </Report>
    <Report key="Report_17" name="profilelikelihood" taskType="unset" separator="&#x09;" precision="6">
      <Comment>
      </Comment>
      <Table printTitle="1">
        <Object cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Metabolites[Smad3n],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
      </Table>
    </Report>
  </ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[Smad3c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad3n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad4c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad4n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad4n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T1R_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T1R_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[T2R_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[T2R_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_Surf]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Surf],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_Cave]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_Cave],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[LRC_EE]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[LRC_EE],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smads_Complex_c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smads_Complex_n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[TGF_beta]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[Smad7]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad7],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Total_Smad2n]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[Total_Smad2c]" type="Curve2D">
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2c],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <SBMLReference file="Zi2012.xml">
    <SBMLMap SBMLid="Kcd" COPASIkey="ModelValue_49"/>
    <SBMLMap SBMLid="Kdeg_T1R_EE" COPASIkey="ModelValue_46"/>
    <SBMLMap SBMLid="Kdeg_T2R_EE" COPASIkey="ModelValue_45"/>
    <SBMLMap SBMLid="Kdiss_Smads_Complex_n" COPASIkey="ModelValue_38"/>
    <SBMLMap SBMLid="Kexp_Smad2n" COPASIkey="ModelValue_43"/>
    <SBMLMap SBMLid="Kexp_Smad4n" COPASIkey="ModelValue_41"/>
    <SBMLMap SBMLid="Kimp_Smad2c" COPASIkey="ModelValue_44"/>
    <SBMLMap SBMLid="Kimp_Smad4c" COPASIkey="ModelValue_42"/>
    <SBMLMap SBMLid="Kimp_Smads_Complex_c" COPASIkey="ModelValue_39"/>
    <SBMLMap SBMLid="Klid" COPASIkey="ModelValue_47"/>
    <SBMLMap SBMLid="LRC_Cave" COPASIkey="Metabolite_183"/>
    <SBMLMap SBMLid="LRC_EE" COPASIkey="Metabolite_185"/>
    <SBMLMap SBMLid="LRC_Surf" COPASIkey="Metabolite_181"/>
    <SBMLMap SBMLid="R10_T1R_EE_degradation" COPASIkey="Reaction_58"/>
    <SBMLMap SBMLid="R11_T2R_production" COPASIkey="Reaction_57"/>
    <SBMLMap SBMLid="R12_T2R_Cave_formation" COPASIkey="Reaction_56"/>
    <SBMLMap SBMLid="R13_T2R_Cave_recycling" COPASIkey="Reaction_55"/>
    <SBMLMap SBMLid="R14_T2R_EE_formation" COPASIkey="Reaction_54"/>
    <SBMLMap SBMLid="R15_T2R_EE_recycling" COPASIkey="Reaction_53"/>
    <SBMLMap SBMLid="R16_T2R_EE_degradation" COPASIkey="Reaction_52"/>
    <SBMLMap SBMLid="R17_LRC_formation" COPASIkey="Reaction_51"/>
    <SBMLMap SBMLid="R18_LRC_Cave_formation" COPASIkey="Reaction_50"/>
    <SBMLMap SBMLid="R19_LRC_Cave_recycling" COPASIkey="Reaction_49"/>
    <SBMLMap SBMLid="R1_Smad2_import" COPASIkey="Reaction_67"/>
    <SBMLMap SBMLid="R20_LRC_EE_formation" COPASIkey="Reaction_48"/>
    <SBMLMap SBMLid="R21_LRC_EE_recycling" COPASIkey="Reaction_47"/>
    <SBMLMap SBMLid="R22_LRC_EE_degradation" COPASIkey="Reaction_46"/>
    <SBMLMap SBMLid="R23_Smads_Complex_formation" COPASIkey="Reaction_45"/>
    <SBMLMap SBMLid="R24_Smads_Complex_import" COPASIkey="Reaction_44"/>
    <SBMLMap SBMLid="R25_Smads_Complex_Dissociation" COPASIkey="Reaction_43"/>
    <SBMLMap SBMLid="R2_Smad2_export" COPASIkey="Reaction_66"/>
    <SBMLMap SBMLid="R3_Smad4_import" COPASIkey="Reaction_65"/>
    <SBMLMap SBMLid="R4_Smad4_export" COPASIkey="Reaction_64"/>
    <SBMLMap SBMLid="R5_T1R_production" COPASIkey="Reaction_63"/>
    <SBMLMap SBMLid="R6_T1R_Cave_formation" COPASIkey="Reaction_62"/>
    <SBMLMap SBMLid="R7_T1R_Cave_recycling" COPASIkey="Reaction_61"/>
    <SBMLMap SBMLid="R8_T1R_EE_formation" COPASIkey="Reaction_60"/>
    <SBMLMap SBMLid="R9_T1R_EE_recycling" COPASIkey="Reaction_59"/>
    <SBMLMap SBMLid="Smad2c" COPASIkey="Metabolite_157"/>
    <SBMLMap SBMLid="Smad2n" COPASIkey="Metabolite_153"/>
    <SBMLMap SBMLid="Smad4c" COPASIkey="Metabolite_145"/>
    <SBMLMap SBMLid="Smad4n" COPASIkey="Metabolite_141"/>
    <SBMLMap SBMLid="Smads_Complex_c" COPASIkey="Metabolite_187"/>
    <SBMLMap SBMLid="Smads_Complex_n" COPASIkey="Metabolite_189"/>
    <SBMLMap SBMLid="T1R_Cave" COPASIkey="Metabolite_57"/>
    <SBMLMap SBMLid="T1R_EE" COPASIkey="Metabolite_47"/>
    <SBMLMap SBMLid="T1R_Surf" COPASIkey="Metabolite_61"/>
    <SBMLMap SBMLid="T2R_Cave" COPASIkey="Metabolite_101"/>
    <SBMLMap SBMLid="T2R_EE" COPASIkey="Metabolite_151"/>
    <SBMLMap SBMLid="T2R_Surf" COPASIkey="Metabolite_117"/>
    <SBMLMap SBMLid="TGF_beta" COPASIkey="Metabolite_191"/>
    <SBMLMap SBMLid="Total_Smad2c" COPASIkey="ModelValue_36"/>
    <SBMLMap SBMLid="Total_Smad2n" COPASIkey="ModelValue_37"/>
    <SBMLMap SBMLid="V_cyt" COPASIkey="Compartment_29"/>
    <SBMLMap SBMLid="V_medium" COPASIkey="Compartment_21"/>
    <SBMLMap SBMLid="V_nuc" COPASIkey="Compartment_27"/>
    <SBMLMap SBMLid="k_LRC" COPASIkey="ModelValue_48"/>
    <SBMLMap SBMLid="k_Smads_Complex_c" COPASIkey="ModelValue_40"/>
    <SBMLMap SBMLid="ki_Cave" COPASIkey="ModelValue_51"/>
    <SBMLMap SBMLid="ki_EE" COPASIkey="ModelValue_53"/>
    <SBMLMap SBMLid="kr_Cave" COPASIkey="ModelValue_50"/>
    <SBMLMap SBMLid="kr_EE" COPASIkey="ModelValue_52"/>
    <SBMLMap SBMLid="v_T1R" COPASIkey="ModelValue_55"/>
    <SBMLMap SBMLid="v_T2R" COPASIkey="ModelValue_54"/>
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
</COPASI>"""
