from selenium import webdriver


def start(config):
    driver = webdriver.Chrome('./chromedriver.exe')


if __name__ == '__main__':
    start(None)
