import React from "react";
import { Flex, IconButton, Link, Tooltip } from "@chakra-ui/react";
import { AddIcon } from "@chakra-ui/icons";
import {
	FaUser,
	FaChartLine,
	FaClipboardList,
	FaCapsules,
} from "react-icons/fa";

// NavButton component to avoid repetition
const NavButton = ({ label, href, icon, isLargeButton = false }) => {
	return (
		<Tooltip label={label} placement="top" style={{ zIndex: 1000 }}>
			<Link href={href} style={{ textDecoration: "none" }}>
				<IconButton
					aria-label={label}
					icon={icon}
					variant={isLargeButton ? "solid" : "ghost"}
					colorScheme={isLargeButton ? "green" : "blue"}
					bgColor={isLargeButton ? "#02ba98" : "#6a95e3"}
					borderRadius="full"
					boxShadow={isLargeButton ? "lg" : "none"}
					size={isLargeButton ? "lg" : "md"}
				/>
			</Link>
		</Tooltip>
	);
};

const BottomNavBar = () => {
	return (
		<Flex
			position="fixed"
			bottom="0"
			left="0"
			right="0"
			bg="#6a95e3"
			p="4"
			boxShadow="md"
			justifyContent="space-between" // Align buttons with equal spacing
			alignItems="center"
			width="100%" // Ensure full width
			zIndex="999" // Set a high z-index to ensure it's above other elements
			maxHeight="80px" // Set minimum height to prevent hiding content
		>
			{/* Using the NavButton component for each navigation button */}
			<NavButton
				label="Home"
				href="/home"
				icon={<FaClipboardList style={{ fontSize: "1.5em" }} />}
			/>
			<NavButton
				label="Insights"
				href="/insights"
				icon={<FaChartLine style={{ fontSize: "1.5em" }} />}
			/>
			<NavButton
				label="Data Log"
				href="/datalog"
				icon={<AddIcon />}
				isLargeButton
			/>
			<NavButton
				label="Medication"
				href="/medication"
				icon={<FaCapsules style={{ fontSize: "1.5em" }} />}
			/>
			<NavButton
				label="Profile"
				href="/profile"
				icon={<FaUser style={{ fontSize: "1.5em" }} />}
			/>
		</Flex>
	);
};

export default BottomNavBar;
