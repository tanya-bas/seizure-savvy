// This is the register process WITH medications in it.
// Not in used, but kept for reference. Will be added in the future.
import React, { useState } from "react";
import {
	Container,
	Button,
	Flex,
	Icon,
	FormControl,
	FormLabel,
	Input,
	Switch,
	Stack,
	FormErrorMessage,
	Text,
	Select,
} from "@chakra-ui/react";
import { ArrowBackIcon, ArrowForwardIcon } from "@chakra-ui/icons";
import { useNavigate } from "react-router-dom";
import PageHeader from "./PageHeader";
import { useAuth } from "../contexts/AuthContext";

const RegistrationForm = () => {
	const { register } = useAuth();
	const [page, setPage] = useState(1);
	const [formData, setFormData] = useState({
		firstName: "",
		lastName: "",
		birthDate: "",
		menstruation: false,
		email: "",
		password: "",
		takeMedication: false,
		medication: "",
		dosage: "",
		frequency: "",
		startDate: new Date().toISOString().split("T")[0],
		firstDose: "08:00",
	});
	const [passwordError, setPasswordError] = useState("");
	const navigate = useNavigate();

	const handleChange = (e) => {
		const { name, value, type, checked } = e.target;
		setFormData((prevData) => ({
			...prevData,
			[name]: type === "checkbox" ? checked : value,
		}));

		if (name === "password") {
			setPasswordError("");
		}
	};

	const handleSubmit = async (e) => {
		e.preventDefault();

		// Validate form data
		if (page === 1) {
			if (!formData.firstName || !formData.lastName || !formData.birthDate) {
				alert("Please fill in all required fields");
				return;
			}
		} else if (page === 2) {
			/*
        if (
          formData.takeMedication &&
          (!formData.medication || !formData.dosage || !formData.frequency)
        ) {
          alert("Please fill in all required fields");
          return;
        }
      */
			nextPage();
		} else if (page === 3) {
			if (!formData.email || !formData.password) {
				alert("Please fill in all required fields");
				return;
			}

			// Validate password
			if (formData.password.length < 8) {
				setPasswordError("Password must be at least 8 characters long");
				return;
			}
		}

		// Proceed to the next page or redirect if registration is successful
		if (page === 1 || page === 2) {
			nextPage();
		} else {
			// Attempt to register
			try {
				await register(formData); // Assumes register function accepts a single object with all user data
				navigate("/login"); // Redirect user to login
			} catch (error) {
				console.error("Registration failed:", error);
				alert("Registration failed. Please try again.");
			}
		}
	};

	const nextPage = () => {
		setPage(page + 1);
	};

	const prevPage = () => {
		setPage(page - 1);
	};

	// Get today's date in YYYY-MM-DD format
	const today = new Date().toISOString().split("T")[0];
	return (
		<>
			<Container
				maxW=""
				bg="#f7f7f7"
				minHeight="100vh"
				p={0}
				display="flex"
				flexDirection="column"
			>
				<PageHeader pageTitle="Register" />
				<Container
					maxW="lg"
					flex="1"
					bg="#f7f7f7"
					p={4}
					pb="100px"
					overflowY="auto"
				>
					{page === 1 && (
						<form onSubmit={handleSubmit}>
							<Stack spacing={4}>
								<FormControl>
									<FormLabel>
										First Name{" "}
										<Text as="span" color="red">
											*
										</Text>
									</FormLabel>
									<Input
										type="text"
										name="firstName"
										value={formData.firstName}
										onChange={handleChange}
										required
									/>
								</FormControl>
								<FormControl>
									<FormLabel>
										Last Name{" "}
										<Text as="span" color="red">
											*
										</Text>
									</FormLabel>
									<Input
										type="text"
										name="lastName"
										value={formData.lastName}
										onChange={handleChange}
										required
									/>
								</FormControl>
								<FormControl>
									<FormLabel>
										Birth Date{" "}
										<Text as="span" color="red">
											*
										</Text>
									</FormLabel>
									<Input
										type="date"
										name="birthDate"
										value={formData.birthDate}
										onChange={handleChange}
										max={today}
										required
									/>
								</FormControl>
								<FormControl display="flex" alignItems="center">
									<FormLabel htmlFor="menstruation" mb="0">
										Do you experience menstruation?
									</FormLabel>
									<Switch
										id="menstruation"
										name="menstruation"
										isChecked={formData.menstruation}
										onChange={handleChange}
									/>
								</FormControl>
							</Stack>
							<Flex justify="flex-end" mt={6}>
								<Button
									rightIcon={<Icon as={ArrowForwardIcon} />}
									colorScheme="blue"
									bgColor="#6a95e3"
									type="submit"
								>
									Next
								</Button>
							</Flex>
						</form>
					)}
					{page === 2 && (
						<form onSubmit={handleSubmit}>
							<Stack spacing={4}>
								<FormControl display="flex" alignItems="center">
									<FormLabel htmlFor="takeMedication" mb="0">
										Do you take any medication for your seizures?
									</FormLabel>
									<Switch
										id="takeMedication"
										name="takeMedication"
										isChecked={formData.takeMedication}
										onChange={handleChange}
									/>
								</FormControl>
								{formData.takeMedication && (
									<>
										<FormControl>
											<FormLabel>
												Medication{" "}
												<Text as="span" color="red">
													*
												</Text>
											</FormLabel>
											<Input
												type="text"
												name="medication"
												value={formData.medication}
												onChange={handleChange}
												required
											/>
										</FormControl>
										<FormControl>
											<FormLabel>
												Dosage (in mg){" "}
												<Text as="span" color="red">
													*
												</Text>
											</FormLabel>
											<Input
												type="number"
												name="dosage"
												value={formData.dosage}
												onChange={handleChange}
												required
											/>
										</FormControl>
										<FormControl>
											<FormLabel>
												Frequency{" "}
												<Text as="span" color="red">
													*
												</Text>
											</FormLabel>
											<Select
												name="frequency"
												value={formData.frequency}
												onChange={handleChange}
												required
											>
												<option value="1">Once a day</option>
												<option value="2">Twice a day</option>
												<option value="3">Three times a day</option>
												<option value="4">Four times a day</option>
											</Select>
										</FormControl>
										<FormControl>
											<FormLabel>Start Date</FormLabel>
											<Input
												type="date"
												name="startDate"
												value={formData.startDate}
												onChange={handleChange}
												max={today}
												required
											/>
										</FormControl>
										<FormControl>
											<FormLabel>First Dose</FormLabel>
											<Input
												type="time"
												name="firstDose"
												value={formData.firstDose}
												onChange={handleChange}
												required
											/>
										</FormControl>
									</>
								)}
							</Stack>
							<Flex justify="space-between" mt={6}>
								<Button
									leftIcon={<Icon as={ArrowBackIcon} />}
									onClick={prevPage}
								>
									Previous
								</Button>
								<Button
									rightIcon={<Icon as={ArrowForwardIcon} />}
									colorScheme="blue"
									bgColor="#6a95e3"
									type="submit"
								>
									Next
								</Button>
							</Flex>
						</form>
					)}
					{page === 3 && (
						<form onSubmit={handleSubmit}>
							<Stack spacing={4}>
								<FormControl>
									<FormLabel>
										Email{" "}
										<Text as="span" color="red">
											*
										</Text>
									</FormLabel>
									<Input
										type="email"
										name="email"
										value={formData.email}
										onChange={handleChange}
										required
									/>
								</FormControl>
								<FormControl>
									<FormLabel>
										Password{" "}
										<Text as="span" color="red">
											*
										</Text>
									</FormLabel>
									<Input
										type="password"
										name="password"
										value={formData.password}
										onChange={handleChange}
										minLength={8}
										required
									/>
									<FormErrorMessage>{passwordError}</FormErrorMessage>
								</FormControl>
							</Stack>
							<Flex justify="space-between" mt={6}>
								<Button
									leftIcon={<Icon as={ArrowBackIcon} />}
									onClick={prevPage}
								>
									Previous
								</Button>
								<Button type="submit" colorScheme="blue" bgColor="#6a95e3">
									Register
								</Button>
							</Flex>
						</form>
					)}
				</Container>
			</Container>
		</>
	);
};

export default RegistrationForm;
