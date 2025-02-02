from my_evaluate import EVALUATE_NAMES
import json
import os
import argparse





def read_results(args):
    """
    read evaluate results
    """
    evaluate_paths = os.listdir(args.evaluate_path)
    
    final_list = {}
    
    for pic_strength_name in evaluate_paths:
        next_path = os.path.join(args.evaluate_path, pic_strength_name)
        idx_paths = os.listdir(next_path)
        
        for idx_file in idx_paths:
            final_path = os.path.join(next_path, idx_file)
            
            idx = idx_file.split('.')[0]
            
            # read the file
            with open(final_path, 'r') as f:
                res_stats_dict = json.load(f)
                final_list[(pic_strength_name, idx)] = res_stats_dict
    
    print(f'=========================== finish read results =============================')
    
    
    
    return final_list
            
            
        
        
        
    
    
    
    
    

def final_report(final_list):
  """
  report the results for different strengths
  """
  print(f'final_list.keys() = {final_list.keys()}\nlen of final_list.keys() = {len(final_list.keys())}')
  
  per_classes = set([name.split('_')[1] for name, idx in final_list.keys()])
  print(f'per_classes: {per_classes}')
  
  key_lists = ['ocr', 'top_1_guess', 'top_3_guess', 'top_1_reason', 'top_3_reason']
  summary_dict = {
    per_class: 
      {name: 
        {key: [] for key in key_lists} 
        for name in EVALUATE_NAMES} 
      for per_class in per_classes
    }
  
  # calculate the average scores for each strength
  for (pic_strength_name, idx), res_stats_dict in final_list.items():
    per_class = pic_strength_name.split('_')[1]
    for name in EVALUATE_NAMES:
      for key in key_lists:
        summary_dict[per_class][name][key].append(res_stats_dict[name][key])
  
  # print the original summary_dict in lines
  print(f'==================== original summary results ====================')
  for per_class in per_classes:
    print(f'==================== {per_class} ====================')
    for name in EVALUATE_NAMES:
      print(f'{name}\t OCR: {summary_dict[per_class][name]["ocr"]}\t top-1 guess: {summary_dict[per_class][name]["top_1_guess"]}\t top-3 guess: {summary_dict[per_class][name]["top_3_guess"]}\t \
          top-1 reason: {summary_dict[per_class][name]["top_1_reason"]}\t top-3 reason: {summary_dict[per_class][name]["top_3_reason"]}')
  
  # average the scores
  for per_class in per_classes:
    for name in EVALUATE_NAMES:
      for key in key_lists:
        tmp_list = summary_dict[per_class][name][key]
        summary_dict[per_class][name][key] = sum(tmp_list) / len(tmp_list)
        
  # print the results in a table
  print(f'==================== summary results ====================')
  for per_class in per_classes:
    print(f'==================== {per_class} ====================')
    for name in EVALUATE_NAMES:
      print(f'{name}\t OCR: {summary_dict[per_class][name]["ocr"]:.3f}\t top-1 guess: {summary_dict[per_class][name]["top_1_guess"]:.3f}\t top-3 guess: {summary_dict[per_class][name]["top_3_guess"]:.3f}\t \
          top-1 reason: {summary_dict[per_class][name]["top_1_reason"]:.3f}\t top_3 reason: {summary_dict[per_class][name]["top_3_reason"]:.3f}')



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--evaluate_path', type=str, default = 'evaluate_results')

    args = parser.parse_args()
    
    final_list = read_results(args)
    
    final_report(final_list)