// App.js
import React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import DataLog from "./pages/DataLog";
import Profile from "./pages/Profile";
import DailySurvey from "./pages/DailySurvey";
import Insights from "./pages/Insights";
import Medication from "./pages/Medication";
import AuthProvider from "./contexts/AuthContext";
import UserProvider from "./contexts/UserContext";
import Home from "./pages/LogDisplay"; 
import { useEffect } from "react";

const App = () => (
	<ChakraProvider>
		<Router>
			<AuthProvider>
				<Routes>
					// Routes
					<Route exact path="/" element={<Login />} />
					<Route exact path="/login" element={<Login />} />
					<Route exact path="/register" element={<Register />} />
					<Route exact path="/home" element={<Home />} />
					<Route exact path="/medication" element={<Medication />} />
					<Route exact path="/dataLog" element={<DataLog />} />
					<Route
						exact
						path="/profile"
						element={
							<UserProvider>
								<Profile />
							</UserProvider>
						}
					/>
					<Route exact path="/dailysurvey" element={<DailySurvey />} />
					<Route exact path="/insights" element={<Insights />} />
					<Route exact path="*" element={<Login />} />
				</Routes>
			</AuthProvider>
		</Router>
	</ChakraProvider>
);

export default App;
