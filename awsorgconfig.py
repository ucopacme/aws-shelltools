

def make_org_config():
    """
    create aws config file with a profile for all accounts in org
    if no args, use [master] profile in ~/.aws/config
    if no args and no [master] profile in ~/.aws/config,
     ask for master account_id, 
     role_name for scanning accounts in master, 
     and default role_name to set in org config file.
    if one arg , use this as 'master' profile
    if 2 arg, first is 'master' profile, second is default role_name to set
    """
    return None
