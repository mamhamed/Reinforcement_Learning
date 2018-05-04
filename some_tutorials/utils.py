import re
import math

SEARCH_ORIGINS = set([
    "GLOBAL_SEARCH_HEADER", # Search performed via global search header.
    "SWITCH_SEARCH_VERTICAL" # Search performed by switching verticals on search result page. (e,g from 'TOP' to 'PEOPLE').
])


@outputSchema("boolean")
def valid_search_origin(search_origin):
    if search_origin is None:
        return False
    return search_origin in SEARCH_ORIGINS


# define labels
SKIP = 0
ENTITY_CLICK = 1
def get_label(search_result):
    """
    get label based on user action
    :param search_result:
    :return:
    """
    label = SKIP
    if search_result[4]:
        if search_result[5] == 'VIEW_ENTITY':
            label = ENTITY_CLICK
        elif search_result[5] != 'SEARCH':
            label = ENTITY_CLICK
        else:
            label = SKIP

    return label


@outputSchema("boolean")
def contain_clicks(search_results):
    """
    check if the list of search results contain more than 1 result, and contain clicks
    also check if the list of search results contain unique label
    :param search_results:
    :return:
    """
    if search_results is None:
        return False

    # filter list with only 1 result
    if len(search_results) < 2:
        return False

    labels = set()
    click_flag = False
    for result in search_results:
        labels.add(get_label(result))
        if result[4]:
            click_flag = True

    # filter list with unique label
    if len(labels) == 1:
        return False

    return click_flag


@outputSchema("boolean")
def any_match(list1, list2):
    """

    :param list1: a list of integers
    :param list2: a list of integers
    :return: true if there is one element in common between the two list. false otherwise
    """
    if list1 is None or list2 is None:
        return False

    if len(list1) == 0 or len(list2) == 0:
        return False

    list1 = [x[0] for x in list1 if x[0] is not None]
    list2 = [x[0] for x in list2 if x[0] is not None]

    list3 = [x for x in list1 if x in list2]

    return len(list3) > 0


@outputSchema("chararray")
def cartesian_product(list1, list2):
    """

    :param list1: a list of integers
    :param list2: a list of integers
    :return: true if there is one element in common between the two list. false otherwise
    """
    if list1 is None or list2 is None:
        return ''

    if len(list1) == 0 or len(list2) == 0:
        return ''

    list1 = [x[0] for x in list1 if x[0] is not None]
    list2 = [x[0] for x in list2 if x[0] is not None]

    try:
        return str(list1[0]) + '-' + str(list2[0])
    except:
        return ''


@outputSchema("boolean")
def query_contains_cn_t(query_tag):
    if query_tag is None:
        return False

    if 'TITLE' in query_tag and 'COMPANY_NAME' in query_tag:
        return True
    else:
        return False


@outputSchema("boolean")
def remove_sales_rectuiter(func_names):
    if func_names is None:
        return False

    if len(func_names) == 0:
        return False

    names = [x[0] for x in func_names]

    for name in names:
        if 'Human Resources' in name or \
                        'Sales' in name or \
                        'Marketing' in name or \
                        'Business Development' in name or \
                        'Entrepreneurship' in name:

            return False


    return True


def assymetric_jaccard_similarity(n,m):
    return len([x for x in n if x in m])*1.0/len(n)


@outputSchema("double")
def title_healine_overlap(healine, titles):
    if titles is None or healine is None:
        return 0.0

    titles = [x[0] for x in titles]

    titles = ' '.join(titles)

    return assymetric_jaccard_similarity(healine, titles)


@outputSchema("chararray")
def quantizer(num, bypass_thr=10, resolution = 10, max_thr=100):
    if num is None:
        return str(-1)

    if num < bypass_thr:
        return str(num)

    if num > bypass_thr and num < max_thr:
        return str((num/resolution+1) * resolution-1)

    if num > max_thr:
        return str(max_thr)

    return str(num)


exec_titles = ['deputy chief executive officer',
               'group chief executive officer',
               'vice chief executive officer',
               'joint chief executive officer',
               'interim chief executive officer',
               'principal chief executive officer'
               'chief executive officer',
               'vice president',
               'senior vice president',
               'chief marketing officer',
               'chief information officer',
               'chief technology officer',
               'chief financial officer',
               'chief data officer',
               'chief executive director'
               ]

def create_abbv(word):
    terms = word.split(' ')
    first_char = [t[0] for t in terms]
    all_abbv = []

    all_abbv.append(''.join(first_char))
    all_abbv.append('.'.join(first_char))
    all_abbv.append('.'.join(first_char) + '.')

    return all_abbv

@outputSchema("boolean")
def is_exec(intitle):
    if intitle is None:
        return False

    title = intitle.lower()
    title = re.sub('[^0-9a-zA-Z]+', ' ', title)
    for t in exec_titles:
        if (t + ' ') in title or (' ' + t) in title or title==t:
            return True
        print create_abbv(t)
        for tt in create_abbv(t):
            if (tt + ' ') in title or (' ' + tt) in title or title==tt:
                return True


    return False

@outputSchema("chararray")
def exec_name(intitle):
    if intitle is None:
        return ''

    title = intitle.lower()
    title = re.sub('[^0-9a-zA-Z]+', ' ', title)
    for t in exec_titles:
        if (t + ' ') in title or (' ' + t) in title or title==t:
            return t
        print create_abbv(t)
        for tt in create_abbv(t):
            if (tt + ' ') in title or (' ' + tt) in title or title==tt:
                return t


    return ''

def getTaggerDict(pattern):
    key_values = {}
    for x in pattern.split(','):
        splitted = x.split(':')
        if len(splitted) < 2:
            continue
        key_values[splitted[0]] = splitted[1]

    return key_values

@outputSchema('tagged_queries:bag{tagged:(keywords:chararray, tag:chararray)}')
def get_entity_from_tagged_query(tagged_query):
    """

    :param list1: a list of integers
    :param list2: a list of integers
    :return: true if there is one element in common between the two list. false otherwise
    """
    if tagged_query is None:
        return None

    pattern = re.compile(r'\(([^)]*)\)')
    all_patterns =  pattern.findall(tagged_query)

    all_tags = [getTaggerDict(x) for x in all_patterns]
    all_tags = [x for x in all_tags if x['keywords'] != '' and x['keywords'] is not None]

    if len(all_tags) == 0:
        return None


    all_tags = [(x['keywords'], x[' tag']) for x in all_tags]

    return all_tags

@outputSchema("double")
def ndcg_calc(results, n, with_spam=1):
    if results is None:
        return ""
    
    result_index = [x[0] for x in results[0]]
    result_click = [x[0] for x in results[1]]
    result_spam = [x[0] for x in results[2]]

    results = zip(result_index, result_click, result_spam)
    results = sorted(results, key=lambda x: x[0])

    if with_spam:
        dcg = dcg_calc(results, n)
        idcg = dcg_calc(sorted(results, key=lambda x: x[1]), n)
        ndcg = dcg/idcg if idcg > 0 else 0.0
        return ndcg
    else:
        results_with_spam = [x for x in results if x[2] == 0]
        dcg = dcg_calc(results_with_spam, n)
        idcg = dcg_calc(sorted(results_with_spam, key=lambda x: x[1]), n)
        ndcg = dcg/idcg if idcg > 0 else 0.0
        return ndcg
       
def dcg_calc(results, n):
    dcg = 0.0
    dcg_no_spam = 0.0
    index_bias = 0.0

    i = 0
    for res in results:
        rel = res[1]
        i += 1 # res[0]
        spam = res[2]

        dcg += rel / math.log(i+1, 2)
        if i > n:
            break

    return dcg
