import React, { useState, useEffect } from "react";
import {
  Container,
  Heading,
  Divider,
  VStack,
  Text,
  Badge,
  Flex,
  Icon,
} from "@chakra-ui/react";
import { FaExclamationCircle } from "react-icons/fa";
import PageHeader from "./PageHeader";
import BottomNavBar from "./BottomNavBar";

const DailyLog = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        // Fetch logs for the last week from the backend
        // const response = await fetch("API_ENDPOINT/logs");
        // if (!response.ok) {
        //   throw new Error("Failed to fetch logs");
        // }
        // const data = await response.json();

        const mockData = [
          {
            date: "2024-04-18",
            seizure: {
              type: "Focal",
              duration: 2,
              frequency: 1,
              emergencyIntervention: true,
              postictalSymptoms: "10/10 confusion for 5 minutes, 7/10 headache for 10 minutes",
              notes: "Very intense",
            },
            triggers: ["Poor sleep", "Skipped a meal", "Skipped medication"],
            prodromes: ["Headache", "Anxiety"],
            auras: ["Visual disturbances", "Déjà vu"],
            notes: "I was feeling unusually tired before the seizure.",
          },
          {
            date: "2024-04-17",
            seizure: {
              type: "Complex",
              duration: 5,
              frequency: 2,
              emergencyIntervention: true,
              postictalSymptoms: "No significant postictal symptoms",
              notes: "Had a stressful day at work",
            },
            triggers: ["Stress", "Lack of sleep", "Missed medication"],
            prodromes: ["Anxiety", "Irritability"],
            auras: ["Visual disturbances", "Déjà vu", "Jamais vu"],
            notes: "I had increased stress levels due to work deadlines.",
          },
          {
            date: "2024-04-16",
            triggers: ["Poor sleep", "Skipped a meal", "Skipped medication"],
            notes: "I was feeling unusually tired before the seizure.",
          },
        ];

        setLogs(mockData);
      } catch (error) {
        console.error("Error fetching logs:", error.message);
      }
    };

    fetchLogs();
  }, []);

  const renderSeizure = (seizure) => {
    if (!seizure) return null;

    return (
      <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
        <Heading as="h3" size="md">
          Seizure
        </Heading>
        <Text>
          Type: {seizure.type} | {seizure.duration} min | {" "}
          {seizure.frequency} time(s){" "}
        </Text>
        {seizure.emergencyIntervention && (
          <Flex align="center" mt={2}>
            <Icon as={FaExclamationCircle} color="red.500" boxSize={5} mr={2} />
            <Text>Emergency intervention</Text>
          </Flex>
        )}
        <Text mt={2}>
          <b>Postictal symptoms:</b> {seizure.postictalSymptoms}
        </Text>
        {seizure.notes && (
          <Text mt={2}>
            <b>Notes:</b> {seizure.notes}
          </Text>
        )}
      </Flex>
    );
  };

  const renderTags = (tags, color) => {
    if (!tags || tags.length === 0) return null;

    return (
      <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
        <Heading as="h3" size="md">
          {color === "blue" && "Triggers"}
          {color === "green" && "Prodromes"}
          {color === "purple" && "Auras"}
        </Heading>
        <Flex wrap="wrap">
          {tags.map((tag, index) => (
            <Badge key={index} colorScheme={color} m={1}>
              {tag}
            </Badge>
          ))}
        </Flex>
      </Flex>
    );
  };

  const renderNotes = (notes) => {
    if (!notes) return null;

    return (
      <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
        <Heading as="h3" size="md">
          Additional Notes
        </Heading>
        <Text mt={2}>{notes}</Text>
      </Flex>
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
      mb={100}
    >
      <PageHeader pageTitle="Daily Log" />
      <Container maxW="lg" mt={8}>
        {logs.map((log, index) => (
          <VStack key={index} spacing={4} align="stretch">
            <Heading as="h2" size="lg" mt={4}>
              {log.date}
            </Heading>
            <Divider />
            {renderSeizure(log.seizure)}
            {renderTags(log.triggers, "blue")}
            {renderTags(log.prodromes, "green")}
            {renderTags(log.auras, "purple")}
            {renderNotes(log.notes)}
          </VStack>
        ))}
        {logs.length === 0 && (
          <VStack spacing={4} align="stretch">
            <Heading as="h2" size="lg">
              No data available
            </Heading>
          </VStack>
        )}
        <BottomNavBar />
      </Container>
    </Container>
  );
};

export default DailyLog;
