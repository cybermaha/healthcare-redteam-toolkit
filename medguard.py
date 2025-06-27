import os
import json
import random
import datetime
import socket
import threading
import time
import subprocess
from collections import defaultdict
import cryptography
from cryptography.fernet import Fernet

# Ethical Boundaries
print("""
MEDGUARD PENTEST SUITE - ETHICAL CONSIDERATIONS
1. This tool simulates attacks for security testing only
2. Never run on production systems without explicit authorization
3. Never interact with real patient data
4. All findings must be reported through proper channels
5. Comply with HIPAA, GDPR, and all relevant regulations
""")

class HealthcareRedTeamToolkit:
    def __init__(self):
        self.medical_devices = self.generate_medical_devices()
        self.hospital_network = self.generate_hospital_network()
        self.patient_records = self.generate_fake_patient_records(50)
        self.attack_history = []
        self.fernet_key = Fernet.generate_key()
        self.cipher = Fernet(self.fernet_key)
    
    def generate_medical_devices(self):
        """Generate simulated medical devices with vulnerabilities"""
        devices = []
        device_types = [
            "Patient Monitor", "Infusion Pump", "Ventilator", "MRI Scanner", 
            "CT Scanner", "Ultrasound", "EKG Machine", "PACS Server", 
            "Pharmacy Dispenser", "Blood Analyzer"
        ]
        manufacturers = ["Medtronic", "GE Healthcare", "Siemens Healthineers", 
                        "Philips Healthcare", "Stryker", "Baxter", "Fresenius"]
        
        for i in range(20):
            device = {
                "id": f"DEV-{random.randint(1000,9999)}",
                "type": random.choice(device_types),
                "manufacturer": random.choice(manufacturers),
                "ip": f"192.168.{random.randint(1,254)}.{random.randint(10,250)}",
                "os": random.choice(["Windows Embedded", "Linux RT", "VxWorks", "Custom OS"]),
                "firmware": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
                "vulnerabilities": [],
                "credentials": [
                    {"username": "admin", "password": "admin"},
                    {"username": "tech", "password": "tech123"},
                    {"username": "service", "password": "service"}
                ]
            }
            
            # Add simulated vulnerabilities
            vulns = []
            if random.random() > 0.3:
                vulns.append({
                    "cve": f"CVE-2023-{random.randint(1000,9999)}",
                    "name": "Hardcoded Credentials",
                    "severity": "High",
                    "description": "Device contains hardcoded administrative credentials"
                })
            if random.random() > 0.5:
                vulns.append({
                    "cve": f"CVE-2022-{random.randint(1000,9999)}",
                    "name": "Unpatched Firmware",
                    "severity": "Critical",
                    "description": f"Firmware version {device['firmware']} contains known vulnerabilities"
                })
            if random.random() > 0.7:
                vulns.append({
                    "cve": f"CVE-2024-{random.randint(1000,9999)}",
                    "name": "Buffer Overflow",
                    "severity": "Critical",
                    "description": "Vulnerable service allows remote code execution"
                })
            
            device["vulnerabilities"] = vulns
            devices.append(device)
        
        return devices
    
    def generate_hospital_network(self):
        """Simulate hospital network infrastructure"""
        departments = [
            "Emergency", "Radiology", "ICU", "Oncology", "Cardiology",
            "Pharmacy", "Laboratory", "Surgery", "Pediatrics", "Administration"
        ]
        
        network = {
            "subnets": [
                {"name": "Clinical Network", "subnet": "192.168.1.0/24", "devices": []},
                {"name": "Guest Network", "subnet": "10.10.1.0/24", "devices": []},
                {"name": "Administrative Network", "subnet": "172.16.1.0/24", "devices": []},
                {"name": "Medical Devices", "subnet": "192.168.100.0/24", "devices": []}
            ],
            "servers": [
                {"name": "EHR Server", "ip": "192.168.1.10", "os": "Windows Server 2022", "services": ["EHR Database", "AD Authentication"]},
                {"name": "PACS Server", "ip": "192.168.1.20", "os": "Linux", "services": ["DICOM", "Imaging Storage"]},
                {"name": "Pharmacy Server", "ip": "192.168.1.30", "os": "Windows Server 2019", "services": ["Drug Database", "Prescription System"]},
                {"name": "AD Domain Controller", "ip": "192.168.1.40", "os": "Windows Server 2022", "services": ["Active Directory", "DNS", "DHCP"]},
            ],
            "firewalls": [
                {"name": "Perimeter Firewall", "model": "Palo Alto PA-5200", "rules": 42},
                {"name": "Internal Firewall", "model": "Cisco ASA 5516", "rules": 28}
            ],
            "security_controls": [
                "Endpoint Protection", "Network Segmentation", "Log Monitoring",
                "Physical Access Control", "Encrypted Backups"
            ]
        }
        
        # Assign devices to networks
        for device in self.medical_devices:
            network["subnets"][3]["devices"].append(device)
        
        # Add workstations
        for dept in departments:
            for i in range(random.randint(3, 8)):
                subnet = random.choice(network["subnets"])
                workstation = {
                    "hostname": f"{dept[:3]}-WS{i+1}",
                    "ip": subnet["subnet"].replace("0/24", str(random.randint(10, 240))),
                    "os": random.choice(["Windows 10", "Windows 11", "macOS"]),
                    "department": dept,
                    "user": self.generate_username()
                }
                subnet["devices"].append(workstation)
        
        return network
    
    def generate_username(self):
        """Generate a random username"""
        first_names = ["john", "sarah", "mike", "lisa", "david", "emma", "james", "olivia"]
        last_names = ["smith", "johnson", "williams", "brown", "jones", "miller", "davis"]
        return f"{random.choice(first_names)}.{random.choice(last_names)}{random.randint(1, 99)}"
    
    def generate_fake_patient_records(self, count):
        """Generate simulated patient records (not real data)"""
        records = []
        medical_conditions = [
            "Hypertension", "Diabetes", "Asthma", "Arthritis", "Coronary Artery Disease",
            "COPD", "Depression", "Chronic Kidney Disease", "Cancer", "Osteoporosis"
        ]
        first_names = ["John", "Sarah", "Michael", "Lisa", "David", "Emma", "James", "Olivia"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis"]
        
        for _ in range(count):
            record = {
                "patient_id": f"PT-{random.randint(100000,999999)}",
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "dob": self.generate_random_date(1930, 2010),
                "admit_date": self.generate_random_date(2018, 2023),
                "condition": random.choice(medical_conditions),
                "attending_physician": f"Dr. {random.choice(first_names)} {random.choice(last_names)}",
                "room": f"{random.randint(1,10)}{random.choice('ABCDE')}",
                "medications": random.sample(["Lisinopril", "Metformin", "Albuterol", "Atorvastatin", "Levothyroxine"], k=2),
                "allergies": random.sample(["Penicillin", "Latex", "Shellfish", "NSAIDs"], k=1),
                "tests": [],
                "encrypted": False
            }
            
            # Add test results
            for _ in range(random.randint(1, 3)):
                test = {
                    "test": random.choice(["Blood Test", "X-Ray", "MRI", "EKG", "Ultrasound"]),
                    "result": random.choice(["Normal", "Abnormal", "Inconclusive"]),
                    "date": self.generate_random_date(2022, 2023)
                }
                record["tests"].append(test)
            
            records.append(record)
        
        return records
    
    def generate_random_date(self, start_year, end_year):
        """Generate a random date between two years"""
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Safe for all months
        return f"{year}-{month:02d}-{day:02d}"
    
    def log_attack(self, attack_type, target, result):
        """Log attack activity for reporting"""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "attack": attack_type,
            "target": target,
            "result": result,
            "attacker": "RedTeam",
            "severity": "High"
        }
        self.attack_history.append(entry)
        print(f"[ATTACK] {attack_type} against {target} - Result: {result}")
    
    def network_reconnaissance(self):
        """Simulate network reconnaissance phase"""
        print("\n=== NETWORK RECONNAISSANCE ===")
        print("Discovering hospital network topology...")
        time.sleep(2)
        
        # Simulate network scanning
        print(f"\nDiscovered {len(self.hospital_network['subnets'])} subnets:")
        for subnet in self.hospital_network["subnets"]:
            print(f"  - {subnet['name']}: {subnet['subnet']} ({len(subnet['devices'])} devices)")
        
        print("\nCritical Servers:")
        for server in self.hospital_network["servers"]:
            print(f"  - {server['name']} ({server['ip']}) - OS: {server['os']}")
        
        print("\nSecurity Controls:")
        print("  - " + "\n  - ".join(self.hospital_network["security_controls"]))
        
        self.log_attack("Network Reconnaissance", "Entire Network", "Network mapping completed")
        return True
    
    def vulnerability_scan(self, target_ip=None):
        """Simulate vulnerability scanning of medical devices"""
        print("\n=== VULNERABILITY SCANNING ===")
        
        if target_ip:
            print(f"Scanning target: {target_ip}")
            target_device = None
            for subnet in self.hospital_network["subnets"]:
                for device in subnet["devices"]:
                    if device.get("ip") == target_ip:
                        target_device = device
                        break
                if target_device:
                    break
            
            if not target_device:
                print(f"Device with IP {target_ip} not found")
                return False
            
            print(f"Scanning {target_device.get('type', 'Device')} ({target_ip})...")
            time.sleep(3)
            
            if target_device.get("vulnerabilities"):
                print(f"Found {len(target_device['vulnerabilities'])} vulnerabilities:")
                for vuln in target_device["vulnerabilities"]:
                    print(f"  - {vuln['name']} ({vuln['cve']}): {vuln['severity']} severity")
                    print(f"    Description: {vuln['description']}")
                self.log_attack("Vulnerability Scan", target_ip, f"Found {len(target_device['vulnerabilities'])} vulnerabilities")
            else:
                print("No critical vulnerabilities found")
                self.log_attack("Vulnerability Scan", target_ip, "No critical vulnerabilities")
            return True
        
        else:
            print("Scanning all medical devices...")
            time.sleep(4)
            
            vulnerable_devices = []
            for device in self.medical_devices:
                if device["vulnerabilities"]:
                    vulnerable_devices.append(device)
            
            print(f"\nFound {len(vulnerable_devices)}/{len(self.medical_devices)} devices with vulnerabilities")
            for device in vulnerable_devices:
                print(f"  - {device['type']} ({device['ip']}): {len(device['vulnerabilities'])} vulnerabilities")
            
            self.log_attack("Vulnerability Scan", "Medical Devices", f"{len(vulnerable_devices)} vulnerable devices found")
            return vulnerable_devices
    
    def exploit_device(self, target_ip):
        """Simulate exploiting a vulnerable medical device"""
        print(f"\n=== EXPLOITING DEVICE: {target_ip} ===")
        
        # Find target device
        target_device = None
        for device in self.medical_devices:
            if device["ip"] == target_ip:
                target_device = device
                break
        
        if not target_device:
            print("Device not found")
            return False
        
        if not target_device["vulnerabilities"]:
            print("No vulnerabilities found on this device")
            return False
        
        # Simulate exploit
        print(f"Exploiting {target_device['type']} ({target_ip})...")
        time.sleep(3)
        
        # 70% success rate for simulation
        if random.random() < 0.7:
            print("Exploit successful! Gained administrative access")
            print("Credentials compromised:")
            for cred in target_device["credentials"]:
                print(f"  - {cred['username']}:{cred['password']}")
            
            # Simulate implanting persistence
            print("Establishing persistent access...")
            time.sleep(2)
            print("Implanted backdoor on device")
            
            self.log_attack("Device Exploit", target_ip, "Successful compromise")
            return True
        else:
            print("Exploit failed - Security controls detected attack")
            self.log_attack("Device Exploit", target_ip, "Blocked by security controls")
            return False
    
    def pivot_to_ehr(self):
        """Simulate pivoting to Electronic Health Records system"""
        print("\n=== ATTACK: PIVOTING TO EHR SYSTEM ===")
        print("Attempting to access Electronic Health Records server...")
        time.sleep(3)
        
        # Simulate lateral movement
        print("Compromising workstation...")
        workstations = []
        for subnet in self.hospital_network["subnets"]:
            for device in subnet["devices"]:
                if "hostname" in device and "WS" in device["hostname"]:
                    workstations.append(device)
        
        if not workstations:
            print("No workstations found")
            return False
        
        target_ws = random.choice(workstations)
        print(f"Compromised {target_ws['hostname']} ({target_ws['ip']}) in {target_ws['department']} department")
        time.sleep(2)
        
        # Attempt EHR access
        print("Searching for EHR credentials...")
        time.sleep(2)
        
        # 60% chance of finding credentials
        if random.random() < 0.6:
            credentials = [
                {"username": "doctor1", "password": "Winter2023!"},
                {"username": "nurse2", "password": "Summer2023?"},
                {"username": "admin_ehr", "password": "P@ssw0rd123"}
            ]
            cred = random.choice(credentials)
            print(f"Found credentials: {cred['username']}:{cred['password']}")
            
            print("Accessing EHR server...")
            time.sleep(2)
            
            # Access patient records
            print("Accessing patient records...")
            time.sleep(1)
            
            # Encrypt records to simulate ransomware
            if random.random() < 0.4:  # 40% chance of ransomware simulation
                print("Deploying ransomware simulation...")
                for record in self.patient_records:
                    if not record["encrypted"]:
                        record["encrypted"] = True
                print(f"Encrypted {len(self.patient_records)} patient records")
                self.log_attack("Ransomware Simulation", "EHR Server", f"Encrypted {len(self.patient_records)} records")
            
            # Exfiltrate data
            print("Exfiltrating simulated patient data...")
            time.sleep(2)
            exfil_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "records_exfiltrated": random.randint(5, 15),
                "data_type": "simulated_patient_records"
            }
            print(f"Exfiltrated simulated data: {exfil_data}")
            self.log_attack("Data Exfiltration", "EHR Server", f"Simulated exfiltration of {exfil_data['records_exfiltrated']} records")
            return True
        else:
            print("Failed to find valid EHR credentials")
            self.log_attack("EHR Access Attempt", "EHR Server", "Failed - Credentials not found")
            return False
    
    def generate_report(self):
        """Generate comprehensive penetration test report"""
        print("\n=== GENERATING FINAL REPORT ===")
        time.sleep(2)
        
        report = {
            "date": datetime.datetime.now().isoformat(),
            "executive_summary": "Simulated penetration test of healthcare network",
            "critical_findings": [],
            "recommendations": [],
            "attack_timeline": self.attack_history,
            "vulnerable_devices": [],
            "security_rating": random.choice(["D", "C", "B", "A"])  # Simulated rating
        }
        
        # Collect vulnerabilities
        for device in self.medical_devices:
            if device["vulnerabilities"]:
                report["vulnerable_devices"].append({
                    "device": device["type"],
                    "ip": device["ip"],
                    "vulnerabilities": device["vulnerabilities"]
                })
        
        # Generate findings based on attack results
        if any("Successful compromise" in a["result"] for a in self.attack_history):
            report["critical_findings"].append("Medical devices compromised with administrative access")
            report["recommendations"].append("Implement medical device security hardening procedures")
            report["recommendations"].append("Change all default credentials on medical devices")
        
        if any("EHR Server" in a["target"] for a in self.attack_history):
            report["critical_findings"].append("EHR system access compromised")
            report["recommendations"].append("Implement multi-factor authentication for EHR access")
            report["recommendations"].append("Conduct regular user awareness training")
        
        if any("Ransomware" in a["attack"] for a in self.attack_history):
            report["critical_findings"].append("Ransomware simulation successfully encrypted patient records")
            report["recommendations"].append("Implement robust backup and recovery procedures")
            report["recommendations"].append("Segment EHR systems from general network")
        
        # Save report
        filename = f"medguard_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"Report generated: {filename}")
        print("\n=== KEY FINDINGS ===")
        print(f"Security Rating: {report['security_rating']}")
        print(f"Critical Findings: {len(report['critical_findings'])}")
        print(f"Vulnerable Devices: {len(report['vulnerable_devices'])}")
        print(f"Recommendations: {len(report['recommendations'])}")
        
        return filename

def display_banner():
    print(r"""
  __  __ ______ _____  _____   ____  _____ _______ ______ _   _ 
 |  \/  |  ____|  __ \|  __ \ / __ \|  __ \__   __|  ____| \ | |
 | \  / | |__  | |  | | |  | | |  | | |__) | | |  | |__  |  \| |
 | |\/| |  __| | |  | | |  | | |  | |  _  /  | |  |  __| | . ` |
 | |  | | |____| |__| | |__| | |__| | | \ \  | |  | |____| |\  |
 |_|  |_|______|_____/|_____/ \____/|_|  \_\ |_|  |______|_| \_|
                                                                
    Healthcare Cybersecurity Red Team Toolkit - MEDGUARD v2.1
    """)

def main_menu():
    tool = HealthcareRedTeamToolkit()
    
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Network Reconnaissance")
        print("2. Vulnerability Scan (All Devices)")
        print("3. Vulnerability Scan (Specific Device)")
        print("4. Exploit Medical Device")
        print("5. Pivot to EHR System")
        print("6. Generate Report")
        print("7. View Simulated Network")
        print("8. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            tool.network_reconnaissance()
        
        elif choice == "2":
            tool.vulnerability_scan()
        
        elif choice == "3":
            ip = input("Enter device IP to scan: ")
            tool.vulnerability_scan(ip)
        
        elif choice == "4":
            ip = input("Enter device IP to exploit: ")
            tool.exploit_device(ip)
        
        elif choice == "5":
            tool.pivot_to_ehr()
        
        elif choice == "6":
            tool.generate_report()
        
        elif choice == "7":
            print("\n=== SIMULATED HOSPITAL NETWORK ===")
            print(json.dumps(tool.hospital_network, indent=2))
            print("\n=== SIMULATED MEDICAL DEVICES ===")
            print(json.dumps(tool.medical_devices, indent=2))
        
        elif choice == "8":
            print("Exiting MedGuard Toolkit")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    display_banner()
    main_menu()
