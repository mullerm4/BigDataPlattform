import time
from fetching_data.mysimbdpfetchdata import Fetching

from clientbatchingestapp_1 import Clientbatching as cl1
from clientbatchingestapp_2 import Clientbatching as cl2


if __name__ == "__main__":

    # pre load files for user 1
    f1 = Fetching("./client_input_directory", "profile_1.json")
    f2 = Fetching("./client_input_directory", "profile_2.json")

    ingested_files_1 = []
    ingested_files_2 = []

    last_insert = time.time()
    while KeyboardInterrupt:

        files = [file for file in f1.fetchFiles() if file not in ingested_files_1]
        while files:
            file = files.pop(-1)
            # Loading client batching ingest for profile 1
            cl1.ingest( user="new_user_1", pw="new_user_1", log_path='log_profile_1', file=file)
            # update staged file list
            ingested_files_1.append(file)
            files = [file for file in f1.fetchFiles() if file not in ingested_files_1]
            last_insert = time.time()
        # pre load files for user 2
        files2 = [file for file in f2.fetchFiles() if file not in ingested_files_2]

        while files2:
            file = files2.pop(-1)
            # Loading client batching ingest for profile 2

            cl2.ingest(user="new_user_2", pw="new_user_2", log_path='./log_profile_2', filename=file)
            # update staged file list
            ingested_files_2.append(file)
            files2 = [file for file in f2.fetchFiles() if file not in ingested_files_2]
            last_insert = time.time()
        if time.time()-last_insert > 3  and not files2 and not files:
            last_insert = time.time()
            print("Files of directory ingested, listening for new input.")
    print("Ingested files for profile_2")
    print(ingested_files_1)

    print("Ingested files for profile_2")
    print(ingested_files_2)
