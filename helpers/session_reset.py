from azure.identity import ManagedIdentityCredential, AzureAuthorityHosts
from azure.mgmt.desktopvirtualization import DesktopVirtualizationMgmtClient

AZURE_SUBSCRIPTION_ID = ''
AZURE_RESOURCE_GROUP_NAME = ''
MANAGED_IDENTITY_CLIENT_ID = ''
AZURE_DESKTOP_VIRTUALIZATION_MGMT_CLIENT_API_VERSION = '2019-09-24-preview'

api_data = {}


# TODO add error handling
def create_avd_client_session():
    credential = ManagedIdentityCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT, client_id=MANAGED_IDENTITY_CLIENT_ID)
    return DesktopVirtualizationMgmtClient(
        credential=credential,
        subscription_id=AZURE_SUBSCRIPTION_ID,
        base_url="https://management.usgovcloudapi.net",
        credential_scopes=['https://management.usgovcloudapi.net/.default'],
        api_version=AZURE_DESKTOP_VIRTUALIZATION_MGMT_CLIENT_API_VERSION
    )


def list_all_host_pools():
    avd_client = create_avd_client_session()
    api_data['host_pool_data'] = []
    host_pools = avd_client.host_pools.list()

    for host_pool_data in host_pools:
        parse_rg_and_hostpool_name = host_pool_data.id.split('/')
        resource_group = parse_rg_and_hostpool_name[4]
        host_pool_name = parse_rg_and_hostpool_name[8]

        api_data['host_pool_data'].append({
            'resource_group': resource_group,
            'host_pool_name': host_pool_name
        })

    return api_data['host_pool_data']


def list_user_sessions(resource_group, host_pool_name):
    avd_client = create_avd_client_session()
    return avd_client.user_sessions.list_by_host_pool(resource_group, host_pool_name)


def find_user_session_data(user_email):
    upn = user_email.strip().lower()
    user_sessions = []
    if '@' in upn:
        for host_pool_info in list_all_host_pools():
            resource_group = host_pool_info['resource_group']
            host_pool_name = host_pool_info['host_pool_name']
            for user_data in list_user_sessions(resource_group, host_pool_name):
                if upn == user_data.user_principal_name:
                    user_sessions.append({'session_host_name': user_data.name,
                            'upn': user_data.user_principal_name,
                            'entra_id_user_name': user_data.active_directory_user_name,
                            'resource_group': resource_group,
                            'host_pool_name': host_pool_name,
                            'application_type': user_data.application_type
                    })
    else:
        print('Invalid email format')
        return None
    return user_sessions

def end_user_session(user_email):
    avd_client = create_avd_client_session()
    user_sessions = find_user_session_data(user_email)

    for session_data in user_sessions:
        parse_session_host_and_user_session_id = session_data['session_host_name'].split('/')
        parse_session_host_application_type = session_data['application_type']
        session_host_name = parse_session_host_and_user_session_id[1]
        user_session_id = parse_session_host_and_user_session_id[2]
        avd_client.user_sessions.delete(
                session_data['resource_group'],
                session_data['host_pool_name'],
                session_host_name,
                user_session_id,
                force = False
            )
    if not user_sessions:
        print(f'No sessions found for: {user_email}')
    else :
        print(f'{len(user_sessions)} sessions ended for user: {user_email}')


if __name__ == '__main__':
    exit(0)
