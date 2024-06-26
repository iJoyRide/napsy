import requests
from time import time, sleep
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv("APPI_KEY")

def check_virustotal(target_url: str, api_key: str, verbosity: bool) -> None:
    url = "https://www.virustotal.com/api/v3/urls"
    payload = f"url={target_url}"
    headers = {
        "accept": "application/json",
        "x-apikey": api_key,
        "content-type": "application/x-www-form-urlencoded"
    }
    max_wait_time = 60
    wait_time = 10
    elapsed_time = 0
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        url_scan_link = response.json()['data']['links']['self']
        while elapsed_time < max_wait_time:
            url_analysis_report = requests.get(url_scan_link, headers=headers)
            if url_analysis_report.status_code == 200:
                url_analysis_report_json = url_analysis_report.json()
                # pprint(url_analysis_report_json)#json
                url_analysis_report_id = url_analysis_report_json['meta']['url_info']['id']
                total_number_of_vendors = len(url_analysis_report_json['data']['attributes']['results'].keys())
                url_report_gui = "https://www.virustotal.com/gui/url/" + url_analysis_report_id
                url_scan_stats = url_analysis_report_json['data']['attributes']['stats']
                malicious_stats = url_scan_stats['malicious']
                results = url_analysis_report_json['data']['attributes']['results']
                
                known_uninteresting_categories = ['harmless', 'timeout']
                for key, value in url_scan_stats.items():
                    if value > 0 and key not in known_uninteresting_categories:
                        pprint(f"{key}: {value}")
                
                # if total_number_of_vendors > 0:
                #     if malicious_stats > 0:
                #         print(f"[gold1][!][/gold1] [red3]{malicious_stats} security vendors flagged this URL as malicious[/red3]")
                #     else:
                #         print(f"[spring_green2][+][/spring_green2] No security vendors flagged this URL as malicious")
                #     print(f"[spring_green2][+][/spring_green2] Security vendors' analysis\n{'-'*32}")
                    
                    
                    # if verbosity:
                    #     pass
                        # for stat, stat_value in url_scan_stats.items():
                        #     print(f"[gold1][!][/gold1] {stat}: {stat_value}/{total_number_of_vendors}")
                        # if malicious_stats > 0:
                        #     table = Table(title="𝔻 𝔼 𝕋 𝔸 𝕀 𝕃 𝕊", show_lines=True)
                        #     table.add_column("VENDOR", justify="center", max_width=60)
                        #     table.add_column("RESULT", justify="center", )
                        #     table.add_column("METHOD", justify="center")
                        #     for key, value in results.items():
                        #         if value['category'] == "malicious":
                        #             table.add_row(key, value['result'], value['method'])
                        #     print(table)
    #                 else:
    #                     for stat, stat_value in url_scan_stats.items():
    #                         # pprint(stat_value)
    #                         print(f"[gold1][!][/gold1] {stat}: {stat_value}/{total_number_of_vendors}")
    #                 print(f"[spring_green2][+][/spring_green2] For more information, you can check the link below ↓")
    #                 print(f"[spring_green2][+][/spring_green2] {url_report_gui}")
    #                 break
    #             else:
    #                 print(f"[gold1][!][/gold1] Scan still in progress. Waiting for {wait_time} seconds...")
    #                 sleep(wait_time)
    #                 elapsed_time += wait_time
    #                 wait_time = 5
    #         else:
    #             print(f"[red3][-][/red3] {url_analysis_report.text}")
    # else:
    #     print(f"[red3][-][/red3] {response.text}")

if __name__ == "__main__":
    target_url = "gomovies.sx"
    verbosity = False  # Define the verbosity variable
    check_virustotal(target_url, api_key, verbosity)

