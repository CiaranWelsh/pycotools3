# -*-coding: utf-8 -*-


class Testmodels():
    @staticmethod
    def get_model1():
        return '''<?xml version="1.0" encoding="UTF-8"?>
        <!-- generated with COPASI 4.19 (Build 140) (http://www.copasi.org) at 2017-06-17 11:41:50 UTC -->
        <?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
        <COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="19" versionDevel="140" copasiSourcesModified="0">
          <ListOfFunctions>
            <Function key="Function_13" name="Mass action (irreversible)" type="MassAction" reversible="false">
              <MiriamAnnotation>
        <rdf:Rdf xmlns:CopasiMT="http://www.copasi.org/Rdf/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
           <rdf:Description rdf:about="#Function_13">
           <CopasiMT:is rdf:resource="urn:miriam:obo.sbo:SBO:0000041" />
           </rdf:Description>
           </rdf:Rdf>
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
          <model key="model_3" name="New model" simulationType="time" timeUnit="s" volumeUnit="ml" areaUnit="m²" lengthUnit="m" quantityUnit="mmol" type="deterministic" avogadroConstant="6.022140857e+023">
            <MiriamAnnotation>
        <rdf:Rdf
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
          <rdf:Description rdf:about="#model_3">
            <dcterms:created>
              <rdf:Description>
                <dcterms:W3CDTF>2017-06-17T12:37:23Z</dcterms:W3CDTF>
              </rdf:Description>
            </dcterms:created>
          </rdf:Description>
        </rdf:Rdf>

            </MiriamAnnotation>
            <ListOfCompartments>
              <Compartment key="Compartment_1" name="nuc" simulationType="fixed" dimensionality="3">
              </Compartment>
              <Compartment key="Compartment_3" name="Cyt" simulationType="fixed" dimensionality="3">
              </Compartment>
            </ListOfCompartments>
            <ListOfmetabolites>
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
            </ListOfmetabolites>
            <ListOfmodelValues>
              <modelValue key="modelValue_0" name="assignment_global_var" simulationType="assignment">
                <MiriamAnnotation>
        <rdf:Rdf
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
          <rdf:Description rdf:about="#modelValue_0">
            <dcterms:created>
              <rdf:Description>
                <dcterms:W3CDTF>2017-06-17T12:38:33Z</dcterms:W3CDTF>
              </rdf:Description>
            </dcterms:created>
          </rdf:Description>
        </rdf:Rdf>

                </MiriamAnnotation>
                <Expression>
                  &lt;CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[A],Reference=Concentration>+&lt;CN=Root,model=New model,Vector=Values[three],Reference=Value>
                </Expression>
              </modelValue>
              <modelValue key="modelValue_1" name="two" simulationType="fixed">
              </modelValue>
              <modelValue key="modelValue_2" name="three" simulationType="fixed">
              </modelValue>
            </ListOfmodelValues>
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
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,model=New model,Vector=Compartments[nuc]">
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
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,model=New model,Vector=Compartments[nuc]">
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
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,model=New model,Vector=Compartments[nuc]">
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
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,model=New model,Vector=Compartments[nuc]">
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
                <KineticLaw function="Function_13" unitType="Default" scalingCompartment="CN=Root,model=New model,Vector=Compartments[nuc]">
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
        <rdf:Rdf
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
          <rdf:Description rdf:about="#Event_0">
            <dcterms:created>
              <rdf:Description>
                <dcterms:W3CDTF>2017-06-17T12:39:41Z</dcterms:W3CDTF>
              </rdf:Description>
            </dcterms:created>
          </rdf:Description>
        </rdf:Rdf>

                </MiriamAnnotation>
                <TriggerExpression>
                  &lt;CN=Root,model=New model,Reference=Time> > 50
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
            <ListOfmodelParameterSets activeSet="modelParameterSet_1">
              <modelParameterSet key="modelParameterSet_1" name="Initial State">
                <modelParameterGroup cn="String=Initial Time" type="Group">
                  <modelParameter cn="CN=Root,model=New model" value="0" type="model" simulationType="time"/>
                </modelParameterGroup>
                <modelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
                  <modelParameter cn="CN=Root,model=New model,Vector=Compartments[nuc]" value="1" type="Compartment" simulationType="fixed"/>
                  <modelParameter cn="CN=Root,model=New model,Vector=Compartments[Cyt]" value="5" type="Compartment" simulationType="fixed"/>
                </modelParameterGroup>
                <modelParameterGroup cn="String=Initial Species Values" type="Group">
                  <modelParameter cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[A]" value="6.022140856999986e+020" type="Species" simulationType="reactions"/>
                  <modelParameter cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[B]" value="6.022140857000001e+021" type="Species" simulationType="reactions"/>
                  <modelParameter cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[C]" value="6.022140857000001e+022" type="Species" simulationType="reactions"/>
                  <modelParameter cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[D]" value="6.022140856999989e+023" type="Species" simulationType="reactions"/>
                  <modelParameter cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[E]" value="6.022140856999983e+024" type="Species" simulationType="reactions"/>
                  <modelParameter cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[F]" value="6.022140857000001e+025" type="Species" simulationType="reactions"/>
                </modelParameterGroup>
                <modelParameterGroup cn="String=Initial Global Quantities" type="Group">
                  <modelParameter cn="CN=Root,model=New model,Vector=Values[assignment_global_var]" value="1.999999999999998" type="modelValue" simulationType="assignment"/>
                  <modelParameter cn="CN=Root,model=New model,Vector=Values[two]" value="50" type="modelValue" simulationType="fixed"/>
                  <modelParameter cn="CN=Root,model=New model,Vector=Values[three]" value="1" type="modelValue" simulationType="fixed"/>
                </modelParameterGroup>
                <modelParameterGroup cn="String=Kinetic Parameters" type="Group">
                  <modelParameterGroup cn="CN=Root,model=New model,Vector=Reactions[reaction]" type="Reaction">
                    <modelParameter cn="CN=Root,model=New model,Vector=Reactions[reaction],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </modelParameterGroup>
                  <modelParameterGroup cn="CN=Root,model=New model,Vector=Reactions[reaction_1]" type="Reaction">
                    <modelParameter cn="CN=Root,model=New model,Vector=Reactions[reaction_1],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </modelParameterGroup>
                  <modelParameterGroup cn="CN=Root,model=New model,Vector=Reactions[reaction_2]" type="Reaction">
                    <modelParameter cn="CN=Root,model=New model,Vector=Reactions[reaction_2],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </modelParameterGroup>
                  <modelParameterGroup cn="CN=Root,model=New model,Vector=Reactions[reaction_3]" type="Reaction">
                    <modelParameter cn="CN=Root,model=New model,Vector=Reactions[reaction_3],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </modelParameterGroup>
                  <modelParameterGroup cn="CN=Root,model=New model,Vector=Reactions[reaction_4]" type="Reaction">
                    <modelParameter cn="CN=Root,model=New model,Vector=Reactions[reaction_4],ParameterGroup=Parameters,Parameter=k1" value="0.1" type="ReactionParameter" simulationType="fixed"/>
                  </modelParameterGroup>
                </modelParameterGroup>
              </modelParameterSet>
            </ListOfmodelParameterSets>
            <StateTemplate>
              <StateTemplatevariable objectReference="model_3"/>
              <StateTemplatevariable objectReference="Metabolite_3"/>
              <StateTemplatevariable objectReference="Metabolite_7"/>
              <StateTemplatevariable objectReference="Metabolite_9"/>
              <StateTemplatevariable objectReference="Metabolite_5"/>
              <StateTemplatevariable objectReference="Metabolite_1"/>
              <StateTemplatevariable objectReference="Metabolite_11"/>
              <StateTemplatevariable objectReference="modelValue_0"/>
              <StateTemplatevariable objectReference="Compartment_1"/>
              <StateTemplatevariable objectReference="Compartment_3"/>
              <StateTemplatevariable objectReference="modelValue_1"/>
              <StateTemplatevariable objectReference="modelValue_2"/>
            </StateTemplate>
            <InitialState type="initialState">
              0 6.022140857000001e+021 6.022140856999989e+023 6.022140856999983e+024 6.022140857000001e+022 6.022140856999986e+020 6.022140857000001e+025 1.999999999999998 1 5 50 1 
            </InitialState>
          </model>
          <ListOfTasks>
            <Task key="Task_14" name="Steady-State" type="steadyState" scheduled="false" updatemodel="false">
              <Report reference="Report_9" target="" append="1" confirmOverwrite="1"/>
              <Problem>
                <Parameter name="JacobianRequested" type="bool" value="1"/>
                <Parameter name="StabilityAnalysisRequested" type="bool" value="1"/>
              </Problem>
              <method name="Enhanced Newton" type="EnhancedNewton">
                <Parameter name="Resolution" type="unsignedFloat" value="1e-009"/>
                <Parameter name="Derivation Factor" type="unsignedFloat" value="0.001"/>
                <Parameter name="Use Newton" type="bool" value="1"/>
                <Parameter name="Use Integration" type="bool" value="1"/>
                <Parameter name="Use Back Integration" type="bool" value="1"/>
                <Parameter name="Accept Negative Concentrations" type="bool" value="0"/>
                <Parameter name="Iteration Limit" type="unsignedInteger" value="50"/>
                <Parameter name="maximum duration for forward integration" type="unsignedFloat" value="1000000000"/>
                <Parameter name="maximum duration for backward integration" type="unsignedFloat" value="1000000"/>
              </method>
            </Task>
            <Task key="Task_15" name="Time-Course" type="timeCourse" scheduled="false" updatemodel="false">
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
              <method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
                <Parameter name="Integrate Reduced model" type="bool" value="0"/>
                <Parameter name="Relative tolerance" type="unsignedFloat" value="1e-006"/>
                <Parameter name="Absolute tolerance" type="unsignedFloat" value="1e-012"/>
                <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
                <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
              </method>
            </Task>
            <Task key="Task_16" name="Scan" type="scan" scheduled="false" updatemodel="false">
              <Problem>
                <Parameter name="Subtask" type="unsignedInteger" value="1"/>
                <ParameterGroup name="ScanItems">
                </ParameterGroup>
                <Parameter name="Output in subtask" type="bool" value="1"/>
                <Parameter name="Adjust initial conditions" type="bool" value="0"/>
              </Problem>
              <method name="Scan Framework" type="ScanFramework">
              </method>
            </Task>
            <Task key="Task_17" name="Elementary Flux modes" type="fluxmode" scheduled="false" updatemodel="false">
              <Report reference="Report_10" target="" append="1" confirmOverwrite="1"/>
              <Problem>
              </Problem>
              <method name="EFM Algorithm" type="EFMAlgorithm">
              </method>
            </Task>
            <Task key="Task_18" name="Optimization" type="optimization" scheduled="false" updatemodel="false">
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
              <method name="Random Search" type="RandomSearch">
                <Parameter name="Number of Iterations" type="unsignedInteger" value="100000"/>
                <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
                <Parameter name="seed" type="unsignedInteger" value="0"/>
              </method>
            </Task>
            <Task key="Task_19" name="Parameter Estimation" type="parameterFitting" scheduled="false" updatemodel="false">
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
              <method name="Evolutionary Programming" type="EvolutionaryProgram">
                <Parameter name="Number of Generations" type="unsignedInteger" value="200"/>
                <Parameter name="Population Size" type="unsignedInteger" value="20"/>
                <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
                <Parameter name="seed" type="unsignedInteger" value="0"/>
              </method>
            </Task>
            <Task key="Task_20" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updatemodel="false">
              <Report reference="Report_13" target="" append="1" confirmOverwrite="1"/>
              <Problem>
                <Parameter name="Steady-State" type="key" value="Task_14"/>
              </Problem>
              <method name="MCA method (Reder)" type="MCAmethod(Reder)">
                <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-009"/>
                <Parameter name="Use Reder" type="bool" value="1"/>
                <Parameter name="Use Smallbone" type="bool" value="1"/>
              </method>
            </Task>
            <Task key="Task_21" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updatemodel="false">
              <Report reference="Report_14" target="" append="1" confirmOverwrite="1"/>
              <Problem>
                <Parameter name="ExponentNumber" type="unsignedInteger" value="3"/>
                <Parameter name="DivergenceRequested" type="bool" value="1"/>
                <Parameter name="TransientTime" type="float" value="0"/>
              </Problem>
              <method name="Wolf method" type="Wolfmethod">
                <Parameter name="Orthonormalization Interval" type="unsignedFloat" value="1"/>
                <Parameter name="Overall time" type="unsignedFloat" value="1000"/>
                <Parameter name="Relative tolerance" type="unsignedFloat" value="1e-006"/>
                <Parameter name="Absolute tolerance" type="unsignedFloat" value="1e-012"/>
                <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
              </method>
            </Task>
            <Task key="Task_22" name="Time scale Separation Analysis" type="timescaleSeparationAnalysis" scheduled="false" updatemodel="false">
              <Report reference="Report_15" target="" append="1" confirmOverwrite="1"/>
              <Problem>
                <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
                <Parameter name="StepSize" type="float" value="0.01"/>
                <Parameter name="Duration" type="float" value="1"/>
                <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
                <Parameter name="OutputStartTime" type="float" value="0"/>
              </Problem>
              <method name="ILDM (LSODA,Deuflhard)" type="TimescaleSeparation(ILDM,Deuflhard)">
                <Parameter name="Deuflhard tolerance" type="unsignedFloat" value="1e-006"/>
              </method>
            </Task>
            <Task key="Task_23" name="Sensitivities" type="sensitivities" scheduled="false" updatemodel="false">
              <Report reference="Report_16" target="" append="1" confirmOverwrite="1"/>
              <Problem>
                <Parameter name="SubtaskType" type="unsignedInteger" value="1"/>
                <ParameterGroup name="TargetFunctions">
                  <Parameter name="SingleObject" type="cn" value=""/>
                  <Parameter name="ObjectListType" type="unsignedInteger" value="7"/>
                </ParameterGroup>
                <ParameterGroup name="ListOfvariables">
                  <ParameterGroup name="variables">
                    <Parameter name="SingleObject" type="cn" value=""/>
                    <Parameter name="ObjectListType" type="unsignedInteger" value="41"/>
                  </ParameterGroup>
                  <ParameterGroup name="variables">
                    <Parameter name="SingleObject" type="cn" value=""/>
                    <Parameter name="ObjectListType" type="unsignedInteger" value="0"/>
                  </ParameterGroup>
                </ParameterGroup>
              </Problem>
              <method name="Sensitivities method" type="Sensitivitiesmethod">
                <Parameter name="Delta factor" type="unsignedFloat" value="0.001"/>
                <Parameter name="Delta minimum" type="unsignedFloat" value="1e-012"/>
              </method>
            </Task>
            <Task key="Task_24" name="Moieties" type="moieties" scheduled="false" updatemodel="false">
              <Problem>
              </Problem>
              <method name="Householder Reduction" type="Householder">
              </method>
            </Task>
            <Task key="Task_25" name="Cross Section" type="crosssection" scheduled="false" updatemodel="false">
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
                <Parameter name="Convergencetolerance" type="float" value="1e-006"/>
                <Parameter name="Threshold" type="float" value="0"/>
                <Parameter name="DelayOutputUntilConvergence" type="bool" value="0"/>
                <Parameter name="OutputConvergencetolerance" type="float" value="1e-006"/>
                <ParameterText name="TriggerExpression" type="expression">

                </ParameterText>
                <Parameter name="Singlevariable" type="cn" value=""/>
              </Problem>
              <method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
                <Parameter name="Integrate Reduced model" type="bool" value="0"/>
                <Parameter name="Relative tolerance" type="unsignedFloat" value="1e-006"/>
                <Parameter name="Absolute tolerance" type="unsignedFloat" value="1e-012"/>
                <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
                <Parameter name="Max Internal Step Size" type="unsignedFloat" value="0"/>
              </method>
            </Task>
            <Task key="Task_26" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updatemodel="false">
              <Report reference="Report_17" target="" append="1" confirmOverwrite="1"/>
              <Problem>
                <Parameter name="Steady-State" type="key" value="Task_14"/>
              </Problem>
              <method name="Linear Noise Approximation" type="LinearNoiseApproximation">
              </method>
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
            <Report key="Report_10" name="Elementary Flux modes" taskType="fluxmode" separator="&#x09;" precision="6">
              <Comment>
                Automatically generated report.
              </Comment>
              <Footer>
                <Object cn="CN=Root,Vector=TaskList[Elementary Flux modes],Object=Result"/>
              </Footer>
            </Report>
            <Report key="Report_11" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
              <Comment>
                Automatically generated report.
              </Comment>
              <Header>
                <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
                <Object cn="String=\[Function Evaluations\]"/>
                <Object cn="separator=&#x09;"/>
                <Object cn="String=\[Best Value\]"/>
                <Object cn="separator=&#x09;"/>
                <Object cn="String=\[Best Parameters\]"/>
              </Header>
              <Body>
                <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
                <Object cn="separator=&#x09;"/>
                <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
                <Object cn="separator=&#x09;"/>
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
                <Object cn="separator=&#x09;"/>
                <Object cn="String=\[Best Value\]"/>
                <Object cn="separator=&#x09;"/>
                <Object cn="String=\[Best Parameters\]"/>
              </Header>
              <Body>
                <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
                <Object cn="separator=&#x09;"/>
                <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
                <Object cn="separator=&#x09;"/>
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
            <Report key="Report_15" name="Time scale Separation Analysis" taskType="timescaleSeparationAnalysis" separator="&#x09;" precision="6">
              <Comment>
                Automatically generated report.
              </Comment>
              <Header>
                <Object cn="CN=Root,Vector=TaskList[Time scale Separation Analysis],Object=Description"/>
              </Header>
              <Footer>
                <Object cn="String=&#x0a;"/>
                <Object cn="CN=Root,Vector=TaskList[Time scale Separation Analysis],Object=Result"/>
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
          <ListOfplots>
            <plotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="plot2D" active="1">
              <Parameter name="log x" type="bool" value="0"/>
              <Parameter name="log Y" type="bool" value="0"/>
              <ListOfplotItems>
                <plotItem name="[A]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,model=New model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[A],Reference=Concentration"/>
                  </ListOfChannels>
                </plotItem>
                <plotItem name="[B]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,model=New model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[B],Reference=Concentration"/>
                  </ListOfChannels>
                </plotItem>
                <plotItem name="[C]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,model=New model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[C],Reference=Concentration"/>
                  </ListOfChannels>
                </plotItem>
                <plotItem name="[D]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,model=New model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[D],Reference=Concentration"/>
                  </ListOfChannels>
                </plotItem>
                <plotItem name="[E]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,model=New model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[E],Reference=Concentration"/>
                  </ListOfChannels>
                </plotItem>
                <plotItem name="[F]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,model=New model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,model=New model,Vector=Compartments[nuc],Vector=metabolites[F],Reference=Concentration"/>
                  </ListOfChannels>
                </plotItem>
                <plotItem name="Values[assignment_global_var]" type="Curve2D">
                  <Parameter name="Line type" type="unsignedInteger" value="0"/>
                  <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="Line width" type="unsignedFloat" value="1"/>
                  <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
                  <Parameter name="color" type="string" value="auto"/>
                  <Parameter name="Recording Activity" type="string" value="during"/>
                  <ListOfChannels>
                    <ChannelSpec cn="CN=Root,model=New model,Reference=Time"/>
                    <ChannelSpec cn="CN=Root,model=New model,Vector=Values[assignment_global_var],Reference=Value"/>
                  </ListOfChannels>
                </plotItem>
              </ListOfplotItems>
            </plotSpecification>
          </ListOfplots>
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
