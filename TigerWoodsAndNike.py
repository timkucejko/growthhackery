import oauth2 as oauth
import urllib2 as urllib
import json
import time

token_key = "GO_TO_https://apps.twitter.com/_to_create_your_own_token_key"
token_secret = "GO_TO_https://apps.twitter.com/_to_create_your_own_token_secret"

consumer_key = "GO_TO_https://apps.twitter.com/_to_create_your_own_consumer_key"
consumer_secret = "GO_TO_https://apps.twitter.com/_to_create_your_own_consumer_secret"

_debug = 0

oauth_token    =  oauth.Token(    key = token_key,     secret=  token_secret)
oauth_consumer =  oauth.Consumer( key = consumer_key,  secret=  consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

def twitterRequest(url, method, parameters):
  request = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)

  request.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = request.to_header()

  if http_method == "POST":
    encoded_post_data = request.to_postdata()
  else:
    encoded_post_data = None
    url = request.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchTwitterData():
  twitterHandles= ["tigerwoods","nike"]
  minutesBetweenRetries = 5

  for handle in twitterHandles:
    cursor = -1
    jsonBlob = ""
    tweetFilename = handle+'Followers.csv'
    f = open(tweetFilename, 'w')
    f.close
    print "starting to collect the followers for " + handle
    while cursor != "0":
      url = "https://api.twitter.com/1.1/followers/ids.json?screen_name=" + handle + "&cursor=" + str(cursor)
      parameters = []
      response = twitterRequest(url, "GET", parameters)
      for line in response:
        jsonBlob = json.loads(line )

      if "errors" in jsonBlob:
        for error in jsonBlob["errors"]:
          if error["code"] == 88:
            print "we're past our rate limit. let's wait " + str(minutesBetweenRetries) + " mins and try again."
            time.sleep(minutesBetweenRetries * 60)
            break

      if "next_cursor_str" in jsonBlob:
        if "ids" in jsonBlob:
          f = open(tweetFilename,'a')
          for userid in jsonBlob["ids"]:
            f.write(str(userid)+"\n")
          f.close()
        print "The next Cursor is: " + str(jsonBlob["next_cursor_str"])
        cursor = str(jsonBlob["next_cursor_str"])
      else:
        print "we're past our rate limit. let's wait " + str(minutesBetweenRetries) + " mins and try again."
        jsonBlob = ""
    print "We've successfully retrieved all of the followers for " + handle
  print "We're done!"

#This is the main code block: 
if __name__ == '__main__':
  fetchTwitterData()
