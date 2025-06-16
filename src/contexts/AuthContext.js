import React, {
	createContext,
	useContext,
	useState,
	useEffect,
	useMemo,
} from "react";
import AuthService from "../services/AuthService";
import PropTypes from "prop-types";
import { jwtDecode } from "jwt-decode";

// Create an instance of AuthService
const authService = new AuthService();

// Create the authentication context with a default value
const AuthContext = createContext({
	user: null,
	login: () => {},
	logout: () => {},
	register: () => {},
	isAuthenticated: false,
});

const AuthProvider = ({ children }) => {
	const [user, setUser] = useState(null);
	const [isAuthenticated, setIsAuthenticated] = useState(false); // Initially set to false

	useEffect(() => {
		const checkUserAuthentication = async () => {
			try {
				const token = localStorage.getItem("accessToken");
				if (token) {
					const decodedToken = jwtDecode(token); // Decode the token
					const currentTime = Date.now() / 1000; // Current time in seconds
					if (decodedToken.exp > currentTime) {
						// Token is not expired
						const userData = await authService.validateUserAuthentication();
						setUser(userData);
						setIsAuthenticated(true);
						return;
					}
				}
				setUser(null);
				setIsAuthenticated(false);
			} catch (error) {
				console.error("Failed to authenticate user on startup:", error);
				setUser(null);
				setIsAuthenticated(false);
			}
		};

		checkUserAuthentication();
	}, []);

	const login = async (email, password) => {
		try {
			const userData = await authService.login(email, password);
			setUser(userData); // Assuming userData contains user info
			setIsAuthenticated(true);
		} catch (error) {
			console.error("Login error:", error);
			setIsAuthenticated(false);
			throw error;
		}
	};

	const register = async (userData) => {
		try {
			await authService.register(userData);
			// Optionally log the user in after registration
		} catch (error) {
			console.error("Registration error:", error);
			setIsAuthenticated(false);
			throw error;
		}
	};

	// TODO: Uncoment the server code after AuthService is implemented
	const logout = () => {
		// Clear user session on the client
		setUser(null);
		setIsAuthenticated(false);
		// Clear user session on the server
		authService.logout();
	};

	// TODO: add refresh token logic

	// Memoize the context value to update only when the user data changes
	const value = useMemo(
		() => ({ user, login, logout, register, isAuthenticated }),
		[user, isAuthenticated]
	);

	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

AuthProvider.propTypes = {
	children: PropTypes.node.isRequired,
};

/**
 * Custom hook to use the authentication client.
 * @returns {object} The authentication state and functions to register, log in,
 * log out a user and get the current user.
 * @example
 * import { useAuth } from "../contexts/AuthContext";
 *
 * function MyComponent() {
 * const { isAuthenticated, register, login, logout } = useAuth();
 * // ...
 * }
 */
export function useAuth() {
	return useContext(AuthContext);
}

export default AuthProvider;
