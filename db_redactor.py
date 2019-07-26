import json
import hashlib
import pymongo
from bson.json_util import dumps
from pprint import pprint
from cryptography.fernet import Fernet
import base64

# keys to encrypt/decrypt username/password
key = hashlib.md5("DHSBFB3DHXNZAJ").hexdigest()
key_64 = base64.urlsafe_b64encode(key)


# returns encrypted username
def getUsername():
    return "gAAAAABdOtrd8SqjxkTb7Pu3EVFdBxOzrhxqvEViNcGNg_UaJ7csPzIAhOaHyFFBU7KZm5vtVqwQpcMim-caw0YJsITGC2157Q=="


# returns encrypted password
def getPassword():
    return "gAAAAABdOtpvxaaxNgNtUkMbAHuEiQgVmk6tXG-1EkI8HOw1CpksiootGi2xS5YuTCR8FYlF3iL-zc5iE9ORPpZHSoluIBt2Xg=="


# decrypts username/password and returns mongodb instance
def connect():
    cipher_suite = Fernet(key_64)
    username = cipher_suite.decrypt(getUsername())
    password = cipher_suite.decrypt(getPassword())
    return pymongo.MongoClient(
        "mongodb://" + username + ":" + password + "@cluster0-shard-00-00-b1bc1.mongodb.net:27017,"
                                                   "cluster0-shard-00-01-b1bc1.mongodb.net:27017,"
                                                   "cluster0-shard-00-02-b1bc1.mongodb."
                                                   "net:27017/test?ssl=true&replicaSet=Cluster0-"
                                                   "shard-0&authSource=admin&retryWrites=true&w="
                                                   "majority")


def redactor(database,collection):

    # Redactor takes the database and collection name and redacts the sensitive fields in the collection with MD5 Hashes

    if database == "mflix" and collection=="movies":
        db = connect().mflix;
        json_input = dumps(db.movies.find().limit(5))
        # Converts returned JSON to Python dict
        json_decoded = json.loads(json_input)
        for i, items in enumerate(json_decoded):
            # Hashes countries and imdb/rating field for each returned document and writes them back into the same JSON
            original_country = json_decoded[i]['countries'][0]
            redacted_country = hashlib.md5(original_country.encode('utf-8')).hexdigest()
            json_decoded[i]['countries'] = redacted_country
            original_imdb = str(json_decoded[i]['imdb']['rating'])
            redacted_imdb = hashlib.md5(original_imdb.encode('utf-8')).hexdigest()
            json_decoded[i]['imdb']['rating'] = redacted_imdb
        output_json = json.dumps(json_decoded)
    else :
        # If the database or collection name isn't supported, the redactor fails
        output_json = 'Database or Collection not supported'
    return output_json


class DbRedactor:

    pprint(redactor("mflix", "movies"))
