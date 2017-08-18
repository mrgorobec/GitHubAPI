import pytest
import time
from pytest import fixture

from API.PullRequest import PullRequestAPI
from exception.exceptions import ResourceNotFound, ExpectedStatusCodeError


@fixture
def list_of_active_pull_request():
    pull = PullRequestAPI()
    response = pull.get_all_pull_requests()
    return response


def test_create_pull_request(list_of_active_pull_request):
    pull = PullRequestAPI()
    count_of_pull_requests_before_test = len(list_of_active_pull_request)
    new_pull_request = pull.create_pull_request()
    all_pull_requests = pull.get_all_pull_requests()
    get_created_pull_request = pull.get_single_pull_requests(new_pull_request)
    assert get_created_pull_request['title'] == new_pull_request['title']
    assert get_created_pull_request['number'] == new_pull_request['number']
    assert get_created_pull_request['body'] == new_pull_request['body']
    assert len(all_pull_requests) == count_of_pull_requests_before_test + 1
    """
    delete created pull request
    """
    pull.update_pull_request(new_pull_request, 'closed')


def test_try_approve_closed_pull_request():
    pull = PullRequestAPI()
    new_pull_request = pull.create_pull_request()
    pull.update_pull_request(new_pull_request, 'closed')
    try:
        is_failed = False
        pull.merge_pull_request(new_pull_request)
    except ResourceNotFound:
        is_failed = True
    assert is_failed


def test_try_merge_not_exist_branch():
    pull = PullRequestAPI()
    try:
        is_failed = False
        pull.create_pull_request('not exist')
    except ExpectedStatusCodeError:
        is_failed = True
    assert is_failed


def test_try_cancel_not_exist_pull_request():
    pull = PullRequestAPI()
    try:
        is_failed = False
        pull.update_pull_request({'number': '999999999'}, 'closed')
    except ExpectedStatusCodeError:
        is_failed = True
    assert is_failed


def test_count_of_pull_requests(list_of_active_pull_request):
    pull = PullRequestAPI()
    count_of_pull_requests_before_test = len(list_of_active_pull_request)
    new_pull_request = pull.create_pull_request()
    pull.update_pull_request(new_pull_request, 'closed')
    count_of_pr_after_closing = pull.get_all_pull_requests()
    assert len(count_of_pr_after_closing) == count_of_pull_requests_before_test


def test_PR_with_conflicts():
    pull = PullRequestAPI()
    new_pull_request = pull.create_pull_request('conflict')
    get_created_pull_request = pull.get_single_pull_requests(new_pull_request)
    while get_created_pull_request['mergeable'] is None:
        time.sleep(2)
        get_created_pull_request = pull.get_single_pull_requests(new_pull_request)
    """
    delete created pull request
    """
    pull.update_pull_request(new_pull_request, 'closed')
    assert get_created_pull_request['mergeable'] == False


def test_PR_without_conflicts():
    pull = PullRequestAPI()
    new_pull_request = pull.create_pull_request('positive')
    get_created_pull_request = pull.get_single_pull_requests(new_pull_request)
    while get_created_pull_request['mergeable'] is None:
        time.sleep(2)
        get_created_pull_request = pull.get_single_pull_requests(new_pull_request)
    """
    delete created pull request
    """
    pull.update_pull_request(new_pull_request, 'closed')
    assert get_created_pull_request['mergeable'] == True
