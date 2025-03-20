import os
import nvdlib
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def get_recent_cves(days_back=7, severity_filter=None):
    """Get recent CVEs from NVD with improved error handling"""
    try:
        # Get API key for NVDLib
        api_key = os.getenv('NVDLIB_API_KEY')
        if not api_key:
            print("NVDLib API key not found")
            return None

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        # Format dates for NVDLib
        start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        print(f"Fetching CVEs from {start_date_str} to {end_date_str}")

        # Get CVEs using nvdlib with API key and retry logic
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                r = nvdlib.searchCVE(
                    key=api_key,
                    pubStartDate=start_date_str,
                    pubEndDate=end_date_str,
                    delay=1.0  # Increased delay for rate limiting
                )
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2

        # Process and format CVE data
        formatted_cves = []
        for cve in r:
            cvss_data = extract_cvss_data(cve)

            if severity_filter and cvss_data['severity'] != severity_filter:
                continue

            formatted_cves.append([
                cve.id,
                cve.descriptions[0].value if cve.descriptions else "No description available",
                cvss_data['score'],
                cve.published,
                cvss_data['severity'],
                cvss_data['vector'],
                cvss_data['attack_vector']
            ])

        print(f"Found {len(formatted_cves)} CVEs")
        return formatted_cves
    except Exception as e:
        print(f"Error fetching NVD data: {str(e)}")
        return None

def extract_cvss_data(cve):
    """Extract CVSS scoring data from a CVE object"""
    data = {
        'score': 0.0,
        'severity': 'NONE',
        'vector': 'N/A',
        'attack_vector': 'N/A'
    }

    if hasattr(cve, 'metrics'):
        # Try CVSS v3.1 first
        if hasattr(cve.metrics, 'cvssMetricV31'):
            cvss = cve.metrics.cvssMetricV31[0].cvssData
            data.update({
                'score': cvss.baseScore,
                'severity': cvss.baseSeverity,
                'vector': cvss.vectorString,
                'attack_vector': cvss.attackVector
            })
        # Fall back to CVSS v3.0
        elif hasattr(cve.metrics, 'cvssMetricV30'):
            cvss = cve.metrics.cvssMetricV30[0].cvssData
            data.update({
                'score': cvss.baseScore,
                'severity': cvss.baseSeverity,
                'vector': cvss.vectorString,
                'attack_vector': cvss.attackVector
            })
        # Fall back to CVSS v2
        elif hasattr(cve.metrics, 'cvssMetricV2'):
            cvss = cve.metrics.cvssMetricV2[0].cvssData
            severity = 'HIGH' if cvss.baseScore >= 7.0 else 'MEDIUM' if cvss.baseScore >= 4.0 else 'LOW'
            data.update({
                'score': cvss.baseScore,
                'severity': severity,
                'vector': cvss.vectorString,
                'attack_vector': cvss.accessVector
            })

    return data

def get_cve_details(cve_id):
    """Get detailed information about a specific CVE"""
    try:
        api_key = os.getenv('NVDLIB_API_KEY')
        if not api_key:
            return None

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                cve = nvdlib.getCVE(cve_id, key=api_key)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2

        details = {
            'id': cve.id,
            'description': cve.descriptions[0].value if cve.descriptions else "No description available",
            'published': cve.published,
            'lastModified': cve.lastModified,
            'references': [ref.url for ref in cve.references] if hasattr(cve, 'references') else [],
            'metrics': {}
        }

        if hasattr(cve, 'metrics'):
            # CVSS v3.1 metrics
            if hasattr(cve.metrics, 'cvssMetricV31'):
                cvss = cve.metrics.cvssMetricV31[0].cvssData
                details['metrics']['v31'] = {
                    'baseScore': cvss.baseScore,
                    'severity': cvss.baseSeverity,
                    'vector': cvss.vectorString,
                    'attackVector': cvss.attackVector,
                    'attackComplexity': cvss.attackComplexity,
                    'privilegesRequired': cvss.privilegesRequired,
                    'userInteraction': cvss.userInteraction,
                    'scope': cvss.scope,
                    'confidentialityImpact': cvss.confidentialityImpact,
                    'integrityImpact': cvss.integrityImpact,
                    'availabilityImpact': cvss.availabilityImpact
                }

            # CVSS v3.0 metrics
            if hasattr(cve.metrics, 'cvssMetricV30'):
                cvss = cve.metrics.cvssMetricV30[0].cvssData
                details['metrics']['v30'] = {
                    'baseScore': cvss.baseScore,
                    'severity': cvss.baseSeverity,
                    'vector': cvss.vectorString
                }

            # CVSS v2 metrics
            if hasattr(cve.metrics, 'cvssMetricV2'):
                cvss = cve.metrics.cvssMetricV2[0].cvssData
                details['metrics']['v2'] = {
                    'baseScore': cvss.baseScore,
                    'vector': cvss.vectorString
                }

        return details
    except Exception as e:
        print(f"Error fetching CVE details: {str(e)}")
        return None

def analyze_vulnerability_trends(days_back=30):
    """Analyze vulnerability trends from collected CVE data"""
    try:
        cves = get_recent_cves(days_back)
        if not cves:
            return None

        # Convert to DataFrame for analysis
        df = pd.DataFrame(cves, columns=['id', 'description', 'score', 'published', 'severity', 'vector', 'attack_vector'])

        # Analyze trends
        analysis = {
            'total_cves': len(df),
            'high_severity': len(df[df['severity'] == 'HIGH']),
            'critical_severity': len(df[df['severity'] == 'CRITICAL']),
            'medium_severity': len(df[df['severity'] == 'MEDIUM']),
            'low_severity': len(df[df['severity'] == 'LOW']),
            'most_recent': cves[0] if cves else None,
            'highest_score': df.loc[df['score'].idxmax()].to_dict() if not df.empty else None,
            'attack_vectors': df['attack_vector'].value_counts().to_dict(),
            'daily_counts': df.groupby(pd.to_datetime(df['published']).dt.date).size().to_dict()
        }

        return analysis
    except Exception as e:
        print(f"Error analyzing vulnerability trends: {str(e)}")
        return None