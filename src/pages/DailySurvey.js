import React, { useState } from "react";
import BottomNavBar from "./BottomNavBar";
import SeizureModal from "./Seizure";
import ProdromeModal from "./Prodrome";
import TriggerModal from "./Triggers";
import AuraModal from "./Auras";
import PageHeader from "./PageHeader";

import {
  Box,
  Button,
  Radio,
  RadioGroup,
  Stack,
  Heading,
  useToast,
  ModalBody,
  Text,
  useDisclosure,
  Modal,
  Textarea,
  Container,
} from "@chakra-ui/react";

const DailySurvey = () => {
  const toast = useToast();
  const [hadSeizure, setHadSeizure] = useState(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const {
    isOpen: isAuraOpen,
    onOpen: onAuraOpen,
    onClose: onAuraClose,
  } = useDisclosure();
  const {
    isOpen: isProdromeOpen,
    onOpen: onProdromeOpen,
    onClose: onProdromeClose,
  } = useDisclosure();
  const [additionalNotes, setAdditionalNotes] = useState("");
  const [prodromes, setProdromes] = useState({
    headache: 0,
    numbnessOrTingling: 0,
    tremor: 0,
    dizziness: 0,
    nausea: 0,
    anxiety: 0,
    moodChanges: 0,
    insomnia: 0,
    difficultyFocusing: 0,
    gastrointestinalDisturbances: 0,
  });

  // SEIZURES
  const handleSeizureSubmit = (seizureData) => {
    console.log("Seizure Data Submitted:", seizureData);
    // Process the seizure data, (API)
  };

  // Open the SeizureModal based on the response
  const handleSeizureResponse = (value) => {
    setHadSeizure(value); // Use setHadSeizure to update the state
    if (value === "yes") {
      onOpen();
    } else {
      // Show toast for "No"
      toast({
        title: "What a great day!",
        description: "No seizure today.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  //PRODROMES
  const handleProdromeChange = (prodrome, value) => {
    setProdromes((prev) => ({ ...prev, [prodrome]: value }));
  };

  const handleSubmitProdromes = (prodromes) => {
    console.log("Prodromes Data Submitted:", prodromes);
    // Process the prodromes data here (e.g., send to an API)
    //onClose(); // close the modal after submission
  };

  //TRIGGERS

  const {
    isOpen: isTriggerOpen,
    onOpen: onTriggerOpen,
    onClose: onTriggerClose,
  } = useDisclosure();

  const [triggers, setTriggers] = useState({
    sleepQuality: 0,
    sleepDuration: 0,
    stressLevel: 0,
    alcoholConsumption: 0,
    caffeineConsumption: 0,
    drugsConsumption: false,
    smoking: 0,
    missingMeal: false,
    fevers: false,
    feverValue: 0, // If fevers is true, user can input a value
    steps: 0,
    highIntensityMinutes: 0,
    flashingLight: false,
    monthlyPeriods: 0, // Day of the cycle
    medicationAdherence: false,
    medicationChanges: false,
  });

  const handleTriggerChange = (name, value) => {
    setTriggers((prev) => ({ ...prev, [name]: value }));
  };

  // Function to handle the submission of trigger data
  const handleSubmitTriggers = (triggersData) => {
    console.log("Triggers Data Submitted:", triggersData);
    // Process the triggers data here
    onTriggerClose();
  };

  //AURAS
  const handleAuraSubmit = (auraData) => {
    console.log("Aura Data Submitted:", auraData);
    // handle the aura data, e.g., send it to your API
  };

  // Extra notes
  const handleSubmitNotes = () => {
    console.log("Additional Notes Submitted:", additionalNotes);
    // send the additional notes to your API/database
    setAdditionalNotes(""); // Reset the notes field after submission
  };

  return (
    <>
      <Container
        maxW=""
        bg="#f7f7f7"
        minHeight="100vh"
        p={0}
        display="flex"
        flexDirection="column"
      >
        <PageHeader pageTitle="Daily Log" />
        <Container
          maxW="lg"
          flex="1"
          bg="#f7f7f7"
          p={4}
          pb="100px"
          overflowY="auto"
        >
          <Box
            ml={50}
            mr={50}
            display="flex"
            flexDirection="column"
            alignItems="center"
            minH="100vh"
          >
            <Heading size="md" mt={6} mb={6}>
              Did you have a seizure today?
            </Heading>
            {hadSeizure === "no" && (
              <Modal>
                <ModalBody>
                  <Text>Lovely. What a nice day!</Text>
                </ModalBody>
              </Modal>
            )}

            <RadioGroup onChange={handleSeizureResponse}>
              <Stack direction="row" spacing={5}>
                <Radio value="yes">Yes</Radio>
                <Radio value="no">No</Radio>
              </Stack>
            </RadioGroup>

            <SeizureModal
              isOpen={isOpen}
              onClose={onClose}
              onSubmit={handleSeizureSubmit}
            />

            <Heading size="md" mt={6}>
              What were your prodromes today?
            </Heading>
            <Button
              onClick={onProdromeOpen}
              colorScheme="blue"
              bgColor="#6a95e3"
              my={4}
            >
              Log your Prodromes
            </Button>
            <ProdromeModal
              isOpen={isProdromeOpen}
              onClose={onProdromeClose}
              prodromes={prodromes}
              handleProdromeChange={handleProdromeChange}
              onSubmit={handleSubmitProdromes}
            />

            <Heading size="md" mt={6}>
              What triggers did you have today?
            </Heading>
            <Button
              onClick={onTriggerOpen}
              colorScheme="blue"
              bgColor="#6a95e3"
              my={4}
            >
              Log your Triggers
            </Button>

            <TriggerModal
              isOpen={isTriggerOpen}
              onClose={onTriggerClose}
              triggers={triggers}
              handleTriggerChange={handleTriggerChange}
              onSubmit={handleSubmitTriggers}
            />

            <Heading size="md" mt={6}>
              What auras did you experience today?
            </Heading>
            <Button
              onClick={onAuraOpen}
              colorScheme="blue"
              bgColor="#6a95e3"
              mt={4}
            >
              Log your Auras
            </Button>
            <AuraModal
              isOpen={isAuraOpen}
              onClose={onAuraClose}
              onSubmit={handleAuraSubmit}
            />

            <Heading size="md" mt={6}>
              Any additional notes for today?
            </Heading>
            <Textarea
              placeholder="Type here..."
              value={additionalNotes}
              onChange={(e) => setAdditionalNotes(e.target.value)}
              mt={4}
            />
            <Button
              colorScheme="blue"
              bgColor="#02ba98"
              mt={4}
              onClick={handleSubmitNotes}
            >
              Submit Notes
            </Button>
          </Box>

          <BottomNavBar />
        </Container>
      </Container>
    </>
  );
};

export default DailySurvey;
