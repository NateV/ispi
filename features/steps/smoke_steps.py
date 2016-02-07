
@given(u'4 plus 4')
def step_impl(context):
    context.nums = {'a': 4, 'b':4}

@then(u'The answer is 8')
def step_impl(context):
    assert (context.nums['a'] + context.nums['a']) == 8
