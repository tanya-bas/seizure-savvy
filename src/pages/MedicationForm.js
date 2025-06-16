import React, { useState } from "react";
import {
  FormControl,
  FormLabel,
  Input,
  Select,
  ModalBody,
  ModalFooter,
  Button,
} from "@chakra-ui/react";

const MedicationForm = ({
  newMedication,
  handleChange,
  handleSaveMedication,
  handleCloseMedicationModal,
}) => {
  return (
    <>
      <ModalBody>
        <FormControl mb={4}>
          <FormLabel>Medication</FormLabel>
          <Input
            type="text"
            name="name"
            value={newMedication.name}
            onChange={handleChange}
          />
        </FormControl>
        <FormControl mb={4}>
          <FormLabel>Dosage (in mg)</FormLabel>
          <Input
            type="number"
            name="dosage"
            value={newMedication.dosage}
            onChange={handleChange}
          />
        </FormControl>
        <FormControl mb={4}>
          <FormLabel>Frequency</FormLabel>
          <Select
            name="frequency"
            value={newMedication.frequency}
            onChange={handleChange}
          >
            <option value="Once a day">Once a day</option>
            <option value="Twice a day">Twice a day</option>
            <option value="Three times a day">Three times a day</option>
            <option value="Four times a day">Four times a day</option>
          </Select>
        </FormControl>
        <FormControl mb={4}>
          <FormLabel>First Dose</FormLabel>
          <Input
            type="time"
            name="firstDose"
            value={newMedication.firstDose}
            onChange={handleChange}
          />
        </FormControl>
        <FormControl mb={4}>
          <FormLabel>Start Date</FormLabel>
          <Input
            type="date"
            name="startDate"
            value={newMedication.startDate}
            onChange={handleChange}
            max={new Date().toISOString().split("T")[0]}
          />
        </FormControl>
      </ModalBody>
      <ModalFooter>
        <Button
          colorScheme="blue"
          bgColor="#6a95e3"
          onClick={handleSaveMedication}
        >
          Save Medication
        </Button>
        <Button onClick={handleCloseMedicationModal} ml={2}>
          Cancel
        </Button>
      </ModalFooter>
    </>
  );
};

export default MedicationForm;
