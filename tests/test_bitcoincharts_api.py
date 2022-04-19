from bitcoincharts_api import upload_to_s3

def test_upload_to_s3():
    upload_to_s3("small.txt")
    # assert file found in s3