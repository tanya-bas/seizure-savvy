import React, { useState, useEffect } from "react";
import {
	Container,
	Text,
	Button,
	VStack,
	useToast,
	Flex,
	FormControl,
	FormLabel,
	Input,
	Switch,
	Modal,
	ModalOverlay,
	ModalContent,
	ModalHeader,
	ModalBody,
	ModalFooter,
	useDisclosure,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import BottomNavBar from "./BottomNavBar";
import PageHeader from "./PageHeader";
import { useAuth } from "../contexts/AuthContext";

const Profile = () => {
	const { user, logout } = useAuth();
	const [isEditing, setIsEditing] = useState(false);
	const [profileData, setProfileData] = useState({
		firstName: "",
		lastName: "",
		birthDate: "",
		menstruation: false,
	});
	const [newPassword, setNewPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [isPasswordMatch, setIsPasswordMatch] = useState(false);
	const [isPasswordValid, setIsPasswordValid] = useState(false);

	const navigate = useNavigate();
	const toast = useToast();
	const { isOpen, onOpen, onClose } = useDisclosure(); // For medication modal

	// Placeholder function for fetching profile data from the backend
	const fetchProfileData = async () => {
		try {
			// Make API call to fetch profile data
			// const response = await fetch('API_ENDPOINT/profile');
			// const data = await response.json();
			// Set mock profile data
			const mockData = {
				firstName: "John",
				lastName: "Doe",
				birthDate: "1990-01-01",
				menstruation: true,
			};
			// Update profile data state
			setProfileData(mockData);
		} catch (error) {
			console.error("Error fetching profile data:", error);
			toast({
				title: "Error",
				description: "Failed to fetch profile data",
				status: "error",
				duration: 5000,
				isClosable: true,
			});
		}
	};

	useEffect(() => {
		// Fetch profile data on component mount
		fetchProfileData();
	}, []);

	const handleEditProfile = () => {
		setIsEditing(true);
	};

	const handleSaveChanges = () => {
		// Placeholder function for updating profile data on the backend
		// Check if any required field is empty
		const isAnyFieldEmpty = Object.values(profileData).some(
			(value) => value === ""
		);
		if (isAnyFieldEmpty) {
			toast({
				title: "Error",
				description: "Please fill out all required fields.",
				status: "error",
				duration: 5000,
				isClosable: true,
			});
			return;
		}

		try {
			// Make API call to update profile data
			// await fetch('API_ENDPOINT/profile', {
			//   method: 'PUT',
			//   headers: {
			//     'Content-Type': 'application/json',
			//   },
			//   body: JSON.stringify(profileData),
			// });
			// Show success message
			toast({
				title: "Profile updated",
				status: "success",
				duration: 3000,
				isClosable: true,
			});
			setIsEditing(false);
		} catch (error) {
			console.error("Error updating profile:", error);
			toast({
				title: "Error",
				description: "Failed to update profile",
				status: "error",
				duration: 5000,
				isClosable: true,
			});
		}
	};

	const handleChange = (e) => {
		const { name, value, type, checked } = e.target;
		setProfileData((prevData) => ({
			...prevData,
			[name]: type === "checkbox" ? checked : value,
		}));
	};

	const handleLogout = () => {
		navigate("/"); // Redirect to login page
		logout(); // Clear user session
	};

	const handleResetPassword = () => {
		onOpen();
	};

	const handleSavePassword = () => {
		if (
			newPassword === confirmPassword &&
			newPassword !== "" &&
			newPassword.length >= 8
		) {
			// Call backend to save password
			onClose();
			toast({
				title: "Password reset successfully",
				status: "success",
				duration: 3000,
				isClosable: true,
			});
		} else {
			setIsPasswordMatch(newPassword === confirmPassword && newPassword !== "");
			setIsPasswordValid(newPassword.length >= 8);
		}
	};

	return (
		<>
			<PageHeader pageTitle="Profile" />
			<Container maxW="md" mt={10} pb="100px">
				{!isEditing ? (
					<VStack spacing={4} align="stretch">
						<Flex direction="column" align="center">
							<Text textAlign="center" fontWeight="bold">
								Name
							</Text>
							<Text>
								{profileData.firstName} {profileData.lastName}
							</Text>
						</Flex>
						<Flex direction="column" align="center">
							<Text textAlign="center" fontWeight="bold">
								Birthday
							</Text>
							<Text>{profileData.birthDate}</Text>
						</Flex>
						<Flex direction="column" align="center">
							<Text textAlign="center" fontWeight="bold">
								Do you experience menstruation?
							</Text>
							<Text>{profileData.menstruation ? "Yes" : "No"}</Text>
						</Flex>
						<Flex justify="center">
							<Button
								mt={6}
								colorScheme="blue"
								bgColor="#6a95e3"
								onClick={handleEditProfile}
							>
								Edit Profile
							</Button>
						</Flex>
						<Flex justify="center">
							<Button
								mt={4}
								colorScheme="green"
								color="white"
								bgColor="#02ba98"
								onClick={handleResetPassword}
							>
								Reset Password
							</Button>
						</Flex>
						<Flex justify="center" mt={6}>
							<Button colorScheme="gray" onClick={handleLogout}>
								Logout
							</Button>
						</Flex>
					</VStack>
				) : (
					<VStack spacing={4} align="stretch">
						<FormControl isRequired>
							<FormLabel>First Name</FormLabel>
							<Input
								type="text"
								name="firstName"
								value={profileData.firstName}
								onChange={handleChange}
							/>
						</FormControl>
						<FormControl isRequired>
							<FormLabel>Last Name</FormLabel>
							<Input
								type="text"
								name="lastName"
								value={profileData.lastName}
								onChange={handleChange}
							/>
						</FormControl>
						<FormControl isRequired>
							<FormLabel>Birthday</FormLabel>
							<Input
								type="date"
								name="birthDate"
								value={profileData.birthDate}
								onChange={handleChange}
							/>
						</FormControl>
						<FormControl display="flex" alignItems="center">
							<FormLabel htmlFor="menstruation" mb="0">
								Do you experience menstruation?
							</FormLabel>
							<Switch
								id="menstruation"
								name="menstruation"
								isChecked={profileData.menstruation}
								onChange={handleChange}
							/>
						</FormControl>
						<Flex justify="center">
							<Button
								mt={6}
								colorScheme="blue"
								bgColor="#6a95e3"
								onClick={handleSaveChanges}
							>
								Save Changes
							</Button>
						</Flex>
					</VStack>
				)}
			</Container>
			<Modal isOpen={isOpen} onClose={onClose}>
				<ModalOverlay />
				<ModalContent>
					<ModalHeader>Reset Password</ModalHeader>
					<ModalBody>
						<FormControl isRequired>
							<FormLabel>New Password</FormLabel>
							<Input
								type="password"
								value={newPassword}
								onChange={(e) => setNewPassword(e.target.value)}
							/>
							{!isPasswordValid && (
								<Text color="red">
									Password must be at least 8 characters long
								</Text>
							)}
						</FormControl>
						<FormControl isRequired mt={4}>
							<FormLabel>Confirm Password</FormLabel>
							<Input
								type="password"
								value={confirmPassword}
								onChange={(e) => setConfirmPassword(e.target.value)}
							/>
							{!isPasswordMatch && (
								<Text color="red">Passwords do not match or are empty.</Text>
							)}
						</FormControl>
					</ModalBody>
					<ModalFooter>
						<Button
							colorScheme="blue"
							bgColor="#6a95e3"
							onClick={handleSavePassword}
						>
							Save
						</Button>
						<Button onClick={onClose}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
			<BottomNavBar />
		</>
	);
};

export default Profile;
