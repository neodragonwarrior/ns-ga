import importlib
import requests
importlib.reload(requests)
#import requests

from bs4 import BeautifulSoup

def get_cwe_details(cwe_id):
    url = f'https://cwe.mitre.org/data/definitions/{cwe_id}.html'
    #print("Fetching details from:", url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            likelihood_div = soup.find('div', id='Likelihood_Of_Exploit')
            if likelihood_div:
                likelihood_value_div = likelihood_div.find('div', class_='indent')
                if likelihood_value_div:
                    likelihood_value = likelihood_value_div.get_text(strip=True)
                    return likelihood_value
                else:
                    print("Likelihood of Exploit value not found within the Likelihood_Of_Exploit div.")
            else:
                print("Likelihood Of Exploit not found in the page for {}".format(cwe_id))
        else:
            print(f"Failed to fetch CWE details: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Error fetching CWE details:", e)
    return None


def fetch_code_scanning_alerts(repo_owner, repo_name, github_token):
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'X-Github-Api-Version': '2022-11-28'
    }
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/code-scanning/alerts'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch code scanning alerts: {response.status_code}")
        return None

def extract_cwe_id(tags):
    for tag in tags:
        if 'cwe' in tag:
            cwe_id = tag.split('/')[-1].split('-')[-1]
            return str(int(cwe_id))
    return None

def print_vulnerabilities_with_details(alerts):
    for alert in alerts:
        if alert['state'] == 'open' and 'rule' in alert:
            # Extracting issue title
            issue_title = alert['rule'].get('description', 'N/A')

            # Extracting severity
            severity = alert['rule'].get('security_severity_level', 'N/A')

            # Extracting CWE ID
            cwe_id = extract_cwe_id(alert['rule'].get('tags', []))

            # Initialize likelihood of exploitability as N/A
            likelihood_of_exploitability = 'N/A'

            # Fetching CWE details if CWE ID is available
            if cwe_id:
                # Fetching CWE details
                cwe_details = get_cwe_details(cwe_id)

                # Update likelihood of exploitability if details fetched successfully
                if cwe_details:
                    likelihood_of_exploitability = cwe_details

            # Print all details
            print(f"Issue Title: {issue_title}")
            print(f"Severity: {severity}")
            print(f"CWE ID: {cwe_id}")
            print(f"Likelihood of Exploitability: {likelihood_of_exploitability}\n")


# Replace these values with your repository details and GitHub token
repo_owner = 'neodragonwarrior'
repo_name = 'ns-ga'
github_token = 'ghp_xxxc'

# Fetch code scanning alerts
alerts = fetch_code_scanning_alerts(repo_owner, repo_name, github_token)
#print(alerts)
if alerts:
    print("Vulnerabilities with severity High or above and Likelihood of Exploitability High or above:\n")
    print_vulnerabilities_with_details(alerts)
else:
    print("Failed to fetch code scanning alerts.")
