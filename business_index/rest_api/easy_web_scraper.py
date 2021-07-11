import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

WBSITE_URL = 'https://easy.co.il/'


def get_first_business_info(data):
    try:
        values = list(data.values())
    except Exception as e:
        print('Conversion of given data from dict to list failed.')
        print(e)
        raise ValueError(f'Expected a dictionary, received {type(data)}.')

    params = ''
    for i, val in enumerate(values[::-1]):
        words = str(val).split(' ')
        for j, w in enumerate(words):
            params += w
            if j < len(words) - 1:
                params += '%20'
        if i < len(values) - 1:
            params += '%20'

    request_url = WBSITE_URL + 'search/' + params

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(request_url)

    try:
        business = {}
        business['title'] = driver.find_elements_by_xpath('//div[@class="biz-inner"]//p[@class="biz-list-name"]')[0].text
        business['sub_title'] = driver.find_elements_by_xpath('//div[@class="biz-inner"]//p[@class="biz-list-class"]')[0].text
        business['grade'] = driver.find_elements_by_xpath('//div[@class="biz-inner"]//span[@class="biz-list-rating"]')[0].text
        address = driver.find_elements_by_xpath('//div[@class="biz-inner"]//p[@class="biz-list-address"]')[0].text
    except Exception as e:
        print('Getting text from html elements failed.')
        print(e)
        return None
    finally:
        driver.quit()

    hebrew_letters_set = 'אבגדהוזחטיכךלמםנןסעפףצץקרשת'
    pattern = re.compile(rf'([{hebrew_letters_set}\'\"\s]+)\s*(\d*),\s([{hebrew_letters_set}\'\"\s]+)')
    try:
        first_match = next(pattern.finditer(address))
    except Exception as e:
        print('Regular expression match not found.')
        print(e)
        return None
    else:
        business['street'] = first_match.group(1)
        business['number'] = first_match.group(2)
        business['city'] = first_match.group(3)

    return business
