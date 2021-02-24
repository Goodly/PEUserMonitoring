import requests
import json
import os
import csv
from utils import get_projectIDs, get_categoryIDs, get_category

PYBOSSA_API_KEY = os.getenv('PYBOSSA_API_KEY')
headers = {
  'Content-Type': 'application/json',
}


def fill_taskrun(project_dict, category_ids, category_dict, write=True):
    '''
    Input: List of project_ids
    Output: csv file with TaskRun info field data
    '''
    task_dict = []
    for project_name in project_dict:
        project_id = project_dict[project_name]
        r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                         '&project_id={}&orderby=id&limit=100'
                         .format(PYBOSSA_API_KEY, project_id),
                         headers=headers)
        # Retrieves (max) 100 TaskRun at a time
        task_runs = json.loads(r.text)
        last = len(task_runs) - 1
        for i in range(len(task_runs)):
            # Isolate the info field of the TaskRun
            task_run = task_runs[i]
            info = task_runs[i]["info"]
            if type(info) is dict:
                task_dict.append(info)
            if i == last:
                lastID = task_run['id']
        # Since we can only retrieve 100 tasks at a time...
        while len(task_runs) == 100:
            r = requests.get('https://pe.goodlylabs.org/api/taskrun?api_key={}'
                             '&project_id={}&last_id={}&orderby=id&limit=100'
                             .format(PYBOSSA_API_KEY, project_id, lastID),
                             headers=headers)
            task_runs = json.loads(r.text)
            last = len(task_runs) - 1
            for i in range(len(task_runs)):
                task_run = task_runs[i]
                info = task_runs[i]["info"] 
                if type(info) is dict:
                    task_dict.append(info)
                if i == last:
                    lastID = task_run['id']
    if write:
        with open('userdata.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["highlight_group", "article_batch_name",
                             "article_sha256", "queue", 'savedAnswers',
                             'article_id', 'highlight_group_id'])
            for i in task_dict:
                writer.writerow([i["highlight_group"], i["article_batch_name"],
                                i["article_sha256"], i["queue"], i["savedAnswers"],
                                i["article_id"], i["highlight_group_id"]])
    else:
        return task_dict


if __name__ == '__main__':
    categories = ["covidarticles", "covidtrainingtasks"]
    # Add whatever project names you want to pull data from 
    project_names = ['Covid_SourceRelevancev1', 'Covid_Semantics1.0',
                     "Covid_Reasoningv1", "Covid_Probabilityv1",
                     "Covid_Languagev1.1", "Covid_Holisiticv1.2",
                     "Covid_Form1.0", "Covid_Evidencev1",
                     "Covid_ArgumentRelevancev1.2",
                     "Covid2_FormTriage", "Covid2_SemanticsTriage",
                     "Covid2.1_Sources", "Covid2.1_Holistic",
                     "Covid2.1_Probability", "Covid2.1_Reasoning",
                     "Covid2.1_Arguments", "Covid2.1_Language",
                     "Covid2.1_Evidence"]
    category_ids = get_categoryIDs(project_names)
    category_dict = get_category(category_ids)
    project_dict = get_projectIDs(project_names)
    taskruns = fill_taskrun(project_dict, category_ids, category_dict, write=True)
