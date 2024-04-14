from ucsmsdk.ucshandle import UcsHandle

def get_service_profile_templates(ucs_domain, ucs_username, ucs_password):
    # Initialize handle with UCS Manager credentials
    handle = UcsHandle(ucs_domain, ucs_username, ucs_password)

    try:
        # Login to UCS Manager
        handle.login()

        # Query for all Service Profile Templates
        sp_templates = handle.query_classid("LsServer")
        # Filter to get only the templates (initial-templates)
        sp_updating_template_names = [sp.name for sp in sp_templates if sp.type == "updating-template"]

        if not sp_updating_template_names:
            print("No service profile templates found.")
            return []

        return sp_updating_template_names
    

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
    sp_template_names = get_service_profile_templates(ucs_domain, ucs_username, ucs_password)

    # Print the list of Service Profile Templates
    print("Service Profile Templates:")
    for template_name in sp_template_names:
        print(template_name)
