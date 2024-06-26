import requests
from time import time, sleep

def check_virustotal(target_url: str, api_key: str) -> dict:
    url = "https://www.virustotal.com/api/v3/urls"
    payload = f"url={target_url}"
    headers = {
        "accept": "application/json",
        "x-apikey": api_key,
        "content-type": "application/x-www-form-urlencoded"
    }
    max_wait_time = 60  # Maximum time to wait for a response
    wait_time = 10      # Time to wait between checks
    start_time = time()  # Record start time
    
    results = {"malicious": 0, "suspicious": 0, "undetected": 0}

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        url_scan_link = response.json()['data']['links']['self']
        while True:
            elapsed_time = time() - start_time  # Update elapsed time
            if elapsed_time > max_wait_time:
                print("Exceeded maximum wait time, exiting.")
                break
            url_analysis_report = requests.get(url_scan_link, headers=headers)
            if url_analysis_report.status_code == 200:
                url_analysis_report_json = url_analysis_report.json()
                url_scan_stats = url_analysis_report_json['data']['attributes']['stats']
                known_uninteresting_categories = ['harmless', 'timeout']
                for key, value in url_scan_stats.items():
                    if key in results:
                        results[key] += value
                break  # Exit the loop after processing the data
            else:
                sleep(wait_time)  # Wait before trying again

    return results

 
if __name__ == "__main__":
    target_url = "gomovies.sx"
    api_key = APPI_KEY = "9761d7d385a80b34aae59ae097aeea7478ec22888c21a65610257dd19c15f11e"
    check_virustotal(target_url, api_key)