from openfabric_pysdk.starter import Starter

if __name__ == '__main__':
    PORT = 8888
    Starter.ignite(debug=False, host="0.0.0.0", port=PORT),


