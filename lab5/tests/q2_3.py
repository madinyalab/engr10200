OK_FORMAT = True
test = {
  'name': 'q2_3',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> stats = compute_statistics(result)
          >>> plots.close('all')
          >>> len(stats)
          2
          >>> round(float(stats[0]), 2) == 26.54
          True
          >>> round(float(stats[1]), 2) == 4269775.77
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
