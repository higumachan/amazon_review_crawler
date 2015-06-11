#coding: utf-8
import sys
from page import Page, RootPage
from pyscalambda import _, SF
from toolz.functoolz import pipe, curry
from toolz.curried import map, filter


def save_reviews(product_id, tag, reviews):
    f = open("{}.{}.csv".format(product_id, tag), "w")
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

def get_reviews(x):
    return pipe(x, 
        _.find_elements_by_class_name("reviewText"),
        map(lambda x: x.text)
    )

def go_review_page(rank):
    return lambda x: pipe(x,
        find_review_anchers,
        _[rank],
        _.click(),
    )

def next_page(page):
    try:
        return next(page.execute_page_transition_yield(
            _.find_element_by_class_name("CMpaginate"),
            _.find_elements_by_tag_name("a"),
            filter(lambda x: u"次" in x.text),
            list,
        )(_.click()))
    except StopIteration:
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

def main(product_id):

    url = "http://www.amazon.co.jp/gp/product/{}/".format(product_id)

    with RootPage(url) as top:
        print top.execute(
            find_review_anchers,
        )
        print "positive(star 5)"
        positive_review = fetch_reviews(top, 0)
        save_reviews(product_id, "p", positive_review)

        print "even (star 3)"
        even_reviews = fetch_reviews(top, 2)
        save_reviews(product_id, "e", even_reviews)

        print "negative(star 1)"
        even_reviews = fetch_reviews(top, 4)
        save_reviews(product_id, "n", even_reviews)

        
if __name__ == '__main__':
    sys.argv.append("4167732017")
    url = sys.argv[1]
    main(url)
