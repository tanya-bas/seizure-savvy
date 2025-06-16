import React, { useState, useEffect } from "react";
import {
  Container,
  Heading,
  Button,
  Flex,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  useDisclosure,
} from "@chakra-ui/react";
import MedicationBanner from "./MedicationBanner";
import MedicationForm from "./MedicationForm";
import BottomNavBar from "./BottomNavBar";
import MedicationChecklist from "./MedicationChecklist";
import PageHeader from "./PageHeader";

const MedicationPage = () => {
  const [medications, setMedications] = useState([]);
  const [isAddingMedication, setIsAddingMedication] = useState(false);
  const [sortedMedications, setSortedMedications] = useState([]);
  const [newMedication, setNewMedication] = useState({
    name: "",
    dosage: "",
    frequency: "Once a day",
    firstDose: "08:00",
    startDate: new Date().toISOString().split("T")[0],
  });

  const toast = useToast();
  const { isOpen, onOpen, onClose } = useDisclosure(); // For medication modal

  // Placeholder function for fetching medications from the backend
  const fetchMedications = async () => {
    try {
      // Make API call to fetch profile data
      // const response = await fetch('API_ENDPOINT/medication');
      // const data = await response.json();
      // Set mock profile data

      const mockMedication = [
        {
          id: 1,
          name: "Kepra",
          dosage: "10",
          frequency: "Three times a day",
          startDate: "2022-04-01",
          firstDose: "08:00",
          endDate: null,
          reasonForStop: null,
        },
        {
          id: 2,
          name: "Pregabalin",
          dosage: "37.5",
          frequency: "Four times a day",
          startDate: "2022-04-05",
          firstDose: "09:00",
          endDate: null,
          reasonForStop: null,
        },
        {
          id: 3,
          name: "Kepra",
          dosage: "30",
          frequency: "Three times a day",
          startDate: "2022-04-01",
          firstDose: "10:00",
          endDate: "2022-04-10",
          reasonForStop: "Side effects",
        },
      ];
      setMedications(mockMedication);
    } catch (error) {
      console.error("Error fetching profile data:", error);
      toast({
        title: "Error",
        description: "Failed to fetch profile data",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const addNewMedication = async () => {
    try {
      // Make API call to add new medication
      // await fetch('API_ENDPOINT/medications', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(newMedication),
      // });
      // Mock adding new medication
      const medicationToAdd = { ...newMedication }; // Create a new object
      setMedications((prevMedications) => [
        ...prevMedications,
        medicationToAdd,
      ]); // Add new medication to state
      // Show success message
      toast({
        title: "Medication added",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error("Error adding medication:", error);
      toast({
        title: "Error",
        description: "Failed to add medication",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  useEffect(() => {
    fetchMedications();
  }, []);

  useEffect(() => {
    // Separate medications into two arrays based on whether they have an endDate or not
    const medicationsWithoutEndDate = medications.filter(
      (medication) => !medication.endDate
    );
    const medicationsWithEndDate = medications.filter(
      (medication) => medication.endDate
    );

    // Sort medications arrays by startDate or endDate
    medicationsWithoutEndDate.sort(
      (a, b) => new Date(b.startDate) - new Date(a.startDate)
    );
    medicationsWithEndDate.sort(
      (a, b) => new Date(b.endDate) - new Date(a.endDate)
    );

    // Concatenate both arrays to display medications in the desired order
    setSortedMedications([
      ...medicationsWithoutEndDate,
      ...medicationsWithEndDate,
    ]);
  }, [medications]);

  const handleOpenMedicationModal = () => {
    setIsAddingMedication(true);
    onOpen();
  };

  const handleCloseMedicationModal = () => {
    setIsAddingMedication(false);
    onClose();
  };

  const handleMedicationFormChange = (e) => {
    const { name, value } = e.target;
    setNewMedication((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSaveMedication = () => {
    addNewMedication();
    setIsAddingMedication(false);
    onClose();
  };

  // Define functions to edit and stop medications
  const editMedication = (medicationId, updatedMedication) => {
    setMedications((prevMedications) =>
      prevMedications.map((medication) =>
        medication.id === medicationId
          ? { ...medication, ...updatedMedication }
          : medication
      )
    );
  };

  const stopMedication = (medicationId, stoppedMedication) => {
    setMedications((prevMedications) =>
      prevMedications.map((medication) =>
        medication.id === medicationId
          ? { ...medication, ...stoppedMedication }
          : medication
      )
    );
  };

  return (
    <Container
      maxW=""
      bg="#f7f7f7"
      minHeight="100vh"
      p={0}
      display="flex"
      flexDirection="column"
    >
      <PageHeader pageTitle="Medication" />
      <Container
        maxW="lg"
        flex="1"
        bg="#f7f7f7"
        p={4}
        pb="100px"
        overflowY="auto"
      >
        {/* Display Today's Medication section */}
        <Heading as="h2" size="xl" textAlign="left" mb={4} ml={4}>
          Today's Medication
        </Heading>
        <Flex direction="column" align="center">
          <MedicationChecklist medications={medications} />
        </Flex>

        {/* Display Your Medication section */}
        <Heading as="h2" size="xl" textAlign="left" mt={8} mb={4} ml={4}>
          Your Medication
        </Heading>
        <Flex direction="column" align="center">
          {/* Display medications without an endDate, sorted by startDate */}
          {sortedMedications.map((medication) => (
            <MedicationBanner
              key={medication.id}
              medication={medication}
              editMedication={editMedication}
              stopMedication={stopMedication}
            />
          ))}
        </Flex>

        <Flex justify="center" mt={6}>
          <Button
            colorScheme="blue"
            bgColor="#6a95e3"
            onClick={handleOpenMedicationModal}
          >
            Add Medication
          </Button>
        </Flex>
      </Container>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Add New Medication</ModalHeader>
          <MedicationForm
            newMedication={newMedication}
            handleChange={handleMedicationFormChange}
            handleSaveMedication={handleSaveMedication}
            handleCloseMedicationModal={handleCloseMedicationModal}
          />
        </ModalContent>
      </Modal>

      <BottomNavBar />
    </Container>
  );
};

export default MedicationPage;
