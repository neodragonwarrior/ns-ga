import importlib
import requests
importlib.reload(requests)
#import requests

def fetch_code_scanning_alerts(repo_owner, repo_name, github_token):
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/code-scanning/alerts'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch code scanning alerts: {response.status_code}")
        return None

def get_cwe_details(cwe_id):
    url = f'https://cwe.mitre.org/data/definitions/{cwe_id}.html'
    response = requests.get(url)
    if response.status_code == 200:
        # Extract likelihood of exploitability from the HTML content
        likelihood_index = response.text.find('<td>Likelihood of Exploit</td>')
        likelihood = response.text[likelihood_index:].split('<td>')[2].split('</td>')[0].strip()
        return likelihood
    else:
        print(f"Failed to fetch CWE details: {response.status_code}")
        return None

def print_vulnerabilities_with_details(alerts):
    for alert in alerts:
        if alert['state'] == 'open' and 'rule' in alert and 'ruleId' in alert['rule']:
            cwe_id = alert['rule']['ruleId']
            cwe_details = get_cwe_details(cwe_id)
            if cwe_details and cwe_details.lower() in ['high', 'very high']:
                print(f"Title: {alert['rule'].get('description', 'N/A')}")
                print(f"Severity: {alert['rule'].get('severity', 'N/A')}")
                print(f"Likelihood of Exploitability: {cwe_details}")
                print(f"Details: {alert.get('html_url', 'N/A')}\n")

# Replace these values with your repository details and GitHub token
repo_owner = 'neodragonwarrior'
repo_name = 'GA_NS'
github_token = 'ghp_XXXc'

# Fetch code scanning alerts
alerts = fetch_code_scanning_alerts(repo_owner, repo_name, github_token)
if alerts:
    print("Vulnerabilities with severity High or above and Likelihood of Exploitability High or above:\n")
    print_vulnerabilities_with_details(alerts)
else:
    print("Failed to fetch code scanning alerts.")

