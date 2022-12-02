from optparse import OptionParser
import os
import dotenv
import web
import pickle
import requests
from bs4 import BeautifulSoup
import re

# ============= Export Environment =============
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
URL = os.environ.get('URL')
token = os.environ.get('TOKEN')

# ============= Tool Function =============
def facebook_login():
    # url_login = 'https://m.facebook.com/login.php'    
    redirect_uri = "http://localhost:8080"
    # data = {
    #     'email': 'Oskey16879@gmail.com',
    #     'pass': '16*8*7*9'
    # }
    # session = requests.session()
    # res = session.post(url_login, data=data, allow_redirects=True)
    # print(res.url)
    # dialog_url = ("https://www.facebook.com/v15.0/dialog/oauth?" +
    #                            "client_id=" + os.environ.get('APP_ID') +
    #                            "&redirect_uri=" + redirect_uri)
    # res1 = session.post(dialog_url, cookies=res.cookies, allow_redirects=True)
    # print(res1.url)
    test_url = "https://m.facebook.com/login.php?refsrc=https%3A%2F%2Fm.facebook.com%2F&amp;refid=9"
    session = None
    get_login = None
    if not os.path.exists("session_save/session.sav"):
        print('session not exists! generating and saving session...')
        session = requests.Session()
        file_save = open("session_save/session.sav", "wb")
        pickle.dump(session, file_save)
        print('session saved!')
    else:
        print('session exists! loading saved session...')
        file_save = open("session_save/session.sav", "rb")
        session = pickle.load(file_save)
        print('load session done!')

    if not os.path.exists("session_save/has_login.sav"):
        print('login session not exists! try logging in...')
        r = session.get('https://m.facebook.com/login.php', allow_redirects=False)
        soup = BeautifulSoup(r.text, features="html.parser")
        tmp = soup.find(attrs={"name": "lsd"})
        lsd = tmp["value"]
        login_cookie = r.cookies
        data = {
            'lsd': lsd,
            'cookies': login_cookie
        }
        data['email'] = ''
        data['pass'] = ''
        data['login'] = 'Log In'
        get_login = session.post(test_url, data=data, allow_redirects=False)
        print(get_login)
        if get_login.status_code == 302:
            print('login successful, saving login session...')
            login_save = open('session_save/has_login.sav', 'wb')
            pickle.dump(get_login, login_save)
            print('login session saved!')
    else:
        print('login session exists! try loading session...')
        login_save = open('session_save/has_login.sav', 'rb')
        get_login = pickle.load(login_save)
        print('load login session done')

    cookies = get_login.cookies
    print(cookies)
    # dialog_url = ("https://m.facebook.com/v15.0/dialog/oauth?" +
    #                            "client_id=" + os.environ.get('APP_ID') +
    #                            "&redirect_uri=" + redirect_uri + 
    #                            "&scope=user_profile")
    # res1 = session.post(dialog_url, cookies=cookies, allow_redirects=True)
    # print(res1.url)
    # r_logout = session.get('https://m.facebook.com/logout.php', allow_redirects=False)
    # print(r_logout)
    # logout = session.post(dialog_url, cookies=cookies, allow_redirects=False)
    # with open("response.html", "wb") as f:
    #     f.write(get_login.content)
    

def get_auth_code(redirect_uri):
    dialog_url = ("https://www.facebook.com/v15.0/dialog/oauth?" +
                               "client_id=" + os.environ.get('APP_ID') +
                               "&redirect_uri=" + redirect_uri)
    req = requests.post(dialog_url)
    # print(req.url)
        

def get_access_token(option, opt_str, value, parser):
    URL_OAUTH = URL + '/oauth/access_token'
    redirect_uri = "http://localhost:8080"
    facebook_login()
    # get_auth_code(redirect_uri)
    # print(code)
    # payload = {
    #     'grant_type': 'authorization_code',
    #     'client_id': os.environ.get('APP_ID'),
    #     'client_secret': os.environ.get('APP_SECRET'),
    #     'redirect_uri': redirect_uri,
    #     'code': code
    # }
    # response = requests.post(URL_OAUTH, params=payload).json()
    # print(response)
    # PARAMS = {'fields':'id', 'access_token':response['access_token']}
    # user_id = requests.get(url = URL + '/1128015791415020', params = PARAMS).json()
    # print(user_id)

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
    parser.add_option("--gettoken", action="callback", callback=get_access_token,
                        help="show user id")
    
    (options, args) = parser.parse_args()

# =================================================
if __name__ == "__main__":
    main()