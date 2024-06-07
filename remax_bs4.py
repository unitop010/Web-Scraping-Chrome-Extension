from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from datetime import datetime
import requests, csv, os, json

def identify_url(url):
  if url == base_url:
    return url
  elif url.startswith(base_url) and 'searchQuery' in url:
    parsed_url = urlparse(url)
    query_string = parsed_url.query
    search_query_dict = json.loads(parse_qs(query_string)['searchQuery'][0])

    # Modify search_query_dict by removing unnecessary keys
    keys_to_remove = ['pageNumber', 'seed', 'count']
    for key in keys_to_remove:
      if key in search_query_dict:
        del search_query_dict[key]

    # Convert the modified searchQuery dict back to a JSON string
    modified_search_query = json.dumps(search_query_dict)
    modified_query_string = urlencode({'searchQuery': modified_search_query})
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, modified_query_string, parsed_url.fragment))
    return new_url
  else:
    return None

def gen_page_url(page_url_id):
  # Generate page urls
  parsed_url = urlparse(input_url)
  query_params = parse_qs(parsed_url.query)
  search_query_json = query_params.get('searchQuery', [''])[0]
  search_query_dict = json.loads(search_query_json)
  search_query_dict.update({"count": 192, "pageNumber": page_url_id})
  updated_search_query_json = json.dumps(search_query_dict)
  encoded_search_query = urlencode({'searchQuery': updated_search_query_json})
  return f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{encoded_search_query}'

def add_header():
  headers = ['Name', 'Phone Number', 'Email', 'Street', 'Address', 'Postal Code']
  
  # Read the existing content
  with open(f'{output_directory}/{output_file_name}', 'r', encoding='utf-8-sig') as csv_file:
    existing_content = csv_file.readlines()
  
  # Write the header followed by the existing content
  with open(f'{output_directory}/{output_file_name}', 'w', newline='', encoding='utf-8-sig') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(headers)  # Writing the header
    csv_file.writelines(existing_content)

def remove_duplications():
  # Remove duplicated rows
  df = pd.read_csv(f'{output_directory}/{output_file_name}')
  os.remove(f'{output_directory}/{output_file_name}')
  df_unique = df.drop_duplicates()
  df_unique.to_csv(f'{output_directory}/{output_file_name}', index=False, encoding='utf-8-sig')

def main():
  # Detect page number
  modified_url = gen_page_url(1)
  response = requests.get(modified_url)
  soup = BeautifulSoup(response.content, 'html.parser')
  try:
    page_num = int(soup.find_all('button', class_='d-pagination-page-button')[-2].text)
  except:
    page_num = 1
  # print(f'This URL has {page_num} pages')

  for page_id in range(1, page_num + 1):
    # print(f'--- {page_id} page ---')
    progress_rate = int(100 * page_id / page_num)
    print(f'{progress_rate}% waiting...')

    # Parse URL of each page
    page_url = gen_page_url(page_id)
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'html.parser') 
    script_tag = page_soup.find('script', type='application/ld+json')

    # Extract the JSON from inside the <script> tag
    json_text = script_tag.string if script_tag else ''
    agents_data = json.loads(json_text)

    # Iterate over the JSON objects (representing real estate agents)
    for agent in agents_data:
      name = agent.get('name')
      telephone = agent.get('telephone')
      email = agent.get('email')
      
      # Address fields
      address = agent.get('address', {})
      address_locality = address.get('addressLocality')
      address_region = address.get('addressRegion')
      postal_code = address.get('postalCode')
      street_address = address.get('streetAddress')
      
      # Print and save the scraped data
      output = [name, telephone, email, street_address, f'{address_locality}, {address_region}', postal_code]
      open_out = open(f'{output_directory}/{output_file_name}','a',newline="", encoding='utf-8-sig')
      file_o_csv = csv.writer(open_out, delimiter=',')
      file_o_csv.writerow(output)
      open_out.close()
  add_header()
  # remove_duplications()
  print(f'The result saved as "{output_file_name}" in "{output_directory}" folder.')

if __name__ == "__main__":
  input_url = input("Please enter your URL: ")

  # Identify valid url
  base_url = 'https://www.remax.com/real-estate-agents'
  input_url = identify_url(input_url)
  if input_url == None:
    while True:
      input_url = input('Please enter valid URL again: ')
      input_url = identify_url(input_url)
      if input_url is not None:
        break
  
  output_file_name = f'output_{datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.csv'
  output_directory = 'output'
  if not os.path.exists(output_directory):
    os.makedirs(output_directory)

  main()