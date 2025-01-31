import os

class KeyManager:
    """Manages application keys."""
    def __init__(self):
        self.keys = {
            'API_KEY': os.getenv('API_KEY', 'default_api_key'),  # API key from environment variable
            'SECRET_TOKEN': os.getenv('SECRET_TOKEN', 'default_secret_token')  # Secret token from environment variable
        }

    def get_key(self, key_name):
        """Retrieve a key by name."""
        return self.keys.get(key_name, None)

    def add_key(self, key_name, key_value):
        """Add or update a key."""
        self.keys[key_name] = key_value
        print(f"Key {key_name} added/updated successfully.")

    def remove_key(self, key_name):
        """Remove a key."""
        if key_name in self.keys:
            del self.keys[key_name]
            print(f"Key {key_name} removed successfully.")
        else:
            print(f"Key {key_name} does not exist.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage application keys.")
    parser.add_argument("action", choices=['get', 'add', 'remove'], help="Action to perform")
    parser.add_argument("key_name", type=str, help="Name of the key")
    parser.add_argument("key_value", nargs="?", type=str, help="Value of the key (for add action only)")

    args = parser.parse_args()

    manager = KeyManager()

    if args.action == "get":
        key = manager.get_key(args.key_name)
        print(f"Value: {key}")
    elif args.action == "add":
        if not args.key_value:
            print("Error: key_value is required for add action.")
        else:
            manager.add_key(args.key_name, args.key_value)
    elif args.action == "remove":
        manager.remove_key(args.key_name)