from ucsmsdk.ucshandle import UcsHandle

def get_service_profiles(ucs_domain, ucs_username, ucs_password):
    # Initialize handle with UCS Manager credentials
    handle = UcsHandle(ucs_domain, ucs_username, ucs_password)

    try:
        # Login to UCS Manager
        handle.login()

        # Query for all Service Profiles
        sps = handle.query_classid("LsServer")
        # Filter to get only the Service Profiles (excluding templates)
        sp_instances = [sp for sp in sps if getattr(sp, 'type', None) == "instance"]

        if not sp_instances:
            print("No service profiles found.")
            return []

        # Display service profiles with indexes
        print("Service Profiles:")
        for i, sp in enumerate(sp_instances, start=1):
            print(f"{i}. {sp.name}")

        # Prompt for specific service profile index
        selected_index = int(input("Enter the index of the Service Profile to view details: "))
        if 1 <= selected_index <= len(sp_instances):
            selected_sp = sp_instances[selected_index - 1]

            # Display selected service profile details
            print(f"Details for {selected_sp.name}:")
            for attr in selected_sp.__dict__:
                if not attr.startswith('_'):
                    print(f"{attr}: {getattr(selected_sp, attr)}")
        else:
            print("Invalid index.")

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

    # Get list of Service Profiles and display details for selected profile
    get_service_profiles(ucs_domain, ucs_username, ucs_password)
