import React, { useState } from "react";
import {
  Box,
  Text,
  Button,
  Flex,
  FormControl,
  FormLabel,
  Input,
  Select,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  useDisclosure,
  Icon,
} from "@chakra-ui/react";
import { BiCapsule } from "react-icons/bi"; // Import the BiCapsulePillIcon
import { FaClock, FaCalendarAlt } from "react-icons/fa"; // Import the FaClock icon

const MedicationBanner = ({ medication, editMedication, stopMedication }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [isEditing, setIsEditing] = useState(false);
  const [medicationData, setMedicationData] = useState({
    medication: medication.name,
    startDate: medication.startDate,
    dosage: medication.dosage,
    frequency: medication.frequency,
    firstDose: medication.firstDose,
    endDate: medication.endDate,
    reasonForStop: medication.reasonForStop,
  });

  const handleEditMedication = () => {
    setIsEditing(true);
    setMedicationData({
      medication: medication.name,
      startDate: medication.startDate,
      dosage: medication.dosage,
      frequency: medication.frequency,
      firstDose: medication.firstDose,
      endDate: medication.endDate,
      reasonForStop: medication.reasonForStop,
    });
    onOpen();
  };

  // Open Modal for stopping medication
  const handleStopMedication = () => {
    setIsEditing(false); // Set editing to false when stopping medication
    onOpen();
  };

  // Handle stopping medication in the database
  const handleStoppedMedication = () => {
    // API to update stopped medication
    if (!medicationData.endDate) {
      alert("Please fill in all required fields");
      return;
    }
    stopMedication(medication.id, medicationData);
    console.log("Stopped medication:", medicationData);
    onClose();
  };

  // Handle saving medication edits to the database
  const handleSaveChanges = () => {
    // Here, you would handle saving changes to the database
    editMedication(medication.id, medicationData);
    console.log("Updated medication data:", medicationData);
    setIsEditing(false);
    onClose();
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setMedicationData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <Box
      bg={medicationData.endDate ? "#dedede" : "#FFF"} // Adjusted background color based on endDate
      p={4}
      mb={4}
      borderRadius={18}
      color="#140F1F"
      width="calc(100% - 45px)" // Adjust width based on whether there is an endDate
      boxShadow="base"
    >
      <Flex alignItems="center">
        {" "}
        {/* Wrap the text and icon in a Flex container */}
        <Icon as={BiCapsule} color="#6a95e3" boxSize={100} mr={4} />{" "}
        {/* Add the BiCapsulePillIcon */}
        <Box>
          <Text fontWeight="bold">
            {medicationData.medication}, {medicationData.dosage} mg
          </Text>
          <Text mb={4}>{medicationData.frequency}</Text>
          <Flex alignItems="center">
            <Icon as={FaCalendarAlt} color="#02ba98" boxSize={4} mr={2} />{" "}
            {/* Add the calendar icon */}
            <Text>
              {new Date(medicationData.startDate).toLocaleDateString()}
            </Text>{" "}
            {/* Display start date */}
          </Flex>
          <Flex alignItems="center">
            {" "}
            {/* Add another Flex container for the clock icon and first dose */}
            <Icon as={FaClock} color="#02ba98" boxSize={4} mr={2} />{" "}
            {/* Add the clock icon */}
            <Text alignSelf="center">{medicationData.firstDose}</Text>{" "}
            {/* Display first dose */}
          </Flex>
          {medicationData.endDate && ( // Display endDate and reason if medication is stopped
            <>
              <Text>
                Stopped on{" "}
                {new Date(medicationData.endDate).toLocaleDateString()}
              </Text>
              <Text>Reason: {medicationData.reasonForStop}</Text>
            </>
          )}
        </Box>
      </Flex>
      <Flex justify="space-between">
        <Button onClick={handleEditMedication} color="#fff" bgColor="#02ba98">
          Edit
        </Button>
        {/* Display "Stop Medication" button only if not stopped */}
        {!medicationData.endDate && (
          <Button onClick={handleStopMedication} color="#fff" bgColor="#6a95e3">
            Stop
          </Button>
        )}
      </Flex>

      {/* Modal for Editing Medication */}
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {isEditing ? "Edit Medication" : "Stop Medication"}
          </ModalHeader>
          <ModalBody>
            {isEditing ? (
              <>
                <FormControl mb={4} isRequired>
                  <FormLabel>Medication</FormLabel>
                  <Input
                    type="text"
                    name="medication"
                    value={medicationData.medication}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl mb={4} isRequired>
                  <FormLabel>Dosage (in mg)</FormLabel>
                  <Input
                    type="number"
                    name="dosage"
                    value={medicationData.dosage}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl mb={4} isRequired>
                  <FormLabel>Frequency</FormLabel>
                  <Select
                    name="frequency"
                    value={medicationData.frequency}
                    onChange={handleChange}
                  >
                    <option value="1">Once a day</option>
                    <option value="2">Twice a day</option>
                    <option value="3">Three times a day</option>
                    <option value="4">Four times a day</option>
                  </Select>
                </FormControl>
                <FormControl mb={4} isRequired>
                  <FormLabel>Start Date</FormLabel>
                  <Input
                    type="date"
                    name="startDate"
                    value={medicationData.startDate}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl isRequired>
                  <FormLabel>First Dose</FormLabel>
                  <Input
                    type="time"
                    name="firstDose"
                    value={medicationData.firstDose}
                    onChange={handleChange}
                  />
                </FormControl>

                <>
                  {medicationData.endDate && (
                    <>
                      <FormControl mb={4} isRequired>
                        <FormLabel>End Date</FormLabel>
                        <Input
                          type="date"
                          name="endDate"
                          value={medicationData.endDate}
                          onChange={handleChange}
                        />
                      </FormControl>
                      <FormControl>
                        <FormLabel>Reason for Stop</FormLabel>
                        <Input
                          type="text"
                          name="reasonForStop"
                          value={medicationData.reasonForStop}
                          onChange={handleChange}
                        />
                      </FormControl>
                    </>
                  )}
                </>
              </>
            ) : (
              <>
                <FormControl mb={4} isRequired>
                  <FormLabel>End Date</FormLabel>
                  <Input
                    type="date"
                    name="endDate"
                    value={medicationData.endDate}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Reason for Stop</FormLabel>
                  <Input
                    type="text"
                    name="reasonForStop"
                    value={medicationData.reasonForStop}
                    onChange={handleChange}
                  />
                </FormControl>
              </>
            )}
          </ModalBody>
          <ModalFooter>
            <Button
              bgColor="#6a95e3"
              onClick={isEditing ? handleSaveChanges : handleStoppedMedication}
            >
              {isEditing ? "Save Changes" : "Stop Medication"}
            </Button>
            <Button onClick={onClose} ml={2}>
              Cancel
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default MedicationBanner;
