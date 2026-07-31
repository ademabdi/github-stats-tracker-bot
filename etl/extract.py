import requests
#pull from Github API, save to df (raw data landing zone)

def extract_from_github(owner,repo):
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}")

    if response.status_code != 200:
        print(f"error getting info: {response.status.code}: {response.json().get('message')}")
        return None
    res = response.json()
    print(res)
    return res


extract_from_github("karpathy","jobs")