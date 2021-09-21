import numpy as np
from sge.parameters import params
import json
import os



def evolution_progress(generation, pop):
    fitness_samples = [i['fitness'] for i in pop]
    data = 'generation: %4d\tmax: %.6e\t min: %.6e\tmean: %.6e\tstd deviation: %.6e' % (generation, np.max(fitness_samples), np.min(fitness_samples), np.mean(fitness_samples), np.std(fitness_samples))
    if params['VERBOSE']:
        print(data)
    save_progress_to_file(data)
    if generation % params['SAVE_STEP'] == 0:
        save_step(generation, pop)


def save_progress_to_file(data):
    if os.environ.get('PonyGE2_PATH') != None:
        os.chdir(os.environ["PonyGE2_PATH"] + '/src')
    with open('%s/run_%d/progress_report.csv' % (params['EXPERIMENT_NAME'], params['RUN']), 'a') as f:
        f.write(data + '\n')
    if os.environ.get('PonyGE2_PATH') != None:
        os.chdir(os.environ["SGE3_PATH"] + '/sge')


def save_step(generation, population):
    c = json.dumps(population)
    if os.environ.get('PonyGE2_PATH') != None:
        os.chdir(os.environ["PonyGE2_PATH"] + '/src')
    open('%s/run_%d/iteration_%02d.json' % (params['EXPERIMENT_NAME'], params['RUN'], generation), 'a').write(c)
    if os.environ.get('PonyGE2_PATH') != None:
        os.chdir(os.environ["SGE3_PATH"] + '/sge')


def save_parameters():
    params_lower = dict((k.lower(), v) for k, v in params.items())
    c = json.dumps(params_lower)
    if os.environ.get('PonyGE2_PATH') != None:
        os.chdir(os.environ["PonyGE2_PATH"] + '/src')
    open('%s/run_%d/parameters.json' % (params['EXPERIMENT_NAME'], params['RUN']), 'a').write(c)
    if os.environ.get('PonyGE2_PATH') != None:
        os.chdir(os.environ["SGE3_PATH"] + '/sge')


def prepare_dumps():
    try:
        if os.environ.get('PonyGE2_PATH') != None:
            os.chdir(os.environ["PonyGE2_PATH"] + '/src')
        os.makedirs('%s/run_%d' % (params['EXPERIMENT_NAME'], params['RUN']))    
        if os.environ.get('PonyGE2_PATH') != None:
            os.chdir(os.environ["SGE3_PATH"] + '/sge')
    except FileExistsError as e:
        print('\033[31m' + "current working directory" + os.getcwd() + '\033[0m')
        print('\033[31m' + "Exception: prepare_dumps() FileExistsError" + '\033[0m')
        pass
    save_parameters()