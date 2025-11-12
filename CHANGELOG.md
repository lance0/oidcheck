# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/SemVer).

## [1.1.0] - 2025-11-12

### Added
- **Mobile Responsive Design**
  - Added CSS breakpoints for mobile devices (768px and 480px)
  - Improved typography with system fonts and better spacing
  - Enhanced button styling with focus indicators and transitions
  - Mobile-first responsive layout with proper touch targets

- **Accessibility Improvements**
  - Added semantic HTML5 elements (main, header, section)
  - Implemented ARIA labels and roles for screen readers
  - Added proper form labels and help text
  - Enhanced keyboard navigation with focus indicators
  - Added live regions for dynamic content updates

- **Code Quality & Documentation**
  - Added comprehensive docstrings to all public functions
  - Improved error handling with specific exception types
  - Enhanced type annotations throughout codebase
  - Added correlation ID tracking for request tracing

- **Testing & Coverage**
  - Added coverage threshold enforcement (80% minimum)
  - Expanded test suite with 29 tests covering all modules
  - Added tests for health endpoint, correlation IDs, and main CLI
  - Improved test fixtures and mocking strategies

- **Production Readiness**
  - Enhanced health check endpoint with dependency verification
  - Added startup environment variable validation
  - Implemented correlation ID tracking across requests
  - Improved structured logging with request context

### Changed
- **Error Handling**
  - Replaced generic Exception with specific types (ValueError, RuntimeError, KeyError)
  - Enhanced error messages with better context
  - Improved error logging with correlation IDs

- **CSS Styling**
  - Modernized visual design with subtle shadows and better contrast
  - Added flash message styling for different alert types
  - Improved form styling with better spacing and typography
  - Enhanced responsive behavior for mobile devices

- **Dependencies**
  - Added pytest-cov for coverage reporting
  - Updated dev dependencies in pyproject.toml
  - Improved dependency organization and optional dependencies

### Fixed
- **Code Formatting**
  - Applied Black code formatting across all files
  - Fixed line length issues and import organization
  - Resolved flake8 warnings and unused imports

- **Test Coverage**
  - Increased overall test coverage from 64% to 85%
  - Added missing tests for utility functions and CLI
  - Fixed test mocking and assertion patterns

### Security
- Enhanced request tracking with correlation IDs
- Improved input validation and error handling
- Added dependency health checks for monitoring

### Performance
- Optimized CSS for faster mobile rendering
- Improved test execution speed with better mocking
- Enhanced logging efficiency with structured output

## [1.0.0] - 2025-01-27

### Added
- **Security Enhancements**
  - Removed hardcoded Flask secret key, now configurable via `FLASK_SECRET_KEY` environment variable
  - Added secure random key generation as fallback
  - Enhanced CSRF protection for web forms
  - Added input sanitization and size limits (10,000 characters max)

- **Development Workflow**
  - Pre-commit hooks configuration (`.pre-commit-config.yaml`) with black, flake8, mypy, and isort
  - GitHub Actions CI/CD pipeline with multi-Python version testing (3.8-3.11)
  - Code coverage reporting with Codecov integration
  - Security vulnerability scanning in CI pipeline

- **Containerization & Deployment**
  - Dockerfile for containerized deployment
  - Health check endpoint (`/health`) for monitoring
  - Production-ready environment variable configuration
  - Non-root user setup in Docker container

- **Code Quality**
  - Comprehensive type hints throughout the codebase
  - Async validation support in CLI for better performance
  - Improved error handling and exception management
  - Enhanced logging with structured JSON output

- **Testing**
  - Expanded test coverage with web route tests
  - Server endpoint testing including rate limiting and input validation
  - Proper test fixtures with CSRF disabled for testing
  - All tests passing (12/12)

- **Web UI Improvements**
  - Flash message display for user feedback
  - Better error presentation in web interface
  - Enhanced CSS styling for error messages
  - Improved user experience with proper validation feedback

- **Configuration Management**
  - Consolidated dependencies in `pyproject.toml` with optional dev dependencies
  - Fixed version consistency across all files
  - Enhanced Pydantic model configuration
  - Better scope field handling with Optional[List[str]]

- **Utility Functions**
  - Added utility functions in `utils.py` for output formatting
  - Support for multiple output formats (text, JSON, HTML)
  - Configuration file loading utilities

### Changed
- **Dependencies**
  - Moved dev dependencies to `pyproject.toml` optional-dependencies
  - Updated to use modern Pydantic configuration
  - Added missing dev dependencies (pytest-mock, black, flake8, mypy)

- **Models**
  - Made `scope` field Optional[List[str]] with proper validation
  - Enhanced model validator for scope string splitting
  - Improved case-insensitive field handling

- **CLI**
  - Implemented async validation for better performance
  - Enhanced error handling and type safety
  - Better configuration loading with None value filtering

### Fixed
- **Security Issues**
  - Resolved hardcoded secret key vulnerability
  - Fixed potential information disclosure through debug logging

- **Type Safety**
  - Added proper type annotations throughout codebase
  - Fixed Pydantic model configuration issues
  - Resolved type checker warnings and errors

- **Web Interface**
  - Fixed flash message display in templates
  - Added proper error handling for validation failures
  - Enhanced rate limiting and input validation

- **Testing**
  - Fixed CSRF token issues in web tests
  - Added proper test fixtures and mocking
  - Resolved test failures and improved coverage

### Security
- Removed hardcoded secrets
- Added secure random key generation
- Enhanced input validation and sanitization
- Implemented proper CSRF protection
- Added security scanning in CI pipeline

### Performance
- Async validation support
- Better error handling to prevent unnecessary processing
- Optimized imports and dependencies

### Documentation
- Updated README with new features and usage instructions
- Added comprehensive changelog
- Enhanced code documentation with type hints

### Deprecated
- None

### Removed
- Hardcoded Flask secret key
- Redundant dependency declarations

### Known Issues
- Rate limiting uses in-memory storage (recommended to configure Redis for production)
- Some Pydantic deprecation warnings may appear (compatible with current functionality)