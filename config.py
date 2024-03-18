# config.py

# Define the addresses for each Raft node
NODES = {
    1: 'localhost:50051',
    2: 'localhost:50052',
    3: 'localhost:50053',
    4: 'localhost:50054',
    5: 'localhost:50055',
}

# Leader lease duration in seconds
LEADER_LEASE_DURATION = 10

# Heartbeat interval in seconds for the leader
HEARTBEAT_INTERVAL = 1

# Election timeout range in seconds
ELECTION_TIMEOUT_LOWER = 5
ELECTION_TIMEOUT_UPPER = 10
