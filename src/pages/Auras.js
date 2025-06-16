import React, { useState } from "react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  Switch,
  Stack,
  Text,
  IconButton,
  Flex,
} from "@chakra-ui/react";
import { InfoOutlineIcon } from "@chakra-ui/icons";


const auraVariables = [
  "Visual disturbances",
  "Hearing sounds",
  "Unusual smell or taste",
  "A ‘rising’ feeling in the stomach",
  "Déjà vu",
  "Jamais vu",
  "Sudden intense feeling of fear or joy",
  "A strange feeling like a ‘wave’ going through your head",
  "Stiffness or twitching in parts of your body",
  "A feeling of numbness or tingling",
  "A sensation that an arm or leg feels bigger or smaller than it actually is",
  "Confusion",
];

const AuraModal = ({ isOpen, onClose, onSubmit }) => {
  const [auraStates, setAuraStates] = useState(
    auraVariables.reduce((acc, variable) => ({ ...acc, [variable]: false }), {})
  );
  const [infoModalOpen, setInfoModalOpen] = useState(false);

  const handleToggle = (variable) => {
    setAuraStates((prevStates) => ({
      ...prevStates,
      [variable]: !prevStates[variable],
    }));
  };

  const resetAuraStates = () => {
    setAuraStates(
      auraVariables.reduce(
        (acc, variable) => ({ ...acc, [variable]: false }),
        {}
      )
    );
  };

  const handleSubmit = () => {
    onSubmit(auraStates);
    resetAuraStates();
    onClose();
  };

  const handleClose = () => {
    resetAuraStates();
    onClose();
    
  };

  const handleInfoIconClick = () => {
    setInfoModalOpen(true);
  };

  const handleInfoModalClose = () => {
    setInfoModalOpen(false);

  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <Flex justify="space-between" align="center" pr={5} pt={8}>
          <ModalHeader flex="1">Today's Auras</ModalHeader>
          <IconButton
            icon={<InfoOutlineIcon />}
            aria-label="Information about Aura"
            onClick={handleInfoIconClick}
          />
        </Flex>
        <ModalCloseButton />
        <ModalBody>
          <Stack spacing={4}>
            {auraVariables.map((variable, index) => (
              <FormControl display="flex" alignItems="center" key={index}>
                <FormLabel htmlFor={variable} mb="0" flex="1">
                  {variable}
                </FormLabel>
                <Switch
                  id={variable}
                  colorScheme="teal"
                  isChecked={auraStates[variable]}
                  onChange={() => handleToggle(variable)}
                />
              </FormControl>
            ))}
          </Stack>
        </ModalBody>
        <ModalFooter>
          <Button colorScheme="gray" mr={3} onClick={handleClose}>
            Close
          </Button>
          <Button colorScheme="teal" onClick={handleSubmit}>
            Submit
          </Button>
        </ModalFooter>
      </ModalContent>
      <Modal isOpen={infoModalOpen} onClose={handleInfoModalClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Aura</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Text>
              An aura is a perceptual disturbance experienced before a seizure
              begins. It is a special type of prodrome which often manifests
              itself as the perception of a strange light, an unpleasant smell,
              or confusing thoughts or experiences.
            </Text>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="teal" onClick={handleInfoModalClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Modal>
  );
};

export default AuraModal;
