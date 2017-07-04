import requests,urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

myAPP_ACCESS_TOKEN = '414289191.86a6757.fd642c31a292425992c1eeb68dfab618'
# instagram users connected in sandbox pktest1111 and acadsquad
#APP_ACCESS_TOKEN ='5629236876.1cc9688.86db895c038043b5960dc2949785299a'
BASE = 'https://api.instagram.com/v1/'


def self_info():
    #gives the information about the instagram id of the owner of the access token
    request_url = (BASE+'users/self/?access_token=%s') % (myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_user_id(insta_username):
    #Gets the id of the instagram of the user you have entered
    request_url = (BASE+'users/search?q=%s&access_token=%s') % (insta_username, myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print user_info['data'][0]['id']
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()




def get_user_info(insta_username):
    #Gets the instagram info of the user you have entered
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE +'users/%s?access_token=%s') % (user_id, myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'



def get_own_post():
    #Gets the recent post of the owner of the aceess token
    request_url = (BASE+ 'users/self/media/recent/?access_token=%s') % (myAPP_ACCESS_TOKEN)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



def get_user_post(insta_username):
    #gets the recent post of the given user
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE + 'users/%s/media/recent/?access_token=%s') % (user_id, myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'





def get_post_id(insta_username):
    #gets the post id of the recent post of the user you have entered
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE + 'users/%s/media/recent/?access_token=%s') % (user_id, myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


def like_a_post(insta_username):
    #Likes the recent post of the user you have entered
    media_id = get_post_id(insta_username)
    print media_id
    request_url = (BASE + 'media/%s/likes') % (media_id)
    payload = {"access_token": myAPP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


def post_comment(insta_username):
    #posts a comment on the recent postof a given user
    media_id = get_post_id(insta_username)
    print media_id
    request_url = (BASE + 'media/%s/comments') % (media_id)
    comment_text = raw_input("Enter the comment you wanna post \n")
    payload = {"access_token": myAPP_ACCESS_TOKEN, "text": comment_text}
    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"



def delete_negative_comment(insta_username):
    #deletes the negative comments on the recent post of a user
    media_id = get_post_id(insta_username)
    print media_id
    request_url = (BASE + 'media/%s/comments/?access_token=%s') % (media_id, myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, myAPP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'



def view_comments(insta_username):

    #gets the list of all the comments on the recent post of the owner
    user_id = get_user_id(insta_username)
    media_id=get_post_id(insta_username)
    print media_id
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE +'media/%s/comments?access_token=%s') % (media_id,myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:

        if len(comment_info['data']):


            for x in range(0,len(comment_info['data'])):
                #comment_text =[]
                comment_text = comment_info['data'][x]['text']
                print comment_info['data'][x]['text']
                #return comment_text
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


def get_media_liked_own(): #function for retrieving the recently liked pic by the owner of the access token
    #user_id = get_user_id()
    #if user_id == None:

    request_url = (BASE + 'users/self/media/liked?access_token=%s') % ( myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    payload = {"access_token": myAPP_ACCESS_TOKEN}
    user_media_liked = requests.get(request_url ,payload).json()

    if user_media_liked['meta']['code'] == 200:
        if len(user_media_liked['data']):
            image_name = user_media_liked['data'][0]['id'] + '.jpeg'
            image_url = user_media_liked['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def location(insta_username):
    user_id = get_user_id(insta_username)
    media_id=get_post_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE +'media/%s?access_token=%s') % (media_id,myAPP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    lat_long = requests.get(request_url).json()

    if lat_long['meta']['code'] == 200:
        if len(lat_long['data']['location']):
            loc= lat_long['data']['location']['id']
            print loc
            return loc

        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()






def start_bot():
    while True:
        print '\n'
        print 'Welcome to InstaBot!'
        print 'Chose from the following menu options:'

        print "1.See your own details\n"
        print "2.Get User id of another user!\n"
        print "3.See details of a user by username\n"
        print "4.Get your own recent post\n"
        print "5.Get the recent post of a user by username\n"
        print "6.Like the recent post of a user\n"
        print "7.Post a comment on the recent post of a user\n"
        print "8. View all the comments on the recent post of a given user\n"
        print "9.Delete the negative comment on a recent post of a user\n"
        print "10. To view the recently liked  media by you\n"
        print "11.Leave InstaBot"

        choice = raw_input("Enter you choice: ")
        if choice == "1":
            self_info()

        elif choice == "2":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!#$%^&*()_+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. Please Enter a valid name of single word without special characters"
            else:
                get_user_id(insta_username)
        elif choice == "3":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!#$%^&*()_+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. Please Enter a valid name of single word without special characters"
            else:
                get_user_info(insta_username)

        elif choice == "4":
            get_own_post()

        elif choice == "5":

            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!#$%^&*()_+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. Please Enter a valid name of single word without special characters"
            else:
                get_user_post(insta_username)

        elif choice == "6":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!#$%^&*()_+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. Please Enter a valid name of single word without special characters"
            else:
                like_a_post(insta_username)

        elif choice == "7":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!#$%^&*()_+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. Please Enter a valid name of single word without special characters"
            else:
                post_comment(insta_username)

        elif choice == "8":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!#$%^&*()_+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. Please Enter a valid name of single word without special characters"
            else:
                view_comments(insta_username)

        elif choice == "9":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!#$%^&*()_+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry. Please Enter a valid name of single word without special characters"
            else:
                delete_negative_comment(insta_username)

        elif choice == "10":

            get_media_liked_own()


        elif choice == "11":
            exit()
        else:
            print "wrong choice"

start_bot()


