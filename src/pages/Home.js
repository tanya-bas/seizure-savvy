import React from "react";
import { Box, Flex, VStack, Text, Divider, Tag } from "@chakra-ui/react";
import BottomNavBar from "./BottomNavBar";
import PageHeader from "./PageHeader";

const Home = () => {
  return (
    <>
      <PageHeader pageTitle="Log Diary" />
      <Box p="4" overflowY="auto">
        <VStack spacing="4" align="stretch">
          <Flex justify="space-between" align="center">
            <Text fontSize="xl">Seizure Episodes</Text>
            {/* Add button for adding new episode if needed */}
          </Flex>
          <Divider />

          {/* Seizure episode blocks */}
          <Flex direction="column" spacing="4">
            {/* Seizure episode block 1 */}
            <Box bg="gray.100" p="4" borderRadius="md" boxShadow="md">
              <Flex justify="space-between" align="baseline">
                <Text fontSize="lg">Seizure Episode 1</Text>
                <Text fontSize="md">MM/DD</Text>
              </Flex>
              <Flex>
                <Text>Symptoms:</Text>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Poor sleep
                </Tag>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Anxiety
                </Tag>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Exercise
                </Tag>
              </Flex>
              <Text mt="2">Additional notes: Nauseous on and off</Text>
            </Box>

            {/* Seizure episode block 2 */}
            <Box bg="gray.100" p="4" borderRadius="md" boxShadow="md">
              <Flex justify="space-between" align="baseline">
                <Text fontSize="lg">Seizure Episode 2</Text>
                <Text fontSize="md">MM/DD</Text>
              </Flex>
              <Flex>
                <Text>Symptoms:</Text>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Stress
                </Tag>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Fatigue
                </Tag>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Flashing lights
                </Tag>
              </Flex>
              <Text mt="2">
                Additional notes: Felt dizzy before the episode
              </Text>
            </Box>

            {/* Daily log entries */}
            {/* Daily log entry 1 */}
            <Box bg="gray.100" p="4" borderRadius="md" boxShadow="md">
              <Flex justify="space-between" align="baseline">
                <Text fontSize="lg">Daily Log Entry 1</Text>
                <Text fontSize="md">MM/DD</Text>
              </Flex>
              <Flex>
                <Text>Symptoms:</Text>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Headache
                </Tag>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Fatigue
                </Tag>
              </Flex>
              <Flex>
                <Text>Lifestyle:</Text>
                <Tag variant="solid" colorScheme="green" ml="2">
                  Low physical activity
                </Tag>
              </Flex>
            </Box>

            {/* Daily log entry 2 */}
            <Box bg="gray.100" p="4" borderRadius="md" boxShadow="md">
              <Flex justify="space-between" align="baseline">
                <Text fontSize="lg">Daily Log Entry 2</Text>
                <Text fontSize="md">MM/DD</Text>
              </Flex>
              <Flex>
                <Text>Symptoms:</Text>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Nausea
                </Tag>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Anxiety
                </Tag>
              </Flex>
              <Flex>
                <Text>Lifestyle:</Text>
                <Tag variant="solid" colorScheme="green" ml="2">
                  High stress
                </Tag>
              </Flex>
            </Box>

            {/* Daily log entry 3 */}
            <Box bg="gray.100" p="4" borderRadius="md" boxShadow="md">
              <Flex justify="space-between" align="baseline">
                <Text fontSize="lg">Daily Log Entry 3</Text>
                <Text fontSize="md">MM/DD</Text>
              </Flex>
              <Flex>
                <Text>Symptoms:</Text>
                <Tag variant="solid" colorScheme="blue" ml="2">
                  Insomnia
                </Tag>
              </Flex>
              <Flex>
                <Text>Lifestyle:</Text>
                <Tag variant="solid" colorScheme="green" ml="2">
                  Late night screen time
                </Tag>
              </Flex>
            </Box>
          </Flex>
        </VStack>
      </Box>
      <BottomNavBar />
    </>
  );
};

export default Home;
