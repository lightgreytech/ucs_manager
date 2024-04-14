from ucsmsdk.ucshandle import UcsHandle

def get_service_profile_list(ucs_domain, ucs_username, ucs_password):
    # Initialize handle with UCS Manager credentials
    handle = UcsHandle(ucs_domain, ucs_username, ucs_password)

    try:
        # Login to UCS Manager
        handle.login()

        # Query for all service profiles
        service_profile = handle.query_classid("LsServer")
        sp_names = [sp.name for sp in service_profile if sp.type == "instance"]

        if not sp_names:
            print("No service profile found.")
            return []

        return sp_names

    except Exception as e:
        print("An error occurred: {}".format(str(e)))
        return []

    finally:
        # Logout from UCS Manager
        handle.logout()

if __name__ == "__main__":
    # Prompt user for UCS Manager domain, username, and password
    ucs_domain = input("Enter UCS Manager Domain/IP: ")
    ucs_username = input("Enter UCS Username: ")
    ucs_password = input("Enter UCS Password: ")

    # Get list of Service Profile Templates
    sp_names = get_service_profile_list(ucs_domain, ucs_username, ucs_password)

    # Print the list of Service Profile Templates
    print("Service Profiles:")
    for sp_name in sp_names:
        print(sp_name)
