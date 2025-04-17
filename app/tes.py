from core.stub import Stub
'''
File for debugging and extracting manifest and schema to structure right API calls with right params.

'''

text_to_image_app_id = "c25dcd829d134ea98f5ae4dd311d13bc.node3.openfabric.network"
image_to_3d_app_id = "f0b5f319156c4819b9827000b17e511a.node3.openfabric.network"

stub = Stub([text_to_image_app_id, image_to_3d_app_id])


manifest = stub.manifest(text_to_image_app_id)
print("Text-to-Image App Manifest:", manifest)

input_schema = stub.schema(text_to_image_app_id, "input")
print("Text-to-Image App Input Schema:", input_schema)

output_schema = stub.schema(text_to_image_app_id, "output")
print("Text-to-Image App Output Schema:", output_schema)

manifest_3d = stub.manifest(image_to_3d_app_id)
input_schema_3d = stub.schema(image_to_3d_app_id, "input")
output_schema_3d = stub.schema(image_to_3d_app_id, "output")
