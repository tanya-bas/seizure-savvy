import React, { useState, useEffect } from "react";
import { Box, Container } from "@chakra-ui/react";
import AlertBanner from "./AlertBanner";
import BottomNavBar from "./BottomNavBar";
import SymptomsRank from "./SymptomsRank";
import PageHeader from "./PageHeader";
import axios from "axios"; // Import axios for making HTTP requests

const InsightsPage = () => {
	const [riskLevel, setRiskLevel] = useState(null);

	// Function to fetch data from the backend
  const fetchModelOutput = async () => {
    try {
      // Make GET request to the backend API endpoint
      const response = await axios.get("/api/predictions_lstm");
      const { prediction_lstm } = response.data;
      translateModelOutput(prediction_lstm); // Translate model output to risk level
    } catch (error) {
      console.error("Error fetching model output:", error);
      // Handle error, set risk level to 'insufficient' or show error message
      setRiskLevel("insufficient");
    }
  };

  // Function to translate model output to risk level
  const translateModelOutput = (output) => {
    if (output === null) {
      setRiskLevel("insufficient");
    } else if (output <= 0.33) {
      setRiskLevel("low");
    } else if (output <= 0.66) {
      setRiskLevel("medium");
    } else {
      setRiskLevel("high");
    }
  };

  useEffect(() => {
    fetchModelOutput();
  }, []); // Fetch model output only on component mount

  return (
    <Box>
      <PageHeader pageTitle="Insights" />
      <Container maxW="lg" pb="100px" mt={10}>
        {riskLevel !== null && <AlertBanner riskLevel={riskLevel} />}
        <SymptomsRank />
        <BottomNavBar />
      </Container>
    </Box>
  );
};

export default InsightsPage;
