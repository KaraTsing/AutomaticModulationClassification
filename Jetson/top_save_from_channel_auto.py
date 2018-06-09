#!/usr/bin/env python2
# -*- coding: utf-8 -*-

##################################################
# Modified 
# - adds conversion and calls GIEexec
# for conversion include convert_to_train module
# for classification include GIexec module
#
##################################################

##################################################
# GNU Radio Python Flow Graph
# Title: Top Save From Channel
# Generated: Sat Mar  3 18:10:56 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import digital
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys
import time

############## My imports ########################
import sys                  # for argv
import convert_to_train
import GIexec_call
import plot_module
##################################################


class top_save_from_channel(gr.top_block, Qt.QWidget):

    ##### Added filename parameter to constructor
    def __init__(self, filename):
        self.filevec = filename
        gr.top_block.__init__(self, "Top Save From Channel")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Save From Channel")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_save_from_channel")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 800e3

        self.sps = sps = 8
        self.nfilts = nfilts = 32

        #self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, 45*nfilts)
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0, 0.35, sps*11*nfilts)

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_source("external", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(800e6, 0)
        self.uhd_usrp_source_0.set_gain(10, 0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.01, ))
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 2048)
        ##### Added parameterized name
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, self.filevec, False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ## PFB ##
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(8, 2*3.14159/100, (rrc_taps), 32, 16, 1.5, 8)
        
        ##################################################
        # Connections
        ##################################################
        # self.connect((self.uhd_usrp_source_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))  
        # self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        # self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_head_0, 0))    
        # self.connect((self.blocks_head_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        # self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))  

        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_head_0, 0))    
        self.connect((self.blocks_head_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))  
        
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_save_from_channel")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)


def main(top_block_cls=top_save_from_channel, options=None):

    if len(sys.argv) < 2:
        print("Needs filename arg")
        sys.exit

    filename = sys.argv[1]
    
    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(filename)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
        #################### Process file ###################
        filevec = convert_to_train.convert_to_train_vec(filename)
        GIexec_call.classify(filevec)
        print("plotting: " + filename)
        #plot_module.plot_time(filename, 128)
        return
        
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
