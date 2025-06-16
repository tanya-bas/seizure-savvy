import axios from "axios";
import convertJSONKeysCase from "../utils/convertJSONKeysCase";

// Base class for API clients to be inherited from
export default class ApiService {
	constructor() {

		this.base_url = "http://127.0.0.1:5000/api";

		// Initialize axios instance with secure defaults
		this.client = axios.create({
			baseURL: this.base_url,
			headers: {
				"Content-Type": "application/json",
			},
			withCredentials: true,
		});

		// Request interceptor to include the authorization token if available
		this.client.interceptors.request.use(
			(config) => {
				const token = localStorage.getItem("accessToken");

				// Include the authorization token if it's available
				if (token) {
					config.headers["Authorization"] = `Bearer ${token}`;
				}
				return config;
			},
			(error) => {
				return Promise.reject(error);
			}
		);
	}

	// Convert JSON keys based on the request method
	convertKeys(data, method) {
		if (method === "GET") {
			return convertJSONKeysCase(data, "camelCase");
		} else {
			return convertJSONKeysCase(data, "snake_case");
		}
	}

	// General request method using axios
	async request(options) {
		try {
			const query = options.query
				? new URLSearchParams(options.query).toString()
				: "";

			const url = options.url + (query ? `?${query}` : "");

			// Convert JSON keys based on the request method
			const convertedBody = this.convertKeys(options.body, options.method);

			const response = await this.client({
				url: url,
				method: options.method,
				data: convertedBody,
				headers: options.headers,
			});

			return {
				ok: response.status >= 200 && response.status < 300,
				status: response.status,
				body: response.data,
			};
		} catch (error) {
			console.error("API Request failed:", error);
			return {
				ok: false,
				status: error.response ? error.response.status : 500,
				body: error.response
					? error.response.data
					: {
							code: 500,
							message: "The server is unresponsive",
							description: error.toString(),
					  },
			};
		}
	}

	// Convenience methods for different request types
	async get(url, query, options = {}) {
		return this.request({ method: "GET", url, query, ...options });
	}

	async post(url, body, options = {}) {
		return this.request({ method: "POST", url, body, ...options });
	}

	async put(url, body, options = {}) {
		return this.request({ method: "PUT", url, body, ...options });
	}

	async patch(url, body, options = {}) {
		return this.request({ method: "PATCH", url, body, ...options });
	}

	async delete(url, options = {}) {
		return this.request({ method: "DELETE", url, ...options });
	}
}
