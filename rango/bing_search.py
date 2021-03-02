import requests
import json

# Add your Microsoft Account Key to a file called bing.key
def read_bing_key():
    bing_api_key = None
    try:
        with open('bing.key','r') as f:
            bing_api_key = f.readline().strip()
    except:
        try:
            with open('../bing.key') as f:
                bing_api_key = f.readline().strip()
        except:
            raise IOError('bing.key file not found')
    
    if not bing_api_key:
        raise KeyError('Bing key not found')

    return bing_api_key

def run_query(search_terms):

    bing_key = read_bing_key()
    search_url = 'https://www.googleapis.com/customsearch/v1'
    #cx: '017576662512468239146:omuauf_lfve'
    # headers = {'key=': bing_key}
    params  = {'key': bing_key,'q': search_terms, 'cx': '9b8b6124271603a05'}
    
    # Issue the request, given the details above.
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()

    # With the response now in play, build up a Python list.
    results = []
    for result in search_results['items']:
        results.append({
            'title': result['title'],
            'link': result['link'],
            'summary': result['snippet']})
    return results


# response1 = run_query("python")
# print(response1)