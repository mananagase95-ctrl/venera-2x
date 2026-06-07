import json
import re
import requests
import os
from datetime import datetime

REPO_URL = "mananagase95-ctrl/venera-2x"
APP_NAME = "venera-2x"
APP_ID = "com.github.wgh136.venera"
SOURCE_URL = f"https://github.com/{REPO_URL}"
ICON_URL = f"https://raw.githubusercontent.com/{REPO_URL}/master/assets/app_icon.png"

def prepare_description(text):
    text = re.sub('<[^<]+?>', '', text) # Remove HTML tags
    text = re.sub(r'#{1,6}\s?', '', text) # Remove markdown header tags
    text = re.sub(r'\*{2}', '', text) # Remove all occurrences of two consecutive asterisks
    text = re.sub(r'(?<=\r|\n)-', '•', text) # Only replace - with • if it is preceded by \r or \n
    text = re.sub(r'`', '"', text) # Replace ` with "
    text = re.sub(r'\r\n\r\n', '\r \n', text) # Replace \r\n\r\n with \r \n (avoid incorrect display of the description regarding paragraphs)
    return text

def fetch_latest_release(repo_url):
    api_url = f"https://api.github.com/repos/{repo_url}/releases"
    headers = {
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        releases = response.json()
        return [
            release
            for release in releases
            if not release.get("draft") and not release.get("prerelease")
        ]
    except requests.RequestException as e:
        print(f"Error fetching releases: {e}")
        raise

def get_file_size(url):
    try:
        response = requests.head(url, timeout=30)
        response.raise_for_status()
        return int(response.headers.get('Content-Length', 0))
    except requests.RequestException as e:
        print(f"Error getting file size: {e}")
        return 194586

def update_json_file_release(json_file, latest_release):
    if isinstance(latest_release, list) and latest_release:
        latest_release = latest_release[0]
    else:
        print("Error getting latest release")
        return

    try:
        with open(json_file, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        data = {"apps": []}
        raise

    data.update({
        "name": APP_NAME,
        "website": SOURCE_URL,
        "subtitle": f"{APP_NAME} AltStore Source.",
        "description": "venera-2x 是一个支持本地漫画和网络漫画阅读的跨平台漫画阅读器。",
        "iconURL": ICON_URL,
    })

    app = data["apps"][0]
    app.update({
        "name": APP_NAME,
        "bundleIdentifier": APP_ID,
        "subtitle": "支持本地漫画和网络漫画阅读的漫画阅读器",
        "iconURL": ICON_URL,
    })

    full_version = latest_release["tag_name"]
    tag = latest_release["tag_name"]
    # Extract version like 1.4.5 from tag, which may be like 'v1.4.5'
    version_match = re.search(r"(\d+\.\d+\.\d+)", full_version)
    if version_match:
        version = version_match.group(1)
    else:
        print("Error: Could not parse version from tag_name.")
        return
    version_date = latest_release["published_at"]
    date_obj = datetime.strptime(version_date, "%Y-%m-%dT%H:%M:%SZ")
    version_date = date_obj.strftime("%Y-%m-%d")

    description = latest_release["body"]
    description = prepare_description(description)

    assets = latest_release.get("assets", [])
    download_url = None
    size = None
    for asset in assets:
        if re.fullmatch(rf"{APP_NAME}-ios-{re.escape(version)}\+\d+\.ipa", asset["name"]):
            download_url = asset["browser_download_url"]
            size = asset["size"]
            break

    if download_url is None or size is None:
        print("Error: IPA file not found in release assets.")
        return

    version_entry = {
        "version": version,
        "date": version_date,
        "localizedDescription": description,
        "downloadURL": download_url,
        "size": size
    }

    duplicate_entries = [item for item in app["versions"] if item["version"] == version]
    if duplicate_entries:
        app["versions"].remove(duplicate_entries[0])

    app["versions"].insert(0, version_entry)

    app.update({
        "version": version,
        "versionDate": version_date,
        "versionDescription": description,
        "downloadURL": download_url,
        "size": size
    })

    if "news" not in data:
        data["news"] = []

    news_identifier = f"release-{full_version}"
    date_string = date_obj.strftime("%d/%m/%y")
    news_entry = {
        "appID": APP_ID,
        "caption": f"{APP_NAME} 新版本已发布。",
        "date": latest_release["published_at"],
        "identifier": news_identifier,
        "notify": True,
        "tintColor": "#0784FC",
        "title": f"{full_version} - {APP_NAME} {date_string}",
        "url": f"{SOURCE_URL}/releases/tag/{tag}"
    }

    news_entry_exists = any(item["identifier"] == news_identifier for item in data["news"])
    if not news_entry_exists:
        data["news"].append(news_entry)

    try:
        with open(json_file, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print("JSON file updated successfully.")
    except IOError as e:
        print(f"Error writing to JSON file: {e}")
        raise

def main():
    try:
        fetched_data_latest = fetch_latest_release(REPO_URL)
        json_file = "alt_store.json"
        update_json_file_release(json_file, fetched_data_latest)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
