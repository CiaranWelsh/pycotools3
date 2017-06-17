# -*- coding: utf-8 -*-
'''
 This file is part of PyCoTools.

 PyCoTools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 PyCoTools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with PyCoTools.  If not, see <http://www.gnu.org/licenses/>.


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 
'''

import PyCoTools
import unittest
import glob
import os
import numpy
import pandas
import time
import re
import shutil 
import scipy
#
#model_string='''<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="16" versionDevel="104" copasiSourcesModified="0">
#  <ListOfFunctions>
#    <Function key="Function_40" name="Function for Ligand receptor complex formation" type="UserDefined" reversible="false">
#      <Expression>
#        ka*ligand*(RI*PM)*(RII*PM)/PM
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_266" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_258" name="RI" order="1" role="substrate"/>
#        <ParameterDescription key="FunctionParameter_268" name="RII" order="2" role="substrate"/>
#        <ParameterDescription key="FunctionParameter_264" name="ka" order="3" role="constant"/>
#        <ParameterDescription key="FunctionParameter_254" name="ligand" order="4" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_41" name="Function for Ligand receptor complex constitutive degradation" type="UserDefined" reversible="false">
#      <Expression>
#        kcd*(lRIRII*PM)/PM
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_262" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_269" name="kcd" order="1" role="constant"/>
#        <ParameterDescription key="FunctionParameter_265" name="lRIRII" order="2" role="substrate"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_42" name="Function for Ligand independent complex degradation" type="UserDefined" reversible="false">
#      <Expression>
#        klid*(lRIRII*PM)/PM
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_272" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_270" name="klid" order="1" role="constant"/>
#        <ParameterDescription key="FunctionParameter_267" name="lRIRII" order="2" role="substrate"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_43" name="Function for Ligand receptor complex internalization" type="UserDefined" reversible="false">
#      <Expression>
#        ki*(lRIRII*PM)
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_275" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_273" name="ki" order="1" role="constant"/>
#        <ParameterDescription key="FunctionParameter_246" name="lRIRII" order="2" role="substrate"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_44" name="Function for RI synthesis" type="UserDefined" reversible="false">
#      <Expression>
#        pRI/PM
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_271" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_276" name="pRI" order="1" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_45" name="Function for RI constitutive degradation" type="UserDefined" reversible="false">
#      <Expression>
#        kcd*(RI*PM)/PM
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_280" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_278" name="RI" order="1" role="substrate"/>
#        <ParameterDescription key="FunctionParameter_277" name="kcd" order="2" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_46" name="Function for RI internalization" type="UserDefined" reversible="false">
#      <Expression>
#        ki*(RI*PM)
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_283" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_274" name="RI" order="1" role="substrate"/>
#        <ParameterDescription key="FunctionParameter_281" name="ki" order="2" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_47" name="Function for RI recycling" type="UserDefined" reversible="false">
#      <Expression>
#        kr*(RI_endo*Endosome)
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_286" name="Endosome" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_279" name="RI_endo" order="1" role="substrate"/>
#        <ParameterDescription key="FunctionParameter_284" name="kr" order="2" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_48" name="Function for Ligand Receptor complex recycling" type="UserDefined" reversible="false">
#      <Expression>
#        kr*(lRIRII_endo*Endosome)
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_289" name="Endosome" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_287" name="kr" order="1" role="constant"/>
#        <ParameterDescription key="FunctionParameter_282" name="lRIRII_endo" order="2" role="substrate"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_49" name="Function for RII synthesis" type="UserDefined" reversible="false">
#      <Expression>
#        pRII/PM
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_285" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_290" name="pRII" order="1" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_50" name="Function for RII constitutive degradation" type="UserDefined" reversible="false">
#      <Expression>
#        kcd*(RII*PM)/PM
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_294" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_292" name="RII" order="1" role="substrate"/>
#        <ParameterDescription key="FunctionParameter_291" name="kcd" order="2" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_51" name="Function for RII internalization" type="UserDefined" reversible="false">
#      <Expression>
#        ki*(RII*PM)
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_297" name="PM" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_288" name="RII" order="1" role="substrate"/>
#        <ParameterDescription key="FunctionParameter_295" name="ki" order="2" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#    <Function key="Function_52" name="Function for RII recycling" type="UserDefined" reversible="false">
#      <Expression>
#        kr*(RII_endo*Endosome)
#      </Expression>
#      <ListOfParameterDescriptions>
#        <ParameterDescription key="FunctionParameter_300" name="Endosome" order="0" role="volume"/>
#        <ParameterDescription key="FunctionParameter_293" name="RII_endo" order="1" role="substrate"/>
#        <ParameterDescription key="FunctionParameter_298" name="kr" order="2" role="constant"/>
#      </ListOfParameterDescriptions>
#    </Function>
#  </ListOfFunctions>
#  <Model key="Model_3" name="Vilar2006_TGFbeta" simulationType="time" timeUnit="h" volumeUnit="l" areaUnit="m&#178;" lengthUnit="m" quantityUnit="#" type="stochastic" avogadroConstant="6.02214179e+023">
#    <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
#  <rdf:Description rdf:about="#Model_3">
#    <dcterms:bibliographicCitation>
#      <rdf:Bag>
#        <rdf:li>
#          <rdf:Description>
#            <CopasiMT:isDescribedBy rdf:resource="http://identifiers.org/pubmed/16446785"/>
#          </rdf:Description>
#        </rdf:li>
#      </rdf:Bag>
#    </dcterms:bibliographicCitation>
#    <dcterms:created>
#      <rdf:Description>
#        <dcterms:W3CDTF>2006-11-28T18:39:38Z</dcterms:W3CDTF>
#      </rdf:Description>
#    </dcterms:created>
#    <dcterms:creator>
#      <rdf:Bag>
#        <rdf:li>
#          <rdf:Description>
#            <vCard:EMAIL>hdharuri@cds.caltech.edu</vCard:EMAIL>
#            <vCard:N>
#              <rdf:Description>
#                <vCard:Family>Dharuri</vCard:Family>
#                <vCard:Given>Harish</vCard:Given>
#              </rdf:Description>
#            </vCard:N>
#            <vCard:ORG>
#              <rdf:Description>
#                <vCard:Orgname>California Institute of Technology</vCard:Orgname>
#              </rdf:Description>
#            </vCard:ORG>
#          </rdf:Description>
#        </rdf:li>
#      </rdf:Bag>
#    </dcterms:creator>
#    <dcterms:modified>
#      <rdf:Description>
#        <dcterms:W3CDTF>2012-07-05T14:45:52Z</dcterms:W3CDTF>
#      </rdf:Description>
#    </dcterms:modified>
#    <CopasiMT:hasPart>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/reactome/REACT_6844.3"/>
#      </rdf:Bag>
#    </CopasiMT:hasPart>
#    <CopasiMT:hasPart>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/kegg.pathway/hsa04350"/>
#      </rdf:Bag>
#    </CopasiMT:hasPart>
#    <CopasiMT:is>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/MODEL4023382414"/>
#      </rdf:Bag>
#    </CopasiMT:is>
#    <CopasiMT:is>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/biomodels.db/BIOMD0000000101"/>
#      </rdf:Bag>
#    </CopasiMT:is>
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007179"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#    <CopasiMT:occursIn>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/taxonomy/131567"/>
#      </rdf:Bag>
#    </CopasiMT:occursIn>
#  </rdf:Description>
#</rdf:RDF>
#
#    </MiriamAnnotation>
#    <Comment>
#      <body xmlns="http://www.w3.org/1999/xhtml">
#    <p>The model reproduces Fig 5A of the paper. The ligand concentration is increased from 3E-5 to 0.01 at time t=2500 to ensure that the system  reaches steady state. Hence, the time t=0 of the paper corresponds to t=2500 in the model. The peak value of the active ligand receptor complex is off by a value of 1.25, the authors have stated that this discrepancy is due to the fact that the figure in the paper corresponds to a slightly different parameter set. The model was successfully tested on MathSBML.</p>
#    <br/>
#    <p>To the extent possible under law, all copyright and related or neighbouring rights to this encoded model have been dedicated to the public domain worldwide. Please refer to      <a href="http://creativecommons.org/publicdomain/zero/1.0/" title="Creative Commons CC0">CC0 Public Domain Dedication</a>
#          for more information.      </p>
#  <p>In summary, you are entitled to use this encoded model in absolutely any manner you deem suitable, verbatim, or with modification, alone or embedded it in a larger context, redistribute it, commercially or not, in a restricted way or not.</p>
#  <br/>
#  <p>To cite BioModels Database, please use:      <a href="http://www.ncbi.nlm.nih.gov/pubmed/20587024" target="_blank">Li C, Donizelli M, Rodriguez N, Dharuri H, Endler L, Chelliah V, Li L, He E, Henry A, Stefan MI, Snoep JL, Hucka M, Le Nov&#232;re N, Laibe C (2010) BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models. BMC Syst Biol., 4:92.</a>
#</p>
#</body>
#    </Comment>
#    <ListOfCompartments>
#      <Compartment key="Compartment_1" name="Plasma membrane" simulationType="fixed" dimensionality="3">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Compartment_1">
#    <CopasiMT:is>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005886"/>
#      </rdf:Bag>
#    </CopasiMT:is>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#      </Compartment>
#      <Compartment key="Compartment_3" name="Endosome" simulationType="fixed" dimensionality="3">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Compartment_3">
#    <CopasiMT:is>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005768"/>
#      </rdf:Bag>
#    </CopasiMT:is>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#      </Compartment>
#    </ListOfCompartments>
#    <ListOfMetabolites>
#      <Metabolite key="Metabolite_1" name="Receptor 1" simulationType="reactions" compartment="Compartment_1">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Metabolite_1">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P36897"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#      </Metabolite>
#      <Metabolite key="Metabolite_3" name="Receptor 2" simulationType="reactions" compartment="Compartment_1">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Metabolite_3">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#      </Metabolite>
#      <Metabolite key="Metabolite_5" name="ligand receptor complex-plasma membrane" simulationType="reactions" compartment="Compartment_1">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Metabolite_5">
#    <CopasiMT:hasPart>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137"/>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P36897"/>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173"/>
#      </rdf:Bag>
#    </CopasiMT:hasPart>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#      </Metabolite>
#      <Metabolite key="Metabolite_7" name="ligand receptor complex-endosome" simulationType="reactions" compartment="Compartment_3">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Metabolite_7">
#    <CopasiMT:hasPart>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P01137"/>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P36897"/>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173"/>
#      </rdf:Bag>
#    </CopasiMT:hasPart>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#      </Metabolite>
#      <Metabolite key="Metabolite_9" name="Receptor 1-endosome" simulationType="reactions" compartment="Compartment_3">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Metabolite_9">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P36897"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#      </Metabolite>
#      <Metabolite key="Metabolite_11" name="Receptor 2 endosome" simulationType="reactions" compartment="Compartment_3">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Metabolite_11">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/uniprot/P37173"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#      </Metabolite>
#    </ListOfMetabolites>
#    <ListOfModelValues>
#      <ModelValue key="ModelValue_0" name="ka" simulationType="fixed">
#      </ModelValue>
#      <ModelValue key="ModelValue_1" name="ligand" simulationType="fixed">
#      </ModelValue>
#      <ModelValue key="ModelValue_2" name="kcd" simulationType="fixed">
#      </ModelValue>
#      <ModelValue key="ModelValue_3" name="klid" simulationType="fixed">
#      </ModelValue>
#      <ModelValue key="ModelValue_4" name="ki" simulationType="fixed">
#      </ModelValue>
#      <ModelValue key="ModelValue_5" name="pRI" simulationType="fixed">
#      </ModelValue>
#      <ModelValue key="ModelValue_6" name="kr" simulationType="fixed">
#      </ModelValue>
#      <ModelValue key="ModelValue_7" name="alpha" simulationType="fixed">
#      </ModelValue>
#      <ModelValue key="ModelValue_8" name="pRII" simulationType="fixed">
#      </ModelValue>
#    </ListOfModelValues>
#    <ListOfReactions>
#      <Reaction key="Reaction_0" name="Ligand receptor complex formation" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_0">
#    <CopasiMT:is>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0007181"/>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0050431"/>
#      </rdf:Bag>
#    </CopasiMT:is>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
#          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_5" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4387" name="ka" value="99.9998"/>
#          <Constant key="Parameter_4386" name="ligand" value="0.000661902"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_40">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_266">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_258">
#              <SourceParameter reference="Metabolite_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_268">
#              <SourceParameter reference="Metabolite_3"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_264">
#              <SourceParameter reference="ModelValue_0"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_254">
#              <SourceParameter reference="ModelValue_1"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_1" name="Ligand receptor complex constitutive degradation" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_1">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0030512"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfConstants>
#          <Constant key="Parameter_4385" name="kcd" value="0.204821"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_41">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_262">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_269">
#              <SourceParameter reference="ModelValue_2"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_265">
#              <SourceParameter reference="Metabolite_5"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_2" name="Ligand independent complex degradation" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_2">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0030512"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfConstants>
#          <Constant key="Parameter_4384" name="klid" value="0.272681"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_42">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_272">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_270">
#              <SourceParameter reference="ModelValue_3"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_267">
#              <SourceParameter reference="Metabolite_5"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_3" name="Ligand receptor complex internalization" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_3">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0030511"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_7" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4383" name="ki" value="8.92617"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_43">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_275">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_273">
#              <SourceParameter reference="ModelValue_4"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_246">
#              <SourceParameter reference="Metabolite_5"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_4" name="RI synthesis" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_4">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006412"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_1" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4382" name="pRI" value="2.38351"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_44">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_271">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_276">
#              <SourceParameter reference="ModelValue_5"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_5" name="RI constitutive degradation" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_5">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032801"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfConstants>
#          <Constant key="Parameter_4381" name="kcd" value="0.204821"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_45">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_280">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_278">
#              <SourceParameter reference="Metabolite_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_277">
#              <SourceParameter reference="ModelValue_2"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_6" name="RI internalization" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_6">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_9" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4380" name="ki" value="8.92617"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_46">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_283">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_274">
#              <SourceParameter reference="Metabolite_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_281">
#              <SourceParameter reference="ModelValue_4"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_7" name="RI recycling" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_7">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0001881"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_1" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4379" name="kr" value="0.042881"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_47">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_286">
#              <SourceParameter reference="Compartment_3"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_279">
#              <SourceParameter reference="Metabolite_9"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_284">
#              <SourceParameter reference="ModelValue_6"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_8" name="Ligand Receptor complex recycling" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_8">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0001881"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_1" stoichiometry="1"/>
#          <Product metabolite="Metabolite_3" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4378" name="kr" value="0.042881"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_48">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_289">
#              <SourceParameter reference="Compartment_3"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_287">
#              <SourceParameter reference="ModelValue_6"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_282">
#              <SourceParameter reference="Metabolite_7"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_9" name="RII synthesis" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_9">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006412"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_3" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4377" name="pRII" value="0.430213"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_49">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_285">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_290">
#              <SourceParameter reference="ModelValue_8"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_10" name="RII constitutive degradation" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_10">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0032801"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfConstants>
#          <Constant key="Parameter_4376" name="kcd" value="0.204821"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_50">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_294">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_292">
#              <SourceParameter reference="Metabolite_3"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_291">
#              <SourceParameter reference="ModelValue_2"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_11" name="RII internalization" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_11">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0031623"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_11" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4375" name="ki" value="8.92617"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_51">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_297">
#              <SourceParameter reference="Compartment_1"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_288">
#              <SourceParameter reference="Metabolite_3"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_295">
#              <SourceParameter reference="ModelValue_4"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#      <Reaction key="Reaction_12" name="RII recycling" reversible="false" fast="false">
#        <MiriamAnnotation>
#<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#  <rdf:Description rdf:about="#Reaction_12">
#    <CopasiMT:isVersionOf>
#      <rdf:Bag>
#        <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0001881"/>
#      </rdf:Bag>
#    </CopasiMT:isVersionOf>
#  </rdf:Description>
#</rdf:RDF>
#        </MiriamAnnotation>
#        <ListOfSubstrates>
#          <Substrate metabolite="Metabolite_11" stoichiometry="1"/>
#        </ListOfSubstrates>
#        <ListOfProducts>
#          <Product metabolite="Metabolite_3" stoichiometry="1"/>
#        </ListOfProducts>
#        <ListOfConstants>
#          <Constant key="Parameter_4374" name="kr" value="0.042881"/>
#        </ListOfConstants>
#        <KineticLaw function="Function_52">
#          <ListOfCallParameters>
#            <CallParameter functionParameter="FunctionParameter_300">
#              <SourceParameter reference="Compartment_3"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_293">
#              <SourceParameter reference="Metabolite_11"/>
#            </CallParameter>
#            <CallParameter functionParameter="FunctionParameter_298">
#              <SourceParameter reference="ModelValue_6"/>
#            </CallParameter>
#          </ListOfCallParameters>
#        </KineticLaw>
#      </Reaction>
#    </ListOfReactions>
#    <ListOfEvents>
#      <Event key="Event_0" name="event_0000001" fireAtInitialTime="0" persistentTrigger="0">
#        <TriggerExpression>
#          &lt;CN=Root,Model=Vilar2006_TGFbeta,Reference=Time&gt; ge 2500
#        </TriggerExpression>
#        <ListOfAssignments>
#          <Assignment targetKey="ModelValue_1">
#            <Expression>
#              0.01
#            </Expression>
#          </Assignment>
#        </ListOfAssignments>
#      </Event>
#    </ListOfEvents>
#    <ListOfModelParameterSets activeSet="ModelParameterSet_1">
#      <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
#        <ModelParameterGroup cn="String=Initial Time" type="Group">
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta" value="0" type="Model" simulationType="time"/>
#        </ModelParameterGroup>
#        <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane]" value="1" type="Compartment" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome]" value="1" type="Compartment" simulationType="fixed"/>
#        </ModelParameterGroup>
#        <ModelParameterGroup cn="String=Initial Species Values" type="Group">
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 1]" value="22.9544" type="Species" simulationType="reactions"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 2]" value="0.00155182" type="Species" simulationType="reactions"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[ligand receptor complex-plasma membrane]" value="0.0001" type="Species" simulationType="reactions"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[ligand receptor complex-endosome]" value="38.8192950146758" type="Species" simulationType="reactions"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 1-endosome]" value="7.62219" type="Species" simulationType="reactions"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 2 endosome]" value="0.385859" type="Species" simulationType="reactions"/>
#        </ModelParameterGroup>
#        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ka]" value="0.779862" type="ModelValue" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ligand]" value="0.0001" type="ModelValue" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kcd]" value="0.0251133" type="ModelValue" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[klid]" value="0.268159" type="ModelValue" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ki]" value="0.390589" type="ModelValue" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRI]" value="6.44406" type="ModelValue" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kr]" value="0.0308656" type="ModelValue" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[alpha]" value="1.04518" type="ModelValue" simulationType="fixed"/>
#          <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRII]" value="4.20542" type="ModelValue" simulationType="fixed"/>
#        </ModelParameterGroup>
#        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand receptor complex formation]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand receptor complex formation],ParameterGroup=Parameters,Parameter=ka" value="99.99979082998443" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ka],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand receptor complex formation],ParameterGroup=Parameters,Parameter=ligand" value="0.0006619016703488301" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ligand],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand receptor complex constitutive degradation]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand receptor complex constitutive degradation],ParameterGroup=Parameters,Parameter=kcd" value="0.2048205249892138" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kcd],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand independent complex degradation]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand independent complex degradation],ParameterGroup=Parameters,Parameter=klid" value="0.2726806766859603" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[klid],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand receptor complex internalization]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand receptor complex internalization],ParameterGroup=Parameters,Parameter=ki" value="8.926166068114043" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ki],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RI synthesis]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RI synthesis],ParameterGroup=Parameters,Parameter=pRI" value="2.383514525738733" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRI],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RI constitutive degradation]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RI constitutive degradation],ParameterGroup=Parameters,Parameter=kcd" value="0.2048205249892138" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kcd],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RI internalization]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RI internalization],ParameterGroup=Parameters,Parameter=ki" value="8.926166068114043" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ki],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RI recycling]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RI recycling],ParameterGroup=Parameters,Parameter=kr" value="0.042880961849497" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kr],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand Receptor complex recycling]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[Ligand Receptor complex recycling],ParameterGroup=Parameters,Parameter=kr" value="0.042880961849497" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kr],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RII synthesis]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RII synthesis],ParameterGroup=Parameters,Parameter=pRII" value="0.430213" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRII],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RII constitutive degradation]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RII constitutive degradation],ParameterGroup=Parameters,Parameter=kcd" value="0.2048205249892138" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kcd],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RII internalization]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RII internalization],ParameterGroup=Parameters,Parameter=ki" value="8.926166068114043" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ki],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#          <ModelParameterGroup cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RII recycling]" type="Reaction">
#            <ModelParameter cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Reactions[RII recycling],ParameterGroup=Parameters,Parameter=kr" value="0.042880961849497" type="ReactionParameter" simulationType="assignment">
#              <InitialExpression>
#                &lt;CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kr],Reference=InitialValue&gt;
#              </InitialExpression>
#            </ModelParameter>
#          </ModelParameterGroup>
#        </ModelParameterGroup>
#      </ModelParameterSet>
#    </ListOfModelParameterSets>
#    <StateTemplate>
#      <StateTemplateVariable objectReference="Model_3"/>
#      <StateTemplateVariable objectReference="Metabolite_1"/>
#      <StateTemplateVariable objectReference="Metabolite_3"/>
#      <StateTemplateVariable objectReference="Metabolite_5"/>
#      <StateTemplateVariable objectReference="Metabolite_7"/>
#      <StateTemplateVariable objectReference="Metabolite_9"/>
#      <StateTemplateVariable objectReference="Metabolite_11"/>
#      <StateTemplateVariable objectReference="Compartment_1"/>
#      <StateTemplateVariable objectReference="Compartment_3"/>
#      <StateTemplateVariable objectReference="ModelValue_0"/>
#      <StateTemplateVariable objectReference="ModelValue_1"/>
#      <StateTemplateVariable objectReference="ModelValue_2"/>
#      <StateTemplateVariable objectReference="ModelValue_3"/>
#      <StateTemplateVariable objectReference="ModelValue_4"/>
#      <StateTemplateVariable objectReference="ModelValue_5"/>
#      <StateTemplateVariable objectReference="ModelValue_6"/>
#      <StateTemplateVariable objectReference="ModelValue_7"/>
#      <StateTemplateVariable objectReference="ModelValue_8"/>
#    </StateTemplate>
#    <InitialState type="initialState">
#      0 0.0001 18.33170201336451 45.89012478791828 38.8192950146758 0.0001234329897578243 9.117063525097914 1 1 99.99979082998443 0.0006619016703488301 0.2048205249892138 0.2726806766859603 8.926166068114043 2.383514525738733 0.042880961849497 63.9748778908782 0.430213 
#    </InitialState>
#  </Model>
#  <ListOfTasks>
#    <Task key="Task_14" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
#      <Report reference="Report_9" target="" append="1" confirmOverwrite="1"/>
#      <Problem>
#        <Parameter name="JacobianRequested" type="bool" value="1"/>
#        <Parameter name="StabilityAnalysisRequested" type="bool" value="1"/>
#      </Problem>
#      <Method name="Enhanced Newton" type="EnhancedNewton">
#        <Parameter name="Resolution" type="unsignedFloat" value="1e-009"/>
#        <Parameter name="Derivation Factor" type="unsignedFloat" value="0.001"/>
#        <Parameter name="Use Newton" type="bool" value="1"/>
#        <Parameter name="Use Integration" type="bool" value="1"/>
#        <Parameter name="Use Back Integration" type="bool" value="1"/>
#        <Parameter name="Accept Negative Concentrations" type="bool" value="0"/>
#        <Parameter name="Iteration Limit" type="unsignedInteger" value="50"/>
#        <Parameter name="Maximum duration for forward integration" type="unsignedFloat" value="1000000000"/>
#        <Parameter name="Maximum duration for backward integration" type="unsignedFloat" value="1000000"/>
#      </Method>
#    </Task>
#    <Task key="Task_15" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
#      <Report reference="Report_48" target="" append="false" confirmOverwrite="false" type="Deterministic(LSODA)" name="Deterministic (LSODA)"/>
#      <Problem type="Deterministic(LSODA)" name="Deterministic (LSODA)">
#        <Parameter name="StepNumber" type="unsignedInteger" value="50"/>
#        <Parameter name="StepSize" type="float" value="100"/>
#        <Parameter name="Duration" type="float" value="5000"/>
#        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
#        <Parameter name="OutputStartTime" type="float" value="0.0"/>
#        <Parameter name="Output Event" type="bool" value="false"/>
#        <Parameter name="Continue on Simultaneous Events" type="bool" value="0"/>
#      </Problem>
#      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
#        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
#        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-6"/>
#        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
#        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
#      </Method>
#    </Task>
#    <Task key="Task_16" name="Scan" type="scan" scheduled="false" updateModel="false">
#      <Report reference="Report_19" target="" append="0" confirmOverwrite="0"/>
#      <Problem>
#        <Parameter name="Subtask" type="unsignedInteger" value="5"/>
#        <ParameterGroup name="ScanItems">
#          <ParameterGroup name="ScanItem">
#            <Parameter name="Number of steps" type="unsignedInteger" value="10"/>
#            <Parameter name="Object" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[ligand receptor complex-endosome],Reference=InitialConcentration"/>
#            <Parameter name="Type" type="unsignedInteger" value="0"/>
#          </ParameterGroup>
#        </ParameterGroup>
#        <Parameter name="Output in subtask" type="bool" value="0"/>
#        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
#      </Problem>
#      <Method name="Scan Framework" type="ScanFramework">
#      </Method>
#    </Task>
#    <Task key="Task_17" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
#      <Report reference="Report_10" target="" append="1" confirmOverwrite="1"/>
#      <Problem>
#      </Problem>
#      <Method name="EFM Algorithm" type="EFMAlgorithm">
#      </Method>
#    </Task>
#    <Task key="Task_18" name="Optimization" type="optimization" scheduled="false" updateModel="false">
#      <Report reference="Report_11" target="" append="1" confirmOverwrite="1"/>
#      <Problem>
#        <Parameter name="Subtask" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
#        <ParameterText name="ObjectiveExpression" type="expression">
#          
#        </ParameterText>
#        <Parameter name="Maximize" type="bool" value="0"/>
#        <Parameter name="Randomize Start Values" type="bool" value="0"/>
#        <Parameter name="Calculate Statistics" type="bool" value="1"/>
#        <ParameterGroup name="OptimizationItemList">
#        </ParameterGroup>
#        <ParameterGroup name="OptimizationConstraintList">
#        </ParameterGroup>
#      </Problem>
#      <Method name="Random Search" type="RandomSearch">
#        <Parameter name="Number of Iterations" type="unsignedInteger" value="100000"/>
#        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
#        <Parameter name="Seed" type="unsignedInteger" value="0"/>
#      </Method>
#    </Task>
#    <Task key="Task_19" name="Parameter Estimation" type="parameterFitting" scheduled="true" updateModel="false">
#      <Report reference="Report_32" target="D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\VilarPEData.txt" append="0" confirmOverwrite="0"/>
#      <Problem>
#        <Parameter name="Maximize" type="bool" value="0"/>
#        <Parameter name="Randomize Start Values" type="bool" value="true"/>
#        <Parameter name="Calculate Statistics" type="bool" value="0"/>
#        <ParameterGroup name="OptimizationItemList">
#          <ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="4.20542"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRII],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.0251133"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kcd],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.779862"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ka],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.0001"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ligand],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.390589"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ki],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="6.44406"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRI],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.0308656"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kr],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="1.04518"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[alpha],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.268159"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[klid],Reference=InitialValue"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="38.8192950147"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[ligand receptor complex-endosome],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="7.62219"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 1-endosome],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.00155182"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 2],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.385859"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 2 endosome],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="22.9544"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 1],Reference=InitialConcentration"/></ParameterGroup><ParameterGroup name="FitItem"><ParameterGroup name="Affected Cross Validation Experiments"/><ParameterGroup name="Affected Experiments"/><Parameter name="LowerBound" type="cn" value="1e-06"/><Parameter name="StartValue" type="float" value="0.0001"/><Parameter name="UpperBound" type="cn" value="1000000"/><Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[ligand receptor complex-plasma membrane],Reference=InitialConcentration"/></ParameterGroup></ParameterGroup>
#        <ParameterGroup name="OptimizationConstraintList">
#        </ParameterGroup>
#        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
#        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
#        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
#        <ParameterGroup name="Experiment Set">
#          <ParameterGroup name="Experiment_0"><Parameter name="Data is Row Oriented" type="bool" value="1"/><Parameter name="Experiment Type" type="unsignedInteger" value="1"/><Parameter name="File Name" type="file" value="vilarTimeCourse.txt"/><Parameter name="First Row" type="unsignedInteger" value="1"/><Parameter name="Key" type="key" value="Experiment_0"/><Parameter name="Last Row" type="unsignedInteger" value="51"/><Parameter name="Normalize Weights per Experiment" type="bool" value="1"/><Parameter name="Number of Columns" type="unsignedInteger" value="16"/><ParameterGroup name="Object Map"><ParameterGroup name="0"><Parameter name="Role" type="unsignedInteger" value="3"/></ParameterGroup><ParameterGroup name="1"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[ligand receptor complex-endosome],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="2"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 2],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="3"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 1-endosome],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="4"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 2 endosome],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="5"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 1],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="6"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[ligand receptor complex-plasma membrane],Reference=Concentration"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="7"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRII],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="8"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kcd],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="9"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ka],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="10"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ligand],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="11"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ki],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="12"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRI],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="13"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kr],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="14"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[alpha],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup><ParameterGroup name="15"><Parameter name="Object CN" type="cn" value="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[klid],Reference=Value"/><Parameter name="Role" type="unsignedInteger" value="2"/></ParameterGroup></ParameterGroup><Parameter name="Row containing Names" type="unsignedInteger" value="1"/><Parameter name="Separator" type="string" value="&#9;"/><Parameter name="Weight Method" type="unsignedInteger" value="1"/></ParameterGroup></ParameterGroup>
#        <ParameterGroup name="Validation Set">
#          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
#          <Parameter name="Weight" type="unsignedFloat" value="1"/>
#        </ParameterGroup>
#      </Problem>
#      <Method name="Genetic Algorithm" type="GeneticAlgorithm"><Parameter name="Number of Generations" type="unsignedInteger" value="10"/><Parameter name="Population Size" type="unsignedInteger" value="10"/><Parameter name="Random Number Generator" type="unsignedInteger" value="1"/><Parameter name="Seed" type="unsignedInteger" value="0"/></Method></Task>
#    <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
#      <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
#      <Problem>
#        <Parameter name="Steady-State" type="key" value="Task_14"/>
#      </Problem>
#      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
#        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-009"/>
#        <Parameter name="Use Reeder" type="bool" value="1"/>
#        <Parameter name="Use Smallbone" type="bool" value="1"/>
#      </Method>
#    </Task>
#    <Task key="Task_21" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
#      <Report reference="Report_14" target="" append="1" confirmOverwrite="1"/>
#      <Problem>
#        <Parameter name="ExponentNumber" type="unsignedInteger" value="3"/>
#        <Parameter name="DivergenceRequested" type="bool" value="1"/>
#        <Parameter name="TransientTime" type="float" value="0"/>
#      </Problem>
#      <Method name="Wolf Method" type="WolfMethod">
#        <Parameter name="Orthonormalization Interval" type="unsignedFloat" value="1"/>
#        <Parameter name="Overall time" type="unsignedFloat" value="1000"/>
#        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
#        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
#        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
#      </Method>
#    </Task>
#    <Task key="Task_22" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
#      <Report reference="Report_15" target="" append="1" confirmOverwrite="1"/>
#      <Problem>
#        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
#        <Parameter name="StepSize" type="float" value="0.01"/>
#        <Parameter name="Duration" type="float" value="1"/>
#        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
#        <Parameter name="OutputStartTime" type="float" value="0"/>
#      </Problem>
#      <Method name="ILDM (LSODA,Deuflhard)" type="TimeScaleSeparation(ILDM,Deuflhard)">
#        <Parameter name="Deuflhard Tolerance" type="unsignedFloat" value="1e-006"/>
#      </Method>
#    </Task>
#    <Task key="Task_23" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
#      <Report reference="Report_16" target="" append="1" confirmOverwrite="1"/>
#      <Problem>
#        <Parameter name="SubtaskType" type="unsignedInteger" value="1"/>
#        <ParameterGroup name="TargetFunctions">
#          <Parameter name="SingleObject" type="cn" value=""/>
#          <Parameter name="ObjectListType" type="unsignedInteger" value="7"/>
#        </ParameterGroup>
#        <ParameterGroup name="ListOfVariables">
#          <ParameterGroup name="Variables">
#            <Parameter name="SingleObject" type="cn" value=""/>
#            <Parameter name="ObjectListType" type="unsignedInteger" value="41"/>
#          </ParameterGroup>
#        </ParameterGroup>
#      </Problem>
#      <Method name="Sensitivities Method" type="SensitivitiesMethod">
#        <Parameter name="Delta factor" type="unsignedFloat" value="0.001"/>
#        <Parameter name="Delta minimum" type="unsignedFloat" value="1e-012"/>
#      </Method>
#    </Task>
#    <Task key="Task_24" name="Moieties" type="moieties" scheduled="false" updateModel="false">
#      <Problem>
#      </Problem>
#      <Method name="Householder Reduction" type="Householder">
#      </Method>
#    </Task>
#    <Task key="Task_25" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
#      <Problem>
#        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
#        <Parameter name="StepSize" type="float" value="0.01"/>
#        <Parameter name="Duration" type="float" value="1"/>
#        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
#        <Parameter name="OutputStartTime" type="float" value="0"/>
#        <Parameter name="Output Event" type="bool" value="0"/>
#        <Parameter name="Continue on Simultaneous Events" type="bool" value="0"/>
#        <Parameter name="LimitCrossings" type="bool" value="0"/>
#        <Parameter name="NumCrossingsLimit" type="unsignedInteger" value="0"/>
#        <Parameter name="LimitOutTime" type="bool" value="0"/>
#        <Parameter name="LimitOutCrossings" type="bool" value="0"/>
#        <Parameter name="PositiveDirection" type="bool" value="1"/>
#        <Parameter name="NumOutCrossingsLimit" type="unsignedInteger" value="0"/>
#        <Parameter name="LimitUntilConvergence" type="bool" value="0"/>
#        <Parameter name="ConvergenceTolerance" type="float" value="1e-006"/>
#        <Parameter name="Threshold" type="float" value="0"/>
#        <Parameter name="DelayOutputUntilConvergence" type="bool" value="0"/>
#        <Parameter name="OutputConvergenceTolerance" type="float" value="1e-006"/>
#        <ParameterText name="TriggerExpression" type="expression">
#          
#        </ParameterText>
#        <Parameter name="SingleVariable" type="cn" value=""/>
#      </Problem>
#      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
#        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
#        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
#        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
#        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
#      </Method>
#    </Task>
#    <Task key="Task_26" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
#      <Report reference="Report_17" target="" append="1" confirmOverwrite="1"/>
#      <Problem>
#        <Parameter name="Steady-State" type="key" value="Task_14"/>
#      </Problem>
#      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
#      </Method>
#    </Task>
#  </ListOfTasks>
#  <ListOfReports>
#    <Report key="Report_9" name="Steady-State" taskType="steadyState" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Footer>
#        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
#      </Footer>
#    </Report>
#    <Report key="Report_10" name="Elementary Flux Modes" taskType="fluxMode" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Footer>
#        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
#      </Footer>
#    </Report>
#    <Report key="Report_11" name="Optimization" taskType="optimization" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Header>
#        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
#        <Object cn="String=\[Function Evaluations\]"/>
#        <Object cn="Separator=&#9;"/>
#        <Object cn="String=\[Best Value\]"/>
#        <Object cn="Separator=&#9;"/>
#        <Object cn="String=\[Best Parameters\]"/>
#      </Header>
#      <Body>
#        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
#        <Object cn="Separator=&#9;"/>
#        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
#        <Object cn="Separator=&#9;"/>
#        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
#      </Body>
#      <Footer>
#        <Object cn="String=&#10;"/>
#        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
#      </Footer>
#    </Report>
#    <Report key="Report_12" name="Parameter Estimation" taskType="parameterFitting" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Header>
#        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
#        <Object cn="String=\[Function Evaluations\]"/>
#        <Object cn="Separator=&#9;"/>
#        <Object cn="String=\[Best Value\]"/>
#        <Object cn="Separator=&#9;"/>
#        <Object cn="String=\[Best Parameters\]"/>
#      </Header>
#      <Body>
#        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
#        <Object cn="Separator=&#9;"/>
#        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
#        <Object cn="Separator=&#9;"/>
#        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
#      </Body>
#      <Footer>
#        <Object cn="String=&#10;"/>
#        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
#      </Footer>
#    </Report>
#    <Report key="Report_13" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Header>
#        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
#      </Header>
#      <Footer>
#        <Object cn="String=&#10;"/>
#        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
#      </Footer>
#    </Report>
#    <Report key="Report_14" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Header>
#        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
#      </Header>
#      <Footer>
#        <Object cn="String=&#10;"/>
#        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
#      </Footer>
#    </Report>
#    <Report key="Report_15" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Header>
#        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
#      </Header>
#      <Footer>
#        <Object cn="String=&#10;"/>
#        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
#      </Footer>
#    </Report>
#    <Report key="Report_16" name="Sensitivities" taskType="sensitivities" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Header>
#        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
#      </Header>
#      <Footer>
#        <Object cn="String=&#10;"/>
#        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
#      </Footer>
#    </Report>
#    <Report key="Report_17" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#9;" precision="6">
#      <Comment>
#        Automatically generated report.
#      </Comment>
#      <Header>
#        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Description"/>
#      </Header>
#      <Footer>
#        <Object cn="String=&#10;"/>
#        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Result"/>
#      </Footer>
#    </Report>
#    <Report taskType="Time-Course" separator="&#9;" precision="6" key="Report_48" name="Time-Course"><Comment/><Table printTitle="1"><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Reference=Time"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[ligand receptor complex-endosome],Reference=Concentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 2],Reference=Concentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 1-endosome],Reference=Concentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 2 endosome],Reference=Concentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 1],Reference=Concentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[ligand receptor complex-plasma membrane],Reference=Concentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRII],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kcd],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ka],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ligand],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ki],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRI],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kr],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[alpha],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[klid],Reference=InitialValue"/></Table></Report><Report taskType="parameterFitting" separator="&#9;" precision="6" key="Report_32" name="parameter_estimation"><Comment/><Table printTitle="1"><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[ligand receptor complex-endosome],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 2],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 1-endosome],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Endosome],Vector=Metabolites[Receptor 2 endosome],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[Receptor 1],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Compartments[Plasma membrane],Vector=Metabolites[ligand receptor complex-plasma membrane],Reference=InitialConcentration"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRII],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kcd],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ka],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ligand],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[ki],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[pRI],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[kr],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[alpha],Reference=InitialValue"/><Object cn="CN=Root,Model=Vilar2006_TGFbeta,Vector=Values[klid],Reference=InitialValue"/><Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/></Table></Report></ListOfReports>
#  <ListOfPlots>
#    <PlotSpecification name="Parameter Estimation Result" type="Plot2D" active="1">
#      <Parameter name="log X" type="bool" value="0"/>
#      <Parameter name="log Y" type="bool" value="0"/>
#      <ListOfPlotItems>
#        <PlotItem name="Experiment_0,[ligand receptor complex-endosome](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#FF0000"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[ligand receptor complex-endosome](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#FF0000"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[ligand receptor complex-endosome](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#FF0000"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 2](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#0000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 2](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#0000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 2](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#0000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 1-endosome](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00E600"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 1-endosome](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00E600"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 1-endosome](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00E600"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 2 endosome](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00BEF0"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 2 endosome](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00BEF0"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 2 endosome](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00BEF0"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 1](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 1](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[Receptor 1](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[ligand receptor complex-plasma membrane](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F0C800"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[ligand receptor complex-plasma membrane](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F0C800"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment_0,[ligand receptor complex-plasma membrane](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F0C800"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#      </ListOfPlotItems>
#    </PlotSpecification>
#    <PlotSpecification name="Parameter Estimation Result_1" type="Plot2D" active="1">
#      <Parameter name="log X" type="bool" value="0"/>
#      <Parameter name="log Y" type="bool" value="0"/>
#      <ListOfPlotItems>
#        <PlotItem name="Experiment,[ligand receptor complex-endosome](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#FF0000"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[ligand receptor complex-endosome](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#FF0000"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[ligand receptor complex-endosome](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#FF0000"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#0000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#0000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#0000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,Receptor 1-endosome.ParticleNumber(Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00E600"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,Receptor 1-endosome.ParticleNumber(Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00E600"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,Receptor 1-endosome.ParticleNumber(Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00E600"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2 endosome](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00BEF0"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2 endosome](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00BEF0"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2 endosome](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#00BEF0"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2 endosome](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2 endosome](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 2 endosome](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F000FF"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 1](Measured Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F0C800"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
#          <Parameter name="Line type" type="unsignedInteger" value="3"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Measured Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 1](Fitted Value)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F0C800"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Fitted Value"/>
#          </ListOfChannels>
#        </PlotItem>
#        <PlotItem name="Experiment,[Receptor 1](Weighted Error)" type="Curve2D">
#          <Parameter name="Color" type="string" value="#F0C800"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="2"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="after"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Weighted Error"/>
#          </ListOfChannels>
#        </PlotItem>
#      </ListOfPlotItems>
#    </PlotSpecification>
#    <PlotSpecification name="Progress of Fit" type="Plot2D" active="1">
#      <Parameter name="log X" type="bool" value="0"/>
#      <Parameter name="log Y" type="bool" value="1"/>
#      <ListOfPlotItems>
#        <PlotItem name="sum of squares" type="Curve2D">
#          <Parameter name="Color" type="string" value="auto"/>
#          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
#          <Parameter name="Line type" type="unsignedInteger" value="0"/>
#          <Parameter name="Line width" type="unsignedFloat" value="1"/>
#          <Parameter name="Recording Activity" type="string" value="during"/>
#          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
#          <ListOfChannels>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
#            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
#          </ListOfChannels>
#        </PlotItem>
#      </ListOfPlotItems>
#    </PlotSpecification>
#  </ListOfPlots>
#  <GUI>
#  </GUI>
#  <SBMLReference file="Vilar2006_TGFbeta.xml">
#    <SBMLMap SBMLid="Endosome" COPASIkey="Compartment_3"/>
#    <SBMLMap SBMLid="PM" COPASIkey="Compartment_1"/>
#    <SBMLMap SBMLid="RI" COPASIkey="Metabolite_1"/>
#    <SBMLMap SBMLid="RII" COPASIkey="Metabolite_3"/>
#    <SBMLMap SBMLid="RII_endo" COPASIkey="Metabolite_11"/>
#    <SBMLMap SBMLid="RI_endo" COPASIkey="Metabolite_9"/>
#    <SBMLMap SBMLid="alpha" COPASIkey="ModelValue_7"/>
#    <SBMLMap SBMLid="ka" COPASIkey="ModelValue_0"/>
#    <SBMLMap SBMLid="kcd" COPASIkey="ModelValue_2"/>
#    <SBMLMap SBMLid="ki" COPASIkey="ModelValue_4"/>
#    <SBMLMap SBMLid="klid" COPASIkey="ModelValue_3"/>
#    <SBMLMap SBMLid="kr" COPASIkey="ModelValue_6"/>
#    <SBMLMap SBMLid="lRIRII" COPASIkey="Metabolite_5"/>
#    <SBMLMap SBMLid="lRIRII_endo" COPASIkey="Metabolite_7"/>
#    <SBMLMap SBMLid="ligand" COPASIkey="ModelValue_1"/>
#    <SBMLMap SBMLid="pRI" COPASIkey="ModelValue_5"/>
#    <SBMLMap SBMLid="pRII" COPASIkey="ModelValue_8"/>
#    <SBMLMap SBMLid="v1" COPASIkey="Reaction_0"/>
#    <SBMLMap SBMLid="v10" COPASIkey="Reaction_9"/>
#    <SBMLMap SBMLid="v11" COPASIkey="Reaction_10"/>
#    <SBMLMap SBMLid="v12" COPASIkey="Reaction_11"/>
#    <SBMLMap SBMLid="v13" COPASIkey="Reaction_12"/>
#    <SBMLMap SBMLid="v2" COPASIkey="Reaction_1"/>
#    <SBMLMap SBMLid="v3" COPASIkey="Reaction_2"/>
#    <SBMLMap SBMLid="v4" COPASIkey="Reaction_3"/>
#    <SBMLMap SBMLid="v5" COPASIkey="Reaction_4"/>
#    <SBMLMap SBMLid="v6" COPASIkey="Reaction_5"/>
#    <SBMLMap SBMLid="v7" COPASIkey="Reaction_6"/>
#    <SBMLMap SBMLid="v8" COPASIkey="Reaction_7"/>
#    <SBMLMap SBMLid="v9" COPASIkey="Reaction_8"/>
#  </SBMLReference>
#</COPASI>
#
#'''
#
#     
#class InsertParametersTest(unittest.TestCase):
#
#    def setUp(self):
#        copasi_file=os.path.join(os.getcwd(),'VilarModel2006pycopitestModel.cps')
#        if os.path.isfile(copasi_file):
#            os.remove(copasi_file)
#        with open(copasi_file,'w') as f:
#            f.write(model_string)
#            
#        self.copasi_file=copasi_file
#        self.copasiML=PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
#        self.GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        self.insert_paraemter_options={}
#        
#        '''
#        simulate a time course for testing 
#        inputting of parameters
#        '''
# 
#        self.timecourse_report_name=os.path.join(os.path.dirname(self.copasi_file),'vilarTimeCourse.txt')
#
#        self.PE_report_name=os.path.join(os.path.dirname(self.copasi_file),'VilarPEData.txt')
#
#        if os.path.isfile(self.timecourse_report_name):
#            os.remove(self.timecourse_report_name)
#            
#            
#        '''
#        create time course. 
#        Prune time course headers
#        use time course in fit against model
#        Dont run time course via parameter estimation task
#        but setup a scan task with a repeat item
#        '''
#            
#        self.TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,StepSize=100,Plot='false',
#                                               Intervals=50,End=5000,
#                                               ReportName=self.timecourse_report_name,
#                                               GlobalQuantities=None)
#        PyCoTools.pycopi.PruneCopasiHeaders(self.timecourse_report_name,replace='true')
#        self.PE=PyCoTools.pycopi.ParameterEstimation(self.copasi_file,self.timecourse_report_name,
#                                                        Method='GeneticAlgorithm',
#                                                        NumberOfGenerations=1,
#                                                        PopulationSize=1,
#                                                        Plot='false')
#        self.PE.write_item_template()
#        self.PE.set_up()
#        self.S=PyCoTools.pycopi.Scan(self.copasi_file,ScanType='repeat',ReportType='parameter_estimation',
#                                        NumberOfSteps=4,Run='true')
#        
#        self.results_directory=os.path.join(os.path.dirname(self.copasi_file),'Results')
#        
#        self.PE_file=os.path.join(self.results_directory,os.path.split(self.S.kwargs['ReportName'])[1])
#
#        if os.path.isdir(self.results_directory)==False:
#            os.mkdir(self.results_directory)
#        
#        if os.path.isfile(self.PE_file):
#            os.remove(self.PE_file)
#            
#        shutil.copy(self.S.kwargs['ReportName'],self.PE_file)
#        
#        PyCoTools.pycopi.PruneCopasiHeaders(self.PE_file,replace='true')
#        self.df=pandas.read_csv(self.PE_file,sep='\t')
#        self.dct= pandas.read_csv(self.PE_file,sep='\t').to_dict()
#
#    def tearDown(self):
#        if os.path.isfile(self.copasi_file):
#            os.remove(self.copasi_file)
#
#            
#        for i in glob.glob('*.jpeg'):
#            os.remove(i)
#        
#        for i in glob.glob('*.txt'):
#            os.remove(i)
#            
#        for i in glob.glob('*.xlsx'):
#            os.remove(i)
#            
#        shutil.rmtree(self.results_directory)
#            
#
#    def test_from_file(self):
#        '''
#        insert parameters from a PE result file
#        '''
#        IP=PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               ParameterPath=self.PE_file,
#                                               Index=0,Save='overwrite')
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        input_parameters= IP.parameters
#        df=pandas.DataFrame.from_dict(GMQ.get_all_params_dict(),orient='index').transpose()
#        for i in IP.parameters:
#            for j in df:
#                if i==j:
#                    self.assertAlmostEqual(float(IP.parameters[i]),float(df[i]))
#                    
#    def test_from_folder(self):
#        '''
#        insert parameters from a folder of parameter estimation results files
#        '''
#        IP=PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               ParameterPath=self.results_directory,
#                                               Index=1,Save='overwrite') 
##        print IP.parameters
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        df=pandas.DataFrame.from_dict(GMQ.get_all_params_dict(),orient='index').transpose()
#        for i in IP.parameters:
#            for j in df:
#                if i==j:
#                    self.assertAlmostEqual(float(IP.parameters[i]),float(df[i]))
##
#    def test_from_df(self):
#        '''
#        insert parameters from a pandas dataframe
#        '''
#        IP=PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               DF=self.df,
#                                               Index=2,Save='overwrite') 
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        df=pandas.DataFrame.from_dict(GMQ.get_all_params_dict(),orient='index').transpose()
#        for i in IP.parameters:
#            for j in df:
#                if i==j:
#                    self.assertAlmostEqual(float(IP.parameters[i]),float(df[i]))
#
#    def test_from_dict(self):
#        '''
#        Insert parameters from a dictionary 
#        '''
#        metab= self.dct.keys()[0]
#        param=self.dct[metab][3]
#        dct={metab:param}
#        PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               ParameterDict=dct,
#                                               Save='overwrite') 
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        df=pandas.DataFrame.from_dict(GMQ.get_all_params_dict(),orient='index').transpose()
#        for i in df:
#            for j in dct:
#                if i==j:
#                    self.assertAlmostEqual(float(dct[i]),float(df[i]))
#                    
##=========================================================================
#
#
#
#'''
#Now we do the same thing but with a different model
#
#'''















model_string='''<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.16 (Build 104) (http://www.copasi.org) at 2016-11-09 10:17:11 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
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
  <Model key="Model_3" name="Goldbeter1995_CircClock" simulationType="time" timeUnit="h" volumeUnit="pl" areaUnit="m²" lengthUnit="m" quantityUnit="µmol" type="deterministic" avogadroConstant="6.02214179e+023">
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
                <vCard:Family>Le Novère</vCard:Family>
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
  <br />
  <p>To cite BioModels Database, please use:      <a href="http://www.ncbi.nlm.nih.gov/pubmed/20587024" target="_blank">Li C, Donizelli M, Rodriguez N, Dharuri H, Endler L, Chelliah V, Li L, He E, Henry A, Stefan MI, Snoep JL, Hucka M, Le Novère N, Laibe C (2010) BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models. BMC Syst Biol., 4:92.</a>
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
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0005737" />
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
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0005634" />
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
        <rdf:li rdf:resource="http://identifiers.org/chebi/CHEBI:33699" />
        <rdf:li rdf:resource="http://identifiers.org/kegg.compound/C00046" />
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
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663" />
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
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663" />
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
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663" />
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
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663" />
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
        <rdf:li rdf:resource="http://identifiers.org/uniprot/P07663" />
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
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006355" />
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0009299" />
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
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006412" />
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
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.11.1" />
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006468" />
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
        <rdf:li rdf:resource="http://identifiers.org/ec-code/3.1.3.16" />
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006470" />
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
        <rdf:li rdf:resource="http://identifiers.org/ec-code/2.7.11.1" />
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006468" />
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
        <rdf:li rdf:resource="http://identifiers.org/ec-code/3.1.3.16" />
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006470" />
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
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006606" />
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
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006611" />
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
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006402" />
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
        <rdf:li rdf:resource="http://identifiers.org/go/GO:0006402" />
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
      <Report reference="Report_18" target="" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="50"/>
        <Parameter name="StepSize" type="float" value="100"/>
        <Parameter name="Duration" type="float" value="5000"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Continue on Simultaneous Events" type="bool" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_16" name="Scan" type="scan" scheduled="true" updateModel="false">
      <Report reference="Report_19" target="VilarModel2006pycopitestModel_PE_results.txt" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="5"/>
        <ParameterGroup name="ScanItems">
          <ParameterGroup name="ScanItem">
            <Parameter name="Number of steps" type="unsignedInteger" value="4"/>
            <Parameter name="Object" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=InitialConcentration"/>
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
      <Report reference="Report_12" target="" append="0" confirmOverwrite="0"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="1"/>
        <Parameter name="Calculate Statistics" type="bool" value="0"/>
        <ParameterGroup name="OptimizationItemList">
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Kd,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.196905"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Vm,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="20813"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=K1,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="128708"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=V2,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1.38621e-006"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=KI,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="19.8721"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=Vs,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.000286224"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=V4,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.00297438"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=V3,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.20815"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=n,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.0137514"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=K4,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.0145912"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=K2,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.0072364"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm],ParameterGroup=Parameters,Parameter=k2,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.000226111"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=V1,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="6.73469e-005"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER],ParameterGroup=Parameters,Parameter=ks,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="93.0415"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=K3,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="12.2604"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus],ParameterGroup=Parameters,Parameter=k1,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="354984"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Vd,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="2.02091"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Km,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="0.9005530000000001"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=InitialConcentration"/>
            <Parameter name="StartValue" type="float" value="6646.32"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=InitialConcentration"/>
            <Parameter name="StartValue" type="float" value="6646.32"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=InitialConcentration"/>
            <Parameter name="StartValue" type="float" value="6646.32"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=InitialConcentration"/>
            <Parameter name="StartValue" type="float" value="6646.32"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="1e-06"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=InitialConcentration"/>
            <Parameter name="StartValue" type="float" value="6646.32"/>
            <Parameter name="UpperBound" type="cn" value="1000000"/>
          </ParameterGroup>
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
          <ParameterGroup name="Experiment_0">
            <Parameter name="Data is Row Oriented" type="bool" value="1"/>
            <Parameter name="Experiment Type" type="unsignedInteger" value="1"/>
            <Parameter name="File Name" type="file" value="vilarTimeCourse.txt"/>
            <Parameter name="First Row" type="unsignedInteger" value="1"/>
            <Parameter name="Key" type="key" value="Experiment_0"/>
            <Parameter name="Last Row" type="unsignedInteger" value="51"/>
            <Parameter name="Normalize Weights per Experiment" type="bool" value="1"/>
            <Parameter name="Number of Columns" type="unsignedInteger" value="8"/>
            <ParameterGroup name="Object Map">
              <ParameterGroup name="0">
                <Parameter name="Role" type="unsignedInteger" value="3"/>
              </ParameterGroup>
              <ParameterGroup name="1">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="2">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="3">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="4">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="5">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="6">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="7">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
            </ParameterGroup>
            <Parameter name="Row containing Names" type="unsignedInteger" value="1"/>
            <Parameter name="Separator" type="string" value="&#x09;"/>
            <Parameter name="Weight Method" type="unsignedInteger" value="1"/>
          </ParameterGroup>
        </ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
        </ParameterGroup>
      </Problem>
      <Method name="Genetic Algorithm" type="GeneticAlgorithm">
        <Parameter name="Number of Generations" type="unsignedInteger" value="1"/>
        <Parameter name="Population Size" type="unsignedInteger" value="1"/>
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
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Reference=Time"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=Concentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=Concentration"/>
      </Table>
    </Report>
    <Report key="Report_19" name="parameter_estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
      </Comment>
      <Table printTitle="1">
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[monophosphorylated PER],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[total PER],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[PER mRNA],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[NUCLEUS],Vector=Metabolites[nuclear PER],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[default],Vector=Metabolites[EmptySet],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[unphosphorylated PER],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Compartments[CYTOPLASM],Vector=Metabolites[biphosphorylated PER],Reference=InitialConcentration"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Kd,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Vm,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=K1,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=V2,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=KI,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=Vs,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=V4,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=V3,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[transcription of PER],ParameterGroup=Parameters,Parameter=n,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the second PER phosphate],ParameterGroup=Parameters,Parameter=K4,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[removal of the first PER phosphate],ParameterGroup=Parameters,Parameter=K2,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the cytoplasm],ParameterGroup=Parameters,Parameter=k2,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[first phosphorylation of PER],ParameterGroup=Parameters,Parameter=V1,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translation of PER],ParameterGroup=Parameters,Parameter=ks,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[second phosphorylation of PER],ParameterGroup=Parameters,Parameter=K3,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[translocation of PER to the nucleus],ParameterGroup=Parameters,Parameter=k1,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER],ParameterGroup=Parameters,Parameter=Vd,Reference=Value"/>
        <Object cn="CN=Root,Model=Goldbeter1995_CircClock,Vector=Reactions[degradation of PER mRNA],ParameterGroup=Parameters,Parameter=Km,Reference=Value"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
      </Table>
    </Report>
  </ListOfReports>
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

'''

'''
It appears that this is not a good strategy for testing the input parameters
lass. Instead, make up some numbers, write to file and test using this data
specific for the test model!
'''
class InsertParametersTest(unittest.TestCase):

    def setUp(self):
        copasi_file=os.path.join(os.getcwd(),'VilarModel2006pycopitestModel.cps')
        if os.path.isfile(copasi_file):
            os.remove(copasi_file)
        with open(copasi_file,'w') as f:
            f.write(model_string)
            
        self.copasi_file=copasi_file
        self.copasiML=PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
        self.GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
        
        '''
        simulate a time course for testing 
        inputting of parameters
        '''
 
        self.timecourse_report_name=os.path.join(os.path.dirname(self.copasi_file),'vilarTimeCourse.txt')

        self.PE_report_name=os.path.join(os.path.dirname(self.copasi_file),'VilarPEData.txt')

        if os.path.isfile(self.timecourse_report_name):
            os.remove(self.timecourse_report_name)
            
            
        '''
        create time course. 
        Prune time course headers
        use time course in fit against model
        Dont run time course via parameter estimation task
        but setup a scan task with a repeat item
        '''
            
        self.TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,StepSize=100,Plot='false',
                                               Intervals=50,End=5000,
                                               ReportName=self.timecourse_report_name,
                                               GlobalQuantities=None)
        PyCoTools.pycopi.PruneCopasiHeaders(self.timecourse_report_name,replace='true')
        self.PE=PyCoTools.pycopi.ParameterEstimation(self.copasi_file,self.timecourse_report_name,
                                                        Method='GeneticAlgorithm',
                                                        NumberOfGenerations=5,
                                                        PopulationSize=5,
                                                        Plot='false')
        self.PE.write_item_template()
        self.PE.set_up()
        self.S=PyCoTools.pycopi.Scan(self.copasi_file,ScanType='repeat',
                                     ReportType='parameter_estimation',
                                     ReportName=self.PE_report_name,
                                     NumberOfSteps=2,Run='true')
#        
#        self.results_directory=os.path.join(os.path.dirname(self.copasi_file),'Results')
##        
#        self.PE_file=os.path.join(self.results_directory,os.path.split(self.S.kwargs['ReportName'])[1])
#
#        if os.path.isdir(self.results_directory)==False:
#            os.mkdir(self.results_directory)
#        
#        if os.path.isfile(self.PE_file):
#            os.remove(self.PE_file)
#            
#        shutil.copy(self.S.kwargs['ReportName'],self.PE_file)
#        
#        PyCoTools.pycopi.PruneCopasiHeaders(self.PE_file,replace='true')
#        self.df=pandas.read_csv(self.PE_file,sep='\t')
#        self.dct= pandas.read_csv(self.PE_file,sep='\t').to_dict()
                                                        
                                                        
    def tearDown(self):
#        if os.path.isfile(self.copasi_file):
#            os.remove(self.copasi_file)
        print self.copasi_file

            
#        for i in glob.glob('*.jpeg'):
#            os.remove(i)
#        
#        for i in glob.glob('*.txt'):
#            os.remove(i)
#            
#        for i in glob.glob('*.xlsx'):
#            os.remove(i)
            
#        shutil.rmtree(self.results_directory)
            

#    def test_global_from_file(self):
#        '''
#        insert global parameters from a PE result file
#        '''
#        IP=PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               ParameterPath=self.PE_report_name,
#                                               Index=0,Save='overwrite')
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        input_parameters= IP.parameters
#        
#        for i in GMQ.get_global_quantities():
#            for j in input_parameters:
#                print i,j
#                if i==j:
#                    
#                    in_PE_file= float(input_parameters[i])
#                    in_est_data=float(GMQ.get_global_quantities()[i])
#                    print in_PE_file,in_est_data
#                    self.assertAlmostEqual(in_PE_file,in_est_data)
##                    
#                    
#    def test_local_from_file(self):
#        '''
#        insert parameters from a PE result file
#        '''
#        IP=PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               ParameterPath=self.PE_report_name,
#                                               Index=0,Save='overwrite')
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        input_parameters= IP.parameters
#        
#        for i in GMQ.get_local_parameters():
#            for j in input_parameters:
#                if i==j:
#                    in_PE_file= float(input_parameters[i])
#                    in_est_data=float(GMQ.get_local_parameters()[i])
#                    self.assertAlmostEqual(in_PE_file,in_est_data)
#                    
#    def test_IC_from_file(self):
#        '''
#        insert parameters from a PE result file
#        '''
#        IP=PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               ParameterPath=self.PE_file,
#                                               Index=0)
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        m= pandas.DataFrame.from_csv(self.PE_report_name,sep='\t',index_col=None)#.iloc[0]['unphosphorylated PER']

#        for i in GMQ.get_metabolites():
#            for j in input_parameters:
#                if i==j:
#                    in_PE_file= float(input_parameters[i])
#                    if GMQ.QuantityType=='concentration':
#                        in_est_data=float(GMQ.get_metabolites()[i]['concentration'])
#                    else:
#                        in_est_data=float(GMQ.get_metabolites()[i]['particle_numbers'])
#                    self.assertAlmostEqual(in_PE_file,in_est_data)                                        
#                    
                    
#                    self.assertAlmostEqual( GMQ.get_global_quantities()[i],float(input_parameters[i]))
#            print i,GMQ.get_global_quantities()[i]
#            print IP.parameters

#        print df,'\n',IP.parameters
#        
#        print IP.parameters['monophosphorylated PER']
#        for i in IP.parameters:
#            for j in df:
#                if i==j:
#                    u=float(IP.parameters[i])
#                    o=float(df[i])
#                    print i
#                    self.assertAlmostEqual(u,o)


#                    self.assertEqual(u,o)
#                if i==j:
#                    print IP.parameters[i]
##                    GMQ.convert_molar_to_particles(float(IP.parameters[i]),GMQ.get_quantity_units(),float(GMQ.get_IC_cns()[i]['compartment_volume']))
                    


#                    self.assertAlmostEqual(round(float(p),4),round(float(df[i]),4))
                    
#    def test_from_folder(self):
#        '''
#        insert parameters from a folder of parameter estimation results files
#        '''
#        IP=PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               ParameterPath=self.results_directory,
#                                               Index=1,Save='overwrite') 
##        print IP.parameters
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        df=pandas.DataFrame.from_dict(GMQ.get_all_params_dict(),orient='index').transpose()
#        for i in IP.parameters:
#            for j in df:
#                if i==j:
#                    self.assertAlmostEqual(float(IP.parameters[i]),float(df[i]))
##
#    def test_from_df(self):
#        '''
#        insert parameters from a pandas dataframe
#        '''
#        IP=PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               DF=self.df,
#                                               Index=2,Save='overwrite') 
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        df=pandas.DataFrame.from_dict(GMQ.get_all_params_dict(),orient='index').transpose()
#        for i in IP.parameters:
#            for j in df:
#                if i==j:
#                    self.assertAlmostEqual(float(IP.parameters[i]),float(df[i]))
#
#    def test_from_dict(self):
#        '''
#        Insert parameters from a dictionary 
#        '''
#        metab= self.dct.keys()[0]
#        param=self.dct[metab][3]
#        dct={metab:param}
#        PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                               ParameterDict=dct,
#                                               Save='overwrite') 
#        GMQ=PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        df=pandas.DataFrame.from_dict(GMQ.get_all_params_dict(),orient='index').transpose()
#        for i in df:
#            for j in dct:
#                if i==j:
#                    self.assertAlmostEqual(float(dct[i]),float(df[i]))
#                    
                    
                    
                    
                    
                    
                    
        
if __name__=='__main__':
    unittest.main()