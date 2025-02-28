from src.app.providers import APIAccessProviderProtocol
from src.app.providers.impls.api_access import APIAccessProviderImpl
from src.settings import settings


def get_api_access_provider() -> APIAccessProviderProtocol:
    return APIAccessProviderImpl(settings.api_key)


APIAccessProvider: APIAccessProviderProtocol = get_api_access_provider()
