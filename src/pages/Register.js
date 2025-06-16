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
	useToast,
} from "@chakra-ui/react";
import { ArrowBackIcon, ArrowForwardIcon } from "@chakra-ui/icons";
import { useNavigate } from "react-router-dom";
import PageHeader from "./PageHeader";
import { useAuth } from "../contexts/AuthContext";
import convertJSONKeysCase from "../utils/convertJSONKeysCase";

const RegistrationForm = () => {
	const { register } = useAuth();
	const toast = useToast();
	const [page, setPage] = useState(1);
	const [formData, setFormData] = useState({
		firstName: "",
		lastName: "",
		birthdate: "", // From birthDate to birthdate to match the database
		hasMenstruation: false,
		email: "",
		password: "",
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

		// Validate form data is not empty is NOT needed, since all fields are required
		// Removed the page === 2 condition and move up email + password
		// See Register v2 for the full code
		if (page === 2) {
			// Validate password
			if (formData.password.length < 8) {
				setPasswordError("Password must be at least 8 characters long");
				return;
			}
		}

		// Removed the page === 2 condition and move up email + password
		if (page === 1) {
			nextPage();
		} else {
			// Attempt to register
			try {
				// Convert keys to snake_case
				// const convertedData = convertJSONKeysCase(formData, "snake_case");
				await register(formData); // Register function accepts a single object with all user data
				toast({
					title: "Register successful",
					description:
						"You have successfully registered. Redirecting to login.",
					status: "success",
					duration: 9000,
					isClosable: true,
				});
				navigate("/login"); // Redirect user to login
			} catch (error) {
				// Display an error toast on login failure
				toast({
					title: "Register failed",
					description:
						error.message ||
						"Failed to log in. Please check your credentials and try again.",
					status: "error",
					duration: 9000,
					isClosable: true,
				});
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
										name="birthdate"
										value={formData.birthdate}
										onChange={handleChange}
										max={today}
										required
									/>
								</FormControl>
								<FormControl display="flex" alignItems="center">
									<FormLabel htmlFor="hasMenstruation" mb="0">
										Do you experience menstruation?
									</FormLabel>
									<Switch
										id="hasMenstruation"
										name="hasMenstruation"
										isChecked={formData.hasMenstruation}
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
					{/* Removed the page === 2 condition and move up email + password */}
					{page === 2 && (
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
