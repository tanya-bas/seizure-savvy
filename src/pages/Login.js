// Login.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
	Button,
	Input,
	FormControl,
	FormLabel,
	Container,
	useToast,
	Text,
} from "@chakra-ui/react";
import PageHeader from "./PageHeader";

import { useAuth } from "../contexts/AuthContext";

const Login = () => {
	const { login } = useAuth(); // Get the login function from the AuthContext
	const [email, setEmail] = useState(""); // Changed from username to email
	const [password, setPassword] = useState("");
	const navigate = useNavigate(); // Hook to navigate to different routes
	const toast = useToast(); // Chakra UI Toast for notifications

	const handleLogin = async (event) => {
		event.preventDefault();

		if (!email || !password) {
			toast({
				title: "Authentication failed",
				description: "Please enter both email and password",
				status: "error",
				duration: 9000,
				isClosable: true,
			});
			return;
		}

		try {
			// Call the login function from the AuthContext
			await login(email, password);
			console.log("Login successful");
			navigate("/home"); // Redirect to the home page upon successful login
		} catch (error) {
			console.error("Login error:", error);
			// Display an error toast on login failure
			toast({
				title: "Login failed",
				description:
					error.message ||
					"Failed to log in. Please check your credentials and try again.",
				status: "error",
				duration: 9000,
				isClosable: true,
			});
		}
	};

	const handleNavigateToRegister = () => {
		// Navigate to the registration page
		navigate("/register");
	};

	return (
		<Container
			maxW=""
			bg="#f7f7f7"
			minHeight="100vh"
			p={0}
			display="flex"
			flexDirection="column"
		>
			<PageHeader pageTitle="Seizure Savvy" />
			<Container
				maxW="lg"
				flex="1"
				bg="#f7f7f7"
				p={4}
				pb="100px"
				overflowY="auto"
			>
				<form onSubmit={handleLogin}>
					<FormControl isRequired>
						<FormLabel htmlFor="email">Email</FormLabel>{" "}
						{/* Changed from username to email */}
						<Input
							id="email"
							type="email" // Changed type to email
							value={email}
							onChange={(e) => setEmail(e.target.value)}
							aria-label="Email"
							placeholder="Enter your email" // Changed placeholder
						/>
					</FormControl>
					<FormControl isRequired mt="4">
						<FormLabel htmlFor="password">Password</FormLabel>
						<Input
							id="password"
							type="password"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							aria-label="Password"
							placeholder="Enter your password"
						/>
					</FormControl>
					<Button
						type="submit"
						colorScheme="blue"
						bgColor="#6a95e3"
						size="lg"
						mt="6"
						w="100%"
					>
						Login
					</Button>
				</form>
				<Text mt="4" textAlign="center">
					Don't have an account?{" "}
					<Button
						colorScheme="teal"
						variant="link"
						onClick={handleNavigateToRegister}
					>
						Click here to register
					</Button>
				</Text>
			</Container>
		</Container>
	);
};

export default Login;
