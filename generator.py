import pandas as pd
import numpy as np

# --------------------------------------------------------------------------------------------- #
# ----------------------------------------- functions ----------------------------------------- #

def print_Ntalk(tmp):
    print('_'*19)
    for c1, c2 in tmp:
        print("| %11s | %d |" % (c1, c2))
    print('='*19)

def find_candi(candi1, people_list):
    coll = collabrate_table[candi1][people_list].values
    min_coll = np.min(coll)
    min_coll_people = people_list[np.where(coll==min_coll)]
    # if(candi1 in group1):
    #     mask = ~np.in1d(min_coll_people, group1)    
    candi2 = np.random.choice(min_coll_people)
    collabrate_table[candi1][candi2] += 1
    collabrate_table[candi2][candi1] += 1
    # print(collabrate_table)
    return candi2
    
# --------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------- #    
    
np.random.seed(42)

group1 = ["Chi Ngam", "Weizhen", "Qishan", "Dylan"]
group2 = ["Wangzheng", "Zhuochao", "Rui", "Rongzi", "Ivan"]
group3 = ["Ken Hui", "Cheung Ling"]

last_schedule = np.array([['Weizhen'    , 'Wangzheng'],
                          ['Hugo'       , 'Anderson' ],
                          ['Zhuochao'   , 'Chi Ngam' ],
                          ['Cheung Ling', 'Kenneth'  ],
                          ['Dylan'      , 'Ken Hui'  ],
                          ['Rongzi'     , 'Wangzheng'],  # joint JC
                          ['Qishan'     , 'Hugo'     ],
                          ['Weizhen'    , 'Ivan'     ],
                          ['Anderson'   , 'Rui'      ],
                          ['Jason'      , 'Yat To'   ],  # joint JC
                          ['Chi Ngam'   , 'Zhuochao' ],
                          ['Cheung Ling', 'Wangzheng'],
                          ['Xurun Huang', 'Postdoc'  ],
                          ['Dylan'      , 'Kenneth'  ],
                          ['Rongzi'     , 'Ken Hui'  ],
                          ['Anderson'   , 'Yat To'   ],
                          ['Rui'        , 'Ivan'     ],
                          ['Weizhen'    , 'Ania'     ],  # joint JC
                          ['Cheung Ling', 'Hugo'     ],
                          ['Rongzi'     , 'Kenneth'  ],
                          ['Chi Ngam'   , 'Zhuochao' ],
                          ['Ken Hui'    , 'solo'     ],
                          ['Wangzheng'  , 'Hemanta'  ],  # joint JC
                          ['Dylan'      , 'Hugo'     ],
                          ['Qishan'     , 'Ivan'     ],
                          ['Weizhen'    , 'Rui'      ],
                          ['Anderson'   , 'Yat To'   ],                          
                          ['Cheung Ling', 'Zhuochao' ],
                          ['Rongzi'     , 'Wangzheng']])

# --------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------- #

# last_schedule = np.append(last_schedule, [['Rongzi', 'Chi Ngam']], axis=0)
# last 3 weeks
last_weeks_list = np.array(['Ivan', 'Weizhen', 'Rui', 'Cheung Ling', 'Zhuochao', 'Rongzi', 'Wangzheng'])
print('last_weeks_list', last_weeks_list)
# create JC member list
people = np.array(group1 + group2 + group3)
people = np.delete(people, np.where(people=='Ken Hui'))
print(people)
# previous JC
last_schedule_tmp = np.hstack(last_schedule).flatten()
# Initialize JC times for each person
report_count = np.empty( len(people), 
                         dtype=np.dtype([('names', '<U20'),('Ntalk', np.int64)]) )
report_count['names'] = people
report_count['Ntalk'] = np.array([np.count_nonzero(last_schedule_tmp==person) for person in people])
# print(report_count['names'])
# print(report_count['Ntalk'])
print_Ntalk(report_count)

collabrate_table = pd.DataFrame( np.zeros((len(people),len(people)), dtype=np.int64), 
                                 index=people, columns=people )
for i in range(len(last_schedule)):
    n1, n2 = last_schedule[i]
    if((n1 in people) and (n2 in people)):
        collabrate_table[n1][n2] += 1
        collabrate_table[n2][n1] += 1     
print(collabrate_table)
        
# --------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------- #    
    
for i in range(10):
    print('-'*50)
    print('Week %d' % (i+1))
    mask = ~np.in1d(people, last_weeks_list)
    candidate_people = people[mask]
    print('last_weeks_list', last_weeks_list)
    print('candidate_people', candidate_people)
    report_count_tmp = report_count[mask]
    
    min_report_count = min(report_count_tmp['Ntalk'])
    min_report_people = np.array([p for p, count in report_count_tmp if count == min_report_count])
    # print(min_report_count, min_report_people, sep=' | ')
    
    # if(len(candidate_people)==1)
    candidate1 = np.random.choice(min_report_people)
    min_report_people = np.delete(min_report_people, np.argwhere(min_report_people==candidate1))    
    if(min_report_people.size):
        # candidate2 = np.random.choice(min_report_people)
        candidate2 = find_candi(candidate1, min_report_people)
        print(candidate1, candidate2, min_report_people)        
    else:
        candidate_people = np.delete(candidate_people, np.argwhere(candidate_people==candidate1))
        # candidate2 = np.random.choice(candidate_people)
        candidate2 = find_candi(candidate1, candidate_people)        
        print(candidate1, candidate2, candidate_people)
    print(candidate1, candidate2, sep=' and ')
    
    mask_tmp = np.in1d(report_count['names'], [candidate1, candidate2])
    mask_tmp = np.where(mask_tmp==1)[0]
    for mm in mask_tmp:
        report_count[mm]['Ntalk'] += 1
    
    last_weeks_list = last_weeks_list[2::]
    last_weeks_list = np.append(last_weeks_list, [candidate1, candidate2])
    print('last_weeks_list', last_weeks_list)
    # print_Ntalk(report_count)
