import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash='', difficulty=4):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculates the hash of the block using SHA-256"""
        block_string = f'{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}'
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def mine_block(self):
        """Perform Proof of Work to find a valid hash"""
        while self.hash[:self.difficulty] != '0' * self.difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block #{self.index} mined: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]# Create the genesis block
        self.difficulty = 5

    def create_genesis_block(self):
        """Create the first block in the chain (genesis block)"""
        return Block(0, time.time(), "Genesis Block", "0")

    def add_block(self, data):
        """Add a new block to the blockchain with Proof of Work"""
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, last_block.hash, self.difficulty)
        new_block.mine_block() # Mine the block to solve the PoW puzzle
        self.chain.append(new_block)

    def is_valid(self):
        """Check if the blockchain is valid"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def display_chain(self):
        """Display the blockchain"""
        for block in self.chain:
            print(f'Block #{block.index}')
            print(f'Timestamp: {time.ctime(block.timestamp)}')
            print(f'Data: {block.data}')
            print(f'Hash: {block.hash}')
            print(f'Previous Hash: {block.previous_hash}')
            print(f'Nonce: {block.nonce}')
            print('-' * 40)


if __name__ == "__main__":# Test the Blockchain with Proof of Work

    blockchain = Blockchain()

    blockchain.add_block("Transaction 1: A -> B")
    blockchain.add_block("Transaction 2: B -> C")
    blockchain.add_block("Transaction 3: C -> D")

    blockchain.display_chain()

    if blockchain.is_valid():
        print("Blockchain is valid.")
    else:
        print("Blockchain is not valid.")
