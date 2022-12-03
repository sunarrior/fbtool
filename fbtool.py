from optparse import OptionParser
import os
import dotenv
import requests
import json

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

def video_upload_limits(option, opt_str, value, parser):
    PARAMS = {'fields':'video_upload_limits', 'access_token':token}
    data = requests.get(url = URL + '/me', params = PARAMS).json()

    dotenv.set_key(dotenv_file, "VIDEO_UPLOAD_LIMITED_LENGTH", str(data['video_upload_limits']['length']))
    dotenv.set_key(dotenv_file, "VIDEO_UPLOAD_LIMITED_SIZE", str(data['video_upload_limits']['size']))
    print(f"Video upload limits: {str(data['video_upload_limits']['length'])} & {str(data['video_upload_limits']['size'])}")

def get_albums(option, opt_str, value, parser):
    PARAMS = {'fields':'albums', 'access_token':token}
    data = requests.get(url = URL + '/me', params = PARAMS).json()

    arr = []
    for album in data['albums']['data']:
        del album['id']
        arr.append(album)
    albums = {
        'quantity':len(data['albums']['data']),
        'info': arr
    }
    with open("./data/album.json", "w+") as outfile:
        json.dump(albums, outfile, indent=4)
    print(f"Albums: {albums}")

def get_post_ids(option, opt_str, value, parser):
    PARAMS = {'fields':'feed', 'access_token':token}
    data = requests.get(url = URL + '/me', params = PARAMS).json()

    arr = []
    for feed in data['feed']['data']:
        del feed['created_time']
        arr.append(feed)
    post_ids = {
        'quantity':len(data['feed']['data']),
        'info': arr
    }
    with open("./data/post_ids.json", "w+") as outfile:
        json.dump(post_ids, outfile, indent=4)
    print(f"Post ids: {post_ids}")

def get_total_friends(option, opt_str, value, parser):
    PARAMS = {'fields':'friends', 'access_token':token}
    data = requests.get(url = URL + '/me', params = PARAMS).json()

    dotenv.set_key(dotenv_file, "TOTAL_FRIENDS", str(data['friends']['summary']['total_count']))
    print(f"Get total friends: {str(data['friends']['summary']['total_count'])}")

def get_pages_like(option, opt_str, value, parser):
    PARAMS = {'fields':'likes', 'access_token':token}
    data = requests.get(url = URL + '/me', params = PARAMS).json()

    arr = []
    for like in data['likes']['data']:
        arr.append(like['name'])
    pages_liked = {
        'quantity':len(data['likes']['data']),
        'info': arr
    }
    with open("./data/pages_liked.json", "w+") as outfile:
        json.dump(pages_liked, outfile, indent=4)
    print(f"Pages liked: {pages_liked}")

def get_music_like(option, opt_str, value, parser):
    PARAMS = {'fields':'music', 'access_token':token}
    data = requests.get(url = URL + '/me', params = PARAMS).json()

    arr = []
    for music in data['music']['data']:
        arr.append(music['name'])
    musics_liked = {
        'quantity':len(data['music']['data']),
        'info': arr
    }
    with open("./data/musics_liked.json", "w+") as outfile:
        json.dump(musics_liked, outfile, indent=4)
    print(f"Musics liked: {musics_liked}")

# ============= Command Line Function =============
def main():
    parser = OptionParser()
    parser.add_option("--getsuid", action="callback", callback=get_and_save_uid,
                        help="get and save user id")
    parser.add_option("--showuid", action="callback", callback=print_uid,
                        help="show user id")

    # ================== Kashuken ==================                    
    parser.add_option("--viupli", action="callback", callback=video_upload_limits,
                        help="video upload limits")
    parser.add_option("--albums", action="callback", callback=get_albums,
                        help="get albums")                    
    parser.add_option("--feed", action="callback", callback=get_post_ids,
                        help="get post ids")
    parser.add_option("--friends", action="callback", callback=get_total_friends,
                        help="get total friends")
    parser.add_option("--pages", action="callback", callback=get_pages_like,
                        help="get pages liked")
    parser.add_option("--music", action="callback", callback=get_music_like,
                        help="get music liked")


    (options, args) = parser.parse_args()

# =================================================
if __name__ == "__main__":
    main()