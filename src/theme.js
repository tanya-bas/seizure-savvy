import { extendTheme } from "@chakra-ui/react"

const theme = extendTheme({
  styles: {
    global: {
      "html, body": {
        backgroundColor: "#f7f7f7",
        fontFamily: "Proxima Nova, sans-serif", 
      }
    }
  },
  components: {
    Container: {
      baseStyle: {
        bg: "#FCFAF8", // Change this to the color you want
      },
      sizes: {
        md: {
          maxW: "28rem",
        },
      },
      variants: {
        centered: {
          maxW: "md",
          textAlign: "center",
        },
      },
    }
  }
})

export default theme;