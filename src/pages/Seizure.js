import React, { useState } from "react";
import {
	Button,
	Modal,
	ModalOverlay,
	ModalContent,
	ModalHeader,
	ModalBody,
	ModalCloseButton,
	ModalFooter,
	FormControl,
	FormLabel,
	Input,
	Select,
	Checkbox,
	VStack,
	Icon,
	IconButton,
	Text,
	Slider,
	SliderTrack,
	SliderFilledTrack,
	SliderThumb,
} from "@chakra-ui/react";
import { InfoOutlineIcon } from "@chakra-ui/icons";

const SeizureModal = ({ isOpen, onClose, onSubmit }) => {
	const [seizureData, setSeizureData] = useState({
		typeOfSeizure: "",
		duration: "",
		frequency: "",
		emergencyIntervention: false,
		postictalSymptoms: {
			Confusion: { duration: "", intensity: 0 },
			Headache: { duration: "", intensity: 0 },
			Fatigue: { duration: "", intensity: 0 },
		},
		notes: "",
	});
	const [infoModalOpen, setInfoModalOpen] = useState(false);

	const handleSeizureChange = (field, value) => {
		setSeizureData((prev) => ({
			...prev,
			[field]: typeof value === "boolean" ? value : value.target.value,
		}));
	};

	const handlePostictalSymptomChange = (symptom, field, value) => {
		setSeizureData((prev) => ({
			...prev,
			postictalSymptoms: {
				...prev.postictalSymptoms,
				[symptom]: {
					...prev.postictalSymptoms[symptom],
					[field]: value,
				},
			},
		}));
	};

	const handleSubmit = () => {
		onSubmit(seizureData);
		onClose();
	};

	const handleInfoIconClick = () => {
		setInfoModalOpen(true);
	};

	const handleInfoModalClose = () => {
		setInfoModalOpen(false);
	};

	return (
		<Modal isOpen={isOpen} onClose={onClose}>
			<ModalOverlay />
			<ModalContent>
				<ModalHeader>Seizure Information</ModalHeader>
				<ModalCloseButton />
				<ModalBody>
					<VStack spacing={4}>
						<FormControl>
							<FormLabel>Type of Seizure</FormLabel>
							<Select
								value={seizureData.typeOfSeizure}
								onChange={(e) => handleSeizureChange("typeOfSeizure", e)}
							>
								<option value="focal">Focal</option>
								<option value="generalized">Generalized</option>
								<option value="complex">Complex</option>
								<option value="unknown">Unknown</option>
							</Select>
						</FormControl>
						<FormControl>
							<FormLabel>Duration (in minutes)</FormLabel>
							<Input
								type="number"
								value={seizureData.duration}
								onChange={(e) => handleSeizureChange("duration", e)}
							/>
						</FormControl>
						<FormControl>
							<FormLabel>Frequency</FormLabel>
							<Input
								type="number"
								value={seizureData.frequency}
								onChange={(e) => handleSeizureChange("frequency", e)}
							/>
						</FormControl>
						<FormControl display="flex" alignItems="center">
							<FormLabel mb="0">Emergency Intervention?</FormLabel>
							<Checkbox
								isChecked={seizureData.emergencyIntervention}
								onChange={(e) =>
									handleSeizureChange("emergencyIntervention", e.target.checked)
								}
							/>
						</FormControl>
						<FormControl>
							<FormLabel>
								Postictal Symptoms{" "}
								<IconButton
									aria-label="info"
									icon={<InfoOutlineIcon />}
									colorScheme="gray"
									onClick={handleInfoIconClick}
								/>
							</FormLabel>
							{Object.entries(seizureData.postictalSymptoms).map(
								([symptom, data]) => (
									<FormControl key={symptom}>
										<VStack align="flex-start">
											<Text>{symptom}</Text>
											<Input
												width="100px"
												placeholder={`Duration of ${symptom}`}
												type="number"
                        mb={2}
												value={data.duration}
												onChange={(e) =>
													handlePostictalSymptomChange(
														symptom,
														"duration",
														e.target.value
													)
												}
											/>
										</VStack>
										<Slider
											aria-label={`Intensity of ${symptom}`}
											min={0}
											max={10}
											value={data.intensity}
											onChange={(value) =>
												handlePostictalSymptomChange(
													symptom,
													"intensity",
													value
												)
											}
										>
											<SliderTrack>
												<SliderFilledTrack />
											</SliderTrack>
											<SliderThumb boxSize={6} fontSize="sm">
												{data.intensity}
											</SliderThumb>
										</Slider>
									</FormControl>
								)
							)}
						</FormControl>
						<FormControl>
							<FormLabel>Notes</FormLabel>
							<Input
								value={seizureData.notes}
								onChange={(e) => handleSeizureChange("notes", e)}
							/>
						</FormControl>
					</VStack>
				</ModalBody>
				<ModalFooter>
					<Button colorScheme="gray" mr={3} onClick={onClose}>
						Close
					</Button>
					<Button colorScheme="blue" onClick={handleSubmit}>
						Submit
					</Button>
				</ModalFooter>
			</ModalContent>
			<Modal isOpen={infoModalOpen} onClose={handleInfoModalClose}>
				<ModalOverlay />
				<ModalContent>
					<ModalHeader>Postictal Symptoms</ModalHeader>
					<ModalCloseButton />
					<ModalBody>
						<Text>
							Postictal symptoms refer to the symptoms that occur after a
							seizure, such as confusion, fatigue, and headache.
						</Text>
					</ModalBody>
					<ModalFooter>
						<Button colorScheme="blue" onClick={handleInfoModalClose}>
							Close
						</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</Modal>
	);
};

export default SeizureModal;
