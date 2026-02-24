import httpx

def get_oauth_base(auth: dict) -> str:
    return auth["server_endpoint"].replace("/rest/", "")

async def refresh_token(auth: dict) -> dict:
    oauth_base = get_oauth_base(auth)

    url = f"{oauth_base}/oauth/token/"

    data = {
        "grant_type": "refresh_token",
        "client_id": auth["client_id"],
        "client_secret": auth["client_secret"],
        "refresh_token": auth["refresh_token"],
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=data, timeout=10)

    token_data = resp.json()

    auth["access_token"] = token_data["access_token"]
    auth["refresh_token"] = token_data.get("refresh_token", auth["refresh_token"])

    return auth