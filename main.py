#coding: utf-8
import sys
from page import Page, RootPage
from pyscalambda import _, SF
from toolz.functoolz import pipe, curry
from toolz.curried import map, filter


def save_reviews(product_id, tag, reviews):
    f = open("data/{}.{}.csv".format(product_id, tag), "w")
    for review in reviews:
        print review
        f.write("{},{}\n".format(
            tag, 
            pipe(
                review, 
                _.split("\n"),
                map(_.strip()),
                map(_.encode("utf-8")),
                SF(" ".join)(_)
            )
        ))
    f.close()

find_review_anchers = _\
    .find_element_by_id("histogramTable")\
    .find_elements_by_tag_name("a")

def or_pipe(x, *args, **kwargs):
    for arg in args:
        t = arg(x)
        if t:
            return t
    return kwargs.get("default", None)

def get_reviews(x):
    return pipe(x, 
        lambda x: or_pipe(x, 
            _.find_elements_by_class_name("reviewText"),
            _.find_elements_by_class_name("review-text"),
            default=[],
        ),
        map(lambda x: x.text)
    )

def go_review_page(rank):
    def test(x):
        print x.tag_name
        return x

    return lambda x: pipe(x,
        find_review_anchers,
        _[rank],
        test,
        _.click(),
    )

def next_page(page):
    try:
        return next(page.execute_page_transition_yield(
            lambda x: or_pipe(x,
                _.find_elements_by_class_name("CMpaginate"),
                _.find_elements_by_class_name("a-last"),
                default=[]
            ),
            _[0],
            _.find_elements_by_tag_name("a"),
            filter(lambda x: u"次" in x.text),
            list,
        )(_.click()))
    except Exception:
        return None

def fetch_reviews(page, rank):
    rp = page.execute_page_transition(
            go_review_page(rank)
    )
    return fetch_reviews_detail(rp)

def fetch_reviews_detail(page):
    if page == None:
        return []
    reviews = None
    with page as review_page:
        reviews = review_page.execute(
                get_reviews,
                list
        ) + fetch_reviews_detail(next_page(page))
    return reviews

def main(product_id, mode):

    url = "http://www.amazon.co.jp/gp/product/{}/".format(product_id)

    with RootPage("http://www.amazon.co.jp/product-reviews/{}/?filterBy=addFiveStar&".format(product_id)) as rp:
        reviews = fetch_reviews_detail(rp)
        save_reviews(product_id, "p", reviews)
    with RootPage("http://www.amazon.co.jp/product-reviews/{}/?filterBy=addThreeStar&".format(product_id)) as rp:
        reviews = fetch_reviews_detail(rp)
        save_reviews(product_id, "e", reviews)
    with RootPage("http://www.amazon.co.jp/product-reviews/{}/?filterBy=addOneStar&".format(product_id)) as rp:
        reviews = fetch_reviews_detail(rp)
        save_reviews(product_id, "n", reviews)

        
if __name__ == '__main__':
    sys.argv.append("4167732017")
    sys.argv.append("pen")
    url = sys.argv[1]
    mode = "pen"
    main(url, mode)
