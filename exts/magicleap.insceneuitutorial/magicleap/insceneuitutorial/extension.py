################################################################################
# MagicLeap Omniverse Kit In-Scene UI Interaction Example                      #
################################################################################

import omni.ext
import omni.ui as ui

from carb import Float2, Float3, events

from pxr import Sdf

from omni.kit.scene_view.usd import UsdSceneView
from omni.kit.xr.sceneview_utils import SceneViewUtils, SceneWidgetManipulator
from omni.timeline import get_timeline_interface
from omni.ui import scene as sc

class MagicleapWidget(ui.Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def __del__(self):
        self.destroy()

    def _build_ui(self):
        self._widget = ui.VStack()
        with self._widget:
            label = ui.Label("Press the buttons to add and delete spheres.")
            with ui.HStack():
                ui.Button("Spawn", clicked_fn=spawn_sphere)
                ui.Button("Delete", clicked_fn=delete_spheres)

class MagicleapInSceneUITutorialExtension(omni.ext.IExt):
    def __init__(self) -> None:
        super().__init__()
        self._scene_view_utils: SceneViewUtils | None = None
        self._widget_container: SceneWidgetManipulator[MagicleapWidget] | None = None

    # Called when this extension is loaded
    def on_startup(self, ext_id):
        print("[magicleap.hello.world] magicleap hello world startup")

        self._stage_evt_handler = omni.usd.get_context().get_stage_event_stream() \
            .create_subscription_to_pop(self.on_stage_event, name="handlestageevents")

        if (omni.usd.get_context().get_stage_state() == omni.usd.StageState.OPENED):
            self._create_widget()

    # Called when this extension is unloaded
    def on_shutdown(self):
        print("[magicleap.hello.world] magicleap hello world shutdown")

        if self._stage_evt_handler:
            self._stage_evt_handler.unsubscribe()
            self._stage_evt_handler = None

        self._destroy_widget()

    # The UI widget can only be instantiated in the current usd stage after one has been opened.
    def on_stage_event(self, e: events.IEvent):
        if e.type == int(omni.usd.StageEventType.OPENED):
            self._create_widget()
        elif e.type == int(omni.usd.StageEventType.CLOSING):
            self._destroy_widget()

    # Leverage SceneViewUtils to create UI elements in the current usd stage
    def _create_widget(self):
        if self._scene_view_utils is None:
            self._scene_view_utils = SceneViewUtils(UsdSceneView)

        if self._widget_container is None:
            self._widget_container = \
                self._scene_view_utils.create_widget_factory(MagicleapWidget) \
                    .with_size(Float2(600, 300)) \
                    .with_position(Float3(0, 300, 0)) \
                    .with_resolution_scale(3) \
                    .with_construct_args() \
                    .with_update_policy(sc.Widget.UpdatePolicy.ALWAYS) \
                    .build()

    # Remove UI elements from the stage
    def _destroy_widget(self):
        if self._widget_container:
            self._widget_container.clear()
            self._widget_container = None

# Spawn a sphere prim in the scene
def spawn_sphere():
    # Ensure stage
    stage = omni.usd.get_context().get_stage()
    if stage is None:
        return

    # Ensure that the timeline is set to play to see physics act on the sphere.
    timeline = get_timeline_interface()
    if timeline.is_stopped():
        timeline.play()

    # Generate a path for the sphere
    sphere_path = Sdf.Path(omni.usd.get_stage_next_free_path(stage, "/World/Sphere", False))

    # Create a sphere prim with a default transform
    omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
        prim_type='Sphere',
        prim_path=sphere_path,
        select_new_prim=True,
        prepend_default_prim=True,
        above_ground=True)

    # Pose the sphere prim above the buttons
    omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
        count=1,
        paths=[str(sphere_path)],
        new_translations=[0.0, 350.0, 0.0],
        new_scales=[1.0, 1.0, 1.0])

    # Attach a rigid body to the sphere and watch it fall!
    omni.kit.commands.execute('SetRigidBody',
        path=sphere_path,
        approximationShape='convexHull',
        kinematic=False)

# Delete all spheres from the scene
def delete_spheres():
    # Ensure stage
    stage = omni.usd.get_context().get_stage()
    if stage is None:
        return

    # Find all spheres in the scene
    spheres = []
    for prim in stage.Traverse():
        name = str(prim.GetName())
        if "Sphere" in name:
            spheres.append(prim.GetPath())

    # Delete all of the spheres that were found
    omni.kit.commands.execute('DeletePrims',
        paths=spheres,
        destructive=False)
