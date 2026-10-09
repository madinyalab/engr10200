OK_FORMAT = True
test = {
  'name': 'q1_3',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> len(observations)
          7
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> bool(abs(5.77 - np.std([simulate_observations() for _ in range(5000)])) < .2)
          True
          >>> bool(abs(21.5 - np.mean([simulate_observations() for _ in range(5000)])) < .2)
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
