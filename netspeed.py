import speedtest
import json
import multiprocessing

def bytes_to_mb(bytes):
  MB = 1048576
  return int(bytes/MB)

def main(event, context):

  try:
    memory_limit_in_mb = context.memory_limit_in_mb
  except Exception:
    memory_limit_in_mb = '0'
    pass

  speed_test = speedtest.Speedtest()

  download_speed = bytes_to_mb(speed_test.download())
  #print("Download", download_speed, "MB")

  upload_speed = bytes_to_mb(speed_test.upload())
  #print("Upload", upload_speed, "MB")

  vcpu = multiprocessing.cpu_count()

  return {
    'statusCode': 200,
    "body": json.dumps({
            "memory_limit_in_mb": memory_limit_in_mb,
            "download" : str(download_speed),
            "upload" : str(upload_speed),
            "vcpu": str(vcpu),
    })
  }
if __name__ == '__main__':
    main("event","context")
