import requests
import json
import os

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def get_ids(project_ids, months=None):
    """
    Input: List of project IDs, (optional) a list of months formatted 'YYYY-MM'
    Output: Dictionary of (key) user_ids and (value) the amount of tasks
    they've completed for the given projects
    """
    user_ids = {}
    if months:
        for m in months:
            for project_id in project_ids:
                r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                                 '&project_id={}&created={}&all=1&orderby=id&limit=100'
                                 .format(PYBOSSA_API_KEY, project_id, m),
                                 headers=headers)
                task_runs = json.loads(r.text)
                # For each task, either add the user id or incremement the id's count
                for task in task_runs:
                    if str(task['user_id']) in user_ids:
                        user_ids[str(task['user_id'])] += 1
                    else:
                        user_ids[str(task['user_id'])] = 1
    else:
        for project_id in project_ids:
            r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                             '&project_id={}&all=1&orderby=id&limit=100'
                             .format(PYBOSSA_API_KEY, project_id),
                             headers=headers)
            task_runs = json.loads(r.text)
            # For each task, either add the user id or incremement the id's count
            for task in task_runs:
                if str(task['user_id']) in user_ids:
                    user_ids[str(task['user_id'])] += 1
                else:
                    user_ids[str(task['user_id'])] = 1
    return user_ids


def get_names(user_ids):
    """
    Input: user_ids dictionary
    Output: a dictionary mapping full name to task count
    """
    names = {}
    for user in user_ids:
        r = requests.get('https://pe.goodlylabs.org'
                         '/api/user/{}?api_key={}&limit=100'
                         .format(user, PYBOSSA_API_KEY), headers=headers)
        user_info = json.loads(r.text)
        names[user_info['fullname']] = user_ids[user]
    return names


def get_projectIDs(project_names):
    """
    Input: list of project short names
    Output: Dictionary mapping project shortname to project ID
    """
    project_ids = {}
    for project_name in project_names:
        r = requests.get('https://pe.goodlylabs.org/api/project?api_key={}'
                         '&short_name={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_name),
                         headers=headers)
        project_info = json.loads(r.text)
        project_ids[project_name] = (project_info[0]['id'])
    return project_ids


def get_categoryIDs(project_names):
    """
    Input: list of project names
    Output: Dictionary mapping project shortname to category id
    """
    project_ids = {}
    for project_name in project_names:
        r = requests.get('https://pe.goodlylabs.org/api/project?api_key={}'
                         '&short_name={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_name),
                         headers=headers)
        project_info = json.loads(r.text)
        project_ids[project_name] = project_info[0]['category_id']
    return project_ids


def get_category(category_ids):
    """
    Input: list of category ids
    Output: Dictionary mapping category id to category shortname
    """
    categories = {}
    for cid in category_ids.values():
        r = requests.get('https://pe.goodlylabs.org/api/category?api_key={}'
                          '&id={}&orderby=id&limit=100'
                          .format(PYBOSSA_API_KEY, cid),
                          headers=headers)
        project_info = json.loads(r.text)
        categories[cid] = project_info[0]['short_name']
    return categories
