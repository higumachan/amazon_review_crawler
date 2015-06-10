import sys
from page import Page, RootPage
from pyscalambda import _, SF
from toolz.functoolz import pipe
from toolz.curried import map


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


def fetch_reviews(page, rank):
    reviews = None
    with page.execute_page_transition(
        go_review_page(rank)
    ) as review_page:
        reviews = list(review_page.execute(
                get_reviews
        ))
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
