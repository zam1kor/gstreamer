#!/usr/bin/python
import sys
import gi
gi.require_version('GLib', '2.0')
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst

Gst.init(sys.argv)

udpPipe = Gst.Pipeline("player")
source = Gst.ElementFactory.make('udpsrc', None)
source.set_property("port", 8999)
#source.set_property("host", "127.0.0.1")
caps = Gst.caps_from_string("application/x-rtp, payload=127")
source.set_property("caps", caps)

rdepay = Gst.ElementFactory.make('rtph264depay', 'rdepay')
vdecode = Gst.ElementFactory.make('avdec_h264', 'vdecode')
sink = Gst.ElementFactory.make('xvimagesink', None)
sink.set_property("sync", False)

udpPipe.add(source, rdepay, vdecode, sink)

#Gst.element_link_many(source, rdepay, vdecode, sink)
source.link(rdepay)
rdepay.link(vdecode)
vdecode.link(sink)

udpPipe.set_state(Gst.State.PLAYING)

GLib.MainLoop().run()