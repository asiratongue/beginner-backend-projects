import os, redis, sys, json, urllib.request
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

load_dotenv(dotenv_path='G:/01101000111101/Programming/Projects/Backend Projects/Weather API Wrapper/config.env')
#change to your own API key .env file.

api_key = os.getenv('YOUR_API_KEY')
db_url = os.getenv('REDIS_CONNECTION_ENDPOINT')
db_port = os.getenv('REDIS_PORT')
db_pass = os.getenv('REDIS_PASS')

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])


RedisClient = redis.Redis(
  host=db_url,
  port=db_port,
  password=db_pass,
)
    
def cache_result(key, value, expiration=3600):

  try:

    RedisClient.setex(key, expiration, json.dumps(value))
    Val = RedisClient.get(key)
    ValData = json.loads(Val)
    return ValData
  
  except Exception as e:
    print(f"Error caching result {e}")

def get_cached_result(key):

  if RedisClient.exists(key) == 0:
    return 0
  else:
    try:
      cached_value = RedisClient.get(key)
      CachedValueData = json.loads(cached_value)
      return CachedValueData
    
    except Exception as e:
      print(f"error finding cached value{e}")


@app.route("/<string:location>", methods = ['GET'])
def FlaskLocate(location):

    Cacheresult = get_cached_result(location)
    if Cacheresult == 0:
      try:
        ResultBytes = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/next7days?unitGroup=uk&key={api_key}&include=days&elements=datetime,tempmax,tempmin,temp,sunrise,description")
        jsonData = json.load(ResultBytes)
        Valret = cache_result(location,jsonData)
        return jsonify(Valret)
             
      except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        return f'Error code:  {e.code}, Error Information: {ErrorInfo}', 400

      except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        return f'Error code:  {e.code}, Error Information: {ErrorInfo}', 400
    else:
      return jsonify(Cacheresult)


if __name__ == '__main__':
    app.run(debug=True)