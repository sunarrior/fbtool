from optparse import OptionParser
import os
import dotenv
import requests

# ============= Export Environment =============
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
URL = os.environ.get('URL')
token = os.environ.get('TOKEN')

# ============= Tool Function =============
def get_and_save_uid(option, opt_str, value, parser):
    PARAMS = {'fields':'id', 'access_token':token}
    user_id = requests.get(url = URL + '/me', params = PARAMS).json()
    # print(user_id)
    dotenv.set_key(dotenv_file, "USER_ID", user_id['id'])
    print(f"Get and save user id: {user_id['id']}")

def print_uid(option, opt_str, value, parser):
    uid = os.environ.get('USER_ID')
    print(f"USER_ID is {uid}")


# ============= Command Line Function =============
def main():
    parser = OptionParser()
    parser.add_option("--getsuid", action="callback", callback=get_and_save_uid,
                        help="get and save user id")
    parser.add_option("--showuid", action="callback", callback=print_uid,
                        help="show user id")

    
    (options, args) = parser.parse_args()

# =================================================
if __name__ == "__main__":
    main()