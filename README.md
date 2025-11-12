# Flask OIDC Config Validator

A CLI and web-based tool to validate `.env` or configuration settings for Flask applications using MSAL and OIDC for authentication. It is especially tailored to help developers working in government cloud environments (like Azure GCC-High) avoid common misconfigurations and security pitfalls.

## ✨ Features

### Core Validation
- **Load and Validate Environment Variables**: Checks for `CLIENT_ID`, `CLIENT_SECRET`, `TENANT_ID`, `AUTHORITY`, `REDIRECT_URI`, and `SCOPE`
- **Simulate OIDC Flow**: Initializes an `msal.ConfidentialClientApplication` to catch configuration errors early without making live network calls
- **Environment-Specific Warnings**: Enhanced detection for GCC-High, DoD, and commercial cloud misconfigurations
- **Security Best Practices**: Recommends using secure secret storage (like Azure Key Vault) and warns about insecure settings

### 🚀 Performance & Scalability
- **Async Validation**: Support for async validation with `validate_config_async()` for better performance
- **Batch Processing**: Validate multiple configurations concurrently with `validate_multiple_configs()`
- **Rate Limiting**: Built-in rate limiting to prevent abuse (200/day, 50/hour, 10/minute for validation)

### 🔐 Security Features
- **CSRF Protection**: Web forms protected against Cross-Site Request Forgery attacks
- **Input Sanitization**: Configuration input limited to 10,000 characters to prevent DoS attacks
- **Structured Logging**: Comprehensive audit trails with JSON-formatted logs for security monitoring
- **Case-Sensitive Variables**: Preserves case sensitivity for environment variables

### 🌐 Government Cloud Support
- **Enhanced GCC-High Detection**: Improved tenant type detection for `.onmicrosoft.us`, `.mail.mil`, and `.gov` domains
- **DoD Environment Support**: Specific validation rules for Department of Defense environments
- **Authority Validation**: Robust checking for mixed commercial/government endpoint configurations

### 📊 Output & Integration
- **Flexible Output**: JSON output for CI/CD integration and strict mode that fails on warnings
- **Web UI**: Easy-to-use web interface with CSRF protection and mobile-responsive design
- **Structured Logs**: JSON-formatted audit logs with correlation ID tracking and user IP logging
- **CLI & Web Modes**: Both command-line and web interfaces available

### 🎨 User Experience & Accessibility
- **Mobile-First Design**: Responsive layout that works seamlessly on phones, tablets, and desktops
- **Accessibility Compliant**: ARIA labels, semantic HTML5, and keyboard navigation support
- **Enhanced Error Handling**: Specific error types with clear, actionable messages
- **Real-time Feedback**: Improved validation results with better visual indicators

### 🔧 Production Readiness
- **Health Monitoring**: Enhanced health check endpoint with dependency verification
- **Request Tracking**: Correlation IDs for end-to-end request tracing
- **Environment Validation**: Startup validation for required configuration
- **Comprehensive Testing**: 85% test coverage with automated CI/CD pipeline

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lance0/oidcheck
    cd oidcheck
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

## 🚀 Usage

### CLI

The tool can be run from the command line to validate a configuration file.

```bash
oidcheck --file .env.example
```

**Options:**

- `--file, -f`: Path to the configuration file (defaults to `.env`)
- `--json`: Output validation results in JSON format
- `--strict`: Exit with a non-zero status code if any warnings or errors are found

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

#### Government Cloud Example:

```env
# GCC-High Configuration
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
TENANT_ID=yourtenant.onmicrosoft.us
AUTHORITY=https://login.microsoftonline.us/yourtenant.onmicrosoft.us
REDIRECT_URI=https://yourapp.mil/getAToken
SCOPE=openid profile
LOG_LEVEL=INFO
```

### Web UI

To use the web-based validator with security features, start the Flask server:

```bash
flask --app oidcheck.server run
```

Then, open your browser to `http://127.0.0.1:5000` to access the UI. The web interface includes:
- CSRF protection for secure form submissions
- Rate limiting to prevent abuse
- Structured audit logging
- Real-time validation feedback

### Async Usage (Advanced)

For applications that need to validate multiple configurations:

```python
import asyncio
from oidcheck.validator import validate_multiple_configs
from oidcheck.models import AppConfig

async def validate_multiple():
    configs = [
        AppConfig(**config_dict_1),
        AppConfig(**config_dict_2),
        # ... more configs
    ]
    results = await validate_multiple_configs(configs)
    return results

# Run async validation
results = asyncio.run(validate_multiple())
```

## 🔍 Validation Rules

### Security Checks
- ✅ HTTPS enforcement for redirect URIs
- ✅ Secure log level recommendations
- ✅ Secret storage best practices
- ✅ Input size validation (DoS prevention)

### OIDC Compliance
- ✅ Required scopes (`openid`, `profile`)
- ✅ Authority URL format validation
- ✅ MSAL client initialization testing
- ✅ Redirect URI format validation

### Government Cloud Specific
- ✅ GCC-High tenant detection (`.onmicrosoft.us`)
- ✅ DoD environment detection (`.mail.mil`, `dod`)
- ✅ Authority/tenant consistency validation
- ✅ Mixed endpoint detection and warnings

### Enhanced Features
- ✅ Case-sensitive environment variable handling
- ✅ Structured JSON logging for audit trails
- ✅ Request ID tracking for debugging
- ✅ User IP logging for security monitoring

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
pytest tests/ -v --cov=oidcheck
```

The project maintains 85% test coverage with comprehensive test coverage for all modules including:
- Unit tests for validation logic
- Integration tests for web endpoints
- CLI functionality tests
- Accessibility and responsive design tests

## 🔧 Development

### Code Quality

The project uses several tools to maintain code quality:

```bash
# Format code
black oidcheck tests

# Run linting
flake8 oidcheck tests

# Type checking
mypy oidcheck

# Run all quality checks
pre-commit run --all-files
```

### Environment Setup

For development, install with optional dependencies:

```bash
pip install -e ".[dev]"
```

This includes pytest, black, flake8, mypy, and other development tools.

## 📋 Dependencies

### Core Dependencies
- Flask: Web framework for the UI
- python-dotenv: Environment variable loading
- msal: Microsoft Authentication Library
- pydantic: Data validation and settings management

### Security & Performance
- flask-limiter: Rate limiting protection
- flask-wtf: CSRF protection and form handling

### Development
- pytest: Testing framework
- pytest-mock: Mocking for tests

## 🔧 Configuration

### Environment Variables

The tool recognizes these configuration variables:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `CLIENT_ID` | ✅ | Azure AD application client ID | `12345678-1234-5678-9012-123456789012` |
| `CLIENT_SECRET` | ✅ | Azure AD application client secret | `your-secret-value` |
| `TENANT_ID` | ✅ | Azure AD tenant ID or domain | `yourtenant.onmicrosoft.us` |
| `AUTHORITY` | ✅ | OIDC authority URL | `https://login.microsoftonline.us/tenant-id` |
| `REDIRECT_URI` | ✅ | OAuth2 redirect URI | `https://yourapp.com/auth/callback` |
| `SCOPE` | ✅ | OIDC scopes (space-separated) | `openid profile email` |
| `LOG_LEVEL` | ❌ | Application log level | `INFO` (default) |

## 🏗️ Project Structure

```
oidcheck/
├── __init__.py              # Package initialization
├── main.py                  # CLI entry point
├── server.py                # Flask web server
├── models.py                # Pydantic data models
├── validator.py             # Core validation logic with async support
├── logging_config.py        # Structured logging configuration
├── static/                  # Web UI assets
│   └── styles.css
└── templates/               # HTML templates
    └── index.html           # Main web UI with CSRF protection
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the Apache 2.0 License. See LICENSE file for details.

## 🔗 Links

- **Homepage**: https://github.com/lance0/oidcheck
- **Bug Tracker**: https://github.com/lance0/oidcheck/issues

## 📈 Recent Updates

### Version 1.1.0 (2025-11-12)
- ✅ **Mobile Responsive Design**: Added CSS breakpoints for tablets and phones
- ✅ **Accessibility Improvements**: ARIA labels, semantic HTML5, keyboard navigation
- ✅ **Enhanced Documentation**: Comprehensive docstrings and type annotations
- ✅ **Improved Error Handling**: Specific exception types with better context
- ✅ **Production Monitoring**: Health checks, correlation IDs, and environment validation
- ✅ **Test Coverage**: Increased to 85% with comprehensive test suite
- ✅ **Code Quality**: Black formatting, linting, and type checking

### Version 1.0.0
- ✅ Restructured project to remove `src/` directory
- ✅ Enhanced GCC-High and DoD environment detection
- ✅ Added async validation support for better performance
- ✅ Implemented structured JSON logging for audit trails
- ✅ Added CSRF protection to web forms
- ✅ Improved input validation and DoS prevention
- ✅ Fixed case sensitivity issues with environment variables
- ✅ Enhanced rate limiting and security features
