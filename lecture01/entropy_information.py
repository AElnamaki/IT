import math
import os
import concurrent.futures
import logging
from typing import Dict, List
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init()

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def read_file_chunk(file_path: str, start: int, end: int) -> str:
    """Read a chunk of a file from start to end and convert it to a binary string."""
    logging.debug(f"Reading file chunk from {start} to {end}")
    with open(file_path, 'rb') as file:
        file.seek(start)
        chunk = file.read(end - start)
        # Convert the chunk of binary data to a binary string
        binary_string = ''.join(format(byte, '08b') for byte in chunk)
        logging.debug(f"Read chunk size: {len(chunk)} bytes, binary string length: {len(binary_string)} bits")
        return binary_string

def calculate_probabilities(binary_sequence: str) -> Dict[str, float]:
    """Calculate the probability of each symbol ('0' and '1') in the binary sequence."""
    total_length = len(binary_sequence)
    if total_length == 0:
        raise ValueError("Binary sequence length is 0, cannot calculate probabilities")
    
    logging.debug(f"Calculating probabilities for binary sequence of length {total_length}")
    probability = {
        '0': binary_sequence.count('0') / total_length,
        '1': binary_sequence.count('1') / total_length
    }
    logging.debug(f"Probabilities: {probability}")
    return probability

def information_content(binary_sequence: str) -> Dict[str, float]:
    """Calculate the information content for each symbol in the binary sequence."""
    probabilities = calculate_probabilities(binary_sequence)
    info_content = {}
    
    for symbol, prob in probabilities.items():
        if prob > 0:  # Avoid log(0) issue
            info_content[symbol] = -math.log2(prob)
        else:
            info_content[symbol] = 0.0
    
    logging.debug(f"Information content: {info_content}")
    return info_content

def shannon_entropy(binary_sequence: str) -> float:
    """Calculate the Shannon entropy of the binary sequence."""
    probabilities = calculate_probabilities(binary_sequence)
    entropy = 0.0
    
    for prob in probabilities.values():
        if prob > 0:  # Avoid log(0) issue
            entropy -= prob * math.log2(prob)
    
    logging.debug(f"Shannon entropy: {entropy}")
    return entropy

def analyze_file_parallel(file_path: str, chunk_size: int = 1024 * 1024) -> None:
    """Read a file, process it in parallel, and calculate Shannon entropy and information content."""
    file_size = os.path.getsize(file_path)
    num_chunks = (file_size + chunk_size - 1) // chunk_size
    
    logging.debug(f"File size: {file_size} bytes, Number of chunks: {num_chunks}")
    
    # List to store futures
    futures: List[concurrent.futures.Future] = []
    
    # Start parallel processing of file chunks
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for start in tqdm(range(0, file_size, chunk_size), total=num_chunks, desc=f"{Fore.GREEN}Processing File{Style.RESET_ALL}"):
            end = min(start + chunk_size, file_size)
            futures.append(executor.submit(read_file_chunk, file_path, start, end))
        
        # Collect results from futures
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    # Combine results
    combined_binary_string = ''.join(results)
    
    logging.debug(f"Combined binary string length: {len(combined_binary_string)} bits")
    
    # Calculate overall probabilities and information content
    combined_probabilities = calculate_probabilities(combined_binary_string)
    combined_info_content = information_content(combined_binary_string)
    combined_entropy = shannon_entropy(combined_binary_string)
    
    print(f"{Fore.CYAN}Binary sequence length: {len(combined_binary_string)} bits{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Information Content (bits): {combined_info_content}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Shannon Entropy (bits/symbol): {combined_entropy}{Style.RESET_ALL}")

# Example of running the parallel analysis
file_path = 'lecture01.pdf'  # Replace with your file path
analyze_file_parallel(file_path)
