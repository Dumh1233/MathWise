import requests

API_KEY = 'wx9gx3dpqb8f82arx'


def get_image_enhancer(image_path):
    response = requests.request(
        "POST",
        "https://techhk.aoscdn.com/api/tasks/visual/scale",
        headers={'X-API-KEY': API_KEY},
        data={'sync': '1', 'type': 'face'},
        files={
            'image_file': open(image_path, 'rb')
        })
    return eval(response.text)


def image_enhancer(image_path):
    enhancerment = get_image_enhancer(image_path)
    image_url = enhancerment["data"]["image"]
    response = requests.get(image_url)
    open(image_path, "wb").write(response.content)
