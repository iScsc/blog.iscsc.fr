import pytest

import new_article

### DISCLAIMER:
# Whereas other extensions are allowed by HUGO: 
# "The extension can be .html, .json or any valid MIME type"
# We only accept Markdown articles and so only parse these
###


@pytest.fixture
def mock_requests_post(mocker):
    mock_post = mocker.MagicMock()
    fake_response = mocker.Mock()

    fake_response.status_code = 200
    mock_post.return_value = fake_response

    mocker.patch("requests.post", mock_post)
    mocker.patch("new_article.ARTICLE_FILE_BASE_PATH", "test_resources/")

    yield mock_post


def test_new_article_file(mock_requests_post):
    new_article.main(["test_resources/article_1.md"])
    
    mock_requests_post.assert_called_once_with(
        'http://iscsc.fr:8001/new-blog',
        json={
            'title': 'article title',
            'summary': 'article summary',
            'date': '2024-02-19 10:52:09+01:00',
            'lastUpdate': '2024-02-19 10:52:09+01:00',
            'tags': "['some', 'tags']",
            'author': 'ctmbl',
            'draft': False,
            'url': 'https://iscsc.fr/posts/article_1'
        }
    )


def test_new_article_file_upper_case(mock_requests_post):
    # Add an article with an Upper case --> URL should be lower case
    new_article.main(["test_resources/Article-2.md"])

    mock_requests_post.assert_called_once_with(
        'http://iscsc.fr:8001/new-blog',
        json={
            'title': 'article title',
            'summary': 'article name contains an upper case letter',
            'date': '2024-05-05T12:00:00+02:00',
            'lastUpdate': '2024-05-05T12:00:00+02:00',
            'tags': "['some', 'tags']",
            'author': 'ctmbl',
            'draft': False,
            'url': 'https://iscsc.fr/posts/article-2'
        }
    )


def test_new_leaf_bundle_article(mock_requests_post):
    new_article.main(["test_resources/leaf_bundle/index.md"])

    mock_requests_post.assert_called_once_with(
        'http://iscsc.fr:8001/new-blog',
        json={
            'title': 'leaf bundle title',
            'summary': 'leaf bundle summary',
            'date': '2024-02-19 10:52:09+01:00',
            'lastUpdate': '2024-02-19 10:52:09+01:00',
            'tags': "['leaf', 'bundle']",
            'author': 'ctmbl',
            'draft': False,
            'url': 'https://iscsc.fr/posts/leaf_bundle'
        }
    )

def test_new_branch_bundle():
    # not yet implemented
    # https://gohugo.io/content-management/page-bundles/#branch-bundles
    pass

def test_headless_bundle():
    # not yet implemented
    # https://gohugo.io/content-management/page-bundles/#headless-bundle
    pass