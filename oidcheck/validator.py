# oidcheck/validator.py
from .models import AppConfig
import msal
import asyncio
from typing import List, Dict, Any

def validate_config(config: AppConfig) -> List[Dict[str, Any]]:
    """
    Validates the OIDC configuration using a Pydantic model.
    """
    results = []

    # 1. Pydantic already handles missing fields if they are not Optional
    # and type validation (e.g., for HttpUrl).

    # 2. Authority validation
    if config.authority:
        authority_lower = config.authority.lower()
        is_commercial = "login.microsoftonline.com" in authority_lower
        is_us_gov = "login.microsoftonline.us" in authority_lower
        is_dod = "login.microsoftonline.us" in authority_lower and "dod" in authority_lower
        is_gcc_high = "login.microsoftonline.us" in authority_lower

        if is_commercial and is_us_gov:
            results.append({"level": "ERROR", "message": "Authority mixes commercial (.com) and US Government (.us) endpoints."})
        elif not is_commercial and not is_us_gov:
            results.append({"level": "WARNING", "message": "Authority does not appear to be a standard Microsoft public cloud endpoint."})
        
        if config.tenant_id:
            tenant_id_lower = config.tenant_id.lower()
            
            # Enhanced GCC-High detection patterns
            tenant_is_gov = (
                ".onmicrosoft.us" in tenant_id_lower or 
                tenant_id_lower.endswith(".us") or
                ".mail.mil" in tenant_id_lower or
                ".gov" in tenant_id_lower
            )
            
            # More specific tenant type detection
            tenant_is_dod = ".mail.mil" in tenant_id_lower or "dod" in tenant_id_lower
            tenant_is_gcc_high = ".onmicrosoft.us" in tenant_id_lower and not tenant_is_dod
            
            if tenant_is_gov and not is_us_gov:
                results.append({"level": "ERROR", "message": "Tenant ID appears to be for a US Government environment, but the authority is not a .us endpoint."})
            elif not tenant_is_gov and is_us_gov:
                results.append({"level": "WARNING", "message": "Authority is a US Government endpoint, but the tenant ID does not appear to be a standard US Government tenant."})
            
            # Additional validation for specific gov cloud types
            if tenant_is_dod and not is_dod:
                results.append({"level": "WARNING", "message": "Tenant appears to be DoD but authority may not be configured for DoD environment."})
            elif tenant_is_gcc_high and not is_gcc_high:
                results.append({"level": "WARNING", "message": "Tenant appears to be GCC-High but authority may not be configured correctly."})

            if config.tenant_id not in config.authority:
                results.append({"level": "WARNING", "message": "TENANT_ID is not present in AUTHORITY string."})

    # 3. Redirect URI validation (Pydantic validates the URL format)
    if config.redirect_uri and config.redirect_uri.scheme != "https":
        results.append({"level": "WARNING", "message": "REDIRECT_URI is not using HTTPS. This is not secure."})

    # 4. Scope validation
    scope_list: List[str] = config.scope if config.scope is not None else []
    if "openid" not in scope_list:
        results.append({"level": "WARNING", "message": "SCOPE is missing 'openid'. This is required for OIDC."})
    if "profile" not in scope_list:
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
            flow = app.initiate_auth_code_flow(scopes=scope_list, redirect_uri=str(config.redirect_uri) if config.redirect_uri else None)
            results.append({"level": "INFO", "message": "Successfully initialized MSAL ConfidentialClientApplication."})
            results.append({"level": "INFO", "message": f"Generated Auth URL: {flow['auth_uri']}"})

        except Exception as e:
            results.append({"level": "ERROR", "message": f"Failed to initialize MSAL client: {e}"})

    return results


async def validate_config_async(config: AppConfig) -> List[Dict[str, Any]]:
    """
    Async version of validate_config for better performance when validating multiple configs.
    """
    return await asyncio.to_thread(validate_config, config)


async def validate_multiple_configs(configs: List[AppConfig]) -> List[List[Dict[str, Any]]]:
    """
    Validates multiple configurations concurrently for better performance.
    """
    tasks = [validate_config_async(config) for config in configs]
    return await asyncio.gather(*tasks)