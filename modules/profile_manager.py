import json
import os


PROFILE_FILE = "memory/profile.json"


DEFAULT_PROFILE = {
    "name": "",
    "interests": [],
    "studies": [],
    "projects": []
}


def load_profile():

    if os.path.exists(PROFILE_FILE):

        with open(PROFILE_FILE, "r") as file:
            return json.load(file)

    else:

        save_profile(DEFAULT_PROFILE)
        return DEFAULT_PROFILE



def save_profile(profile):

    os.makedirs(
        "memory",
        exist_ok=True
    )

    with open(PROFILE_FILE, "w") as file:

        json.dump(
            profile,
            file,
            indent=4
        )



def update_profile(category, value):

    profile = load_profile()


    if category == "name":

        profile["name"] = value


    elif category in profile:

        if value not in profile[category]:

            profile[category].append(value)


    save_profile(profile)



def get_profile():

    return load_profile()
