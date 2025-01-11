import requests
import json
import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



def get_token():
    # API 요청 정보
    api_url = "https://openapi.playauto.io/api/auth"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-api-key": "z5pKdRY7ky8BJMkVwqumk8XEv33UNFS57wfopSP3"  # API Key
    }
    body = {
        "email": os.getenv("API_EMAIL"),  # 환경 변수에서 이메일 가져오기
        "password": os.getenv("API_PASSWORD")  # 환경 변수에서 비밀번호 가져오기
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
            print("Token:", token)
            return token
        else:
            print("Token not found in response.")
    else:
        print(f"Failed to fetch token. HTTP Status Code: {response.status_code}")
        print("Response:", response.text)

def get_stock_condition(token):
    api_url = "https://openapi.playauto.io/api/stock/condition"
    headers = {
        # "Content-Type": "application/json; charset=UTF-8",
        "x-api-key": "z5pKdRY7ky8BJMkVwqumk8XEv33UNFS57wfopSP3",  # API Key
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
        "depot_no": 45204 #지깅프로(김포점)
    }

    # POST 요청 보내기
    response = requests.post(api_url, headers=headers, json=body)

    # 응답 확인
    if response.status_code == 200:
        # JSON 파싱
        data = response.json()["results"]


        if data:
            for datum in data:
                prod_name = datum["prod_name"]
                attri = datum["attri"]
                stock_cnt = datum["stock_cnt"]
                print(f"상품명: {prod_name}, 속성: {attri}, 재고수량: {stock_cnt}")
        else:
            print("No data")
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        print("Response:", response.text)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    token = get_token()
    get_stock_condition(token)
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

