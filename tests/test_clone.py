from lib.elements import Clone, EmbroideryElement, FillStitch
from lib.commands import add_commands
from lib.svg.tags import INKSTITCH_ATTRIBS, SVG_RECT_TAG, INKSCAPE_LABEL
from lib.utils import cache_module
from inkex import SvgDocumentElement, Rectangle, Circle, Group, Use, Transform, TextElement
from inkex.tester import TestCase
from inkex.tester.svg import svg

from typing import Optional

from math import sqrt


def element_fill_angle(element: EmbroideryElement) -> Optional[float]:
    angle = element.node.get(INKSTITCH_ATTRIBS['angle'])
    if angle is not None:
        angle = float(angle)
    return angle


class CloneElementTest(TestCase):
    # Monkey-patch the cahce to forcibly disable it: We may need to refactor this out for tests.
    def setUp(self):
        from pytest import MonkeyPatch
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(cache_module, "is_cache_disabled", lambda: True)

    def tearDown(self):
        self.monkeypatch.undo()
        return super().tearDown()

    def assertAngleAlmostEqual(self, a, b):
        # Take the mod 180 of the returned angles, because e.g. -130deg and 50deg produce fills along the same angle.
        # We have to use a precision of 4 decimal digits because of the precision of the matrices as they are stored in the svg trees
        # generated by these tests.
        self.assertAlmostEqual(a % 180, b % 180, 4)

    def test_not_embroiderable(self):
        root: SvgDocumentElement = svg()
        text = root.add(TextElement())
        text.text = "Can't embroider this!"
        use = root.add(Use())
        use.href = text

        clone = Clone(use)
        stitch_groups = clone.to_stitch_groups(None)
        self.assertEqual(len(stitch_groups), 0)

    def test_not_clone(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use(attrib={
            INKSTITCH_ATTRIBS["clone"]: "false"
        }))
        use.href = rect

        clone = Clone(use)
        stitch_groups = clone.to_stitch_groups(None)
        self.assertEqual(len(stitch_groups), 0)

    # These tests make sure the element cloning works as expected, using the `clone_elements` method.

    def test_basic(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAlmostEqual(element_fill_angle(elements[0]), 30)

    def test_hidden_cloned_elements_not_embroidered(self):
        root = svg()
        g = root.add(Group())
        g.add(Rectangle(attrib={
            INKSCAPE_LABEL: "NotHidden",
            "width": "10",
            "height": "10"
        }))
        g.add(Rectangle(attrib={
            INKSCAPE_LABEL: "Hidden",
            "width": "10",
            "height": "10",
            "style": "display:none"
        }))
        hidden_group = g.add(Group(attrib={
            "style": "display:none"
        }))
        hidden_group.add(Rectangle(attrib={
            INKSCAPE_LABEL: "ChildOfHidden",
            "width": "10",
            "height": "10",
        }))
        use = root.add(Use())
        use.href = g

        clone = Clone(use)

        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertEqual(elements[0].node.get(INKSCAPE_LABEL), "NotHidden")

    def test_angle_rotated(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(20))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), 10)

    def test_angle_flipped(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_scale(-1, 1))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -30)

    def test_angle_flipped_rotated(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(20).add_scale(-1, 1))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Fill angle goes from 30 -> -30 after flip -> -50 after rotate
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -50)

    def test_angle_non_uniform_scale(self):
        """
        The angle isn't *as* well-defined for non-rotational scales, but we try to follow how the slope will be altered.
        """
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(10).add_scale(1, -sqrt(3)))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Slope of the stitching goes from tan(30deg) = 1/sqrt(3) to -sqrt(3)/sqrt(3) = tan(-45deg),
            # then rotated another -10 degrees to -55
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -55)

    def test_angle_inherits_down_tree(self):
        """
        The stitching angle of a clone is based in part on the relative transforms of the source and clone.
        """
        root: SvgDocumentElement = svg()
        g1 = root.add(Group())
        g1.set('transform', Transform().add_rotate(3))
        rect = g1.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        g2 = root.add(Group())
        g2.set('transform', Transform().add_translate((20, 0)).add_rotate(-7))
        use = g2.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(11))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Angle goes from 30 -> 40 (g1 -> g2) -> 29 (use)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), 29)

    def test_angle_not_applied_twice(self):
        """Make sure that angle changes are not applied twice to an element with both stroke and fill."""
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            "style": "stroke: skyblue; fill: red;"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(30))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 2)  # One for the stroke, one for the fill
            self.assertEqual(elements[0].node, elements[1].node)
            # Angle goes from 0 -> -30
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -30)

    def test_angle_not_applied_to_non_fills(self):
        """Make sure that angle changes are not applied to non-fill elements."""
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            "style": "stroke: skyblue; fill-opacity: 0;"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(30))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)  # One for the stroke, one for the fill
            self.assertIsNone(elements[0].get_param("angle", None))  # Angle as not set, as this isn't a fill

    def test_style_inherits(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10"
        }))
        rect.set('style', 'stroke: skyblue; fill-opacity: 0;')
        use = root.add(Use())
        use.href = rect
        use.set('style', 'stroke: red; stroke-width: 2;')

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            style = elements[0].node.cascaded_style()
            # Source style takes precedence over any attributes specified in the clone
            self.assertEqual(style["stroke"], "skyblue")
            self.assertEqual(style["stroke-width"], "2")

    def test_transform_inherits_from_cloned_element(self):
        """
        Elements cloned by cloned_elements need to inherit their transform from their href'd element and their use to match what's shown.
        """
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30",
        }))
        rect.set('transform', Transform().add_scale(2, 2))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_translate((5, 10)))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertTransformEqual(
                elements[0].node.composed_transform(),
                Transform().add_translate((5, 10)).add_scale(2, 2))

    def test_transform_inherits_from_tree(self):
        root: SvgDocumentElement = svg()
        g1 = root.add(Group())
        g1.set('transform', Transform().add_translate((0, 5)).add_rotate(5))
        rect = g1.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30",
        }))
        rect.set('transform', Transform().add_scale(2, 2))
        use = root.add(Use())
        use.href = g1
        use.set('transform', Transform().add_translate((5, 10)))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertTransformEqual(
                elements[0].node.composed_transform(),
                Transform().add_translate((5, 10))  # use
                .add_translate((0, 5)).add_rotate(5)  # g1
                .add_scale(2, 2),  # rect
                5)

    def test_transform_inherits_from_tree_up_tree(self):
        root: SvgDocumentElement = svg()
        g1 = root.add(Group())
        g1.set('transform', Transform().add_translate((0, 5)).add_rotate(5))
        rect = g1.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30",
        }))
        rect.set('transform', Transform().add_scale(2, 2))
        circ = g1.add(Circle())
        circ.radius = 5
        g2 = root.add(Group())
        g2.set('transform', Transform().add_translate((1, 2)).add_scale(0.5, 1))
        use = g2.add(Use())
        use.href = g1
        use.set('transform', Transform().add_translate((5, 10)))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 2)
            self.assertTransformEqual(
                elements[0].node.composed_transform(),
                Transform().add_translate((1, 2)).add_scale(0.5, 1)  # g2
                .add_translate((5, 10))  # use
                .add_translate((0, 5)).add_rotate(5)  # g1
                .add_scale(2, 2),  # rect
                5)
            self.assertTransformEqual(
                elements[1].node.composed_transform(),
                Transform().add_translate((1, 2)).add_scale(0.5, 1)  # g2
                .add_translate((5, 10))  # use
                .add_translate((0, 5)).add_rotate(5),  # g1
                5)

    def test_clone_fill_angle_not_specified(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(20))

        clone = Clone(use)
        self.assertEqual(clone.clone_fill_angle, None)

    def test_clone_fill_angle(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set(INKSTITCH_ATTRIBS["angle"], 42)
        use.set('transform', Transform().add_rotate(20))

        clone = Clone(use)
        self.assertEqual(clone.clone_fill_angle, 42)

        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), 42)

    def test_angle_manually_flipped(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(20))
        use.set(INKSTITCH_ATTRIBS["flip_angle"], True)

        clone = Clone(use)
        self.assertTrue(clone.flip_angle)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -10)

    # Recursive use tests

    def test_recursive_uses(self):
        root: SvgDocumentElement = svg()
        g1 = root.add(Group())
        rect = g1.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
        }))
        u1 = g1.add(Use())
        u1.set('transform', Transform().add_translate((20, 0)))
        u1.href = rect
        u2 = root.add(Use())
        u2.set('transform', Transform().add_translate((0, 20)).add_scale(0.5, 0.5))
        u2.href = g1
        u3 = root.add(Use())
        u3.set('transform', Transform().add_translate((0, 30)))
        u3.href = u2

        clone = Clone(u3)
        with clone.clone_elements() as elements:
            # There should be two elements cloned from u3, two rects, one corresponding to rect and one corresponding to u1.
            # Their transforms should derive from the elements they href.
            self.assertEqual(len(elements), 2)
            self.assertEqual(elements[0].node.tag, SVG_RECT_TAG)
            self.assertTransformEqual(elements[0].node.composed_transform(),
                                      Transform().add_translate((0, 30))  # u3
                                      .add_translate(0, 20).add_scale(0.5, 0.5)  # u2
                                      )

            self.assertEqual(elements[1].node.tag, SVG_RECT_TAG)
            self.assertTransformEqual(elements[1].node.composed_transform(),
                                      Transform().add_translate((0, 30))  # u3
                                      .add_translate((0, 20)).add_scale(0.5, 0.5)  # u2
                                      .add_translate((20, 0))  # u1
                                      )

    def test_recursive_uses_angle(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        u1 = root.add(Use())
        u1.set('transform', Transform().add_rotate(60))
        u1.href = rect

        clone = Clone(u1)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Angle goes from 30 -> -30
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -30)

        g = root.add(Group())
        g.set('transform', Transform().add_rotate(-10))
        u2 = g.add(Use())
        u2.href = u1

        clone = Clone(u2)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Angle goes from -30 -> -20 (u1 -> g)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -20)

        u3 = root.add(Use())
        u3.set('transform', Transform().add_rotate(7))
        u3.href = g

        clone = Clone(u3)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Angle goes from -20 -> -27
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -27)

        # Cloning u2 directly, the relative transform of g does not apply
        u4 = root.add(Use())
        u4.set('transform', Transform().add_rotate(7))
        u4.href = u2

        clone = Clone(u4)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Angle goes from -30 -> -37
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -37)

    def test_recursive_uses_angle_with_specified_angle(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        u1 = root.add(Use())
        u1.set('transform', Transform().add_rotate(60))
        u1.href = rect
        g = root.add(Group())
        g.set('transform', Transform().add_rotate(-10))
        u2 = g.add(Use())
        u2.href = u1
        u2.set(INKSTITCH_ATTRIBS["angle"], "0")
        u3 = root.add(Use())
        u3.set_id('U3')
        u3.set('transform', Transform().add_rotate(7))
        u3.href = g

        clone = Clone(u3)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Angle goes from 0 (g -> u2) -> -7 (u3)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -7)

    # Command clone tests

    def test_copies_directly_attached_commands(self):
        """
        Check that commands attached to the clone target directly are applied to clones.
        """
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
        }))

        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_translate(10, 10))

        original = FillStitch(rect)
        add_commands(original, ["fill_end"])

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            cmd_orig = original.get_command("fill_end")
            cmd_clone = elements[0].get_command("fill_end")
            self.assertIsNotNone(cmd_clone)
            self.assertAlmostEqual(cmd_orig.target_point[0]+10, cmd_clone.target_point[0], 4)
            self.assertAlmostEqual(cmd_orig.target_point[1]+10, cmd_clone.target_point[1], 4)

    def test_copies_indirectly_attached_commands(self):
        """
        Check that commands attached to children of the clone target are copied to clones.
        """
        root: SvgDocumentElement = svg()
        group = root.add(Group())
        rect = group.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
        }))

        use = root.add(Use())
        use.href = group
        use.set('transform', Transform().add_translate(10, 10))

        original = FillStitch(rect)
        add_commands(original, ["fill_end"])

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            cmd_orig = original.get_command("fill_end")
            cmd_clone = elements[0].get_command("fill_end")
            self.assertIsNotNone(cmd_clone)
            self.assertAlmostEqual(cmd_orig.target_point[0]+10, cmd_clone.target_point[0], 4)
            self.assertAlmostEqual(cmd_orig.target_point[1]+10, cmd_clone.target_point[1], 4)

    # Checks that trim_after and stop_after commands and settings in cloned elements aren't overridden

    def test_trim_after(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["trim_after"]: "true"
        }))

        use = root.add(Use())
        use.href = rect

        clone = Clone(use)

        stitch_groups = clone.embroider(None)
        self.assertGreater(len(stitch_groups), 0)
        self.assertTrue(stitch_groups[-1].trim_after)

    def test_trim_after_command(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
        }))
        add_commands(FillStitch(rect), ["trim"])

        use = root.add(Use())
        use.href = rect

        clone = Clone(use)

        stitch_groups = clone.embroider(None)
        self.assertGreater(len(stitch_groups), 0)
        self.assertTrue(stitch_groups[-1].trim_after)

    def test_trim_after_command_on_clone(self):
        """
        If the clone element has a trim command, it should apply!
        """
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
        }))

        use = root.add(Use())
        use.href = rect

        clone = Clone(use)
        add_commands(clone, ["trim"])

        stitch_groups = clone.embroider(None)
        self.assertGreater(len(stitch_groups), 0)
        self.assertTrue(stitch_groups[-1].trim_after)

    def test_stop_after(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["stop_after"]: "true"
        }))

        use = root.add(Use())
        use.href = rect

        clone = Clone(use)

        stitch_groups = clone.embroider(None)
        self.assertGreater(len(stitch_groups), 0)
        self.assertTrue(stitch_groups[-1].stop_after)

    def test_stop_after_command(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
        }))
        fill_stitch = FillStitch(rect)
        add_commands(fill_stitch, ["stop"])

        use = root.add(Use())
        use.href = rect

        clone = Clone(use)

        stitch_groups = clone.embroider(None)
        self.assertGreater(len(stitch_groups), 0)
        self.assertTrue(stitch_groups[-1].stop_after)

    def test_stop_after_command_on_clone(self):
        """
        If the clone element has a stop command, it should still apply!
        """
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
        }))

        use = root.add(Use())
        use.href = rect

        clone = Clone(use)
        add_commands(clone, ["stop"])

        stitch_groups = clone.embroider(None)
        self.assertGreater(len(stitch_groups), 0)
        self.assertTrue(stitch_groups[-1].stop_after)
