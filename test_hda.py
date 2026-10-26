import csv
import os
import unreal

def export_hda_report(filepath="C:/Users/Reza/Documents/hda_report.csv"):
    # This inner function handles the cook event and writes the CSV file
    def on_hda_cooked(in_wrapper):
        num_outputs = in_wrapper.get_num_outputs()
        print('num_outputs: {}'.format(num_outputs))
        
        if num_outputs > 0:
            # Ensure target directory exists before writing
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            try:
                with open(filepath, mode='w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    
                    # Write assignments mandatory headers
                    writer.writerow(["Output Index", "Output Type", "Object Name", "Is Proxy"])
                    
                    # Loop through outputs and write rows instead of printing
                    for output_idx in range(num_outputs):
                        output_type = in_wrapper.get_output_type_at(output_idx)
                        identifiers = in_wrapper.get_output_identifiers_at(output_idx)
                        
                        for identifier in identifiers:
                            obj = in_wrapper.get_output_object_at(output_idx, identifier)
                            is_proxy = in_wrapper.is_output_current_proxy_at(output_idx, identifier)
                            
                            # Cleanly resolve object name safely
                            obj_name = obj.get_name() if obj else 'None'
                            
                            # Write data row matching assignment columns
                            writer.writerow([output_idx, output_type, obj_name, is_proxy])
                            
                print("Successfully saved report to: {}".format(filepath))
                
            except IOError as e:
                print("Error saving CSV file to {}: {}".format(filepath, e))

    # Get the editor subsystem and selected actors
    selected = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()
    
    if not selected:
        print("Please first select an HDA Actor in the level")
    else:
        api = unreal.HoudiniPublicAPIAssetWrapper
        wrapper = api.create_wrapper(None, selected[0])
        
        # Register our CSV writing function to the delegate
        wrapper.on_post_processing_delegate.add_callable(on_hda_cooked)
        print("Wrapper created, waiting for HDA cook to complete...")

# Prevents execution on automatic import
if __name__ == "__main__":
    export_hda_report()
