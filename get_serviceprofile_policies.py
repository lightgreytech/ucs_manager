from ucsmsdk.ucshandle import UcsHandle
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def select_policy(handle, sp):
    policies = {}
    for attr in sp.__dict__:
        if not attr.startswith('_'):
            value = getattr(sp, attr)
            if "policy" in attr.lower():  # assuming policy-related attributes contain 'policy'
                policies[attr] = value

    while True:
        if policies:
            print(Fore.GREEN + "Available Policies:")
            for i, policy in enumerate(policies, start=1):
                print(f"{Fore.YELLOW}{i}. {Fore.CYAN}{policy}")
            
            policy_index = input(Fore.GREEN + "Enter the index of the policy to view details, 'back' to go back, or 'exit' to exit: ")
            if policy_index.lower() == 'back':
                break
            elif policy_index.lower() == 'exit':
                return True  # Return a signal to exit

            try:
                policy_index = int(policy_index)
                if 1 <= policy_index <= len(policies):
                    selected_policy_key = list(policies.keys())[policy_index - 1]
                    selected_policy_value = policies[selected_policy_key]
                    policy_details = handle.query_dn(selected_policy_value) if selected_policy_value else None
                    if policy_details:
                        for detail in policy_details.__dict__:
                            if not detail.startswith('_'):
                                print(f"{Fore.MAGENTA}{detail}: {Fore.WHITE}{getattr(policy_details, detail)}")
                        if input(Fore.YELLOW + "Enter 'back' to return to policy list or 'exit' to exit: ").lower() == 'exit':
                            return True
                    else:
                        print(Fore.RED + f"No additional details found for {selected_policy_key}")
                else:
                    print(Fore.RED + "Invalid policy index.")
            except ValueError:
                print(Fore.RED + "Invalid input.")
        else:
            print(Fore.RED + "No policies available for this service profile.")
            break

    return False  # No exit signal

def select_service_profile(handle, sp_instances):
    while True:
        print(Fore.GREEN + "Service Profiles:")
        for i, sp in enumerate(sp_instances, start=1):
            print(f"{Fore.YELLOW}{i}. {Fore.CYAN}{sp.name}")

        selected_index = input(Fore.GREEN + "Enter the index of the Service Profile to view details, 'exit' to quit: ")
        if selected_index.lower() == 'exit':
            break
        
        try:
            selected_index = int(selected_index)
            if 1 <= selected_index <= len(sp_instances):
                selected_sp = sp_instances[selected_index - 1]
                print(f"{Fore.GREEN}Details for {Fore.CYAN}{selected_sp.name}:")
                for attr in selected_sp.__dict__:
                    if not attr.startswith('_'):
                        print(f"{Fore.MAGENTA}{attr}: {Fore.WHITE}{getattr(selected_sp, attr)}")
                if select_policy(handle, selected_sp):
                    break  # Break if exit signal received from policy selection
            else:
                print(Fore.RED + "Invalid index.")
        except ValueError:
            print(Fore.RED + "Invalid input.")

def get_service_profiles(ucs_domain, ucs_username, ucs_password):
    handle = UcsHandle(ucs_domain, ucs_username, ucs_password)

    try:
        handle.login()
        sps = handle.query_classid("LsServer")
        sp_instances = [sp for sp in sps if getattr(sp, 'type', None) == "instance"]

        if not sp_instances:
            print(Fore.RED + "No service profiles found.")
            return
        
        select_service_profile(handle, sp_instances)

    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")
    finally:
        handle.logout()

if __name__ == "__main__":
    while True:
        ucs_domain = input(Fore.GREEN + "Enter UCS Manager Domain/IP: ")
        ucs_username = input(Fore.GREEN + "Enter UCS Username: ")
        ucs_password = input(Fore.GREEN + "Enter UCS Password: ")
        get_service_profiles(ucs_domain, ucs_username, ucs_password)
        if input(Fore.YELLOW + "Enter 'continue' to start a new session or any other key to exit: ").lower() != 'continue':
            break