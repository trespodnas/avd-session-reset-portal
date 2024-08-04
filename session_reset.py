
from azure.identity import DefaultAzureCredential, AzureAuthorityHosts
from azure.mgmt.desktopvirtualization import DesktopVirtualizationMgmtClient

AZURE_SUBSCRIPTION_ID = ''
AZURE_RESOURCE_GROUP_NAME = ''
AZURE_HOST_POOL_NAME = ''
AZURE_DESKTOPVIRTUALIZATION_MGMT_CLIENT_API_VERSION = '2019-09-24-preview'


# TODO add error handling
def create_avd_client_session():
    credential = DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
    return DesktopVirtualizationMgmtClient(
        credential=credential,
        subscription_id=AZURE_SUBSCRIPTION_ID,
        base_url="https://management.usgovcloudapi.net",
        credential_scopes=['https://management.usgovcloudapi.net/.default'],
        api_version= AZURE_DESKTOPVIRTUALIZATION_MGMT_CLIENT_API_VERSION
    )


def get_avd_session_hosts(client, rg_name, host_pool_name):
    return client.session_hosts.list(rg_name, host_pool_name)


def list_host_pool_user_session_data():
    api_data = {}
    avd_client = create_avd_client_session()
    list_user_sessions = avd_client.user_sessions.list_by_host_pool(AZURE_RESOURCE_GROUP_NAME, AZURE_HOST_POOL_NAME)
    api_data['data'] = list_user_sessions
    if api_data['data']:
        for _ in api_data['data']:
            return api_data['data']
    else:
        print(f'nodata, {__name__}')
        return 1

# TODO convert loop to generator
def find_user_avd_session_data(user_upn):
    # TODO add error handling
    user_email = user_upn.strip()
    # TODO better validation ?
    if '@' in user_email:
        for data in list_host_pool_user_session_data():
            output_format = {"session_host_name": data.name, "upn": data.user_principal_name,
                             "entra_id_user_name": data.active_directory_user_name}
            if user_email == data.user_principal_name:
                return output_format
    else:
        ## TODO break or exit 1 here / Logging here
        print('no email found')
        return 1


def end_user_avd_session(user_upn):
    # TODO add error handling
    parse_session_host_and_user_session_id = find_user_avd_session_data(user_upn)[
        'session_host_name'].split('/')
    session_host_name = parse_session_host_and_user_session_id[1]
    user_session_id = parse_session_host_and_user_session_id[2]
    avd_client = create_avd_client_session()
    return avd_client.user_sessions.delete(AZURE_RESOURCE_GROUP_NAME, AZURE_HOST_POOL_NAME, session_host_name,
                                           user_session_id, force=True)


if __name__ == '__main__':
    exit(0)

