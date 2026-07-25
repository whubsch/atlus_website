# Atlus - parse US addresses for OpenStreetMap

This project is a web application that allows users to input US address strings and converts them into OpenStreetMap tagging format. It consists of a FastAPI backend for handling address parsing and a React frontend for the user interface, hosted at [atlus.dev](https://atlus.dev). There is also phone number and opening hours parsing functionality. Canadian addresses sometimes can be processed, but the backend uses the [usaddress](https://github.com/datamade/usaddress) Python package with some additional logic that is geared mostly toward US addresses and address patterns.

## Features

- **Address Parsing:** Enter a US address, and the application will convert it into OpenStreetMap format.
- **Phone Parsing:** Enter a US or Canadian phone number, and the application will format it for the `phone` tag.
- **Opening Hours Parsing:** Enter a raw opening hours string, and the application will convert it into the OSM `opening_hours` syntax.
- **FastAPI Backend:** The backend handles the address parsing logic and provides an API endpoint for the frontend and power users.
- **React Frontend:** A user-friendly interface for entering addresses and viewing the parsed results.
- **Cloud Infrastructure:** Deployed on AWS Lambda with API Gateway and CloudFront CDN for reliable, scalable performance.
- **GitHub Pages:** Frontend hosted on GitHub Pages for fast, global content delivery.

## Usage

### Website

1. Enter a US address, phone number, or opening hours string in the provided input field.
2. Click the "Submit" button.
3. View the parsed address in OpenStreetMap format, and optionally copy the output to your clipboard.

### API

1. Read [the documentation](https://api.atlus.dev/docs).
2. Submit post requests to the API path: `api.atlus.dev/`.
3. Abusing the API will result in bans.

## Contributing

If you would like to contribute to this project, we welcome pull requests and new issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
