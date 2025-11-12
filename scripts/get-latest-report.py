import requests
import json
import sys


def main():
    url = "https://api.github.com/repos/monarch-initiative/omim-ingest/releases/latest"

    # Get the latest release from the GitHub API
    response = requests.get(url)
    if response.status_code == 404:
        print(f"No releases found at {url}")
        print("Skipping report download - will use locally generated reports")
        return

    if response.status_code != 200:
        print(f"Warning: Failed to get latest release from {url}", file=sys.stderr)
        print(f"Status: {response.status_code} - {response.text}", file=sys.stderr)
        print("Skipping report download - will use locally generated reports")
        return

    data = json.loads(response.text)

    # Get the download URLs for the reports
    reports = {}
    for asset in data["assets"]:
        report_name = asset["name"]
        if "report.tsv" in asset["name"].split("_"):
            file_url = asset["browser_download_url"]
            reports[report_name] = file_url

    if not reports:
        print("No report assets found in the latest release")
        print("Skipping report download - will use locally generated reports")
        return

    # Download the reports
    print(f"Downloading {len(reports)} report(s) from latest release...")
    for fn, url in reports.items():
        response = requests.get(url)
        output_fn = "_".join(fn.split("_")[-2:])
        with open(f"docs/{output_fn}", "wb") as f:
            f.write(response.content)
        print(f"  ✓ Downloaded {output_fn}")


if __name__ == "__main__":
    main()

