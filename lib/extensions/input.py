import os
from inkex import etree
import inkex
import pyembroidery

from ..svg import PIXELS_PER_MM, render_stitch_plan
from ..svg.tags import INKSCAPE_LABEL
from ..stitch_plan import StitchPlan


class Input(object):
    def affect(self, args):
        embroidery_file = args[0]
        pattern = pyembroidery.read(embroidery_file)
        pattern = pattern.get_pattern_interpolate_trim(2)

        stitch_plan = StitchPlan()
        color_block = None

        for raw_stitches, thread in pattern.get_as_colorblocks():
            if len(raw_stitches) > 1:
                color_block = stitch_plan.new_color_block(thread)
            trim_after = False
            for x, y, command in raw_stitches:
                if command == pyembroidery.STITCH:
                    if trim_after:
                        color_block.add_stitch(trim=True)
                        trim_after = False
                    color_block.add_stitch(x * PIXELS_PER_MM / 10.0, y * PIXELS_PER_MM / 10.0)
                if len(color_block) > 0 and command == pyembroidery.TRIM:
                    trim_after = True

        extents = stitch_plan.extents
        svg = etree.Element("svg", nsmap=inkex.NSS, attrib={
            "width": str(extents[0] * 2),
            "height": str(extents[1] * 2),
            "viewBox": "0 0 %s %s" % (extents[0] * 2, extents[1] * 2),
        })
        render_stitch_plan(svg, stitch_plan)

        # rename the Stitch Plan layer so that it doesn't get overwritten by Embroider
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
        layer.set(INKSCAPE_LABEL, os.path.basename(embroidery_file.decode("UTF-8")))
        layer.attrib.pop('id')

        # Shift the design so that its origin is at the center of the canvas
        # Note: this is NOT the same as centering the design in the canvas!
        layer.set('transform', 'translate(%s,%s)' % (extents[0], extents[1]))

        print etree.tostring(svg)
