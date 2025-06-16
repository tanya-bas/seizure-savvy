import React from "react";
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
        {/* Today */}
        <Heading as="h2" size="lg" mb={4}>
          Today
        </Heading>
        <Divider mb={2} />
        <VStack spacing={4} align="stretch">
          {/* Seizure */}
          <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
            <Heading as="h3" size="md">
              Seizure
            </Heading>
            <Text>Type: Focal | Duration: 2 min | Frequency: 1 time(s)</Text>
            <Flex align="center" mt={2}>
              <Icon
                as={FaExclamationCircle}
                color="red.500"
                boxSize={5}
                mr={2}
              />
              <Text>Emergency intervention</Text>
            </Flex>
            <Text mt={2}>
              <b>Postictal symptoms:</b> Nausea, Headache
            </Text>
          </Flex>

          {/* Triggers */}
          <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
            <Heading as="h3" size="md">
              Triggers
            </Heading>
            <Flex wrap="wrap">
              <Badge colorScheme="blue" m={1}>
                Poor sleep
              </Badge>
              <Badge colorScheme="blue" m={1}>
                Skipped meal
              </Badge>
              <Badge colorScheme="blue" m={1}>
                Skipped medication
              </Badge>
            </Flex>
          </Flex>

          {/* Prodromes */}
          <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
            <Heading as="h3" size="md">
              Prodromes
            </Heading>
            <Flex wrap="wrap">
              <Badge colorScheme="green" m={1}>
                Headache
              </Badge>
              <Badge colorScheme="green" m={1}>
                Anxiety
              </Badge>
            </Flex>
          </Flex>

          {/* Auras */}
          <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
            <Heading as="h3" size="md">
              Auras
            </Heading>
            <Flex wrap="wrap">
              <Badge colorScheme="purple" m={1}>
                Visual disturbances
              </Badge>
              <Badge colorScheme="purple" m={1}>
                Déjà vu
              </Badge>
            </Flex>
          </Flex>

          {/* Additional Notes */}
          <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
            <Heading as="h3" size="md">
              Additional Notes
            </Heading>
            <Text mt={2}>I felt unusually tired before the seizure.</Text>
          </Flex>
        </VStack>

        {/* Yesterday */}
        <Heading as="h2" size="lg" mt={8} mb={4}>
          Yesterday
        </Heading>
        <Divider mb={2} />
        <Text>No data available.</Text>

        {/* Date: 17-04-2024 */}
      <Heading as="h2" size="lg" mt={8} mb={4}>17-04-2024</Heading>
      <Divider mb={2} />
      <VStack spacing={4} align="stretch">
        {/* Seizure */}
        <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
          <Heading as="h3" size="md">Seizure</Heading>
          <Text>Type: Complex | Duration: 5 min | Frequency: 2 time(s)</Text>
          <Flex align="center" mt={2}>
            <Icon as={FaExclamationCircle} color="red.500" boxSize={5} mr={2} />
            <Text>Emergency intervention</Text>
          </Flex>
          <Text mt={2}><b>Postictal symptoms:</b> Confusion, Fatigue</Text>
        </Flex>

        {/* Triggers */}
        <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
          <Heading as="h3" size="md">Triggers</Heading>
          <Flex wrap="wrap">
            <Badge colorScheme="blue" m={1}>Stress</Badge>
            <Badge colorScheme="blue" m={1}>Lack of sleep</Badge>
            <Badge colorScheme="blue" m={1}>Skipped medication</Badge>
          </Flex>
        </Flex>

        {/* Prodromes */}
        <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
          <Heading as="h3" size="md">Prodromes</Heading>
          <Flex wrap="wrap">
            <Badge colorScheme="green" m={1}>Headache</Badge>
            <Badge colorScheme="green" m={1}>Nausea</Badge>
          </Flex>
        </Flex>

        {/* Auras */}
        <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
          <Heading as="h3" size="md">Auras</Heading>
          <Flex wrap="wrap">
            <Badge colorScheme="purple" m={1}>Visual disturbances</Badge>
            <Badge colorScheme="purple" m={1}>Déjà vu</Badge>
            <Badge colorScheme="purple" m={1}>Confusion</Badge>
          </Flex>
        </Flex>

        {/* Additional Notes */}
        <Flex direction="column" borderWidth="3px" borderRadius="lg" p={4}>
          <Heading as="h3" size="md">Additional Notes</Heading>
          <Text mt={2}>I had increased stress levels due to work deadlines.</Text>
        </Flex>
      </VStack>
      <BottomNavBar />
      </Container>
    </Container>
  );
};

export default DailyLog;