OK_FORMAT = True
test = {
  'name': 'q1_1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> bool(12 <= modified_result <= 32)
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> bool(action_succeeded == (modified_result > 15))
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
