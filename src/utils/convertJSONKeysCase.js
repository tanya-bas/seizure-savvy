/**
 * Converts the keys of a JSON object between camelCase and snake_case.
 *
 * @param {Object} data - The JSON object to convert.
 * @param {string} convertTo - The case to convert to ("snake_case" / "send" or "camelCase" / "receive"). Defaults to "snake_case".
 * @returns {Object} The converted JSON object.
 *
 * @example
 * const data = {
 *  firstName: "John",
 *  lastName: "Doe",
 * };
 * const convertedData = convertJSONKeysCase(data, "snake_case");
 * console.log(convertedData); // { first_name: "John", last_name: "Doe" }
 */
export default function convertJSONKeysCase(data, convertTo = "snake_case") {
	// Check if data is json object
	if (typeof data !== "object" || Array.isArray(data)) {
		throw new Error("Data must be a JSON object.");
	}
	if (typeof convertTo !== "string") {
		throw new Error("convertTo must be a string.");
	}

	// Check if convertTo is valid
	if (convertTo === "snake_case" || convertTo === "send") {
		return convertKeys(data, camelToSnake);
	} else if (convertTo === "camelCase" || convertTo === "receive") {
		return convertKeys(data, snakeToCamel);
	} else {
		throw new Error(
			"Invalid case type. Must be 'snake_case' to send data to server or 'camelCase' to receive data from server."
		);
	}
}

/**
 * Converts a string from snake_case to camelCase.
 *
 * @param {string} str - The string to convert.
 * @returns {string} The converted string.
 */
function snakeToCamel(str) {
	return str.replace(/([-_]\w)/g, (matches) => matches[1].toUpperCase());
}

/**
 * Converts a string from camelCase to snake_case.
 *
 * @param {string} str - The string to convert.
 * @returns {string} The converted string.
 */
function camelToSnake(str) {
	return str.replace(/[A-Z]/g, (matches) => `_${matches.toLowerCase()}`);
}

/**
 * Converts the keys of a JSON object using a specified converter function.
 *
 * @param {Object} data - The JSON object to convert.
 * @param {Function} converter - The function to use for converting the keys.
 * @returns {Object} The converted JSON object.
 */
function convertKeys(data, converter) {
	if (data === null || data === undefined) {
		return data;
	}
	if (Array.isArray(data)) {
		return data.map((item) => convertKeys(item, converter));
	} else if (typeof data === "object") {
		return Object.keys(data).reduce((newObject, key) => {
			const newKey = converter(key);
			newObject[newKey] = convertKeys(data[key], converter);
			return newObject;
		}, {});
	} else {
		return data;
	}
}
