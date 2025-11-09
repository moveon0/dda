import os
import json
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "serverconfig.json")

_config = {}
if os.path.isfile(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _config = json.load(f)
    except Exception as e:
        logging.warning("serverconfig.json 읽기 실패: %s", e)

MONGO_URI = _config.get("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = _config.get("DB_NAME", "SeoulBike")

client = None
reviews_collection = None
_in_memory_reviews = []

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # 연결 테스트
    client.server_info()
    db = client[DB_NAME]
    reviews_collection = db["reviews"]
    logging.info("MongoDB 연결 성공: %s / DB: %s", MONGO_URI, DB_NAME)
except Exception as e:
    logging.warning("MongoDB 연결 실패, 메모리 저장소 사용: %s", e)
    client = None
    reviews_collection = None
    _in_memory_reviews = []

def insert_review(review):
    """
    review: dict
    반환: 저장된 review (몽고일 경우 그대로, 메모리일 경우에도 동일 객체)
    """
    if reviews_collection:
        reviews_collection.insert_one(review)
        return review
    else:
        _in_memory_reviews.append(review)
        return review

def find_reviews_by_bike(bike_number):
    """
    bike_number: str
    반환: 리스트 of dict (Mongo의 _id 필드는 제거)
    """
    if reviews_collection:
        results = list(reviews_collection.find({"bike_number": bike_number}, {"_id": 0}))
        return results
    else:
        return [r for r in _in_memory_reviews if r.get("bike_number") == bike_number]