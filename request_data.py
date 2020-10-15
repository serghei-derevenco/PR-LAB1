import requests
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

def get_token():
    response = requests.get('http://localhost:5000/register')
    access_token = response.json()['access_token']
    return access_token

def make_request(path):
    link = 'http://localhost:5000' + path
    response = requests.get(link, headers={'X-Access-Token': get_token()}).json()
    return response

def get_data():
    links = make_request('/home')['link']
    executor = ThreadPoolExecutor(max_workers=6)
    queue = [executor.submit(make_request, links[key]) for key in links]
    
    results = []

    while queue:
        done, queue = wait(queue, return_when=FIRST_COMPLETED)
        for future in done:
            result = future.result()
            results.append(result)
            if 'link' in result and 'msg' not in result:
                links = result['link']
                for key in links:
                    queue.add(executor.submit(make_request, links[key]))

    return results