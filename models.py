from dataclasses import dataclass

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class IPAddressData:
    ipAddress: Optional[str] = None
    isPublic: Optional[bool] = None
    ipVersion: Optional[int] = None
    isWhitelisted: Optional[bool] = None
    abuseConfidenceScore: Optional[int] = None
    countryCode: Optional[str] = None
    usageType: Optional[str] = None
    isp: Optional[str] = None
    domain: Optional[str] = None
    hostnames: Optional[List[str]] = None
    isTor: Optional[bool] = None
    totalReports: Optional[int] = None
    numDistinctUsers: Optional[int] = None
    lastReportedAt: Optional[str] = None

@dataclass
class UrlsToScan:
    urls: Optional[List[str]] = None
    
    
if "__name__" == "__main__":
# Example of how to use this class with the provided JSON data
    data = {
        "ipAddress": "104.31.16.126",
        "isPublic": True,
        "ipVersion": 4,
        "isWhitelisted": True,
        "abuseConfidenceScore": 0,
        "countryCode": "US",
        "usageType": "Content Delivery Network",
        "isp": "CloudFlare Inc.",
        "domain": "cloudflare.com",
        "hostnames": [],
        "isTor": False,
        "totalReports": 0,
        "numDistinctUsers": 0,
        "lastReportedAt": "2023-05-22T09:31:16+00:00"
    }

    # # Convert the 'lastReportedAt' field to a datetime object
    # if 'lastReportedAt' in data:
    #     data['lastReportedAt'] = datetime.fromisoformat(data['lastReportedAt'])

    ip_address_data = IPAddressData(**data)
    print(ip_address_data)