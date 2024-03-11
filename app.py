from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)



@app.route('/hotels', methods=['GET'])
def scrape_data():  # put application's code here
    place = request.args.get('place')

    if not place:
        return jsonify({'error': 'Please provide a place parameter'})

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }
    # for hotel reservation
    url_booking_hotel = f"https://www.booking.com/searchresults.en-gb.html?ss={place}"

    response = requests.get(url_booking_hotel, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    # titles = [item.text for item in soup.find_all(attrs={"data-testid": "title"})]
    hotel_links = [item['href'] for item in soup.find_all('a', attrs={"data-testid": "title-link"})]
    hotel_names = [item.text for item in soup.find_all('div', attrs={'data-testid': "title"})]
    hotel_descriptions = [item.text for item in soup.find_all('div', attrs={'class': 'abf093bdfe'}) if len(item.text) > 50]
    hotel_images = [item['src'] for item in soup.find_all('img', attrs={'data-testid': "image"})]

    hotels_data = [{'name': name, 'link': link, 'desc': desc, 'image_link': img_link} for name, link, desc, img_link in zip(hotel_names, hotel_links, hotel_descriptions, hotel_images)]

    return jsonify({'response': hotels_data})


@app.route('/things_to_do', methods=['GET'])
def open_street_map():
    place = request.args.get('place')

    if not place:
        return jsonify({'error': 'Please provide a place parameter'})

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    url = f"https://www.klook.com/en-PH/search/result/?query={place}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')


    # print(response.content)
    return jsonify({'url': url})


if __name__ == '__main__':
    app.run()
