'''
def get_blob(app_id: str, blob_path: str) :
    """
    Retrieves blob data from the specified app using the blob path.
    
    Args:
        app_id: The app ID that owns the blob (e.g., "c25dcd829d134ea98f5ae4dd311d13bc.node3.openfabric.network")
        blob_path: The blob resource path (e.g., "data_blob_.../executions/...")
        
    Returns:
        The binary blob data
    """
    import requests
    
    # Construct the full URL to the blob
    url = f"https://{app_id}/{blob_path}"
    
    # Make the request to retrieve the blob
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve blob: HTTP {response.status_code}")
    
    return response.content


# For the text-to-image result (likely a PNG or JPEG)
app_id = "c25dcd829d134ea98f5ae4dd311d13bc.node3.openfabric.network"
blob_path = "data_blob_18a0244177d65c6ec25a329228a486e2a722ecd5e78fb532a6d0a3c6f74eeca5/executions/bbcc1f4c9a384f0aad5a27424c56cb2c"

# Get the blob data
blob_data = get_blob(app_id, blob_path)

# Save it to a file
with open("generated_image.png", "wb") as f:
    f.write(blob_data)

'''
import requests

reid = "data_WebGL_3a9264aac0250aa89acdf55cb3d03e6f5a72858b836b319ab91d30490dbf1f44/resources"
url = f"https://f0b5f319156c4819b9827000b17e511a.node3.openfabric.network/resource?reid={reid}"

response = requests.get(url)

print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("Length:", len(response.content))

if response.ok and response.content:
    with open("model.glb", "wb") as f:
        f.write(response.content)
        print("Saved to model.glb ✅")
else:
    print("No content received or resource not found.")

