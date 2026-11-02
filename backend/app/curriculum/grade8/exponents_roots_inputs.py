"""Original worked, independent and parallel Grade 8 roots tasks.

Each tuple names a visual situation and exact values. The task solver writes
the full distinct mathematical sequence for each instance.
"""
WORKED = {
 3: [('square_root',['36']),('cube_root',['64']),('square_root',['144']),
     ('cube_root',['216']),('root_pair',['81','125']),('square_root',['196']),
     ('cube_root',['512']),('root_pair',['144','216']),('square_area',['169']),
     ('cube_volume',['343']),('root_pair',['225','512']),('square_area',['256']),
     ('cube_volume',['729']),('root_pair',['324','1000']),('square_area',['361'])],
 4: [('mixed',['2','3','36','8']),('square_area',['64']),('cube_volume',['125']),
     ('mixed',['3','3','49','27']),('square_area',['121']),('cube_volume',['216']),
     ('mixed',['4','3','144','64']),('square_area',['196']),('cube_volume',['343']),
     ('mixed',['5','3','169','125']),('square_area',['256']),('cube_volume',['512']),
     ('mixed',['6','3','225','216']),('square_area',['324']),('mixed',['7','3','289','343'])]
}
PRACTICE = {
 3: [('square_root',['49']),('cube_root',['27']),('square_root',['121']),
     ('cube_root',['125']),('root_pair',['64','216']),('square_root',['225']),
     ('cube_root',['343']),('root_pair',['169','64']),('square_area',['144']),
     ('cube_volume',['512']),('root_pair',['196','343']),('square_area',['225']),
     ('cube_volume',['1000']),('root_pair',['361','729']),('square_area',['400'])],
 4: [('mixed',['2','4','49','27']),('square_area',['81']),('cube_volume',['8']),
     ('mixed',['3','4','64','8']),('square_area',['169']),('cube_volume',['27']),
     ('mixed',['4','4','121','125']),('square_area',['225']),('cube_volume',['64']),
     ('mixed',['5','3','196','216']),('square_area',['289']),('cube_volume',['729']),
     ('mixed',['6','3','256','343']),('square_area',['361']),('mixed',['7','3','324','512'])]
}
MASTERY = {
 3: [('root_pair',['100','343']),('square_root',['256']),('cube_volume',['216']),('square_area',['289']),('root_pair',['361','512'])],
 4: [('mixed',['4','3','196','125']),('square_area',['400']),('cube_volume',['1000']),('mixed',['5','4','225','216']),('mixed',['6','3','289','343'])]
}
REASSESS = {
 3: [('root_pair',['121','512']),('cube_volume',['64']),('square_area',['324'])],
 4: [('mixed',['3','4','225','64']),('root_pair',['256','729']),('square_area',['400'])]
}
