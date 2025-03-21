import random
from datetime import datetime, timedelta

# Define possible attack types and breach terms
attack_types = [
    'Failed password attempt',
    'Unauthorized access',
    'Malicious payload detected',
    'Intrusion detected',
    'DDoS attack',
    'SQL injection',
    'Cross-site scripting (XSS)',
    'Privilege escalation',
    'Data exfiltration'
]

breach_terms = [
    'breach',
    'attack',
    'intrusion',
    'compromise',
    'malicious',
    'unauthorized',
    'failed attempt'
]

# Generate random IP addresses


def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

# Generate random timestamps


def generate_random_timestamp(start_time, end_time):
    delta = end_time - start_time
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_time + timedelta(seconds=random_seconds)

# Generate random log entries


def generate_log_entry():
    timestamp = generate_random_timestamp(
        datetime(2025, 3, 1), datetime(2025, 3, 20)
    ).strftime('%Y-%m-%d %H:%M:%S')
    ip_address = generate_random_ip()
    attack_type = random.choice(attack_types)
    breach_term = random.choice(breach_terms)

    log_entry = f"{timestamp} - {ip_address} - {attack_type} - {breach_term}"
    return log_entry

# Generate a specified number of log entries


def generate_attack_data(num_entries):
    return [generate_log_entry() for _ in range(num_entries)]

# Save generated log entries to a file


def save_attack_data(log_entries, output_file):
    try:
        with open(output_file, 'w') as file:
            for entry in log_entries:
                file.write(entry + '\n')
        print(f"Attack data saved to {output_file}")
    except Exception as e:
        print(f"Failed to save attack data: {e}")


def main():
    num_entries = 1000  # Number of log entries to generate
    output_file = 'synthetic_attack_data.log'

    log_entries = generate_attack_data(num_entries)
    save_attack_data(log_entries, output_file)


if __name__ == "__main__":
    main()
