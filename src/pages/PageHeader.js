import { Box, Container, Heading } from "@chakra-ui/react";

const PageHeader = ({ pageTitle }) => {
  return (
    <Box bg="#FCFAF8" py={6} mb={0} position="sticky" top="0" zIndex="sticky">
      <Box
        position="absolute"
        top="-50px"
        left="0"
        right="0"
        bottom="0"
        bg="#6a95e3"
        borderBottomRadius={20}
        zIndex="-1"
      />
      <Container maxW="md" textAlign="center">
        <Heading as="h2" size="xl" color="white">
          {pageTitle}
        </Heading>
      </Container>
    </Box>
  );
};

export default PageHeader;
