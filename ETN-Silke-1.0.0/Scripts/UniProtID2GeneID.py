# This method is retrieved from: https://www.uniprot.org/help/id_mapping
import re
import time
import json
import zlib
from xml.etree import ElementTree
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.adapters import HTTPAdapter, Retry
import pickle5 as pickle
from itertools import chain
import sys

path = '/home/guest/VIB_Traineeship/HumanComplexes/onlyHumanComplexes_imex_nr.pickle'

# Extract list of genes to use
genes = []

# Load in the pickle file to use
onlyHumanComplexes = pickle.load(open(path,"rb"))
#print(len(onlyHumanComplexes))
#print(onlyHumanComplexes)

# Iterate over the onlyHumanComplexes dictionary and append the genes to a list
for key, value in onlyHumanComplexes.items():
	#print(key, value)
	genes.append(value)
# Convert the nested genes list into a single list
genes = list(chain.from_iterable(genes))
#print(genes)

# Filter out the isoforms from the gene ids
genes_noisoforms = []
for gene in genes:
	if '-' in gene:
		gene_noisoform = re.split("-",gene)[0]
		genes_noisoforms.append(gene_noisoform)
	else:
		genes_noisoforms.append(gene)
#print(genes_noisoforms)
#print(len(genes))
#print(len(genes_noisoforms))

# Split up the list of genes if the number of genes is too large to do the conversion all at once
genes1 = genes_noisoforms[0:80000]
genes2 = genes_noisoforms[80000:160000]
genes3 = genes_noisoforms[160000:223243]
# Some prints to check the split up lists
print(len(genes1))
print(len(genes2))
print(len(genes3))
print(len(genes1)+len(genes2)+len(genes3))


POLLING_INTERVAL = 3
API_URL = "https://rest.uniprot.org"

# Create Retry object with configuration of the retry behaviour for HTTP requests 
retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
# Create Session object from the requests library
session = requests.Session()
# Mount the Retry object to the Session object for handling the retry logic
session.mount("https://", HTTPAdapter(max_retries=retries))

# Check response status of HTTP request and handle HTTP errors
def check_response(response):
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print(response.json())
        raise

# Send a POST request to the ID mapping API endpoint, check response for errors and return the jobId from response JSON
def submit_id_mapping(from_db, to_db, ids):
    request = requests.post(
        f"{API_URL}/idmapping/run",
        data={"from": from_db, "to": to_db, "ids": ",".join(ids)},
    )
    check_response(request)
    return request.json()["jobId"]

# Extract the URL of the next page from response headers
def get_next_link(headers):
    re_next_link = re.compile(r'<(.+)>; rel="next"')
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

# Check if the id mapping results are ready
def check_id_mapping_results_ready(job_id):
    while True:
        request = session.get(f"{API_URL}/idmapping/status/{job_id}")
        check_response(request)
        j = request.json()
        if "jobStatus" in j:
            if j["jobStatus"] == "RUNNING":
                print(f"Retrying in {POLLING_INTERVAL}s")
                time.sleep(POLLING_INTERVAL)
            else:
                raise Exception(j["jobStatus"])
        else:
            return bool(j["results"] or j["failedIds"])

# Get batches of id mapping results
def get_batch(batch_response, file_format, compressed):
    batch_url = get_next_link(batch_response.headers)
    while batch_url:
        batch_response = session.get(batch_url)
        batch_response.raise_for_status()
        yield decode_results(batch_response, file_format, compressed)
        batch_url = get_next_link(batch_response.headers)

# Combine batches of id mapping results into on result set
def combine_batches(all_results, batch_results, file_format):
    if file_format == "json":
        for key in ("results", "failedIds"):
            if key in batch_results and batch_results[key]:
                all_results[key] += batch_results[key]
    elif file_format == "tsv":
        return all_results + batch_results[1:]
    else:
        return all_results + batch_results
    return all_results

# Get the link to the id mapping results
def get_id_mapping_results_link(job_id):
    url = f"{API_URL}/idmapping/details/{job_id}"
    request = session.get(url)
    check_response(request)
    return request.json()["redirectURL"]

# Decode the results based on file format and decompress the response content
def decode_results(response, file_format, compressed):
    if compressed:
        decompressed = zlib.decompress(response.content, 16 + zlib.MAX_WBITS)
        if file_format == "json":
            j = json.loads(decompressed.decode("utf-8"))
            return j
        elif file_format == "tsv":
            return [line for line in decompressed.decode("utf-8").split("\n") if line]
        elif file_format == "xlsx":
            return [decompressed]
        elif file_format == "xml":
            return [decompressed.decode("utf-8")]
        else:
            return decompressed.decode("utf-8")
    elif file_format == "json":
        return response.json()
    elif file_format == "tsv":
        return [line for line in response.text.split("\n") if line]
    elif file_format == "xlsx":
        return [response.content]
    elif file_format == "xml":
        return [response.text]
    return response.text

# Get the xml namespace from an elements tag
def get_xml_namespace(element):
    m = re.match(r"\{(.*)\}", element.tag)
    return m.groups()[0] if m else ""

# Merge xml results into one xml result
def merge_xml_results(xml_results):
    merged_root = ElementTree.fromstring(xml_results[0])
    for result in xml_results[1:]:
        root = ElementTree.fromstring(result)
        for child in root.findall("{http://uniprot.org/uniprot}entry"):
            merged_root.insert(-1, child)
    ElementTree.register_namespace("", get_xml_namespace(merged_root[0]))
    return ElementTree.tostring(merged_root, encoding="utf-8", xml_declaration=True)

# Print the progress of fetching the batches
def print_progress_batches(batch_index, size, total):
    n_fetched = min((batch_index + 1) * size, total)
    print(f"Fetched: {n_fetched} / {total}")

# Get the results of the id mapping search
def get_id_mapping_results_search(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    file_format = query["format"][0] if "format" in query else "json"
    if "size" in query:
        size = int(query["size"][0])
    else:
        size = 500
        query["size"] = size
    compressed = (
        query["compressed"][0].lower() == "true" if "compressed" in query else False
    )
    parsed = parsed._replace(query=urlencode(query, doseq=True))
    url = parsed.geturl()
    request = session.get(url)
    check_response(request)
    results = decode_results(request, file_format, compressed)
    total = int(request.headers["x-total-results"])
    print_progress_batches(0, size, total)
    for i, batch in enumerate(get_batch(request, file_format, compressed), 1):
        results = combine_batches(results, batch, file_format)
        print_progress_batches(i, size, total)
    if file_format == "xml":
        return merge_xml_results(results)
    return results

# Get the streamed results of an id mapping search 
def get_id_mapping_results_stream(url):
    if "/stream/" not in url:
        url = url.replace("/results/", "/results/stream/")
    request = session.get(url)
    check_response(request)
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    file_format = query["format"][0] if "format" in query else "json"
    compressed = (
        query["compressed"][0].lower() == "true" if "compressed" in query else False
    )
    return decode_results(request, file_format, compressed)

# Provide a job id to the UniProt API
job_id = submit_id_mapping(
    from_db="UniProtKB_AC-ID", to_db="GeneID", ids=genes_noisoforms)
# Check the status of the submitted job. If status is ready then get the results
if check_id_mapping_results_ready(job_id):
	link = get_id_mapping_results_link(job_id)
	results = get_id_mapping_results_search(link)

# Print the sucessful and failed results of the conversion
print(results)
# {'results': [{'from': 'P05067', 'to': 'CHEMBL2487'}], 'failedIds': ['P12345']}

# Write the results to a pickle file
with open('UniProtKB2GeneID_intact_no-isoforms.pickle', 'wb') as output:
	pickle.dump(results, output, pickle.HIGHEST_PROTOCOL)

# Uncomment line 227-237 if the file with gene ids to start with does exceed 100.000 items.
# For these files with more genes, the analysis should be run multiple times and the results should be concatenated (ConcatenatePickle.py)
'''
job_id = submit_id_mapping(
    from_db="UniProtKB_AC-ID", to_db="GeneID", ids=genes3)
if check_id_mapping_results_ready(job_id):
	link = get_id_mapping_results_link(job_id)
	results = get_id_mapping_results_search(link)

print(results)
# {'results': [{'from': 'Q96C28', 'to': '286075'}], 'failedIds': ['P80748']}

with open('UniProtKB2GeneID_imex3.pickle', 'wb') as output:
	pickle.dump(results, output, pickle.HIGHEST_PROTOCOL)
'''