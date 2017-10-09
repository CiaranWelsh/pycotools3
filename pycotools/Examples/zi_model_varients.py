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
<!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-10-09 14:30:25 UTC -->
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
  </ListOfFunctions>
  <Model key="Model_10" name="Zi2007_TGFbeta_signaling" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="nmol" type="deterministic" avogadroConstant="6.022140857e+23">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_10">
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
      <Compartment key="Compartment_18" name="Medium" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_18">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005576" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_24" name="Nucleus" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_24">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_26" name="Cytoplasm" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_26">
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
      <Metabolite key="Metabolite_137" name="Smad3c" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_137">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_133" name="Smad3n" simulationType="reactions" compartment="Compartment_24">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_133">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_125" name="Smad4c" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_125">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_121" name="Smad4n" simulationType="reactions" compartment="Compartment_24">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_121">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_21" name="T1R_Surf" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_21">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_17" name="T1R_Cave" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_17">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_7" name="T1R_EE" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_7">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_97" name="T2R_Surf" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_97">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_81" name="T2R_Cave" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_81">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_131" name="T2R_EE" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_131">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_161" name="LRC_Surf" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_161">
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
      <Metabolite key="Metabolite_163" name="LRC_Cave" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_163">
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
      <Metabolite key="Metabolite_165" name="LRC_EE" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_165">
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
      <Metabolite key="Metabolite_167" name="Smads_Complex_c" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_167">
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
      <Metabolite key="Metabolite_169" name="Smads_Complex_n" simulationType="reactions" compartment="Compartment_24">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_169">
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
      <Metabolite key="Metabolite_171" name="TGF_beta" simulationType="reactions" compartment="Compartment_18">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_171">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_173" name="Smad7" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_173">
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
      <Metabolite key="Metabolite_175" name="Ski" simulationType="reactions" compartment="Compartment_26">
      </Metabolite>
      <Metabolite key="Metabolite_177" name="Smad7_mRNA" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_177">
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
      <Metabolite key="Metabolite_179" name="Ski_mRNA" simulationType="reactions" compartment="Compartment_26">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_179">
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
      <ModelValue key="ModelValue_27" name="v_T1R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_26" name="v_T2R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_25" name="ki_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_24" name="kr_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_23" name="ki_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_22" name="kr_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_21" name="Kcd" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_20" name="k_LRC" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_19" name="Klid" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_18" name="Kdeg_T1R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_17" name="Kdeg_T2R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_16" name="Kimp_Smad2c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_15" name="Kexp_Smad2n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_14" name="Kimp_Smad4c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_13" name="Kexp_Smad4n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_12" name="k_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_11" name="Kimp_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_10" name="Kdiss_Smads_Complex_n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_9" name="Total_Smad2n" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_8" name="Total_Smad2c" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_7" name="SkiObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_7">
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
      <ModelValue key="ModelValue_6" name="Smad7Obs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_6">
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
      <ModelValue key="ModelValue_5" name="SkiSF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_5">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_4" name="Smad7SF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_4">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:45Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_3" name="Smad7mRNAObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_3">
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
      <ModelValue key="ModelValue_2" name="Smad7mRNAInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_1" name="SkiInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_0" name="Smad7ProteinInitial" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_33" name="R1_Smad2_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_33">
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
          <Substrate metabolite="Metabolite_137" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_133" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4006" name="Kimp_Smad2c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_40" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="ModelValue_16"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_137"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Compartment_26"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_32" name="R2_Smad2_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_32">
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
          <Substrate metabolite="Metabolite_133" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_137" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4007" name="Kexp_Smad2n" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_41" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="ModelValue_15"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_133"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Compartment_24"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_31" name="R3_Smad4_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_31">
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
          <Substrate metabolite="Metabolite_125" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_121" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4257" name="Kimp_Smad4c" value="0.08"/>
        </ListOfConstants>
        <KineticLaw function="Function_42" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="ModelValue_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Metabolite_125"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Compartment_26"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_30" name="R4_Smad4_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_30">
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
          <Substrate metabolite="Metabolite_121" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_125" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4256" name="Kexp_Smad4n" value="0.5"/>
        </ListOfConstants>
        <KineticLaw function="Function_43" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="ModelValue_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_121"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Compartment_24"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_29" name="R5_T1R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_29">
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
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4255" name="v" value="0.0103"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_27"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_28" name="R6_T1R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_28">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4384" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_27" name="R7_T1R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_27">
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
          <Substrate metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4383" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_22"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_17"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_26" name="R8_T1R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_26">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4382" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_25" name="R9_T1R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_25">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4381" name="k1" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_24"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_24" name="R10_T1R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_24">
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
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4380" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_18"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_23" name="R11_T2R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_23">
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
          <Product metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4379" name="v" value="0.02869"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_26"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_22" name="R12_T2R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_22">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_81" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4378" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_97"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_21" name="R13_T2R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_21">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_81" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4377" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_22"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_81"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_20" name="R14_T2R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_20">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_131" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4376" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_97"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_19" name="R15_T2R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_19">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_131" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_97" stoichiometry="1"/>
          <Product metabolite="Metabolite_171" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4375" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_44" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Metabolite_131"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Compartment_26"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="ModelValue_24"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_18" name="R16_T2R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_18">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_131" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4374" name="k1" value="0.025"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_131"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_17" name="R17_LRC_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_17">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005160" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_171" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_97" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_161" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4373" name="k_LRC" value="2197"/>
        </ListOfConstants>
        <KineticLaw function="Function_45" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_97"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_171"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Compartment_26"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="ModelValue_20"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_16" name="R18_LRC_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_16">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_161" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_163" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4372" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_161"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_15" name="R19_LRC_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_15">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_163" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
          <Product metabolite="Metabolite_171" stoichiometry="1"/>
          <Product metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4371" name="kr_Cave" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_46" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Metabolite_163"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Compartment_26"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="ModelValue_22"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_14" name="R20_LRC_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_14">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_161" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_165" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4370" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_161"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_13" name="R21_LRC_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_13">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_165" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
          <Product metabolite="Metabolite_97" stoichiometry="1"/>
          <Product metabolite="Metabolite_171" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4369" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_47" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Metabolite_165"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Compartment_26"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="ModelValue_24"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_12" name="R22_LRC_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_12">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_165" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4368" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_165"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_11" name="R23_Smads_Complex_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_11">
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
          <Substrate metabolite="Metabolite_137" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_125" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_167" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_165" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4367" name="k_Smads_Complex_c" value="6.85e-05"/>
        </ListOfConstants>
        <KineticLaw function="Function_48" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Metabolite_165"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Metabolite_137"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Metabolite_125"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="ModelValue_12"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_10" name="R24_Smads_Complex_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_10">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_167" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_169" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4366" name="Kimp_Smads_Complex_c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_49" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="ModelValue_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Metabolite_167"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Compartment_26"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_9" name="R25_Smads_Complex_Dissociation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_169" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_121" stoichiometry="1"/>
          <Product metabolite="Metabolite_133" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4365" name="k1" value="0.1174"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_10"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_169"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_8" name="Smad7Trascription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_169" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_169" stoichiometry="1"/>
          <Product metabolite="Metabolite_177" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4364" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4364"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_169"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_7" name="SkiTranscription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_169" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_169" stoichiometry="1"/>
          <Product metabolite="Metabolite_179" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4363" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4363"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_169"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_6" name="Smad7mRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_177" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4362" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4362"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_177"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_5" name="SkimRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_179" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4361" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4361"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_179"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_4" name="Smad7Translation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_177" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_177" stoichiometry="1"/>
          <Product metabolite="Metabolite_173" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4360" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4360"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_177"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_3" name="SkiTranslation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_179" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_179" stoichiometry="1"/>
          <Product metabolite="Metabolite_175" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4359" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4359"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_179"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_2" name="SkiDeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_175" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4358" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4358"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_175"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1" name="Smad7Feedback" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_173" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_163" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_173" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4357" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4357"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_173"/>
              <SourceParameter reference="Metabolite_163"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_0" name="Smad7Deg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_173" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4349" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4349"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_173"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_0">
      <ModelParameterSet key="ModelParameterSet_0" name="Initial State">
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
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta]" value="48177126855999.97" type="Species" simulationType="reactions"/>
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
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Trascription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Trascription],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
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
      <StateTemplateVariable objectReference="Model_10"/>
      <StateTemplateVariable objectReference="Metabolite_21"/>
      <StateTemplateVariable objectReference="Metabolite_97"/>
      <StateTemplateVariable objectReference="Metabolite_121"/>
      <StateTemplateVariable objectReference="Metabolite_137"/>
      <StateTemplateVariable objectReference="Metabolite_161"/>
      <StateTemplateVariable objectReference="Metabolite_7"/>
      <StateTemplateVariable objectReference="Metabolite_131"/>
      <StateTemplateVariable objectReference="Metabolite_163"/>
      <StateTemplateVariable objectReference="Metabolite_165"/>
      <StateTemplateVariable objectReference="Metabolite_173"/>
      <StateTemplateVariable objectReference="Metabolite_175"/>
      <StateTemplateVariable objectReference="Metabolite_177"/>
      <StateTemplateVariable objectReference="Metabolite_179"/>
      <StateTemplateVariable objectReference="Metabolite_167"/>
      <StateTemplateVariable objectReference="Metabolite_171"/>
      <StateTemplateVariable objectReference="Metabolite_169"/>
      <StateTemplateVariable objectReference="Metabolite_17"/>
      <StateTemplateVariable objectReference="Metabolite_81"/>
      <StateTemplateVariable objectReference="Metabolite_125"/>
      <StateTemplateVariable objectReference="Metabolite_133"/>
      <StateTemplateVariable objectReference="ModelValue_9"/>
      <StateTemplateVariable objectReference="ModelValue_8"/>
      <StateTemplateVariable objectReference="ModelValue_7"/>
      <StateTemplateVariable objectReference="ModelValue_6"/>
      <StateTemplateVariable objectReference="ModelValue_3"/>
      <StateTemplateVariable objectReference="Compartment_18"/>
      <StateTemplateVariable objectReference="Compartment_24"/>
      <StateTemplateVariable objectReference="Compartment_26"/>
      <StateTemplateVariable objectReference="ModelValue_27"/>
      <StateTemplateVariable objectReference="ModelValue_26"/>
      <StateTemplateVariable objectReference="ModelValue_25"/>
      <StateTemplateVariable objectReference="ModelValue_24"/>
      <StateTemplateVariable objectReference="ModelValue_23"/>
      <StateTemplateVariable objectReference="ModelValue_22"/>
      <StateTemplateVariable objectReference="ModelValue_21"/>
      <StateTemplateVariable objectReference="ModelValue_20"/>
      <StateTemplateVariable objectReference="ModelValue_19"/>
      <StateTemplateVariable objectReference="ModelValue_18"/>
      <StateTemplateVariable objectReference="ModelValue_17"/>
      <StateTemplateVariable objectReference="ModelValue_16"/>
      <StateTemplateVariable objectReference="ModelValue_15"/>
      <StateTemplateVariable objectReference="ModelValue_14"/>
      <StateTemplateVariable objectReference="ModelValue_13"/>
      <StateTemplateVariable objectReference="ModelValue_12"/>
      <StateTemplateVariable objectReference="ModelValue_11"/>
      <StateTemplateVariable objectReference="ModelValue_10"/>
      <StateTemplateVariable objectReference="ModelValue_5"/>
      <StateTemplateVariable objectReference="ModelValue_4"/>
      <StateTemplateVariable objectReference="ModelValue_2"/>
      <StateTemplateVariable objectReference="ModelValue_1"/>
      <StateTemplateVariable objectReference="ModelValue_0"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 149860975226 127729607577 116288744377000 311489514795000 0 1302589067370 725908858903.0001 0 0 463707204823.9352 6323247899850 6182762730.987911 41388964352.41602 0 48177126855999.97 0 1322823460650 1124273476590 726794113608999.8 49837732197299.99 236.4499999999157 492.6100000007736 0.0654552296667 0.73333706375 0.00977782751667 1 0.00035 0.00105 0.0103 0.02869 0.33 0.033 0.33 0.03742 0.005 2197 0.02609 0.005 0.025 0.16 1 0.08 0.5 6.85e-05 0.16 0.1174 1 1 0.00977782751667 0.0654552296667 0.73333706375 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_12" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_19" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_1" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Report reference="Report_7" target="../../Models/2017/09_Sept/zi_timecourse_simulation.csv" append="0" confirmOverwrite="0"/>
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
    <Task key="Task_2" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report reference="Report_8" target="zi_repeat.csv" append="0" confirmOverwrite="0"/>
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
    <Task key="Task_3" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_18" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_4" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_0" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_5" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_1" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_6" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_2" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_12"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Use Reder" type="bool" value="1"/>
        <Parameter name="Use Smallbone" type="bool" value="1"/>
      </Method>
    </Task>
    <Task key="Task_7" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_3" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_8" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_4" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_9" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_5" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_10" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
    <Task key="Task_11" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
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
    <Task key="Task_13" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_6" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_12"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_19" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_18" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_0" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
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
    <Report key="Report_1" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
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
    <Report key="Report_2" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
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
    <Report key="Report_3" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
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
    <Report key="Report_4" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
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
    <Report key="Report_5" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
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
    <Report key="Report_6" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
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
    <Report key="Report_7" name="Time-Course" taskType="unset" separator="&#x09;" precision="6">
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
    <Report key="Report_8" name="profilelikelihood" taskType="unset" separator="&#x09;" precision="6">
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
    <SBMLMap SBMLid="Kcd" COPASIkey="ModelValue_21"/>
    <SBMLMap SBMLid="Kdeg_T1R_EE" COPASIkey="ModelValue_18"/>
    <SBMLMap SBMLid="Kdeg_T2R_EE" COPASIkey="ModelValue_17"/>
    <SBMLMap SBMLid="Kdiss_Smads_Complex_n" COPASIkey="ModelValue_10"/>
    <SBMLMap SBMLid="Kexp_Smad2n" COPASIkey="ModelValue_15"/>
    <SBMLMap SBMLid="Kexp_Smad4n" COPASIkey="ModelValue_13"/>
    <SBMLMap SBMLid="Kimp_Smad2c" COPASIkey="ModelValue_16"/>
    <SBMLMap SBMLid="Kimp_Smad4c" COPASIkey="ModelValue_14"/>
    <SBMLMap SBMLid="Kimp_Smads_Complex_c" COPASIkey="ModelValue_11"/>
    <SBMLMap SBMLid="Klid" COPASIkey="ModelValue_19"/>
    <SBMLMap SBMLid="LRC_Cave" COPASIkey="Metabolite_163"/>
    <SBMLMap SBMLid="LRC_EE" COPASIkey="Metabolite_165"/>
    <SBMLMap SBMLid="LRC_Surf" COPASIkey="Metabolite_161"/>
    <SBMLMap SBMLid="R10_T1R_EE_degradation" COPASIkey="Reaction_24"/>
    <SBMLMap SBMLid="R11_T2R_production" COPASIkey="Reaction_23"/>
    <SBMLMap SBMLid="R12_T2R_Cave_formation" COPASIkey="Reaction_22"/>
    <SBMLMap SBMLid="R13_T2R_Cave_recycling" COPASIkey="Reaction_21"/>
    <SBMLMap SBMLid="R14_T2R_EE_formation" COPASIkey="Reaction_20"/>
    <SBMLMap SBMLid="R15_T2R_EE_recycling" COPASIkey="Reaction_19"/>
    <SBMLMap SBMLid="R16_T2R_EE_degradation" COPASIkey="Reaction_18"/>
    <SBMLMap SBMLid="R17_LRC_formation" COPASIkey="Reaction_17"/>
    <SBMLMap SBMLid="R18_LRC_Cave_formation" COPASIkey="Reaction_16"/>
    <SBMLMap SBMLid="R19_LRC_Cave_recycling" COPASIkey="Reaction_15"/>
    <SBMLMap SBMLid="R1_Smad2_import" COPASIkey="Reaction_33"/>
    <SBMLMap SBMLid="R20_LRC_EE_formation" COPASIkey="Reaction_14"/>
    <SBMLMap SBMLid="R21_LRC_EE_recycling" COPASIkey="Reaction_13"/>
    <SBMLMap SBMLid="R22_LRC_EE_degradation" COPASIkey="Reaction_12"/>
    <SBMLMap SBMLid="R23_Smads_Complex_formation" COPASIkey="Reaction_11"/>
    <SBMLMap SBMLid="R24_Smads_Complex_import" COPASIkey="Reaction_10"/>
    <SBMLMap SBMLid="R25_Smads_Complex_Dissociation" COPASIkey="Reaction_9"/>
    <SBMLMap SBMLid="R2_Smad2_export" COPASIkey="Reaction_32"/>
    <SBMLMap SBMLid="R3_Smad4_import" COPASIkey="Reaction_31"/>
    <SBMLMap SBMLid="R4_Smad4_export" COPASIkey="Reaction_30"/>
    <SBMLMap SBMLid="R5_T1R_production" COPASIkey="Reaction_29"/>
    <SBMLMap SBMLid="R6_T1R_Cave_formation" COPASIkey="Reaction_28"/>
    <SBMLMap SBMLid="R7_T1R_Cave_recycling" COPASIkey="Reaction_27"/>
    <SBMLMap SBMLid="R8_T1R_EE_formation" COPASIkey="Reaction_26"/>
    <SBMLMap SBMLid="R9_T1R_EE_recycling" COPASIkey="Reaction_25"/>
    <SBMLMap SBMLid="Smad2c" COPASIkey="Metabolite_137"/>
    <SBMLMap SBMLid="Smad2n" COPASIkey="Metabolite_133"/>
    <SBMLMap SBMLid="Smad4c" COPASIkey="Metabolite_125"/>
    <SBMLMap SBMLid="Smad4n" COPASIkey="Metabolite_121"/>
    <SBMLMap SBMLid="Smads_Complex_c" COPASIkey="Metabolite_167"/>
    <SBMLMap SBMLid="Smads_Complex_n" COPASIkey="Metabolite_169"/>
    <SBMLMap SBMLid="T1R_Cave" COPASIkey="Metabolite_17"/>
    <SBMLMap SBMLid="T1R_EE" COPASIkey="Metabolite_7"/>
    <SBMLMap SBMLid="T1R_Surf" COPASIkey="Metabolite_21"/>
    <SBMLMap SBMLid="T2R_Cave" COPASIkey="Metabolite_81"/>
    <SBMLMap SBMLid="T2R_EE" COPASIkey="Metabolite_131"/>
    <SBMLMap SBMLid="T2R_Surf" COPASIkey="Metabolite_97"/>
    <SBMLMap SBMLid="TGF_beta" COPASIkey="Metabolite_171"/>
    <SBMLMap SBMLid="Total_Smad2c" COPASIkey="ModelValue_8"/>
    <SBMLMap SBMLid="Total_Smad2n" COPASIkey="ModelValue_9"/>
    <SBMLMap SBMLid="V_cyt" COPASIkey="Compartment_26"/>
    <SBMLMap SBMLid="V_medium" COPASIkey="Compartment_18"/>
    <SBMLMap SBMLid="V_nuc" COPASIkey="Compartment_24"/>
    <SBMLMap SBMLid="k_LRC" COPASIkey="ModelValue_20"/>
    <SBMLMap SBMLid="k_Smads_Complex_c" COPASIkey="ModelValue_12"/>
    <SBMLMap SBMLid="ki_Cave" COPASIkey="ModelValue_23"/>
    <SBMLMap SBMLid="ki_EE" COPASIkey="ModelValue_25"/>
    <SBMLMap SBMLid="kr_Cave" COPASIkey="ModelValue_22"/>
    <SBMLMap SBMLid="kr_EE" COPASIkey="ModelValue_24"/>
    <SBMLMap SBMLid="v_T1R" COPASIkey="ModelValue_27"/>
    <SBMLMap SBMLid="v_T2R" COPASIkey="ModelValue_26"/>
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
<!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-10-09 14:29:39 UTC -->
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
  </ListOfFunctions>
  <Model key="Model_8" name="Zi2007_TGFbeta_signaling" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="nmol" type="deterministic" avogadroConstant="6.022140857e+23">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_8">
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
      <Compartment key="Compartment_12" name="Medium" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_12">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005576" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_18" name="Nucleus" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_18">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_20" name="Cytoplasm" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_20">
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
      <Metabolite key="Metabolite_97" name="Smad3c" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_97">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_93" name="Smad3n" simulationType="reactions" compartment="Compartment_18">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_93">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_85" name="Smad4c" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_85">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_81" name="Smad4n" simulationType="reactions" compartment="Compartment_18">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_81">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_7" name="T1R_Surf" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_7">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_9" name="T1R_Cave" simulationType="reactions" compartment="Compartment_20">
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
      <Metabolite key="Metabolite_17" name="T1R_EE" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_17">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_37" name="T2R_Surf" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_37">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_21" name="T2R_Cave" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_21">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_91" name="T2R_EE" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_91">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_121" name="LRC_Surf" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_121">
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
      <Metabolite key="Metabolite_123" name="LRC_Cave" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_123">
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
      <Metabolite key="Metabolite_125" name="LRC_EE" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_125">
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
      <Metabolite key="Metabolite_127" name="Smads_Complex_c" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_127">
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
      <Metabolite key="Metabolite_129" name="Smads_Complex_n" simulationType="reactions" compartment="Compartment_18">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_129">
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
      <Metabolite key="Metabolite_131" name="TGF_beta" simulationType="reactions" compartment="Compartment_12">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_131">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_133" name="Smad7" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_133">
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
      <Metabolite key="Metabolite_135" name="Ski" simulationType="reactions" compartment="Compartment_20">
      </Metabolite>
      <Metabolite key="Metabolite_137" name="Smad7_mRNA" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_137">
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
      <Metabolite key="Metabolite_139" name="Ski_mRNA" simulationType="reactions" compartment="Compartment_20">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_139">
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
      <ModelValue key="ModelValue_20" name="SkiObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_20">
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
      <ModelValue key="ModelValue_21" name="Smad7Obs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_21">
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
      <ModelValue key="ModelValue_22" name="SkiSF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_22">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_23" name="Smad7SF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_23">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:45Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_24" name="Smad7mRNAObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_24">
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
      <ModelValue key="ModelValue_25" name="Smad7mRNAInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_26" name="SkiInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_27" name="Smad7ProteinInitial" simulationType="fixed">
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
          <Substrate metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_93" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4402" name="Kimp_Smad2c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_40" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="ModelValue_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_97"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Compartment_20"/>
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
          <Substrate metabolite="Metabolite_93" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4403" name="Kexp_Smad2n" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_41" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="ModelValue_12"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_93"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Compartment_18"/>
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
          <Substrate metabolite="Metabolite_85" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_81" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4161" name="Kimp_Smad4c" value="0.08"/>
        </ListOfConstants>
        <KineticLaw function="Function_42" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="ModelValue_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Metabolite_85"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Compartment_20"/>
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
          <Substrate metabolite="Metabolite_81" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_85" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4162" name="Kexp_Smad4n" value="0.5"/>
        </ListOfConstants>
        <KineticLaw function="Function_43" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="ModelValue_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_81"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Compartment_18"/>
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
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4163" name="v" value="0.0103"/>
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
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4164" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_7"/>
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
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4165" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_9"/>
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
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4166" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_7"/>
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
          <Substrate metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4167" name="k1" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_17"/>
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
          <Substrate metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4168" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_17"/>
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
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4169" name="v" value="0.02869"/>
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
          <Substrate metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4170" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_37"/>
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
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4171" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_21"/>
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
          <Substrate metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_91" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4172" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_37"/>
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
          <Substrate metabolite="Metabolite_91" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
          <Product metabolite="Metabolite_131" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4173" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_44" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Metabolite_91"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Compartment_20"/>
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
          <Substrate metabolite="Metabolite_91" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4174" name="k1" value="0.025"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_10"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_91"/>
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
          <Substrate metabolite="Metabolite_131" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_37" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_121" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4175" name="k_LRC" value="2197"/>
        </ListOfConstants>
        <KineticLaw function="Function_45" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_37"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_131"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Compartment_20"/>
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
          <Substrate metabolite="Metabolite_121" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_123" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4176" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_121"/>
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
          <Substrate metabolite="Metabolite_123" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
          <Product metabolite="Metabolite_131" stoichiometry="1"/>
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4177" name="kr_Cave" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_46" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Metabolite_123"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Compartment_20"/>
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
          <Substrate metabolite="Metabolite_121" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_125" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4178" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_121"/>
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
          <Substrate metabolite="Metabolite_125" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
          <Product metabolite="Metabolite_131" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4179" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_47" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Metabolite_125"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Compartment_20"/>
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
          <Substrate metabolite="Metabolite_125" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4180" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_6"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_125"/>
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
          <Substrate metabolite="Metabolite_97" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_85" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_127" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_125" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4181" name="k_Smads_Complex_c" value="6.85e-05"/>
        </ListOfConstants>
        <KineticLaw function="Function_48" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Metabolite_125"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Metabolite_97"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Metabolite_85"/>
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
          <Substrate metabolite="Metabolite_127" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_129" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4182" name="Kimp_Smads_Complex_c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_49" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="ModelValue_16"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Metabolite_127"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Compartment_20"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_24" name="R25_Smads_Complex_Dissociation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_129" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_81" stoichiometry="1"/>
          <Product metabolite="Metabolite_93" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4183" name="k1" value="0.1174"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_129"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_25" name="Smad7Trascription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_129" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_129" stoichiometry="1"/>
          <Product metabolite="Metabolite_137" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4184" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4184"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_129"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_26" name="SkiTranscription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_129" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_129" stoichiometry="1"/>
          <Product metabolite="Metabolite_139" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4185" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4185"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_129"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_27" name="Smad7mRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_137" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4186" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4186"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_137"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_28" name="SkimRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_139" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4187" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4187"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_139"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_29" name="Smad7Translation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_137" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_137" stoichiometry="1"/>
          <Product metabolite="Metabolite_133" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4188" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4188"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_137"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_30" name="SkiTranslation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_139" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_139" stoichiometry="1"/>
          <Product metabolite="Metabolite_135" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4189" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4189"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_139"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_31" name="SkiDeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_135" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4190" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4190"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_135"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_32" name="Smad7Feedback" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_133" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_123" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4191" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4191"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_133"/>
              <SourceParameter reference="Metabolite_123"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_33" name="Smad7Deg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_133" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4274" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4274"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_133"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_0">
      <ModelParameterSet key="ModelParameterSet_0" name="Initial State">
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
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta]" value="48177126855999.97" type="Species" simulationType="reactions"/>
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
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Trascription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Trascription],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
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
      <StateTemplateVariable objectReference="Model_8"/>
      <StateTemplateVariable objectReference="Metabolite_7"/>
      <StateTemplateVariable objectReference="Metabolite_37"/>
      <StateTemplateVariable objectReference="Metabolite_81"/>
      <StateTemplateVariable objectReference="Metabolite_97"/>
      <StateTemplateVariable objectReference="Metabolite_133"/>
      <StateTemplateVariable objectReference="Metabolite_121"/>
      <StateTemplateVariable objectReference="Metabolite_17"/>
      <StateTemplateVariable objectReference="Metabolite_91"/>
      <StateTemplateVariable objectReference="Metabolite_125"/>
      <StateTemplateVariable objectReference="Metabolite_135"/>
      <StateTemplateVariable objectReference="Metabolite_137"/>
      <StateTemplateVariable objectReference="Metabolite_139"/>
      <StateTemplateVariable objectReference="Metabolite_123"/>
      <StateTemplateVariable objectReference="Metabolite_127"/>
      <StateTemplateVariable objectReference="Metabolite_131"/>
      <StateTemplateVariable objectReference="Metabolite_129"/>
      <StateTemplateVariable objectReference="Metabolite_9"/>
      <StateTemplateVariable objectReference="Metabolite_21"/>
      <StateTemplateVariable objectReference="Metabolite_93"/>
      <StateTemplateVariable objectReference="Metabolite_85"/>
      <StateTemplateVariable objectReference="ModelValue_18"/>
      <StateTemplateVariable objectReference="ModelValue_19"/>
      <StateTemplateVariable objectReference="ModelValue_20"/>
      <StateTemplateVariable objectReference="ModelValue_21"/>
      <StateTemplateVariable objectReference="ModelValue_24"/>
      <StateTemplateVariable objectReference="Compartment_12"/>
      <StateTemplateVariable objectReference="Compartment_18"/>
      <StateTemplateVariable objectReference="Compartment_20"/>
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
      <StateTemplateVariable objectReference="ModelValue_22"/>
      <StateTemplateVariable objectReference="ModelValue_23"/>
      <StateTemplateVariable objectReference="ModelValue_25"/>
      <StateTemplateVariable objectReference="ModelValue_26"/>
      <StateTemplateVariable objectReference="ModelValue_27"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 149860975226 127729607577 116288744377000 311489514795000 463707204823.9352 0 1302589067370 725908858903.0001 0 6323247899850 6182762730.987911 41388964352.41602 0 0 48177126855999.97 0 1322823460650 1124273476590 49837732197299.99 726794113608999.8 236.4499999999157 492.6100000007736 0.0654552296667 0.73333706375 0.00977782751667 1 0.00035 0.00105 0.0103 0.02869 0.33 0.033 0.33 0.03742 0.005 2197 0.02609 0.005 0.025 0.16 1 0.08 0.5 6.85e-05 0.16 0.1174 1 1 0.00977782751667 0.0654552296667 0.73333706375 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_0" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_8" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_11" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
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
    <Task key="Task_10" name="Scan" type="scan" scheduled="true" updateModel="false">
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
      <Report reference="Report_5" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_6" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_4" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_0"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Use Reder" type="bool" value="1"/>
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
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
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
        <Parameter name="Deuflhard Tolerance" type="unsignedFloat" value="1e-06"/>
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
    <Task key="Task_2" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
    <Task key="Task_1" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
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
    <Task key="Task_12" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_0" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_0"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_8" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_7" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_6" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
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
    <Report key="Report_5" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
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
    <Report key="Report_4" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
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
    <Report key="Report_3" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
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
    <Report key="Report_2" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
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
    <Report key="Report_1" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
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
    <Report key="Report_0" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
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
    <SBMLMap SBMLid="LRC_Cave" COPASIkey="Metabolite_123"/>
    <SBMLMap SBMLid="LRC_EE" COPASIkey="Metabolite_125"/>
    <SBMLMap SBMLid="LRC_Surf" COPASIkey="Metabolite_121"/>
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
    <SBMLMap SBMLid="R2_Smad2_export" COPASIkey="Reaction_1"/>
    <SBMLMap SBMLid="R3_Smad4_import" COPASIkey="Reaction_2"/>
    <SBMLMap SBMLid="R4_Smad4_export" COPASIkey="Reaction_3"/>
    <SBMLMap SBMLid="R5_T1R_production" COPASIkey="Reaction_4"/>
    <SBMLMap SBMLid="R6_T1R_Cave_formation" COPASIkey="Reaction_5"/>
    <SBMLMap SBMLid="R7_T1R_Cave_recycling" COPASIkey="Reaction_6"/>
    <SBMLMap SBMLid="R8_T1R_EE_formation" COPASIkey="Reaction_7"/>
    <SBMLMap SBMLid="R9_T1R_EE_recycling" COPASIkey="Reaction_8"/>
    <SBMLMap SBMLid="Smad2c" COPASIkey="Metabolite_97"/>
    <SBMLMap SBMLid="Smad2n" COPASIkey="Metabolite_93"/>
    <SBMLMap SBMLid="Smad4c" COPASIkey="Metabolite_85"/>
    <SBMLMap SBMLid="Smad4n" COPASIkey="Metabolite_81"/>
    <SBMLMap SBMLid="Smads_Complex_c" COPASIkey="Metabolite_127"/>
    <SBMLMap SBMLid="Smads_Complex_n" COPASIkey="Metabolite_129"/>
    <SBMLMap SBMLid="T1R_Cave" COPASIkey="Metabolite_9"/>
    <SBMLMap SBMLid="T1R_EE" COPASIkey="Metabolite_17"/>
    <SBMLMap SBMLid="T1R_Surf" COPASIkey="Metabolite_7"/>
    <SBMLMap SBMLid="T2R_Cave" COPASIkey="Metabolite_21"/>
    <SBMLMap SBMLid="T2R_EE" COPASIkey="Metabolite_91"/>
    <SBMLMap SBMLid="T2R_Surf" COPASIkey="Metabolite_37"/>
    <SBMLMap SBMLid="TGF_beta" COPASIkey="Metabolite_131"/>
    <SBMLMap SBMLid="Total_Smad2c" COPASIkey="ModelValue_19"/>
    <SBMLMap SBMLid="Total_Smad2n" COPASIkey="ModelValue_18"/>
    <SBMLMap SBMLid="V_cyt" COPASIkey="Compartment_20"/>
    <SBMLMap SBMLid="V_medium" COPASIkey="Compartment_12"/>
    <SBMLMap SBMLid="V_nuc" COPASIkey="Compartment_18"/>
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
    def smad7_not_reproduced_alternative(self):
        """

        :return:
        """
        return """<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-10-06 01:22:16 UTC -->
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
  </ListOfFunctions>
  <Model key="Model_6" name="Zi2007_TGFbeta_signaling" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="nmol" type="deterministic" avogadroConstant="6.022140857e+23">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_6">
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
      <Compartment key="Compartment_3" name="Medium" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_3">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005576" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_12" name="Nucleus" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_12">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005634" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_14" name="Cytoplasm" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_14">
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
      <Metabolite key="Metabolite_37" name="Smad3c" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_37">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_33" name="Smad3n" simulationType="reactions" compartment="Compartment_12">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_33">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q15796" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_25" name="Smad4c" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_25">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_21" name="Smad4n" simulationType="reactions" compartment="Compartment_12">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_21">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q13485" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_17" name="T1R_Surf" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_17">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/Q8NER5" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_13" name="T1R_Cave" simulationType="reactions" compartment="Compartment_14">
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
      <Metabolite key="Metabolite_9" name="T1R_EE" simulationType="reactions" compartment="Compartment_14">
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
      <Metabolite key="Metabolite_1" name="T2R_Surf" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_1">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_7" name="T2R_Cave" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_7">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_31" name="T2R_EE" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_31">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_81" name="LRC_Surf" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_81">
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
      <Metabolite key="Metabolite_83" name="LRC_Cave" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_83">
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
      <Metabolite key="Metabolite_85" name="LRC_EE" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_85">
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
      <Metabolite key="Metabolite_87" name="Smads_Complex_c" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_87">
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
      <Metabolite key="Metabolite_89" name="Smads_Complex_n" simulationType="reactions" compartment="Compartment_12">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_89">
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
      <Metabolite key="Metabolite_91" name="TGF_beta" simulationType="reactions" compartment="Compartment_3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_91">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_93" name="Smad7" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_93">
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
      <Metabolite key="Metabolite_95" name="Ski" simulationType="reactions" compartment="Compartment_14">
      </Metabolite>
      <Metabolite key="Metabolite_97" name="Smad7_mRNA" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_97">
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
      <Metabolite key="Metabolite_99" name="Ski_mRNA" simulationType="reactions" compartment="Compartment_14">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_99">
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
      <ModelValue key="ModelValue_27" name="v_T1R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_26" name="v_T2R" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_25" name="ki_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_24" name="kr_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_23" name="ki_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_22" name="kr_Cave" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_21" name="Kcd" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_20" name="k_LRC" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_19" name="Klid" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_18" name="Kdeg_T1R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_17" name="Kdeg_T2R_EE" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_16" name="Kimp_Smad2c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_15" name="Kexp_Smad2n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_14" name="Kimp_Smad4c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_13" name="Kexp_Smad4n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_12" name="k_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_11" name="Kimp_Smads_Complex_c" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_10" name="Kdiss_Smads_Complex_n" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_9" name="Total_Smad2n" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smad3n],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus],Vector=Metabolites[Smads_Complex_n],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_8" name="Total_Smad2c" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad3c],Reference=Concentration>+&lt;CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smads_Complex_c],Reference=Concentration>
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_7" name="SkiObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_7">
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
      <ModelValue key="ModelValue_6" name="Smad7Obs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_6">
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
      <ModelValue key="ModelValue_5" name="SkiSF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_5">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:48Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_4" name="Smad7SF" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_4">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2017-10-05T16:13:45Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_3" name="Smad7mRNAObs" simulationType="assignment">
        <MiriamAnnotation>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_3">
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
      <ModelValue key="ModelValue_2" name="Smad7mRNAInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_1" name="SkiInitial" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_0" name="Smad7ProteinInitial" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_32" name="R1_Smad2_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_32">
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
          <Substrate metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_33" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4113" name="Kimp_Smad2c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_40" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="ModelValue_16"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_37"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Compartment_14"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_31" name="R2_Smad2_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_31">
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
          <Substrate metabolite="Metabolite_33" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_37" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4114" name="Kexp_Smad2n" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_41" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="ModelValue_15"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Metabolite_33"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Compartment_12"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_30" name="R3_Smad4_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_30">
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
          <Substrate metabolite="Metabolite_25" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_3999" name="Kimp_Smad4c" value="0.08"/>
        </ListOfConstants>
        <KineticLaw function="Function_42" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="ModelValue_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Metabolite_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Compartment_14"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_29" name="R4_Smad4_export" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_29">
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
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_25" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4000" name="Kexp_Smad4n" value="0.5"/>
        </ListOfConstants>
        <KineticLaw function="Function_43" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="ModelValue_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Compartment_12"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_28" name="R5_T1R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_28">
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
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4001" name="v" value="0.0103"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_27"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_27" name="R6_T1R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_27">
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
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4002" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_17"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_26" name="R7_T1R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_26">
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
          <Substrate metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4003" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_22"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_13"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_25" name="R8_T1R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_25">
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
          <Product metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4004" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_17"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_24" name="R9_T1R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_24">
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
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4005" name="k1" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_24"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_23" name="R10_T1R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_23">
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
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4006" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_18"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_22" name="R11_T2R_production" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_22">
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
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4007" name="v" value="0.02869"/>
        </ListOfConstants>
        <KineticLaw function="Function_6" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_49">
              <SourceParameter reference="ModelValue_26"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_21" name="R12_T2R_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_21">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4008" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_20" name="R13_T2R_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_20">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4009" name="k1" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_22"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_19" name="R14_T2R_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_19">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_31" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4010" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_18" name="R15_T2R_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_18">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0002090" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_31" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
          <Product metabolite="Metabolite_91" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4011" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_44" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Metabolite_31"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Compartment_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="ModelValue_24"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_17" name="R16_T2R_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_17">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_31" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4012" name="k1" value="0.025"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_31"/>
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
          <Substrate metabolite="Metabolite_91" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_81" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4013" name="k_LRC" value="2197"/>
        </ListOfConstants>
        <KineticLaw function="Function_45" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Metabolite_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Metabolite_91"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Compartment_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="ModelValue_20"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_15" name="R18_LRC_Cave_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_15">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_81" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_83" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4014" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_81"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_14" name="R19_LRC_Cave_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_14">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_83" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
          <Product metabolite="Metabolite_91" stoichiometry="1"/>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4015" name="kr_Cave" value="0.03742"/>
        </ListOfConstants>
        <KineticLaw function="Function_46" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Metabolite_83"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Compartment_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="ModelValue_22"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_13" name="R20_LRC_EE_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_13">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_81" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_85" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4016" name="k1" value="0.33"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_81"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_12" name="R21_LRC_EE_recycling" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_12">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_85" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
          <Product metabolite="Metabolite_91" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4017" name="kr_EE" value="0.033"/>
        </ListOfConstants>
        <KineticLaw function="Function_47" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Metabolite_85"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Compartment_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="ModelValue_24"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_11" name="R22_LRC_EE_degradation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_11">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0017015" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_85" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4018" name="k1" value="0.005"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_85"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_10" name="R23_Smads_Complex_formation" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_10">
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
          <Substrate metabolite="Metabolite_37" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_25" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_87" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_85" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_4019" name="k_Smads_Complex_c" value="6.85e-05"/>
        </ListOfConstants>
        <KineticLaw function="Function_48" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Metabolite_85"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Metabolite_37"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Metabolite_25"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="ModelValue_12"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_9" name="R24_Smads_Complex_import" reversible="false" fast="false">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_9">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007184" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_87" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_89" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4020" name="Kimp_Smads_Complex_c" value="0.16"/>
        </ListOfConstants>
        <KineticLaw function="Function_49" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="ModelValue_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Metabolite_87"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Compartment_14"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_8" name="R25_Smads_Complex_Dissociation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_89" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
          <Product metabolite="Metabolite_33" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4021" name="k1" value="0.1174"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Nucleus]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_10"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_89"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_7" name="Smad7Trascription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_89" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_89" stoichiometry="1"/>
          <Product metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4022" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4022"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_89"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_6" name="SkiTranscription" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_89" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_89" stoichiometry="1"/>
          <Product metabolite="Metabolite_99" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4023" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4023"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_89"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_5" name="Smad7mRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4024" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4024"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_97"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_4" name="SkimRNADeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_99" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4025" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4025"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_99"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_3" name="Smad7Translation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_97" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_97" stoichiometry="1"/>
          <Product metabolite="Metabolite_93" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4026" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4026"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_97"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_2" name="SkiTranslation" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_99" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_99" stoichiometry="1"/>
          <Product metabolite="Metabolite_95" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4027" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4027"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_99"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1" name="SkiDeg" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_95" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4028" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4028"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_95"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_0" name="Smad7Feedback" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_93" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_83" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_4029" name="k1" value="0.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm]">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="Parameter_4029"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_93"/>
              <SourceParameter reference="Metabolite_83"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_0">
      <ModelParameterSet key="ModelParameterSet_0" name="Initial State">
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
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Cytoplasm],Vector=Metabolites[Smad4c]" value="726794113608999.9" type="Species" simulationType="reactions"/>
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
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Compartments[Medium],Vector=Metabolites[TGF_beta]" value="48177126855999.99" type="Species" simulationType="reactions"/>
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
          <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Values[Total_Smad2n]" value="236.4499999999158" type="ModelValue" simulationType="assignment"/>
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
          <ModelParameterGroup cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Trascription]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=Zi2007_TGFbeta_signaling,Vector=Reactions[Smad7Trascription],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
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
      <StateTemplateVariable objectReference="Model_6"/>
      <StateTemplateVariable objectReference="Metabolite_17"/>
      <StateTemplateVariable objectReference="Metabolite_1"/>
      <StateTemplateVariable objectReference="Metabolite_21"/>
      <StateTemplateVariable objectReference="Metabolite_37"/>
      <StateTemplateVariable objectReference="Metabolite_81"/>
      <StateTemplateVariable objectReference="Metabolite_9"/>
      <StateTemplateVariable objectReference="Metabolite_31"/>
      <StateTemplateVariable objectReference="Metabolite_83"/>
      <StateTemplateVariable objectReference="Metabolite_85"/>
      <StateTemplateVariable objectReference="Metabolite_95"/>
      <StateTemplateVariable objectReference="Metabolite_97"/>
      <StateTemplateVariable objectReference="Metabolite_99"/>
      <StateTemplateVariable objectReference="Metabolite_89"/>
      <StateTemplateVariable objectReference="Metabolite_93"/>
      <StateTemplateVariable objectReference="Metabolite_91"/>
      <StateTemplateVariable objectReference="Metabolite_87"/>
      <StateTemplateVariable objectReference="Metabolite_13"/>
      <StateTemplateVariable objectReference="Metabolite_7"/>
      <StateTemplateVariable objectReference="Metabolite_33"/>
      <StateTemplateVariable objectReference="Metabolite_25"/>
      <StateTemplateVariable objectReference="ModelValue_9"/>
      <StateTemplateVariable objectReference="ModelValue_8"/>
      <StateTemplateVariable objectReference="ModelValue_7"/>
      <StateTemplateVariable objectReference="ModelValue_6"/>
      <StateTemplateVariable objectReference="ModelValue_3"/>
      <StateTemplateVariable objectReference="Compartment_3"/>
      <StateTemplateVariable objectReference="Compartment_12"/>
      <StateTemplateVariable objectReference="Compartment_14"/>
      <StateTemplateVariable objectReference="ModelValue_27"/>
      <StateTemplateVariable objectReference="ModelValue_26"/>
      <StateTemplateVariable objectReference="ModelValue_25"/>
      <StateTemplateVariable objectReference="ModelValue_24"/>
      <StateTemplateVariable objectReference="ModelValue_23"/>
      <StateTemplateVariable objectReference="ModelValue_22"/>
      <StateTemplateVariable objectReference="ModelValue_21"/>
      <StateTemplateVariable objectReference="ModelValue_20"/>
      <StateTemplateVariable objectReference="ModelValue_19"/>
      <StateTemplateVariable objectReference="ModelValue_18"/>
      <StateTemplateVariable objectReference="ModelValue_17"/>
      <StateTemplateVariable objectReference="ModelValue_16"/>
      <StateTemplateVariable objectReference="ModelValue_15"/>
      <StateTemplateVariable objectReference="ModelValue_14"/>
      <StateTemplateVariable objectReference="ModelValue_13"/>
      <StateTemplateVariable objectReference="ModelValue_12"/>
      <StateTemplateVariable objectReference="ModelValue_11"/>
      <StateTemplateVariable objectReference="ModelValue_10"/>
      <StateTemplateVariable objectReference="ModelValue_5"/>
      <StateTemplateVariable objectReference="ModelValue_4"/>
      <StateTemplateVariable objectReference="ModelValue_2"/>
      <StateTemplateVariable objectReference="ModelValue_1"/>
      <StateTemplateVariable objectReference="ModelValue_0"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 149860975226 127729607577 116288744377000 311489514795000 0 1302589067370 725908858903.0001 0 0 6323247899850 6182762730.987911 41388964352.41602 0 463707204823.9352 48177126855999.99 0 1322823460650 1124273476590 49837732197299.99 726794113608999.9 236.4499999999158 492.6100000007736 0.0654552296667 0.73333706375 0.00977782751667 1 0.00035 0.00105 0.0103 0.02869 0.33 0.033 0.33 0.03742 0.005 2197 0.02609 0.005 0.025 0.16 1 0.08 0.5 6.85e-05 0.16 0.1174 1 1 0.00977782751667 0.0654552296667 0.73333706375 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_13" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_19" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_1" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Report reference="Report_7" target="../../Models/2017/09_Sept/zi_timecourse_simulation.csv" append="0" confirmOverwrite="0"/>
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
    <Task key="Task_2" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report reference="Report_8" target="zi_repeat.csv" append="0" confirmOverwrite="0"/>
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
    <Task key="Task_3" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_18" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_4" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_0" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_5" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_1" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_6" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_2" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_13"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Use Reder" type="bool" value="1"/>
        <Parameter name="Use Smallbone" type="bool" value="1"/>
      </Method>
    </Task>
    <Task key="Task_7" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_3" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_8" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_4" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_9" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_5" target="" append="1" confirmOverwrite="1"/>
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
    <Task key="Task_10" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
    <Task key="Task_11" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
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
    <Task key="Task_0" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_6" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_13"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_19" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_18" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_0" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
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
    <Report key="Report_1" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
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
    <Report key="Report_2" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
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
    <Report key="Report_3" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
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
    <Report key="Report_4" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
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
    <Report key="Report_5" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
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
    <Report key="Report_6" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
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
    <Report key="Report_7" name="Time-Course" taskType="unset" separator="&#x09;" precision="6">
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
    <Report key="Report_8" name="profilelikelihood" taskType="unset" separator="&#x09;" precision="6">
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
    <SBMLMap SBMLid="Kcd" COPASIkey="ModelValue_21"/>
    <SBMLMap SBMLid="Kdeg_T1R_EE" COPASIkey="ModelValue_18"/>
    <SBMLMap SBMLid="Kdeg_T2R_EE" COPASIkey="ModelValue_17"/>
    <SBMLMap SBMLid="Kdiss_Smads_Complex_n" COPASIkey="ModelValue_10"/>
    <SBMLMap SBMLid="Kexp_Smad2n" COPASIkey="ModelValue_15"/>
    <SBMLMap SBMLid="Kexp_Smad4n" COPASIkey="ModelValue_13"/>
    <SBMLMap SBMLid="Kimp_Smad2c" COPASIkey="ModelValue_16"/>
    <SBMLMap SBMLid="Kimp_Smad4c" COPASIkey="ModelValue_14"/>
    <SBMLMap SBMLid="Kimp_Smads_Complex_c" COPASIkey="ModelValue_11"/>
    <SBMLMap SBMLid="Klid" COPASIkey="ModelValue_19"/>
    <SBMLMap SBMLid="LRC_Cave" COPASIkey="Metabolite_83"/>
    <SBMLMap SBMLid="LRC_EE" COPASIkey="Metabolite_85"/>
    <SBMLMap SBMLid="LRC_Surf" COPASIkey="Metabolite_81"/>
    <SBMLMap SBMLid="R10_T1R_EE_degradation" COPASIkey="Reaction_23"/>
    <SBMLMap SBMLid="R11_T2R_production" COPASIkey="Reaction_22"/>
    <SBMLMap SBMLid="R12_T2R_Cave_formation" COPASIkey="Reaction_21"/>
    <SBMLMap SBMLid="R13_T2R_Cave_recycling" COPASIkey="Reaction_20"/>
    <SBMLMap SBMLid="R14_T2R_EE_formation" COPASIkey="Reaction_19"/>
    <SBMLMap SBMLid="R15_T2R_EE_recycling" COPASIkey="Reaction_18"/>
    <SBMLMap SBMLid="R16_T2R_EE_degradation" COPASIkey="Reaction_17"/>
    <SBMLMap SBMLid="R17_LRC_formation" COPASIkey="Reaction_16"/>
    <SBMLMap SBMLid="R18_LRC_Cave_formation" COPASIkey="Reaction_15"/>
    <SBMLMap SBMLid="R19_LRC_Cave_recycling" COPASIkey="Reaction_14"/>
    <SBMLMap SBMLid="R1_Smad2_import" COPASIkey="Reaction_32"/>
    <SBMLMap SBMLid="R20_LRC_EE_formation" COPASIkey="Reaction_13"/>
    <SBMLMap SBMLid="R21_LRC_EE_recycling" COPASIkey="Reaction_12"/>
    <SBMLMap SBMLid="R22_LRC_EE_degradation" COPASIkey="Reaction_11"/>
    <SBMLMap SBMLid="R23_Smads_Complex_formation" COPASIkey="Reaction_10"/>
    <SBMLMap SBMLid="R24_Smads_Complex_import" COPASIkey="Reaction_9"/>
    <SBMLMap SBMLid="R25_Smads_Complex_Dissociation" COPASIkey="Reaction_8"/>
    <SBMLMap SBMLid="R2_Smad2_export" COPASIkey="Reaction_31"/>
    <SBMLMap SBMLid="R3_Smad4_import" COPASIkey="Reaction_30"/>
    <SBMLMap SBMLid="R4_Smad4_export" COPASIkey="Reaction_29"/>
    <SBMLMap SBMLid="R5_T1R_production" COPASIkey="Reaction_28"/>
    <SBMLMap SBMLid="R6_T1R_Cave_formation" COPASIkey="Reaction_27"/>
    <SBMLMap SBMLid="R7_T1R_Cave_recycling" COPASIkey="Reaction_26"/>
    <SBMLMap SBMLid="R8_T1R_EE_formation" COPASIkey="Reaction_25"/>
    <SBMLMap SBMLid="R9_T1R_EE_recycling" COPASIkey="Reaction_24"/>
    <SBMLMap SBMLid="Smad2c" COPASIkey="Metabolite_37"/>
    <SBMLMap SBMLid="Smad2n" COPASIkey="Metabolite_33"/>
    <SBMLMap SBMLid="Smad4c" COPASIkey="Metabolite_25"/>
    <SBMLMap SBMLid="Smad4n" COPASIkey="Metabolite_21"/>
    <SBMLMap SBMLid="Smads_Complex_c" COPASIkey="Metabolite_87"/>
    <SBMLMap SBMLid="Smads_Complex_n" COPASIkey="Metabolite_89"/>
    <SBMLMap SBMLid="T1R_Cave" COPASIkey="Metabolite_13"/>
    <SBMLMap SBMLid="T1R_EE" COPASIkey="Metabolite_9"/>
    <SBMLMap SBMLid="T1R_Surf" COPASIkey="Metabolite_17"/>
    <SBMLMap SBMLid="T2R_Cave" COPASIkey="Metabolite_7"/>
    <SBMLMap SBMLid="T2R_EE" COPASIkey="Metabolite_31"/>
    <SBMLMap SBMLid="T2R_Surf" COPASIkey="Metabolite_1"/>
    <SBMLMap SBMLid="TGF_beta" COPASIkey="Metabolite_91"/>
    <SBMLMap SBMLid="Total_Smad2c" COPASIkey="ModelValue_8"/>
    <SBMLMap SBMLid="Total_Smad2n" COPASIkey="ModelValue_9"/>
    <SBMLMap SBMLid="V_cyt" COPASIkey="Compartment_14"/>
    <SBMLMap SBMLid="V_medium" COPASIkey="Compartment_3"/>
    <SBMLMap SBMLid="V_nuc" COPASIkey="Compartment_12"/>
    <SBMLMap SBMLid="k_LRC" COPASIkey="ModelValue_20"/>
    <SBMLMap SBMLid="k_Smads_Complex_c" COPASIkey="ModelValue_12"/>
    <SBMLMap SBMLid="ki_Cave" COPASIkey="ModelValue_23"/>
    <SBMLMap SBMLid="ki_EE" COPASIkey="ModelValue_25"/>
    <SBMLMap SBMLid="kr_Cave" COPASIkey="ModelValue_22"/>
    <SBMLMap SBMLid="kr_EE" COPASIkey="ModelValue_24"/>
    <SBMLMap SBMLid="v_T1R" COPASIkey="ModelValue_27"/>
    <SBMLMap SBMLid="v_T2R" COPASIkey="ModelValue_26"/>
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
