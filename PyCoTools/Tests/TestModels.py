# -*-coding: utf-8 -*-


class TestModels():
    @staticmethod
    def get_model1():
        return '''<?xml version="1.0" encoding="UTF-8"?>
        <!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-06-17 11:41:50 UTC -->
        <?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
        <COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="19" versionDevel="140" copasiSourcesModified="0">
          <ListOfFunctions>
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
          </ListOfFunctions>
          <Model key="Model_3" name="New Model" simulationType="time" timeUnit="s" volumeUnit="ml" areaUnit="m²" lengthUnit="m" quantityUnit="mmol" type="deterministic" avogadroConstant="6.022140857e+023">
            <MiriamAnnotation>
        <rdf:RDF
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
          <rdf:Description rdf:about="#Model_3">
            <dcterms:created>
              <rdf:Description>
                <dcterms:W3CDTF>2017-06-17T12:37:23Z</dcterms:W3CDTF>
              </rdf:Description>
            </dcterms:created>
          </rdf:Description>
        </rdf:RDF>

            </MiriamAnnotation>
            <ListOfCompartments>
              <Compartment key="Compartment_1" name="nuc" simulationType="fixed" dimensionality="3">
              </Compartment>
              <Compartment key="Compartment_3" name="Cyt" simulationType="fixed" dimensionality="3">
              </Compartment>
            </ListOfCompartments>
            <ListOfMetabolites>
              <Metabolite key="Metabolite_1" name="A" simulationType="reactions" compartment="Compartment_1">
              </Metabolite>
              <Metabolite key="Metabolite_3" name="B" simulationType="reactions" compartment="Compartment_1">
              </Metabolite>
              <Metabolite key="Metabolite_5" name="C" simulationType="reactions" compartment="Compartment_1">
              </Metabolite>
              <Metabolite key="Metabolite_7" name="D" simulationType="reactions" compartment="Compartment_1">
              </Metabolite>
              <Metabolite key="Metabolite_9" name="E" simulationType="reactions" compartment="Compartment_1">
              </Metabolite>
              <Metabolite key="Metabolite_11" name="F" simulationType="reactions" compartment="Compartment_1">
              </Metabolite>
            </ListOfMetabolites>
            <ListOfModelValues>
              <ModelValue key="ModelValue_0" name="assignment_global_var" simulationType="assignment">
                <MiriamAnnotation>
        <rdf:RDF
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
          <rdf:Description rdf:about="#ModelValue_0">
            <dcterms:created>
              <rdf:Description>
                <dcterms:W3CDTF>2017-06-17T12:38:33Z</dcterms:W3CDTF>
              </rdf:Description>
            </dcterms:created>
          </rdf:Description>
        </rdf:RDF>

                </MiriamAnnotation>
                <Expression>
                  &lt;CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration>+&lt;CN=Root,Model=New Model,Vector=Values[three],Reference=Value>
                </Expression>
              </ModelValue>
              <ModelValue key="ModelValue_1" name="two" simulationType="fixed">
              </ModelValue>
              <ModelValue key="ModelValue_2" name="three" simulationType="fixed">
              </ModelValue>
            </ListOfModelValues>
            <ListOfReactions>
              <Reaction key="Reaction_0" name="reaction" reversible="false" fast="false">
                <ListOfSubstrates>
                  <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
                </ListOfSubstrates>
                <ListOfProducts>
                  <Product metabolite="Metabolite_3" stoichiometry="1"/>
                </ListOfProducts>
                <ListOfConstants>
                  <Constant key="Parameter_4435" name="k1" value="0.1"/>
                </ListOfConstants>
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=New Model,Vector=Compartments[nuc]">
                  <ListOfCallParameters>
                    <CallParameter functionParameter="FunctionParameter_81">
                      <SourceParameter reference="Parameter_4435"/>
                    </CallParameter>
                    <CallParameter functionParameter="FunctionParameter_79">
                      <SourceParameter reference="Metabolite_1"/>
                    </CallParameter>
                  </ListOfCallParameters>
                </KineticLaw>
              </Reaction>
              <Reaction key="Reaction_1" name="reaction_1" reversible="false" fast="false">
                <ListOfSubstrates>
                  <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
                </ListOfSubstrates>
                <ListOfProducts>
                  <Product metabolite="Metabolite_5" stoichiometry="1"/>
                </ListOfProducts>
                <ListOfConstants>
                  <Constant key="Parameter_4436" name="k1" value="0.1"/>
                </ListOfConstants>
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=New Model,Vector=Compartments[nuc]">
                  <ListOfCallParameters>
                    <CallParameter functionParameter="FunctionParameter_81">
                      <SourceParameter reference="Parameter_4436"/>
                    </CallParameter>
                    <CallParameter functionParameter="FunctionParameter_79">
                      <SourceParameter reference="Metabolite_3"/>
                    </CallParameter>
                  </ListOfCallParameters>
                </KineticLaw>
              </Reaction>
              <Reaction key="Reaction_2" name="reaction_2" reversible="false" fast="false">
                <ListOfSubstrates>
                  <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
                </ListOfSubstrates>
                <ListOfProducts>
                  <Product metabolite="Metabolite_7" stoichiometry="1"/>
                </ListOfProducts>
                <ListOfConstants>
                  <Constant key="Parameter_4437" name="k1" value="0.1"/>
                </ListOfConstants>
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=New Model,Vector=Compartments[nuc]">
                  <ListOfCallParameters>
                    <CallParameter functionParameter="FunctionParameter_81">
                      <SourceParameter reference="Parameter_4437"/>
                    </CallParameter>
                    <CallParameter functionParameter="FunctionParameter_79">
                      <SourceParameter reference="Metabolite_5"/>
                    </CallParameter>
                  </ListOfCallParameters>
                </KineticLaw>
              </Reaction>
              <Reaction key="Reaction_3" name="reaction_3" reversible="false" fast="false">
                <ListOfSubstrates>
                  <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
                </ListOfSubstrates>
                <ListOfProducts>
                  <Product metabolite="Metabolite_9" stoichiometry="1"/>
                </ListOfProducts>
                <ListOfConstants>
                  <Constant key="Parameter_4438" name="k1" value="0.1"/>
                </ListOfConstants>
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=New Model,Vector=Compartments[nuc]">
                  <ListOfCallParameters>
                    <CallParameter functionParameter="FunctionParameter_81">
                      <SourceParameter reference="Parameter_4438"/>
                    </CallParameter>
                    <CallParameter functionParameter="FunctionParameter_79">
                      <SourceParameter reference="Metabolite_7"/>
                    </CallParameter>
                  </ListOfCallParameters>
                </KineticLaw>
              </Reaction>
              <Reaction key="Reaction_4" name="reaction_4" reversible="false" fast="false">
                <ListOfSubstrates>
                  <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
                </ListOfSubstrates>
                <ListOfProducts>
                  <Product metabolite="Metabolite_11" stoichiometry="1"/>
                </ListOfProducts>
                <ListOfConstants>
                  <Constant key="Parameter_4439" name="k1" value="0.1"/>
                </ListOfConstants>
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,Model=New Model,Vector=Compartments[nuc]">
                  <ListOfCallParameters>
                    <CallParameter functionParameter="FunctionParameter_81">
                      <SourceParameter reference="Parameter_4439"/>
                    </CallParameter>
                    <CallParameter functionParameter="FunctionParameter_79">
                      <SourceParameter reference="Metabolite_9"/>
                    </CallParameter>
                  </ListOfCallParameters>
                </KineticLaw>
              </Reaction>
            </ListOfReactions>
            <ListOfEvents>
              <Event key="Event_0" name="event" fireAtInitialTime="0" persistentTrigger="0">
                <MiriamAnnotation>
        <rdf:RDF
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
          <rdf:Description rdf:about="#Event_0">
            <dcterms:created>
              <rdf:Description>
                <dcterms:W3CDTF>2017-06-17T12:39:41Z</dcterms:W3CDTF>
              </rdf:Description>
            </dcterms:created>
          </rdf:Description>
        </rdf:RDF>

                </MiriamAnnotation>
                <TriggerExpression>
                  &lt;CN=Root,Model=New Model,Reference=Time> > 50
                </TriggerExpression>
                <ListOfAssignments>
                  <Assignment targetKey="Metabolite_1">
                    <Expression>
                      597641
                    </Expression>
                  </Assignment>
                </ListOfAssignments>
              </Event>
            </ListOfEvents>
            <ListOfModelParameterSets activeSet="ModelParameterSet_1">
              <ModelParameterSet key="ModelParameterSet_1" name="Initial State">
                <ModelParameterGroup cn="String=Initial Time" type="Group">
                  <ModelParameter cn="CN=Root,Model=New Model" value="0" type="Model" simulationType="time"/>
                </ModelParameterGroup>
                <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Compartments[nuc]" value="1" type="Compartment" simulationType="fixed"/>
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Compartments[Cyt]" value="5" type="Compartment" simulationType="fixed"/>
                </ModelParameterGroup>
                <ModelParameterGroup cn="String=Initial Species Values" type="Group">
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A]" value="6.022140856999986e+020" type="Species" simulationType="reactions"/>
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[B]" value="6.022140857000001e+021" type="Species" simulationType="reactions"/>
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[C]" value="6.022140857000001e+022" type="Species" simulationType="reactions"/>
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[D]" value="6.022140856999989e+023" type="Species" simulationType="reactions"/>
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[E]" value="6.022140856999983e+024" type="Species" simulationType="reactions"/>
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[F]" value="6.022140857000001e+025" type="Species" simulationType="reactions"/>
                </ModelParameterGroup>
                <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Values[assignment_global_var]" value="1.999999999999998" type="ModelValue" simulationType="assignment"/>
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Values[two]" value="50" type="ModelValue" simulationType="fixed"/>
                  <ModelParameter cn="CN=Root,Model=New Model,Vector=Values[three]" value="1" type="ModelValue" simulationType="fixed"/>
                </ModelParameterGroup>
                <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
                  <ModelParameterGroup cn="CN=Root,Model=New Model,Vector=Reactions[reaction]" type="Reaction">
                    <ModelParameter cn="CN=Root,Model=New Model,Vector=Reactions[reaction],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </ModelParameterGroup>
                  <ModelParameterGroup cn="CN=Root,Model=New Model,Vector=Reactions[reaction_1]" type="Reaction">
                    <ModelParameter cn="CN=Root,Model=New Model,Vector=Reactions[reaction_1],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </ModelParameterGroup>
                  <ModelParameterGroup cn="CN=Root,Model=New Model,Vector=Reactions[reaction_2]" type="Reaction">
                    <ModelParameter cn="CN=Root,Model=New Model,Vector=Reactions[reaction_2],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </ModelParameterGroup>
                  <ModelParameterGroup cn="CN=Root,Model=New Model,Vector=Reactions[reaction_3]" type="Reaction">
                    <ModelParameter cn="CN=Root,Model=New Model,Vector=Reactions[reaction_3],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </ModelParameterGroup>
                  <ModelParameterGroup cn="CN=Root,Model=New Model,Vector=Reactions[reaction_4]" type="Reaction">
                    <ModelParameter cn="CN=Root,Model=New Model,Vector=Reactions[reaction_4],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </ModelParameterGroup>
                </ModelParameterGroup>
              </ModelParameterSet>
            </ListOfModelParameterSets>
            <StateTemplate>
              <StateTemplateVariable objectReference="Model_3"/>
              <StateTemplateVariable objectReference="Metabolite_3"/>
              <StateTemplateVariable objectReference="Metabolite_7"/>
              <StateTemplateVariable objectReference="Metabolite_9"/>
              <StateTemplateVariable objectReference="Metabolite_5"/>
              <StateTemplateVariable objectReference="Metabolite_1"/>
              <StateTemplateVariable objectReference="Metabolite_11"/>
              <StateTemplateVariable objectReference="ModelValue_0"/>
              <StateTemplateVariable objectReference="Compartment_1"/>
              <StateTemplateVariable objectReference="Compartment_3"/>
              <StateTemplateVariable objectReference="ModelValue_1"/>
              <StateTemplateVariable objectReference="ModelValue_2"/>
            </StateTemplate>
            <InitialState type="initialState">
              0 6.022140857000001e+021 6.022140856999989e+023 6.022140856999983e+024 6.022140857000001e+022 6.022140856999986e+020 6.022140857000001e+025 1.999999999999998 1 5 50 1 
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
              <Problem>
                <Parameter name="AutomaticStepSize" type="bool" value="0"/>
                <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
                <Parameter name="StepSize" type="float" value="10"/>
                <Parameter name="Duration" type="float" value="1000"/>
                <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
                <Parameter name="OutputStartTime" type="float" value="0"/>
                <Parameter name="Output Event" type="bool" value="0"/>
                <Parameter name="Start in Steady State" type="bool" value="0"/>
              </Problem>
              <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
                <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
                <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
                <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
                <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
                <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
              </Method>
            </Task>
            <Task key="Task_16" name="Scan" type="scan" scheduled="false" updateModel="false">
              <Problem>
                <Parameter name="Subtask" type="unsignedInteger" value="1"/>
                <ParameterGroup name="ScanItems">
                </ParameterGroup>
                <Parameter name="Output in subtask" type="bool" value="1"/>
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
                  <Parameter name="Weight" type="unsignedFloat" value="1"/>
                  <Parameter name="Threshold" type="unsignedInteger" value="5"/>
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
                <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-009"/>
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
                  <ParameterGroup name="Variables">
                    <Parameter name="SingleObject" type="cn" value=""/>
                    <Parameter name="ObjectListType" type="unsignedInteger" value="0"/>
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
          </ListOfReports>
          <ListOfPlots>
            <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
              <Parameter name="log X" type="bool" value="0"/>
              <Parameter name="log Y" type="bool" value="0"/>
              <ListOfPlotItems>
                <PlotItem name="[A]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,Model=New Model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration"/>
                  </ListOfChannels>
                </PlotItem>
                <PlotItem name="[B]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,Model=New Model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[B],Reference=Concentration"/>
                  </ListOfChannels>
                </PlotItem>
                <PlotItem name="[C]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,Model=New Model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[C],Reference=Concentration"/>
                  </ListOfChannels>
                </PlotItem>
                <PlotItem name="[D]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,Model=New Model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[D],Reference=Concentration"/>
                  </ListOfChannels>
                </PlotItem>
                <PlotItem name="[E]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,Model=New Model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[E],Reference=Concentration"/>
                  </ListOfChannels>
                </PlotItem>
                <PlotItem name="[F]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,Model=New Model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,Model=New Model,Vector=Compartments[nuc],Vector=Metabolites[F],Reference=Concentration"/>
                  </ListOfChannels>
                </PlotItem>
                <PlotItem name="Values[assignment_global_var]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,Model=New Model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,Model=New Model,Vector=Values[assignment_global_var],Reference=Value"/>
                  </ListOfChannels>
                </PlotItem>
              </ListOfPlotItems>
            </PlotSpecification>
          </ListOfPlots>
          <GUI>
          </GUI>
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
        '''
