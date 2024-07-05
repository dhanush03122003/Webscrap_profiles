from django.shortcuts import render
from webscrap_app.models import Code_chef_det, leet_code_det
import requests
from urllib.parse import urlparse
from webscrap_app.Get_Current_Date import get_current_date, calculate_days_difference
import re

def get_user_info_1(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None

    html_content = response.text
    pattern = r'<div class="content">(.*?)</div>\s*</div>'
    match = re.search(pattern, html_content, re.DOTALL)
    username = url.split('/')[-1]
    if not match:
        return None

    content_div = match.group(0)
    html_string = content_div

    def extract_pattern(pattern, html_string):
        match = re.search(pattern, html_string)
        return int(match.group(1)) if match else None

    rating_number = extract_pattern(r'<div class="rating-number">(\d+)</div>', html_string)
    div_number = extract_pattern(r'<div>\(Div (\d+)\)</div>', html_string)
    highest_rating = extract_pattern(r'\(Highest Rating (\d+)\)', html_string)
    global_rank = extract_pattern(r'<a href="/ratings/all"><strong>(\d+)</strong></a>\s*Global Rank', html_string)

    start_tag = html_string.find('<a href="/ratings/all?filterBy=Country%3DIndia"><strong>') + len('<a href="/ratings/all?filterBy=Country%3DIndia"><strong>')
    end_tag = html_string.find('</strong>', start_tag)
    country_rank_str = html_string[start_tag:end_tag]
    country_rank = int(country_rank_str) if country_rank_str.isdigit() else None

    star = (
        1 if rating_number <= 1399 else
        2 if rating_number <= 1599 else
        3 if rating_number <= 1799 else
        4 if rating_number <= 1999 else
        5 if rating_number <= 2199 else
        6 if rating_number <= 2499 else
        7
    ) if rating_number else None

    return {
        'url': url,
        'Division': div_number,
        'Username': username,
        'rating': rating_number,
        'star': star,
        'H_Rating': highest_rating,
        'global_rank': global_rank,
        'country_rank': country_rank
    }

def get_leet_code_user_logo(username):
    url = f"https://alfa-leetcode-api.onrender.com/{username}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('avatar', " ")
    except:
        pass
    return " "

def get_user_info_2(url):
    result = {}
    parsed_url = urlparse(url)
    username = parsed_url.path.split('/')[-1]
    result['url'] = url
    result['Username'] = username

    api_url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            result.update({
                'rank': data.get('ranking'),
                'prob_sol': data.get('totalSolved'),
                'easy': data.get('easySolved'),
                'medium': data.get('mediumSolved'),
                'hard': data.get('hardSolved')
            })
            return result
    except Exception as e:
        print(e)
    return None

def handle_codechef_request(url, o1):
    data = get_user_info_1(url)
    if not data:
        return None

    username = data['Username']
    current_date = get_current_date()
    if username in [obj.Username for obj in o1]:
        existing_record = Code_chef_det.objects.get(Username=username)
        diff = int(calculate_days_difference(existing_record.date, current_date))
        existing_record.delete()
        data['days'] = diff
    else:
        data['days'] = 0

    Code_chef_det.objects.create(**data)
    return data

def handle_leetcode_request(url, o2):
    data = get_user_info_2(url)
    if not data:
        return None

    username = data['Username']
    data['logo'] = get_leet_code_user_logo(username)
    current_date = get_current_date()
    if username in [obj.Username for obj in o2]:
        existing_record = leet_code_det.objects.get(Username=username)
        diff = int(calculate_days_difference(existing_record.date, current_date))
        existing_record.delete()
        data['days'] = diff
    else:
        data['days'] = 0

    leet_code_det.objects.create(**data)
    return data

def get_code_chef_det(request):
    # input("111")
    update_records()
    # input('222')
    o1 = Code_chef_det.objects.all()
    o2 = leet_code_det.objects.all()
    if request.method == "POST":
        try : 
            response = requests.get(request.POST['link'])
            print( response.status_code )
            if response.status_code != 200:
                return render(request, 'web_scrap_code_chef.html', {'o1': o1, 'o2': o2, 'error': 1})
        except:
            return render(request, 'web_scrap_code_chef.html', {'o1': o1, 'o2': o2, 'error': 1})
        url = request.POST['link'].rstrip('/')
        parsed_url = urlparse(url)
        username = parsed_url.path.split('/')[-1]
      
        
        if not username or ("leetcode.com" not in url and "codechef.com" not in url):
            return render(request, 'web_scrap_code_chef.html', {'o1': o1, 'o2': o2, 'error': 1})
        
        if request.POST['type'] == 'code_chef' and "codechef.com" in url:
            data = handle_codechef_request(url, o1)
        elif request.POST['type'] == 'leet_code' and "leetcode.com" in url:
            data = handle_leetcode_request(url, o2)
        else:
            data = None

        if not data:
            return render(request, 'web_scrap_code_chef.html', {'o1': o1, 'o2': o2, 'error': 1})

    o1 = Code_chef_det.objects.all()
    o2 = leet_code_det.objects.all()
    return render(request, 'web_scrap_code_chef.html', {'o1': o1, 'o2': o2})

def update_record(record, is_codechef=True):
    if is_codechef:
        url = f"https://www.codechef.com/users/{record.Username}"
        handle_codechef_request(url, [record])
    else:
        url = f"https://leetcode.com/{record.Username}"
        handle_leetcode_request(url, [record])
import concurrent.futures

def update_records():
    codechef_records = Code_chef_det.objects.all()
    leetcode_records = leet_code_det.objects.all()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        codechef_futures = {executor.submit(update_record, record, True): record for record in codechef_records}
        leetcode_futures = {executor.submit(update_record, record, False): record for record in leetcode_records}

        for future in concurrent.futures.as_completed(codechef_futures):
            record = codechef_futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error updating CodeChef record for {record.Username}: {e}")

        for future in concurrent.futures.as_completed(leetcode_futures):
            record = leetcode_futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error updating LeetCode record for {record.Username}: {e}")
