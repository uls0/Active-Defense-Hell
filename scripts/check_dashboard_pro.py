import requests
import json

def check_dashboard_pro():
    host = "178.128.72.149"
    try:
        # Check HTML
        r_html = requests.get(f"http://{host}:8888", timeout=5)
        # Check Stats API
        r_stats = requests.get(f"http://{host}:8888/api/stats", timeout=5)
        # Check Loot API
        r_loot = requests.get(f"http://{host}:8888/api/loot", timeout=5)
        
        results = {
            "html_ok": r_html.status_code == 200,
            "api_stats": r_stats.json(),
            "api_loot": r_loot.json()
        }
        return results
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    report = check_dashboard_pro()
    print(json.dumps(report, indent=2))
