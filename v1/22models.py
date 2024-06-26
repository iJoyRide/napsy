from dataclasses import dataclass
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
class Virus:
    malicious: Optional[str] = None
    suspicious: Optional[str] = None
    undetected: Optional[str] = None

    
    
if "__name__" == "__main__":
    ip_address_data = IPAddressData(**data)
    print(ip_address_data)