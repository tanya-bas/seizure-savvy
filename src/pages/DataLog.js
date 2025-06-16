import React, { useState } from "react";
import Calendar from "react-calendar";
import { Box, useToast, Heading, Flex } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import "react-calendar/dist/Calendar.css";
import BottomNavBar from "./BottomNavBar";
import PageHeader from "./PageHeader";

const DataLogPage = () => {
  const [medications, setMedications] = useState([]);
  const toast = useToast();
  const navigate = useNavigate();

  const handleDayClick = (value, event) => {
    // Navigate to the data survey page with the selected date
    navigate("/dailysurvey");
    toast({
      title: "Selected date for data logging.",
      description: `You've selected ${value.toLocaleDateString()}. Redirecting to log data...`,
      status: "info",
      duration: 5000,
      isClosable: true,
    });
  };

  const handleMedicationSubmit = (event) => {
    event.preventDefault();
    const { dosage, medication } = event.target.elements;

    //  send the data to backend via API
    // just add it to local state
    setMedications((prev) => [
      ...prev,
      { dosage: dosage.value, medication: medication.value },
    ]);

    dosage.value = ""; // Clear the form
    medication.value = ""; // Clear the form
  };

  return (
    <>
      <Box>
        <PageHeader pageTitle="New Log" />
        <Flex justify="center">
          <Heading size="md" mt={6} mb={6}>
            Click on a Day to Log your data
          </Heading>
        </Flex>
        <Flex justify="center">
          <Calendar onClickDay={handleDayClick} />
        </Flex>
      </Box>
      <BottomNavBar />
    </>
  );
};

export default DataLogPage;
