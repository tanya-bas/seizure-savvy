import ApiService from "./ApiService";

class UserService extends ApiService {
	/**
	 * Retrieve the details of the logged-in user.
	 * @returns {Promise} A promise that resolves with the user profile.
	 */
	async getUserProfile() {
		try {
			const response = await this.get("/user/profile");
			if (response.ok) {
				return response.body.data; // User profile data
			} else {
				throw new Error(
					response.body.message || "Failed to retrieve user profile."
				);
			}
		} catch (error) {
			throw new Error(error.message || "Failed to retrieve user profile data.");
		}
	}

	/**
	 * Update the personal details of the logged-in user.
	 * @param {Object} data The updated user data.
	 * @returns {Promise} A promise that resolves with the update response.
	 */
	async updateUserProfile(data) {
		try {
			const response = await this.put("/user/profile", data);
			if (response.ok) {
				return response.body; // Success message
			} else {
				throw new Error(
					response.body.message || "Failed to update user profile."
				);
			}
		} catch (error) {
			console.error(
				"Update profile error:",
				error.message || "An unexpected error occurred."
			);
			throw new Error(error.message || "Failed to update user profile.");
		}
	}

	/**
	 * Change the password of the logged-in user.
	 * @param {string} oldPassword The old password.
	 * @param {string} newPassword The new password.
	 * @returns {Promise} A promise that resolves with the change password response.
	 */
	async changePassword(oldPassword, newPassword) {
		try {
			const response = await this.put("/user/change-password", {
				old_password: oldPassword,
				new_password: newPassword,
			});
			if (response.ok) {
				return response.body; // Success message
			} else {
				throw new Error(response.body.message || "Failed to change password.");
			}
		} catch (error) {
			throw new Error(
				error.message || "Failed to change password. Please try again."
			);
		}
	}

	/**
	 * Delete the account of the logged-in user.
	 * @returns {Promise} A promise that resolves with the delete account response.
	 */
	async deleteAccount() {
		try {
			const response = await this.delete("/user/delete-account");
			if (response.ok) {
				return response.body; // Success message
			} else {
				throw new Error(response.body.message || "Failed to delete account.");
			}
		} catch (error) {
			throw new Error(error.message || "Failed to delete user account.");
		}
	}
}

export default UserService;
