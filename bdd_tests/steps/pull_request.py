from behave import *
from pytest import fixture

from API.PullRequest import PullRequestAPI


@given('we check count of active pull requests')
def all_user_pull_requests(context):
    context.pull = PullRequestAPI()
    context.count_of_pull_requests_before_test = len(context.pull.get_all_pull_requests())


@then('we create new pull requests')
def create_new_pull_request(context):
    context.new_pull_request = context.pull.create_pull_request()


@then('we check count of pull requests increased for {count}')
def check_count_of_current_pull_request(context, count):
    all_pull_requests = context.pull.get_all_pull_requests()
    get_created_pull_request = context.pull.get_single_pull_requests(context.new_pull_request)
    assert get_created_pull_request['title'] == context.new_pull_request['title']
    assert get_created_pull_request['number'] == context.new_pull_request['number']
    assert get_created_pull_request['body'] == context.new_pull_request['body']
    assert len(all_pull_requests) == context.count_of_pull_requests_before_test + int(count)


@then('we delete created pull request')
def delete_created_pull_requests(context):
    context.pull.update_pull_request(context.new_pull_request, 'closed')
