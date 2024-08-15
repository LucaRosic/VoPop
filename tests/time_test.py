import time
import subprocess

def test_time():
    start_time =time.time()

    try:
        result = subprocess.run(['python3', 'scrapper.py'], capture_output= True, text= True)

        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

        assert execution_time < 35, "Script took too long to run"

    except:
        print("Script was longer than 35 seconds and was terminated")
        assert False, "Test failed due to timeout"

if __name__ == "__main__":
    test_time()