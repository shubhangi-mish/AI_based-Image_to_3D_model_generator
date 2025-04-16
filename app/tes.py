from core.stub import Stub

# Initialize the stub with your app IDs
text_to_image_app_id = "c25dcd829d134ea98f5ae4dd311d13bc.node3.openfabric.network"
image_to_3d_app_id = "f0b5f319156c4819b9827000b17e511a.node3.openfabric.network"
   # From your logs

stub = Stub([text_to_image_app_id, image_to_3d_app_id])

# Get manifest for the text-to-image app
manifest = stub.manifest(text_to_image_app_id)
print("Text-to-Image App Manifest:", manifest)

# Get input schema for the text-to-image app
input_schema = stub.schema(text_to_image_app_id, "input")
print("Text-to-Image App Input Schema:", input_schema)

# Get output schema for the text-to-image app
output_schema = stub.schema(text_to_image_app_id, "output")
print("Text-to-Image App Output Schema:", output_schema)

# Do the same for the image-to-3D app
manifest_3d = stub.manifest(image_to_3d_app_id)
input_schema_3d = stub.schema(image_to_3d_app_id, "input")
output_schema_3d = stub.schema(image_to_3d_app_id, "output")
