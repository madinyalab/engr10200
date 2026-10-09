OK_FORMAT = True
test = {
  'name': 'q2_4',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> len(convenience_sample.columns)
          12
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> len(convenience_sample)
          44
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> bool((convenience_sample['Age'] < 22).all())
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
