
import React, { useState } from "react";
import {
  Box,
  Button,
  FormLabel,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Slider,
  SliderFilledTrack,
  SliderThumb,
  SliderTrack,
  Text,
  VStack,
  Flex,
  IconButton,
} from "@chakra-ui/react";
import { InfoOutlineIcon } from "@chakra-ui/icons";

const ProdromeModal = ({
  isOpen,
  onClose,
  prodromes,
  handleProdromeChange,
  onSubmit,
}) => {
  const [infoModalOpen, setInfoModalOpen] = useState(false);

  const renderProdromeSlider = (prodrome, label) => (
    <Flex key={prodrome} align="center">
      <FormLabel htmlFor={prodrome} mb="0" flex="1">
        {label}
      </FormLabel>
      <Box flex="2" position="relative">
        <Slider
          id={prodrome}
          defaultValue={prodromes[prodrome]}
          min={0}
          max={10}
          onChangeEnd={(val) => handleProdromeChange(prodrome, val)}
        >
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb boxSize={6} fontSize="sm">
            {prodromes[prodrome]}
          </SliderThumb>
        </Slider>
      </Box>
    </Flex>
  );

  const handleSubmit = () => {
    onSubmit(prodromes);
    onClose();
  };

  const handleClose = () => {
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
        <ModalHeader>
          <Flex mt={8} justify="space-between" align="center">
            <Text>Today's Prodromes</Text>
            <IconButton
              icon={<InfoOutlineIcon />}
              aria-label="Information about Prodrome"
              onClick={handleInfoIconClick}
            />
          </Flex>
        </ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack align="stretch" spacing={4}>
            {Object.keys(prodromes).map((key) =>
              renderProdromeSlider(
                key,
                key
                  .replace(/([A-Z])/g, " $1")
                  .replace(/^./, (str) => str.toUpperCase())
              )
            )}
          </VStack>
        </ModalBody>
        <ModalFooter>
          <Button colorScheme="gray" mr={3} onClick={handleClose}>
            Close
          </Button>
          <Button colorScheme="blue" onClick={handleSubmit}>
            Submit
          </Button>
        </ModalFooter>
      </ModalContent>
      <Modal isOpen={infoModalOpen} onClose={handleInfoModalClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Prodrome</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Text>
              A prodrome is a set of early symptoms that can indicate the onset
              of a seizure. It refers to the symptoms that occur before the
              actual seizure takes place.
            </Text>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="blue" onClick={handleInfoModalClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Modal>
  );
};

export default ProdromeModal;
