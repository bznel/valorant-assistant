import sys, requests, os, base64

storage = os.getenv('LOCALAPPDATA')+"\\valassistant\\"
if not os.path.exists(storage):
    os.makedirs(storage)

# when the C code runs this, it passes through an argument specifying what it wants this code to do
# Right now we're only using the -clientinfo option, so ignore the others (-playerinfo and -gamestate)

if (sys.argv[1] == "-clientinfo"):  # this is for getting basic info about the client and authentication info, which is used for more api access

    lockfile_data = sys.argv[2].split(':')  # If you already read the C code, you'll know we got data from a "lockfile"
                                            # for whatever reason, each field in that data is seperated by a ':' so we'll seperate them here

    port = lockfile_data[2]     # This is the port valorant's local server is running at 
    password = lockfile_data[3] # and this is the password needed to access the server

    res = requests.get(
        f"https://127.0.0.1:{port}/entitlements/v1/token", # send the request to the localserver at the given port
        headers = {                                        # also giving it the password via a header in a certain format (just figured it out with boring documentation pages)
            "Authorization": "Basic "+ base64.b64encode(bytes(f"riot:{password}", 'utf-8')).decode()
        }, 
        verify=False
    ).json()

    open(storage+"clientInfo.json", 'w').write(str(res))   # then we store the client info from the server in a file for the C code to access

if (sys.argv[1] == "-playerinfo"):  # this is for getting info about their valorant account (not used yet)
    auth_token = sys.argv[2]
    res = requests.get(
        "https://auth.riotgames.com/userinfo",
        headers= {
            "Authorization": f"Bearer {auth_token}"
        },
        verify = True
    ).json()

    open(storage+"playerInfo.json", 'w').write(res)
if (sys.argv[1] == "-gamestate"):   # and this is for getting info about their current match (other players stats, server location, etc.) (not used yet)

    puuid = sys.argv[2]
    entitlement_token = sys.argv[3]
    auth_token = sys.argv[4]
    
    game_state = requests.get(
            f"https://glz-na-1.na.a.pvp.net/core-game/v1/players/{puuid}",
            headers = {
                "X-Riot-Entitlements-JWT": entitlement_token,
                "Authorization": f"Bearer {auth_token}"
            },
            verify = True
    ).json()
    try:
        if game_state['httpStatus'] == 404:
            in_game = False
        else:
            in_game = True
    except KeyError:
        in_game = True

    if in_game:
        match_id = game_state['MatchID']

        res = requests.get(
                f"https://glz-na-1.na.a.pvp.net/core-game/v1/matches/{match_id}",
                headers = {
                    "X-Riot-Entitlements-JWT": entitlement_token,
                    "Authorization": f"Bearer {auth_token}"
                },
                verify = True
        ).json()

        open(storage+"gameState.json", 'w').write(res)

    



