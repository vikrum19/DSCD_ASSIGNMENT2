import threading
import random
import time

class RaftNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers  # Dictionary of peer addresses {node_id: address}
        self.state = 'follower'
        self.term = 0
        self.vote_count = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.election_timeout = self.get_election_timeout()
        self.heartbeat_interval = 1.0  # 1 second
        self.election_timer = threading.Timer(self.election_timeout, self.start_election)
        self.election_timer.start()
    
    def get_election_timeout(self):
        return random.uniform(5, 10)
    
    def start_election(self):
        self.state = 'candidate'
        self.term += 1
        self.vote_count = 1  # vote for self
        self.voted_for = self.node_id
        self.reset_election_timer()

        # Send vote requests to all other nodes
        for peer_id in self.peers:
            self.request_vote(peer_id)

    def append_entries(self, entries, term):
        if term < self.term:
            return False
        self.reset_election_timer()
        # Here you would have the logic to append entries to the log
        return True

    def request_vote(self, peer_id):
        # Placeholder for sending a vote request to a peer
        # In a real implementation, you would send a network request here
        pass

    def receive_vote_request(self, candidate_term, candidate_id, last_log_index, last_log_term):
        if candidate_term > self.term and self.is_candidate_log_up_to_date(last_log_index, last_log_term):
            self.term = candidate_term
            self.voted_for = candidate_id
            self.reset_election_timer()
            return True
        return False

    def is_candidate_log_up_to_date(self, last_log_index, last_log_term):
        # Here you would check if the candidate's log is at least up-to-date as this node's log
        return True

    def reset_election_timer(self):
        self.election_timer.cancel()
        self.election_timer = threading.Timer(self.get_election_timeout(), self.start_election)
        self.election_timer.start()
    
    # Additional methods for handling RPCs and other Raft logic would go here

if __name__ == "__main__":
    # This would be run for each RaftNode in separate processes or VMs
    node_id = 1  # This should be dynamically determined or passed as an argument
    peers = {2: 'localhost:5001', 3: 'localhost:5002', 4: 'localhost:5003', 5: 'localhost:5004'}
    node = RaftNode(node_id, peers)
    # The node would start running here, listening for RPCs and performing Raft logic
