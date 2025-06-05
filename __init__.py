import bpy

def get_selected_armatures(context):
    return [o for o in context.selected_objects if o.type == 'ARMATURE']

# ---------- Operator: Batch add Copy Transforms ----------
class POSE_OT_sync_common_bones(bpy.types.Operator):
    bl_idname = "pose.sync_common_bones"
    bl_label = "Sync Common Bones"
    bl_description = ("Add Copy Transforms constraints to bones with matching "
                      "names between the last two selected Armatures")

    clear_existing: bpy.props.BoolProperty(
        name="Clear old constraints",
        default=True,
        description="Remove previous SyncFrom_ constraints before adding new ones")

    def execute(self, context):
        sel = get_selected_armatures(context)
        if len(sel) < 2:
            self.report({'ERROR'}, "Select at least TWO Armatures (source then target)")
            return {'CANCELLED'}

        # Use order of selection: last is active (target), previous is source
        dst = sel[-1]
        src = sel[-2]

        synced = 0
        for pb in dst.pose.bones:
            if self.clear_existing:
                for c in [c for c in pb.constraints
                          if c.type == 'COPY_TRANSFORMS' and c.name.startswith("SyncFrom_")]:
                    pb.constraints.remove(c)
            if pb.name in src.pose.bones:
                con = pb.constraints.new(type='COPY_TRANSFORMS')
                con.name = f"SyncFrom_{src.name}"
                con.target = src
                con.subtarget = pb.name
                con.owner_space = 'POSE'
                con.target_space = 'POSE'
                synced += 1

        self.report({'INFO'}, f"Synced {synced} bones from {src.name} ➜ {dst.name}")
        return {'FINISHED'}


# ---------- Operator: Bake & Clear ----------
class POSE_OT_bake_synced(bpy.types.Operator):
    bl_idname = "pose.bake_synced_bones"
    bl_label = "Bake Synced Bones"
    bl_description = "Bake the Copy Transforms results into keyframes on the active Armature"

    frame_start: bpy.props.IntProperty(default=1, description="Start frame")
    frame_end: bpy.props.IntProperty(default=250, description="End frame")

    def execute(self, context):
        active = context.object
        if not active or active.type != 'ARMATURE':
            self.report({'ERROR'}, "Active object must be an Armature to bake")
            return {'CANCELLED'}

        bpy.ops.nla.bake(frame_start=self.frame_start,
                         frame_end=self.frame_end,
                         only_selected=False,
                         visual_keying=True,
                         clear_constraints=True,
                         bake_types={'POSE'})
        self.report({'INFO'}, f"Baked frames {self.frame_start}-{self.frame_end} on {active.name}")
        return {'FINISHED'}


# ---------- UI Panel ----------
class VIEW3D_PT_sync_common_bones(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bone Sync'
    bl_label = 'Sync & Bake'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="1. Select SRC then DST Armatures")
        col.operator("pose.sync_common_bones", icon='CONSTRAINT_BONE')
        col.separator()
        col.label(text="2. Bake (optional)")
        col.operator("pose.bake_synced_bones", icon='ACTION')


# ---------- Registration ----------
classes = (
    POSE_OT_sync_common_bones,
    POSE_OT_bake_synced,
    VIEW3D_PT_sync_common_bones,
)
register, unregister = bpy.utils.register_classes_factory(classes)