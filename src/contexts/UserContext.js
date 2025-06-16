import React, {
	createContext,
	useContext,
	useState,
	useMemo,
	useCallback,
} from "react";
import UserService from "../services/UserService";
import PropTypes from "prop-types";

// Create a context for user-related state
const UserContext = createContext();

// Custom hook to access the UserContext
export const useUser = () => {
	const context = useContext(UserContext);
	if (!context) {
		throw new Error(
			"useUser must be used within a UserProvider. Wrap the component inside UserProvider to fix this error, either component itself or its ancestor, like App.js."
		);
	}
	return context;
};

// UserProvider component to manage user-related state
const UserProvider = ({ children }) => {
	// Create an instance of UserService
	const userService = useMemo(() => new UserService(), []);

	const [profileData, setProfileData] = useState(null);

	// Function to fetch user profile
	const fetchUserProfile = useCallback(async () => {
		try {
			const profile = await userService.getUserProfile();
			setProfileData(profile);
		} catch (error) {
			console.log(error);
			// TODO: Redirect the user to login page if the token is invalid
			throw error;
		}
	}, [userService]);

	// Function to update user profile
	const updateProfile = useCallback(
		async (data) => {
			try {
				await userService.updateUserProfile(data);
				await fetchUserProfile(); // Refresh user profile after update
			} catch (error) {
				console.log(error);
				throw error;
			}
		},
		[userService, fetchUserProfile]
	);

	// Function to handle password change
	const changePassword = useCallback(
		async (oldPassword, newPassword) => {
			try {
				await userService.changePassword(oldPassword, newPassword);
				// You might want to clear sensitive data from the state after this operation
			} catch (error) {
				console.log(error);
				throw error;
			}
		},
		[userService]
	);

	// Function to delete user account
	const deleteAccount = useCallback(async () => {
		try {
			await userService.deleteAccount();
			setProfileData(null); // Clear user profile after deletion
			// You might want to redirect the user after account deletion
		} catch (error) {
			console.log(error);
			throw error;
		}
	}, [userService]);

	// Wrap the 'value' object in a useMemo hook
	const value = useMemo(
		() => ({
			profileData,
			setProfileData,
			fetchUserProfile,
			updateProfile,
			changePassword,
			deleteAccount,
		}),
		[
			profileData,
			fetchUserProfile,
			updateProfile,
			changePassword,
			deleteAccount,
		]
	);

	// Render the UserContext.Provider with the provided value
	return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

// Define prop types for UserProvider
UserProvider.propTypes = {
	children: PropTypes.node.isRequired,
};

export default UserProvider;
