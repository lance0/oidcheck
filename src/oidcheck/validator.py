# oidcheck/validator.py
from .models import AppConfig
import msal

def validate_config(config: AppConfig):
    """
    Validates the OIDC configuration using a Pydantic model.
    """
    results = []

    # 1. Pydantic already handles missing fields if they are not Optional
    # and type validation (e.g., for HttpUrl).

    # 2. Authority validation
    if config.authority:
        if "login.microsoftonline.us" in config.authority and ".com" in config.authority:
            results.append({"level": "ERROR", "message": "Authority seems to mix GCC-High and commercial endpoints."})
        elif "login.microsoftonline.us" not in config.authority and config.tenant_id and "us" in config.tenant_id.lower():
             results.append({"level": "WARNING", "message": "Tenant appears to be a US Gov tenant, but authority is not a .us endpoint."})
        if config.tenant_id and config.tenant_id not in config.authority:
            results.append({"level": "WARNING", "message": "TENANT_ID is not present in AUTHORITY string."})

    # 3. Redirect URI validation (Pydantic validates the URL format)
    if config.redirect_uri and config.redirect_uri.scheme != "https":
        results.append({"level": "WARNING", "message": "REDIRECT_URI is not using HTTPS. This is not secure."})

    # 4. Scope validation
    if "openid" not in config.scope:
        results.append({"level": "WARNING", "message": "SCOPE is missing 'openid'. This is required for OIDC."})
    if "profile" not in config.scope:
        results.append({"level": "WARNING", "message": "SCOPE is missing 'profile'. This is often needed to get user information."})

    # 5. Log Level
    if config.log_level.upper() in ["DEBUG", "TRACE"]:
        results.append({"level": "WARNING", "message": f"LOG_LEVEL is set to '{config.log_level}'. This may log sensitive information."})

    # 6. Secret Storage
    results.append({"level": "INFO", "message": "For production, use a secure secret storage like Azure Key Vault instead of .env files."})

    # 7. MSAL ConfidentialClientApplication simulation
    if config.client_id and config.authority:
        try:
            app = msal.ConfidentialClientApplication(
                client_id=config.client_id,
                authority=config.authority,
                client_credential=config.client_secret,
            )
            # This doesn't make a network call, just validates the authority format
            flow = app.initiate_auth_code_flow(scopes=config.scope, redirect_uri=str(config.redirect_uri) if config.redirect_uri else None)
            results.append({"level": "INFO", "message": "Successfully initialized MSAL ConfidentialClientApplication."})
            results.append({"level": "INFO", "message": f"Generated Auth URL: {flow['auth_uri']}"})

        except Exception as e:
            results.append({"level": "ERROR", "message": f"Failed to initialize MSAL client: {e}"})

    return results