import React from "react";
import { Box, Text } from "@chakra-ui/react";


const AlertBanner = ({ riskLevel }) => {
  // Function to determine the background color based on risk level
  const getBackgroundColor = () => {
    if (riskLevel === "low") {
      return "#02ba98";
    } else if (riskLevel === "medium") {
      return "#f4ca38";
    } else if (riskLevel === "high") {
      return "#fc436d";
    } else {
      return "#aaa";
    }
  };

  // Function to determine the text based on risk level
  const getRiskText = () => {
    if (riskLevel === "low") {
      return "Low";
    } else if (riskLevel === "medium") {
      return "Medium";
    } else if (riskLevel === "high") {
      return "High";
    } else {
      return "Insufficient Data";
    }
  };

  return (
    <Box
      bg={getBackgroundColor()}
      p={4}
      borderRadius="xl" // Rounded corners
      textAlign="center"
      color="#fff"
      fontWeight="bold"
      boxShadow="lg" // Add shading
      width="calc(100% - 45px)"
      mx="auto" // Center the box horizontally
    >
      <Text fontSize="lg" mb={2}>
        Today's Seizure Risk Assessment
      </Text>
      <Text fontSize="xl">{getRiskText()}</Text>
    </Box>
  );
};

export default AlertBanner;
