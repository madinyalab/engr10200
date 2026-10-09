OK_FORMAT = True
test = {
  'name': 'q3_1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Make sure your probability is expressed as a decimal value
          >>> bool(np.isclose(pizza_prob, 0.7))
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
