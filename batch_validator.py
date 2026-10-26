import sys
import unreal
from PySide2 import QtWidgets, QtCore

# Keep the UI window reference alive globally to prevent it from closing instantly
if 'hda_validator_ui' not in globals():
    hda_validator_ui = None

class HdaBatchValidatorWindow(QtWidgets.QWidget):
    def __init__(self):
        super(HdaBatchValidatorWindow, self).__init__()
        self.setWindowTitle("Houdini HDA Batch Validator")
        self.setMinimumSize(400, 150)
        
        # Keep window on top of the main Unreal Editor window frame
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        
        # Create Layout
        layout = QtWidgets.QVBoxLayout(self)
        
        # Info Label
        self.label = QtWidgets.QLabel("Select an HDA Actor in your level, then click validate.")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label)
        
        # Run Button
        self.run_btn = QtWidgets.QPushButton("Run Validation")
        self.run_btn.setStyleSheet("background-color: #2c3e50; color: white; font-weight: bold; font-size: 14px; padding: 8px;")
        self.run_btn.clicked.connect(self.execute_validation)
        layout.addWidget(self.run_btn)

    def execute_validation(self):
        selected_actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()
        
        if not selected_actors:
            unreal.log_warning("Batch Validator: Please first select an HDA Actor in the level viewport!")
            self.label.setText("❌ Error: No HDA Actor Selected!")
            return
            
        target_hda_actor = selected_actors[0]
        
        # Access the asset wrapper API directly
        api = unreal.HoudiniPublicAPIAssetWrapper
        wrapper = api.create_wrapper(None, target_hda_actor)
        
        if not wrapper:
            unreal.log_error("Batch Validator: Failed to resolve the HDA asset wrapper structure.")
            return
            
        num_outputs = wrapper.get_num_outputs()
        unreal.log(f"--- Starting Validation Batch for {target_hda_actor.get_name()} ({num_outputs} outputs) ---")
        
        has_failures = False
        
        # Iterate systematically through all generated HDA outputs
        for output_idx in range(num_outputs):
            identifiers = wrapper.get_output_identifiers_at(output_idx)
            
            for identifier in identifiers:
                obj = wrapper.get_output_object_at(output_idx, identifier)
                
                # INTEGRATED LOGIC: Run compliance check on Static Mesh assets
                if isinstance(obj, unreal.StaticMesh):
                    has_collision = obj.get_editor_property("has_collision")
                    num_lods = obj.get_num_lods()
                    
                    status = "PASS" if has_collision and num_lods > 0 else "FAIL"
                    log_msg = f"[{status}] {obj.get_name()} -> Collision: {has_collision}, LODs: {num_lods}"
                    
                    if status == "PASS":
                        unreal.log(log_msg)
                    else:
                        has_failures = True
                        # Requirements Check 3: Print a prominent log WARNING if asset validation fails
                        unreal.log_warning(f"⚠️ VALIDATION CRITICAL FAILURE: Mesh asset '{obj.get_name()}' missing Collision or LOD chains!")
                        unreal.log_warning(f"  └ Details -> {log_msg}")
                        
        if has_failures:
            self.label.setText("⚠️ Validation finished with WARNINGS! Check Output Log.")
        else:
            self.label.setText("✅ All assets passed validation successfully!")


def launch_validator_tool():
    global hda_validator_ui
    
    # Safely close existing panel instance if open
    if hda_validator_ui:
        hda_validator_ui.close()
        
    # Generate and display the new interactive tool window
    hda_validator_ui = HdaBatchValidatorWindow()
    hda_validator_ui.show()

if __name__ == "__main__":
    launch_validator_tool()
