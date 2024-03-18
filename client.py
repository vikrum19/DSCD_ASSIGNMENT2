import random
import grpc
import raft_rpc_pb2
import raft_rpc_pb2_grpc

class RaftClient:
    def __init__(self, node_addresses):
        self.node_addresses = node_addresses
        self.leader_address = None

    def set_leader_address(self, address):
        self.leader_address = address

    def send_request(self, command, key, value=None):
        if not self.leader_address:
            self.leader_address = random.choice(self.node_addresses)

        channel = grpc.insecure_channel(self.leader_address)
        stub = raft_rpc_pb2_grpc.RaftServiceStub(channel)

        if command.upper() == 'SET':
            response = stub.Set(raft_rpc_pb2.SetRequest(key=key, value=value))
        elif command.upper() == 'GET':
            response = stub.Get(raft_rpc_pb2.GetRequest(key=key))
        else:
            raise ValueError("Command must be 'SET' or 'GET'.")

        if response.success:
            return response.value
        else:
            # This would be where you handle a failed request, for example:
            # - Update the leader address if the current one is outdated
            # - Retry the request with the new leader
            # - Handle the case where there is no leader
            print(f"Request failed: {response.message}")
            if response.leader_address:
                self.set_leader_address(response.leader_address)
                return self.send_request(command, key, value)
            else:
                return "No leader available."

if __name__ == "__main__":
    node_addresses = ['localhost:5000', 'localhost:5001', 'localhost:5002', 'localhost:5003', 'localhost:5004']
    client = RaftClient(node_addresses)

    # Example usage:
    print(client.send_request('SET', 'key1', 'value1'))
    print(client.send_request('GET', 'key1'))
