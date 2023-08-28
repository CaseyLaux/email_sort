import subprocess
import threading
import time
import argparse
 
 
def autoformat(unformatted_data):
    
    
    command = f'openai tools fine_tunes.prepare_data -f {unformatted_data}'
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def feed_input(process):
        while True:
            time.sleep(1)  # Replace '1' with the number of seconds to wait between sending 'y's
            if process.poll() is not None:
                break  # The process has ended; stop sending 'y'
            process.stdin.write(b'y\n')
            process.stdin.flush()

    def read_output(process):
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break  # The process has ended; stop reading
            if output:
                try:
                    print(output.decode().strip())  # Or do whatever you need to do with the output
                except UnicodeDecodeError:
                    break
    # Start the threads
    input_thread = threading.Thread(target=feed_input, args=(process,))
    output_thread = threading.Thread(target=read_output, args=(process,))
    input_thread.start()
    output_thread.start()

    # Wait for the threads to finish
    input_thread.join()
    output_thread.join()

    # Wait for the process to finish
    process.communicate()
