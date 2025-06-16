import React, { useState, useEffect } from "react";
import {
  Box,
  Checkbox,
  CheckboxGroup,
  Stack,
  Text,
  Flex,
  Icon,
} from "@chakra-ui/react";
import { BiCapsule } from "react-icons/bi"; // Import the BiCapsulePillIcon

const MedicationChecklist = ({ medications }) => {
  const [medicationDoses, setMedicationDoses] = useState([]);

  useEffect(() => {
    fetchMedicationDosesToday();
  }, []);

  const fetchMedicationDosesToday = async () => {
    try {
      // API call to fetch medication doses logged today
      // Mock response
      const mockData = [
        { medication_id: 1, dose_time: "2024-04-16T08:00:00.000Z" },
        { medication_id: 2, dose_time: "2024-04-16T13:00:00.000Z" },
      ];

      // Convert dose_time from ISO format to 'h:mm a' format
      const updatedData = mockData.map((data) => {
        const timeParts = data.dose_time.split("T")[1].split(":");
        const hours = parseInt(timeParts[0]);
        const minutes = timeParts[1];
        const ampm = hours >= 12 ? "pm" : "am";
        const formattedHours = hours > 12 ? hours - 12 : hours;
        const formattedTime = `${formattedHours}:${minutes} ${ampm}`;
        return { ...data, dose_time: formattedTime };
      });

      setMedicationDoses(updatedData);

      console.log("Medication doses today:", updatedData);
    } catch (error) {
      console.error("Error fetching medication doses today:", error.message);
    }
  };

  const addMedicationDose = async (medicationDoseData) => {
    try {
      // Uncomment the following lines to make the API call
      // const response = await fetch('/api/medication-doses', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(medicationDoseData),
      // });

      // if (!response.ok) {
      //   throw new Error('Failed to add medication dose');
      // }

      // const data = await response.json();
      // console.log('Medication dose added successfully:', data);

      // Mock response
      console.log("Medication dose added successfully:", medicationDoseData);
    } catch (error) {
      console.error("Error adding medication dose:", error.message);
    }
  };

  const generateChecklist = (medication) => {
    const { id, name, frequency, dosage, firstDose } = medication;
    const doseTimes = calculateDoseTimes(frequency, firstDose);

    const handleCheckboxChange = (time) => {
      // Get current date and time in ISO format
      const currentDate = new Date();
      const [hours, minutes, ampm] = time.split(/:| /);
      const isPM = ampm.toLowerCase() === "pm";
      currentDate.setHours(isPM ? parseInt(hours) + 12 : parseInt(hours));
      currentDate.setMinutes(parseInt(minutes));

      // Trigger addMedicationDose function with medication id and dose time
      addMedicationDose({
        medication_id: id,
        dose_time: currentDate.toISOString(),
      });
    };

    return (
      <Box
        key={id}
        bg="#FFF"
        p={4}
        borderRadius={18}
        mb={4}
        boxShadow="base"
        width="calc(100% - 45px)"
      >
        <Flex alignItems="center">
          <Icon as={BiCapsule} color="#02ba98" boxSize={7} mr={2} mb={2} />{" "}
          {/* Add the calendar icon */}
          <Text fontWeight="bold" fontSize="lg" mb={2}>
            {name} {dosage}mg
          </Text>
        </Flex>
        <CheckboxGroup colorScheme="white">
          <Stack spacing={2}>
            {doseTimes.map((time) => (
              <Box key={time} bg="#F7f7f7" p={4} borderRadius={18}>
                <Checkbox
                  size="lg"
                  defaultChecked={medicationDoses.some(
                    (dose) =>
                      dose.medication_id === id && dose.dose_time === time
                  )}
                  iconColor="#6a95e3"
                  onChange={() => handleCheckboxChange(time)}
                >
                  {time}
                </Checkbox>
              </Box>
            ))}
          </Stack>
        </CheckboxGroup>
      </Box>
    );
  };

  const calculateDoseTimes = (frequency, firstDose) => {
    const timesPerDay = {
      "Once a day": 1,
      "Twice a day": 2,
      "Three times a day": 3,
      "Four times a day": 4,
    };

    const hoursPerDay = 24;
    const doses = timesPerDay[frequency];
    const startTime = new Date(`2000-01-01T${firstDose}:00`);
    const doseInterval =
      doses === 4 ? 4 : doses === 3 ? 7 : hoursPerDay / doses;
    const doseTimes = [];

    for (let i = 0; i < doses; i++) {
      const doseTime = new Date(
        startTime.getTime() + i * doseInterval * 60 * 60 * 1000
      );
      doseTimes.push(formatTime(doseTime));
    }

    console.log(doseTimes);

    return doseTimes;
  };

  const formatTime = (time) => {
    const formattedTime = time.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
    // Split the formatted time string to get hours, minutes, and AM/PM
    const [hours, minutes, ampm] = formattedTime.split(/:| /); // Split by colon or space
    // Remove leading zero for hours if it exists
    const formattedHours = hours.startsWith("0") ? hours.substr(1) : hours;
    // Combine hours, minutes, and AM/PM with a colon
    return `${formattedHours}:${minutes} ${ampm.toLowerCase()}`;
  };

  return (
    <>
      {medications.map((medication) => {
        if (medication.endDate === null) {
          return generateChecklist(medication);
        } else {
          return null; // Skip generating checklist for medications with an end date
        }
      })}
    </>
  );
};

export default MedicationChecklist;
