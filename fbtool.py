from optparse import OptionParser
import os
import dotenv
import requests

# ============= Export Environment =============
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
URL = os.environ.get('URL')
token = os.environ.get('TOKEN')
token_info = os.environ.get('TOKEN_INFO')
token_favorite = os.environ.get('TOKEN_FAVORITE')

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

def get_info_user(option, opt_str, value, parser):
    PARAMS_NAME = {'fields':'name', 'access_token':token_info}
    PARAMS_BIRTHDAY = {'fields':'birthday', 'access_token':token_info}
    PARAMS_EMAIL = {'fields':'email', 'access_token':token_info}
    PARAMS_LOCATION = {'fields':'location', 'access_token':token_info}
    PARAMS_GENDER = {'fields':'gender', 'access_token':token_info}

    user_name = requests.get(url = URL + '/me', params = PARAMS_NAME).json()
    birthday = requests.get(url = URL + '/me', params = PARAMS_BIRTHDAY).json()
    email = requests.get(url = URL + '/me', params = PARAMS_EMAIL).json()
    location = requests.get(url = URL + '/me', params = PARAMS_LOCATION).json()
    gender = requests.get(url = URL + '/me', params = PARAMS_GENDER).json()

    print(f"Get username: {user_name['name']}")
    print(f"Get gender: {gender['gender']}")
    print(f"Get birthday: {birthday['birthday']}")
    print(f"Get email: {email['email']}")
    print(f"Get location: {location['location']['name']}")

def get_favorite_teams(option, opt_str, value, parser):
    PARAMS_FAVORITE = {'fields':'favorite_teams', 'access_token':token_favorite}
    user_favorite = requests.get(url = URL + '/me', params = PARAMS_FAVORITE).json()
    print(f"Get list favorite user:")
    for i in range(len(user_favorite['favorite_teams'])):
        print(user_favorite['favorite_teams'][i]['name'])

# ============= Command Line Function =============
def main():
    parser = OptionParser()
    parser.add_option("--getsuid", action="callback", callback=get_and_save_uid,
                        help="get and save user id")
    parser.add_option("--showuid", action="callback", callback=print_uid,
                        help="show user id")
    parser.add_option("--getsuinfo", action="callback", callback=get_info_user,
                        help="show user information")
    parser.add_option("--getsufavorite", action="callback", callback=get_favorite_teams,
                        help="show favorite")

    
    (options, args) = parser.parse_args()

# =================================================
if __name__ == "__main__":
    main()