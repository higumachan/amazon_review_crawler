from toolz.functoolz import pipe
from selenium import webdriver

class Page(object):
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Firefox()

    def __enter__(self):
        self.driver.get(self.url)
        return self

    def __exit__(self, type, value, traceback):
        self.driver.back()
        self.driver.current_url

    def execute(self, *args):
        return pipe(self.driver, *args)

    def execute_page_transition(self, *args):
        pipe(self.driver, *args)
        return LinkedPage(self.driver)

    def execute_page_transition_yield(self, *args):
        print "test"
        def execute_page_transition_yield_detail(yield_fn):
            for t in pipe(self.driver, *args):
                print "test"
                yield_fn(t)
                yield LinkedPage(self.driver)
        return execute_page_transition_yield_detail



class RootPage(Page):

    def __exit__(self, type, value, traceback):
        self.driver.close()



class LinkedPage(Page):
    def __init__(self, driver):
        self.driver = driver
        
    def __enter__(self):
        return self
    
