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
def check_authenticate_info():
    user_id = os.environ.get('USER_ID')
    if token == 'access_token':
        print("user access_token haven't been set!")
        return;
    # if user_id == 'user_id':
    #     print("user id haven't been'set!")
    #     return;

def get_and_save_uid(option, opt_str, value, parser):
    PARAMS = {'fields':'id', 'access_token':token}
    user_id = requests.get(url = URL + '/me', params = PARAMS).json()
    dotenv.set_key(dotenv_file, 'USER_ID', user_id['id'])
    print(f"Get and save user id: {user_id['id']}")

def get_post_on_feed():
    PARAMS = {'fields':'feed', 'access_token':token}
    post_id = requests.get(url = URL + '/me', params = PARAMS).json()
    if len(post_id['feed']['data']) == 0:
        print("Feed don't have any post!")
        return;
    lst_post_id = post_id['feed']['data']
    return lst_post_id

def show_post_list(option, opt_str, value, parser):
    lst_post_id = get_post_on_feed()
    with open('list_post.json', 'w') as file:
        file.write(json.dumps(lst_post_id))
        file.close()
    print(lst_post_id)
    
def get_reaction_count(post_id, type):
    name_of_summary_mapping = {
        'LIKE': 'reaction_like',
        'LOVE': 'reaction_love',
        'CARE': 'reaction_care',
        'HAHA': 'reaction_haha',
        'WOW': 'reaction_wow',
        'SAD': 'reaction_sad',
        'ANGRY': 'reaction_angry'
    }

    reaction_count_json = {}
    reaction_count_json['post_id'] = post_id
    reaction_count_json['reaction_count'] = {}

    for i in range(len(type)):
        name_of_summary = name_of_summary_mapping[type[i]]
        PARAMS = {
            'ids':post_id, 
            'fields':f"reactions.type({type[i]}).limit(0).summary(total_count).as({name_of_summary})", 
            'access_token':token}
        reaction_count_results = requests.get(url = URL, params = PARAMS).json()
        if 'error' in reaction_count_results:
            print(reaction_count_results['error']['message'])
            return
        reaction_count = reaction_count_results[post_id][name_of_summary]['summary']['total_count']
        if reaction_count == None:
            print(f"no {type[i]} reaction")
            reaction_count = 0
        reaction_count_json['reaction_count'][name_of_summary] = reaction_count
    
    with open('reaction_count.json', 'w') as file:
        file.write(json.dumps(reaction_count_json))
        file.close()

    return reaction_count_json

def summary_reactions_on_one_post(option, opt_str, value, parser):
    check_authenticate_info()
    if parser.values.p == None:
        print("missing -p argument")
        return
    if parser.values.p == None:
        print("missing -t argument")
        return
    list_reactions = [t.upper() for t in parser.values.t.split(',')]
    reaction_count = get_reaction_count(
        parser.values.p, 
        list_reactions, 
    )
    if reaction_count != None:
        print(reaction_count)

# ============= Command Line Function =============
def main():
    parser = OptionParser()
    parser.add_option("--get_uid", action="callback", callback=get_and_save_uid,
                        help="get and save user id")
    parser.add_option("--get_post_on_feed", action="callback", callback=show_post_list,
                        help="show post id on feed")
    parser.add_option("--get_one_post_react", action="callback", callback=summary_reactions_on_one_post,
                        help="-p [post_id] -t [type_reaction] --get_one_post_react, \n \
                                show reaction count in one post")
    parser.add_option("-p", help="set post id")
    parser.add_option("-t", help="set type of reaction [Like, Love, Thankful, Haha, Wow, Sad, Angry] \
                                    can be multiple type (ex: haha,love)"
                                    )

    
    (options, args) = parser.parse_args()


# =================================================
if __name__ == "__main__":
    main()