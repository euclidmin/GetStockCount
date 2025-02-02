import requests
import json
import os
from datetime import datetime

TOKEN_FILE = "token.json"  # 토큰이 저장될 파일명

def save_token_to_file(token):
    """토큰과 저장 시간을 JSON 파일로 저장"""
    token_data = {
        "token": token,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 저장 시간 추가
    }
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=4)

def load_token_from_file():
    """저장된 토큰을 파일에서 로드"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            token_data = json.load(f)
            return token_data.get("token")  # 토큰 값 반환
    return None  # 파일이 없으면 None 반환

def get_token():
    """토큰을 가져오는 함수 (파일에서 읽거나, 없으면 API 요청)"""
    token = load_token_from_file()  # 파일에서 토큰 로드
    if token:
        print("기존 토큰을 사용합니다.")
        return token

    print("토큰이 존재하지 않거나 만료됨. 새로운 토큰을 요청합니다.")

    # API 요청 정보
    api_url = "https://openapi.playauto.io/api/auth"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-api-key": "z5pKdRY7ky8BJMkVwqumk8XEv33UNFS57wfopSP3"
    }
    body = {
        "email": os.getenv("API_EMAIL"),
        "password": os.getenv("API_PASSWORD")
    }

    # POST 요청 보내기
    response = requests.post(api_url, headers=headers, json=body)

    # 응답 확인
    if response.status_code == 200:
        # JSON 파싱
        data = response.json()
        # token 값 추출
        token = data[0].get("token", None)
        if token:
            save_token_to_file(token)  # 새 토큰을 파일에 저장
            print("새로운 토큰을 저장하였습니다:", token)
            return token
        else:
            print("Token not found in response.")
    else:
        print(f"Failed to fetch token. HTTP Status Code: {response.status_code}")
        print("Response:", response.text)

    return None  # 토큰 요청 실패 시 None 반환

def get_stock_condition(token):
    """ API를 통해 특정 상품의 재고 데이터를 가져오는 함수 """
    api_url = "https://openapi.playauto.io/api/stock/condition"
    headers = {
        "x-api-key": "z5pKdRY7ky8BJMkVwqumk8XEv33UNFS57wfopSP3",
        "Authorization": "Token " + token
    }
    body = {
        "start": 0,
        "limit": 100,
        "orderbyColumn": "wdate",
        "orderbyType": "DESC",
        "search_key": "prod_name",
        "search_word": "빅게임 프로 BGP-1",
        "search_type": "partial",
        "date_type": "wdate",
        "sdate": "2021-01-01",
        "edate": "2024-12-09",
        "depot_no": 45204
    }

    # POST 요청 보내기
    response = requests.post(api_url, headers=headers, json=body)

    # 응답 확인
    if response.status_code == 200:
        # JSON 파싱
        data = response.json()["results"]

        if data:
            stock_list = []
            for datum in data:
                prod_name = datum["prod_name"]
                attri = datum["attri"]
                stock_cnt = datum["stock_cnt"]
                stock_list.append({
                    "상품명": prod_name,
                    "속성": attri,
                    "재고수량": stock_cnt
                })
            return stock_list
        else:
            print("No data available.")
            return []
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        print("Response:", response.text)
        return []

def write_stock_count_excel(stock_list):
    """ 가져온 재고 데이터를 엑셀 파일로 저장하는 함수 """
    import pandas as pd

    if not stock_list:
        print("저장할 데이터가 없습니다.")
        return

    df = pd.DataFrame(stock_list)
    file_name = "stock_data.xlsx"
    df.to_excel(file_name, index=False)

    print(f"재고 데이터가 '{file_name}' 파일로 저장되었습니다.")

# 실행 부분
if __name__ == '__main__':
    token = get_token()
    if token:
        stock_data = get_stock_condition(token)
        write_stock_count_excel(stock_data)
