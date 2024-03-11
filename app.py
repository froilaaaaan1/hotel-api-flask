from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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
    hotel_links = [item['href'] for item in soup.find_all('a', attrs={"data-testid": "title-link"})]
    hotel_names = [item.text for item in soup.find_all('div', attrs={'data-testid': "title"})]
    hotel_descriptions = [item.text for item in soup.find_all('div', attrs={'class': 'abf093bdfe'}) if
                          len(item.text) > 50]
    hotel_images = [item['src'] for item in soup.find_all('img', attrs={'data-testid': "image"})]

    hotels_data = [{'name': name, 'link': link, 'desc': desc, 'image_link': img_link} for name, link, desc, img_link in
                   zip(hotel_names, hotel_links, hotel_descriptions, hotel_images)]

    return hotels_data


@app.route('/things_to_do', methods=['GET'])
def open_street_map():
    place = request.args.get('place')

    if not place:
        return jsonify({'error': 'Please provide a place parameter'})
    where_to_url = f"https://guidetothephilippines.ph/search?q={place}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(where_to_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    anchor_titles = [item.text.strip() for item in soup.find_all('a', attrs={"class": "title"})]
    excerpts = [item.text.strip() for item in soup.find_all('p', attrs={"class": "excerpt"})]
    tags = [item.text for item in soup.find_all('a', attrs={"class": "cat search-cat-tour"})]
    tag_links = [f"https://guidetothephilippines.ph{item['href']}" for item in soup.find_all('a', attrs={"class": "search-cat-tour"})]
    link_to_articles = [f"https://guidetothephilippines.ph{item['href']}" for item in soup.find_all('a', attrs={"class": "image"})]
    image_links = [item['src'] for item in soup.find_all('img', attrs={"width": "150"})]

    items_data = [{
        'title': title,
        'excerpt': excerpt,
        'tags': tag,
        'tag_link': tag_link,
        'link_to_article': article_link,
        'image_link': img_link
    } for title, excerpt, tag, tag_link, article_link, img_link in zip(anchor_titles, excerpts, tags, tag_links, link_to_articles, image_links)]

    return jsonify({'items': items_data})


if __name__ == '__main__':
    app.run()
