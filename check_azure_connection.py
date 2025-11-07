# from azure.storage.blob import BlobServiceClient
#
# conn_str = "7KaLBIS3KpBHd6LWrg1TynzRg4zMetilWJLoqI6xPHg0oqqMvO3gjbOd/ZaBdGhnZ5aS1ErEEnG6+AStJ1uYag=="
#
# try:
#     blob_service_client = BlobServiceClient.from_connection_string(conn_str)
#     print("✅ Connection string is valid.")
# except Exception as e:
#     print(f"❌ Error: {e}")
#
from azure.storage.blob import BlobServiceClient

# Replace this with your actual connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=adlgen2reuben;AccountKey=XPxHX9M/AJqBLuPP0WYK2t+jeR9EF5FDK0kyrt7lXUrhky/li7+pi6CKPc6n/NJad0zFgxgMFVuK+ASt86CpmQ==;EndpointSuffix=core.windows.net"

try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    print("✅ Azure Blob connection successful.")
except Exception as e:
    print("❌ Failed to connect:", e)

# import base64
#
# # Replace with your actual key string
# account_key = "XPxHX9M/AJqBLuPP0WYK2t+jeR9EF5FDK0kyrt7lXUrhky/li7+pi6CKPc6n/NJad0zFgxgMFVuK+ASt86CpmQ=="
#
# # Will raise an exception if it's invalid
# base64.b64decode(account_key)