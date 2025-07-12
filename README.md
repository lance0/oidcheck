# Flask OIDC Config Validator

A CLI and web-based tool to validate `.env` or configuration settings for Flask applications using MSAL and OIDC for authentication. It is especially tailored to help developers working in government cloud environments (like Azure GCC-High) avoid common misconfigurations and security pitfalls.

## Features

- **Load and Validate Environment Variables**: Checks for `CLIENT_ID`, `CLIENT_SECRET`, `TENANT_ID`, `AUTHORITY`, `REDIRECT_URI`, and `SCOPE`.
- **Simulate OIDC Flow**: Initializes an `msal.ConfidentialClientApplication` to catch configuration errors early without making live network calls.
- **Environment-Specific Warnings**: Detects misconfigurations, such as using a commercial `.com` authority in a GCC-High deployment.
- **Security Best Practices**: Recommends using secure secret storage (like Azure Key Vault) and warns about insecure settings like non-HTTPS redirect URIs or overly permissive log levels.
- **Flexible Output**: Offers JSON output for CI/CD integration and a strict mode that fails on warnings.
- **Web UI**: Provides an easy-to-use web interface to paste and validate configurations.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd flask-oidc-config-validator
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the package in editable mode:**
    ```bash
    pip install -e .
    ```

## Usage

### CLI

The tool can be run from the command line to validate a configuration file.

```bash
oidcheck --file .env.example
```

**Options:**

- `--file, -f`: Path to the configuration file (defaults to `.env`).
- `--json`: Output validation results in JSON format.
- `--strict`: Exit with a non-zero status code if any warnings or errors are found.

#### Example `.env` file:

```env
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
TENANT_ID=your-tenant-id
AUTHORITY=https://login.microsoftonline.com/your-tenant-id
REDIRECT_URI=https://localhost:5000/getAToken
SCOPE=openid profile email
LOG_LEVEL=INFO
```

### Web UI

To use the web-based validator, start the Flask server:

```bash
flask --app oidcheck.server run
```

Then, open your browser to `http://127.0.0.1:5000` to access the UI. Paste your configuration into the text area and click "Validate".
