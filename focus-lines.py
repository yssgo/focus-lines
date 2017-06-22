#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
# Author: Sengsu Iun
# Copyright 2017 Sengsu <Iun cieltero(at)gmail(dot)com>
# License: GPL v3
# GIMP plugin to draw center focus lines
import random
from gimpfu import *


gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def python_fu_focus_lines(image,layer,inLayerWidth,inLayerHeight,inUseImageSize,inLineCount,inMinLineWidth,inMaxLineWidth,inLineHeight,inVariance,inColor):
    pdb.gimp_image_undo_group_start(image)
    image_height = pdb.gimp_image_height(image)      
    image_width = pdb.gimp_image_width(image)      
    
    if inUseImageSize==FALSE:
        layer = pdb.gimp_layer_new(image,inLayerWidth, inLayerHeight, RGBA_IMAGE, "집중선", 100, NORMAL_MODE)
    else:
        layer = pdb.gimp_layer_new(image,image_width, image_height, RGBA_IMAGE, "집중선", 100, NORMAL_MODE)
    pdb.gimp_image_insert_layer(image, layer, None, -1)
    
    saveforeground = pdb.gimp_context_get_foreground()
    pdb.gimp_context_set_foreground(inColor)
    
    for i in range(inLineCount):        
        w=random.uniform(inMinLineWidth,inMaxLineWidth)
        
        h=random.uniform(inLineHeight*(1.0-inVariance/100.0/2.0),inLineHeight*(1.0+inVariance/100.0/2.0))
        
        if inUseImageSize==FALSE:
            offset=random.uniform(0,inLayerWidth-w)
        else:
            offset=random.uniform(0,image_width-w)
        
        if i==0:
            select_mode=CHANNEL_OP_REPLACE
        else:
            select_mode=CHANNEL_OP_ADD
        pdb.gimp_image_select_rectangle(image, select_mode, offset, 0, w, h)
        pdb.gimp_edit_bucket_fill(layer, FG_BUCKET_FILL, NORMAL_MODE, 100, 0, FALSE,0, 0)
        
    pdb.gimp_selection_none(image)     
    pdb.plug_in_polar_coords(image, layer, 0, 0, TRUE, FALSE,TRUE)
    
    pdb.gimp_context_set_foreground(saveforeground)
    pdb.gimp_undo_push_group_end(image)
    
    pdb.gimp_displays_flush()

register(
    "python-fu-focus-layout",
    _("Draw Lines going to near the center"),
    _("Draw Lines going to near the center"),
    "Sengsu Iun<cieltero(at)gmail(dot)com>",
    "(c) Sengsu Iun, Published under GPL version 3",
    "June 22, 2017",
    _("<Image>/Image/_Focus Lines"),
    "*",
    [
    (PF_INT, "inLayerWidth", _("Layer _Width:"), 400),
    (PF_INT, "inLayerHeight", _("Layer _Hidth:"), 400),
    (PF_TOGGLE, "inUseImageSize",_("Image Sized Layer:"),TRUE),     
    (PF_INT, "inLineCount",  _("_Lines:"), 200),
    (PF_INT, "inMinLineWidth",  _("Mi_ninum Width:"), 1),
    (PF_INT, "inMaxLineWidth",  _("Ma_ximum Width:"), 2),
    (PF_INT, "inMinLineHeight",  _("L_ine Height:"), 300),
    (PF_SLIDER, "inVariance",  _("_Variance %:"), 50, (0, 100, 1)),
    (PF_COLOR, "inColor", _("_Color:"), (0, 0, 0) ),
    ],
    [],
    python_fu_focus_lines,
    domain=("gimp20-python", gimp.locale_directory)
    )

main()


