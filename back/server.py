# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import uuid
import os

# db 모듈에서 함수 가져오기
from db import insert_review, find_reviews_by_bike

app = Flask(__name__)
CORS(app)  # 프론트(로컬 파일/다른 포트)에서 접근 가능하도록 허용

# 프론트 정적 파일 경로
FRONT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "front"))

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"received": data})

# 새 엔드포인트: 리뷰 저장
@app.route("/api/reviews", methods=["POST"])
def create_review():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    bike = data.get("bike_number")
    pedal = data.get("pedal")
    brake = data.get("brake")
    tire = data.get("tire")
    text = data.get("text", "")

    if not bike or not isinstance(bike, str):
        return jsonify({"error": "bike_number required"}), 400
    try:
        pedal = int(pedal); brake = int(brake); tire = int(tire)
    except:
        return jsonify({"error": "ratings must be integers"}), 400

    review = {
        "id": str(uuid.uuid4()),
        "bike_number": bike,
        "pedal": pedal,
        "brake": brake,
        "tire": tire,
        "text": text
    }
    # db 모듈의 insert_review 사용
    insert_review(review)
    return jsonify(review), 201

# 특정 따릉이 번호에 대한 리뷰 검색
@app.route("/api/reviews/<bike_number>", methods=["GET"])
def get_reviews_by_bike(bike_number):
    if not bike_number:
        return jsonify({"error": "bike_number is required"}), 400

    reviews = find_reviews_by_bike(bike_number)
    if not reviews:
        return jsonify({"message": "No reviews found for this bike number"}), 404

    return jsonify(reviews), 200

# 프론트 정적 파일 서빙 (API 라우트와 충돌하지 않도록 반드시 API 정의 뒤에 위치)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_front(path):
    # API 경로는 여기서 처리하지 않음
    if path.startswith("api/") or path.startswith("api"):
        return jsonify({"error": "not found"}), 404

    if path == "" or path.endswith("/"):
        return send_from_directory(FRONT_DIR, "index.html")

    target = os.path.join(FRONT_DIR, path)
    if os.path.isfile(target):
        return send_from_directory(FRONT_DIR, path)

    # 파일이 없으면 SPA 용으로 index.html 반환
    return send_from_directory(FRONT_DIR, "index.html")

if __name__ == "__main__":
    # Windows에서 실행: python c:\dda\back\server.py
    app.run(host="0.0.0.0", port=8000, debug=True)