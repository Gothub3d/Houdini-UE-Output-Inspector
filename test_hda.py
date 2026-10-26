import csv
import os
import unreal

# Keep wrapper alive globally so it stays active in memory
if 'hda_wrapper_instance' not in globals():
    hda_wrapper_instance = None

# UPDATED: Filepath is now pointed directly into your project's local git repository directory
def export_hda_report(filepath="C:/Users/Reza/Documents/GitHub/Houdini-UE-Output-Inspector/hda_report.csv"):
    global hda_wrapper_instance
    
    def on_hda_cooked(in_wrapper):
        num_outputs = in_wrapper.get_num_outputs()
        print('LogPython: num_outputs: {}'.format(num_outputs))
        
        if num_outputs > 0:
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            try:
                with open(filepath, mode='w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Output Index", "Output Type", "Object Name", "Is Proxy"])
                    
                    for output_idx in range(num_outputs):
                        output_type = in_wrapper.get_output_type_at(output_idx)
                        identifiers = in_wrapper.get_output_identifiers_at(output_idx)
                        
                        for identifier in identifiers:
                            obj = in_wrapper.get_output_object_at(output_idx, identifier)
                            is_proxy = in_wrapper.is_output_current_proxy_at(output_idx, identifier)
                            obj_name = obj.get_name() if obj else 'None'
                            
                            writer.writerow([output_idx, output_type, obj_name, is_proxy])
                            
                print("LogPython: Successfully saved report to: {}".format(filepath))
                
            except IOError as e:
                print("LogPython: Error saving CSV file: {}".format(e))

    # Get the selected list
    selected_actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()
    
    if not selected_actors:
        print("LogPython: Please first select an HDA Actor in the level")
        return
        
    target_hda_actor = selected_actors[0]
    
    # Create and arm our listener wrapper
    api = unreal.HoudiniPublicAPIAssetWrapper
    hda_wrapper_instance = api.create_wrapper(None, target_hda_actor)
    
    if hda_wrapper_instance:
        hda_wrapper_instance.on_post_processing_delegate.add_callable(on_hda_cooked)
        print("LogPython: Script armed with Git path! Click Recook on your HDA now...")

# Run the script setup
export_hda_report()
