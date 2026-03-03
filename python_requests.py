import requests

# --- 1. 환경 설정 ---
API_KEY = "발급받으신_키를_여기에_넣으세요" # 매일 갱신해야 하는 그 키!
GAME_NAME = "Hide on bush"
TAG_LINE = "KR1"

def get_faker_latest_match():
    # 공정 A: 계정명으로 PUUID(고유번호) 찾기
    account_url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}?api_key={API_KEY}"
    
    response = requests.get(account_url)
    
    if response.status_code != 200:
        print(f"❌ 계정 찾기 실패! 에러 코드: {response.status_code}")
        if response.status_code == 403: print("👉 API 키가 만료된 것 같아요. 갱신해주세요!")
        return None

    puuid = response.json().get('puuid')
    print(f"✅ 페이커 PUUID 확보: {puuid[:10]}...") # 보안상 앞부분만 출력

    # 공정 B: 확보한 PUUID로 최근 경기 ID 딱 1개만 가져오기
    # asia 서버를 사용하며, count=1로 설정해 최신 경기만 타겟팅합니다.
    match_list_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1&api_key={API_KEY}"
    
    match_res = requests.get(match_list_url)
    
    if match_res.status_code == 200:
        match_ids = match_res.json()
        if match_ids:
            latest_id = match_ids[0]
            print(f"✅ 최신 경기 ID 확보: {latest_id}")
            return latest_id
        else:
            print("❌ 최근 경기 기록이 없습니다.")
    else:
        print(f"❌ 경기 목록 가져오기 실패! 에러 코드: {match_res.status_code}")
    
    return None

# 실행부
faker_match_id = get_faker_latest_match()

if faker_match_id:
    print("-" * 30)
    print(f"최종 결과값: {faker_match_id}")
    print("-" * 30)
