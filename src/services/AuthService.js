import ApiService from "./ApiService";

class AuthService extends ApiService {
	/**
	 * Validate whether the user is authenticated or not.
	 * @returns {Promise} A promise that resolves with the user profile.
	 */
	async validateUserAuthentication() {
		try {
			const response = await this.get("/user/profile");
			if (response.ok) {
				return response.body; // User profile data
			} else {
				throw new Error(response.body.message || "Failed to get current user.");
			}
		} catch (error) {
			throw new Error(error.message || "Failed to verify user authentication.");
		}
	}
	/**
	 * Register a new user with the provided details.
	 * @param {Object} userData The user data for registration.
	 * @returns {Promise} A promise that resolves with the registration response.
	 */
	async register(userData) {
		try {
			const response = await this.post("/auth/register", userData);
			if (response.ok) {
				return response.body; // Registration success, could include user data or confirmation message
			} else {
				throw new Error(response.body.message || "Registration failed.");
			}
		} catch (error) {
			console.error(
				"Registration error:",
				error.message || "An unexpected error occurred."
			);
			throw new Error(
				`Registration error: ${error.message || "Failed to register."}`
			);
		}
	}

	/**
	 * Login a user with the provided credentials.
	 * @param {string} email 
	 * @param {string} password 
	 * @returns {Promise} A promise that resolves with the login response.
	 */
	async login(email, password) {
		try {
			const credentials = { email, password };
			const response = await this.post("/auth/login", credentials);

			// Check the 'ok' field to determine if the request was successful
			if (response.ok) {
				// Store the access token in local storage
				localStorage.setItem("accessToken", response.body.access_token);
				return response.body;
			} else {
				// Handle unsuccessful attempts by throwing an error
				throw new Error(response.body.message || "Login failed.");
			}
		} catch (error) {
			console.error(
				"Login error:",
				error.message || "An unexpected error occurred."
			);
			// Re-throw to allow further handling by the caller, such as displaying error messages in the UI
			throw new Error(error.message || "Failed to log in.");
		}
	}

	/**
	 * Refresh the access token using the refresh token.
	 * @returns {Promise} A promise that resolves with the new access token.
	 */
	async refreshAccessToken() {
		try {
			const response = await this.post("/auth/refresh");
			if (response.ok) {
				// Store the new access token in local storage
				localStorage.setItem("accessToken", response.body.access_token);
			} else {
				throw new Error(response.body.message || "Failed to refresh token.");
			}
		} catch (error) {
			const errorMessage = error.body?.message || "Failed to refresh token.";
			console.error("Token refresh error:", errorMessage);
			throw new Error(errorMessage);
		}
	}

	async logout() {
		// Remove the access token from local storage
		localStorage.removeItem("accessToken");
	}
}

export default AuthService;
