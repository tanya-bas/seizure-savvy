import React, { useState, useEffect } from "react";
import { Box, Text } from "@chakra-ui/react";
import axios from "axios"; // Import axios for making HTTP requests


const SymptomsRank = () => {
	const [topSymptoms, setTopSymptoms] = useState([]);

	const fetchTopSymptoms = async () => {
    try {
      // Make API call to fetch top symptoms using XGBoost model
      const response = await axios.get("/api/predictions/xgboost", {
        params: {
          user_id: "user123", // Pass the user ID if needed
        },
      });
      const { feature_importance } = response.data;
      // Set top symptoms state
      setTopSymptoms(feature_importance);
    } catch (error) {
      console.error("Error fetching top symptoms:", error);
    }
  };


	useEffect(() => {
		fetchTopSymptoms();
	}, []);

  return (
    <Box
      bg={topSymptoms.length > 0 ? "teal" : "#aaa"}
      p={4}
      borderRadius="xl" // Rounded corners
      mt={4}
      textAlign="center"
      color="#fff"
      fontWeight="bold"
      boxShadow="lg"
      width="calc(100% - 45px)"
      mx="auto" // Center the box horizontally
    >
      <Text fontSize="lg" mb={2}>
        Your top 5 symptoms are:
      </Text>
      {topSymptoms.length > 0 ? (
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {topSymptoms.map((symptom, index) => (
            <li key={index}>{symptom}</li>
          ))}
        </ul>
      ) : (
        <Text>Insufficient data to display the symptoms.</Text>
      )}
    </Box>
  );
};

export default SymptomsRank;
