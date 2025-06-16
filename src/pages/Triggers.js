// Trigger.js
import React, { useState, useEffect } from "react";
import {
  Button,
  Flex,
  FormLabel,
  Input,
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
  Switch, // Import Switch component
} from "@chakra-ui/react";

const TriggerModal = ({
  isOpen,
  onClose,
  triggers,
  handleTriggerChange,
  onSubmit,
}) => {
  const [userAge, setUserAge] = useState("2020-01-01"); // mock data for user's birthdate
  const [isMenstruating, setIsMenstruating] = useState(false); // mock data for menstruation status

  // useEffect(() => {
  //   // Function to fetch user profile data from an API
  //   const fetchUserProfile = async () => {
  //     try {
  //       // Replace 'apiEndpoint' with the actual URL of your API endpoint
  //       const response = await fetch('apiEndpoint');
  //       if (response.ok) {
  //         const userData = await response.json();
  //         // Assuming the API returns the user's birthdate in the 'birthdate' field
  //         setUserAge(userData.birthdate);
  //       } else {
  //         console.error('Failed to fetch user profile data');
  //       }
  //     } catch (error) {
  //       console.error('Error fetching user profile data:', error);
  //     }
  //   };

  //   // Call the function to fetch user profile data
  //   fetchUserProfile();
  // }, []); // Run this effect only once, when the component mounts

  // Function to check if the user is 18 years old or more
  const isUserAdult = () => {
    if (!userAge) return false; // If userAge is null, assume user is not adult
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const userBirthYear = new Date(userAge).getFullYear();
    return currentYear - userBirthYear >= 18;
  };

  // useEffect(() => {
  //   const fetchMenstruationStatus = async () => {
  //     try {
  //       const response = await fetch('/api/menstruationStatus'); // Replace '/api/menstruationStatus' with your actual API endpoint
  //       if (!response.ok) {
  //         throw new Error('Failed to fetch menstruation status');
  //       }
  //       const data = await response.json();
  //       setIsMenstruating(data.isMenstruating);
  //     } catch (error) {
  //       console.error(error);
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   fetchMenstruationStatus();
  // }, []);

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Today's Triggers</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack spacing={4} align="stretch">
            {/* Mapping over each trigger to create a form input or checkbox */}

            {/* Sleep Quality */}
            <Flex align="left" direction="column">
              <FormLabel flexBasis="40%" mb="0">
                Sleep Quality (0-10)
              </FormLabel>
              <Slider
                mt={2}
                flex="1"
                aria-label="sleep-quality-slider"
                defaultValue={triggers.sleepQuality}
                min={0}
                max={10}
                step={1}
                onChange={(value) => handleTriggerChange("sleepQuality", value)}
              >
                <SliderTrack>
                  <SliderFilledTrack />
                </SliderTrack>
                <SliderThumb boxSize={6} fontSize="sm">
                  {triggers.sleepQuality}
                </SliderThumb>
              </Slider>
            </Flex>

            {/* Sleep Duration */}
            <Flex align="center">
              <FormLabel flex="1" mb="0">
                Sleep Duration (hours)
              </FormLabel>
              <Input
                type="number"
                name="sleepDuration"
                value={triggers.sleepDuration}
                onChange={(e) =>
                  handleTriggerChange("sleepDuration", e.target.value)
                }
                width="100px"
              />
            </Flex>

            {/* Stress Level */}
            <Flex align="left" direction="column">
              <FormLabel flex="1" mb="0">
                Stress Level (0-10)
              </FormLabel>
              <Slider
                mt={2}
                flex="1"
                aria-label="stress-level-slider"
                defaultValue={triggers.stressLevel}
                min={0}
                max={10}
                step={1}
                onChange={(value) => handleTriggerChange("stressLevel", value)}
              >
                <SliderTrack>
                  <SliderFilledTrack />
                </SliderTrack>
                <SliderThumb boxSize={6} fontSize="sm">
                  {triggers.stressLevel}
                </SliderThumb>
              </Slider>
            </Flex>

            {/* Caffeine Consumption */}
            <Flex align="center">
              <FormLabel flex="1" mb="0">
                Caffeine Consumption (cups)
              </FormLabel>
              <Input
                type="number"
                name="caffeineConsumption"
                value={triggers.caffeineConsumption}
                onChange={(e) =>
                  handleTriggerChange("caffeineConsumption", e.target.value)
                }
                width="100px"
              />
            </Flex>

            {/* Alcohol Consumption */}
            {isUserAdult() && (
              <Flex align="center">
                <FormLabel flex="1" mb="0">
                  Alcohol Consumption (cups)
                </FormLabel>
                <Input
                  type="number"
                  name="alcoholConsumption"
                  value={triggers.alcoholConsumption}
                  onChange={(e) =>
                    handleTriggerChange("alcoholConsumption", e.target.value)
                  }
                  width="100px"
                />
              </Flex>
            )}

            {/* Recreational Drug Consumption */}
            {isUserAdult() && (
              <Flex align="center">
                <FormLabel flex="1" mb="0">
                  Recreational Drug Consumption
                </FormLabel>
                <Switch
                  isChecked={triggers.drugsConsumption}
                  onChange={(e) =>
                    handleTriggerChange("drugsConsumption", e.target.checked)
                  }
                />
              </Flex>
            )}

            {/* Smoking */}
            {isUserAdult() && (
              <Flex align="center">
                <FormLabel flex="1" mb="0">
                  Smoked (number of cigarettes)
                </FormLabel>
                <Input
                  type="number"
                  name="smoking"
                  value={triggers.smoking}
                  onChange={(e) =>
                    handleTriggerChange("smoking", e.target.value)
                  }
                  width="100px"
                />
              </Flex>
            )}

            {/* Missing a Meal */}
            <Flex align="center">
              <FormLabel flex="1" mb="0">
                Skipped a Meal
              </FormLabel>
              <Switch
                isChecked={triggers.missingMeal}
                onChange={(e) =>
                  handleTriggerChange("missingMeal", e.target.checked)
                }
              />
            </Flex>

            {/* Fever */}
            <Flex direction="column">
              <Flex flex="1" alignItems="center">
                <FormLabel flex="1" mb="0">
                  Fever (°C)
                </FormLabel>
                <Switch
                  isChecked={triggers.fevers}
                  onChange={(e) =>
                    handleTriggerChange("fevers", e.target.checked)
                  }
                />
              </Flex>
              {triggers.fevers && (
                <Input
                  mt={2}
                  type="text"
                  name="feverValue"
                  placeholder="°C"
                  value={triggers.feverValue}
                  onChange={(e) =>
                    handleTriggerChange("feverValue", e.target.value)
                  }
                  width="100px"
                />
              )}
            </Flex>

            {/* Steps */}
            <Flex align="center">
              <FormLabel flex="1" mb="0">
                Step Count
              </FormLabel>
              <Input
                type="number"
                name="steps"
                value={triggers.steps}
                onChange={(e) => handleTriggerChange("steps", e.target.value)}
                width="100px"
              />
            </Flex>

            {/* High Intensity Minutes */}
            <Flex align="center">
              <FormLabel flex="1" mb="0">
                High Physical Exertion (minutes)
              </FormLabel>
              <Input
                type="number"
                name="highIntensityMinutes"
                value={triggers.highIntensityMinutes}
                onChange={(e) =>
                  handleTriggerChange("highIntensityMinutes", e.target.value)
                }
                width="100px"
              />
            </Flex>

            {/* Flashing Light */}
            <Flex align="center">
              <FormLabel flex="1" mb="0">
                Flashing light exposure
              </FormLabel>
              <Switch
                isChecked={triggers.flashingLight}
                onChange={(e) =>
                  handleTriggerChange("flashingLight", e.target.checked)
                }
              />
            </Flex>

            {/* Menstruation */}
            {isMenstruating && (
              <Flex align="center">
                <FormLabel flex="1" mb="0">
                  Menstruating
                </FormLabel>
                <Switch
                  isChecked={triggers.menstruating}
                  onChange={(e) =>
                    handleTriggerChange("menstruating", e.target.checked)
                  }
                />
              </Flex>
            )}

            {/* Adherence to Prescribed Medication Regimen */}
            <Flex align="center">
              <FormLabel flex="1" mb="0">
                Skipped medication
              </FormLabel>
              <Switch
                isChecked={triggers.medicationAdherence}
                onChange={(e) =>
                  handleTriggerChange("medicationAdherence", e.target.checked)
                }
              />
            </Flex>

            {/* Changes in Medication Dosage or Type */}
            <Flex align="center">
              <FormLabel flex="1" mb="0">
                Change in Medication
              </FormLabel>
              <Switch
                isChecked={triggers.medicationChanges}
                onChange={(e) =>
                  handleTriggerChange("medicationChanges", e.target.checked)
                }
              />
            </Flex>
          </VStack>
        </ModalBody>
        <ModalFooter>
          <Button colorScheme="gray" mr={3} onClick={onClose}>
            Close
          </Button>
          <Button colorScheme="blue" onClick={() => onSubmit(triggers)}>
            Submit
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default TriggerModal;
