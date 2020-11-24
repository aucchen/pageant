import json

from automated_player import test_with_script

if __name__ == '__main__':
    # test a variety of scenarios, representing different runs.
    test_with_script('standard_runs/emily_test_script.txt', output_path='standard_runs/emily_output.txt', data_path='standard_runs/emily_data.txt', dump_stats=0, use_headless=False)
    with open('standard_runs/emily_data.txt') as f:
        data = json.load(f)
    if data['qualities']['emily_date'] != 1:
        print('FAILURE: emily_date should be 1')
    if data['qualities']['emily'] != 9:
        print('FAILURE: emily should be 9')
    if data['qualities']['pageant_success'] != 1:
        print('FAILURE: pageant_success should be 1')
