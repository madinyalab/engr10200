OK_FORMAT = True
test = {
  'name': 'q2_2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> old = result.assign(Age=result['Age'] * 3)
          >>> bins = histograms(old)
          >>> plots.close('all')
          >>> bool(np.max(bins) > np.max(old['Age']))
          True
          >>> bool(np.min(bins) == np.min(old['Age']))
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
