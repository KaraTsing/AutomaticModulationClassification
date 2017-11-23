#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Wed Nov  1 00:59:16 2017
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys
from gnuradio import qtgui
from data_generators_WIN import *


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        		
        qtgui.util.check_set_qss()
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
        
        # create buttons
        self.buttonQPSK = Qt.QPushButton('QPSK Gen', self.top_widget)
        self.buttonQPSK.clicked.connect(self.handle_QPSK)
        
        self.buttonBPSK = Qt.QPushButton('BPSK Gen', self.top_widget)
        self.buttonBPSK.clicked.connect(self.handle_BPSK)
        
        self.buttonQAM16 = Qt.QPushButton('QAM16 Gen', self.top_widget)
        self.buttonQAM16.clicked.connect(self.handle_QAM16)
        
        self.buttonQAM64 = Qt.QPushButton('QAM64 Gen', self.top_widget)
        self.buttonQAM64.clicked.connect(self.handle_QPSK)
        
        self.button8PSK = Qt.QPushButton('8PSK Gen', self.top_widget)
        self.button8PSK.clicked.connect(self.handle_8PSK)
        
        self.buttonPAM4 = Qt.QPushButton('PAM4 Gen', self.top_widget)
        self.buttonPAM4.clicked.connect(self.handle_PAM4)
        
        self.buttonAMDSB = Qt.QPushButton('AMDSB Gen', self.top_widget)
        self.buttonAMDSB.clicked.connect(self.handle_AMBDSB)
        
        self.buttonCPFSK = Qt.QPushButton('CPFSK Gen', self.top_widget)
        self.buttonCPFSK.clicked.connect(self.handle_CPFSK)
        
        self.buttonGFSK = Qt.QPushButton('GFSK Gen', self.top_widget)
        self.buttonGFSK.clicked.connect(self.handle_GFSK)
        
        self.buttonAMSSB = Qt.QPushButton('AMSSB Gen', self.top_widget)
        self.buttonAMSSB.clicked.connect(self.handle_AMSSB)
        
        self.buttonWBFM = Qt.QPushButton('WBFM Gen', self.top_widget)
        self.buttonWBFM.clicked.connect(self.handle_WBFM)
       
        self.statusLabel = Qt.QLabel("Status: ", self.top_widget)
        
        # create SNR slider
        self.SNRSlider = Qt.QSlider(1, self.top_widget)
        self.SNRSlider.setTickPosition(Qt.QSlider.TicksBelow)
        self.SNRSlider.setMinimum(-20)
        self.SNRSlider.setMaximum(20)
        self.SNRSlider.setSingleStep(2)
        self.SNRLabel = Qt.QLabel("SNR: -20:20 dB", self.top_widget)
        
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
    
        self.top_grid_layout = Qt.QGridLayout()
        
        # add buttons to container
        self.top_grid_layout.addWidget(self.buttonQPSK, 0, 0)
        self.top_grid_layout.addWidget(self.buttonBPSK, 0, 1)
        self.top_grid_layout.addWidget(self.buttonQAM16, 0, 2)
        self.top_grid_layout.addWidget(self.button8PSK, 1, 0)
        self.top_grid_layout.addWidget(self.buttonPAM4, 1, 1)
        self.top_grid_layout.addWidget(self.buttonQAM64, 1, 2)
        self.top_grid_layout.addWidget(self.buttonGFSK, 2, 0)
        self.top_grid_layout.addWidget(self.buttonAMSSB, 2, 1)
        self.top_grid_layout.addWidget(self.buttonWBFM, 2, 2)
        self.top_grid_layout.addWidget(self.buttonCPFSK, 3, 0)
        self.top_grid_layout.addWidget(self.buttonAMDSB, 3, 1)
        self.top_layout.addWidget(self.statusLabel)
        self.top_layout.addWidget(self.SNRLabel)
        self.top_layout.addWidget(self.SNRSlider)
        
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())
        
        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200e3

        ##################################################
        # Blocks
        ##################################################
        
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	512, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
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
        self.channels_cfo_model_1 = channels.cfo_model(
                samp_rate,
                10,
                500e3,
                0
        )
        self.channels_cfo_model_0 = channels.cfo_model(
                samp_rate,
                10,
                500e3,
                0
        )
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_float*1, '192.168.1.187', 45000, 1472, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 200e3, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 250e3, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.channels_cfo_model_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.channels_cfo_model_1, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.channels_cfo_model_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.channels_cfo_model_1, 0), (self.blocks_add_xx_1, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.channels_cfo_model_1.set_samp_rate(self.samp_rate)
        self.channels_cfo_model_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        
    def handle_QPSK(self):
        self.statusLabel.setText("Status: Generating QPSK Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        src = gen_qpsk(SNRval)
        self.lock
        self.disconnect(self.qtgui_freq_sink_x_0)
        self.connect((src, 0), (self.qtgui_freq_sink_x_0, 0))
        self.unlock()

    def handle_BPSK(self):
        self.statusLabel.setText("Status: Generating BPSK Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        gen_bpsk(SNRval)
        
    def handle_QAM16(self):
        self.statusLabel.setText("Status: Generating QAM16 Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        gen_qam16(SNRval)
        
    def handle_QAM64(self):
        self.statusLabel.setText("Status: Generating QAM64 Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        gen_qam64(SNRval)
     
    def handle_PAM4(self):
        self.statusLabel.setText("Status: Generating PAM4 Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        gen_pam4(SNRval)
        
    def handle_CPFSK(self):
        self.statusLabel.setText("Status: Generating CPFSK Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        gen_cpfsk(SNRval)
    
    def handle_GFSK(self):
        self.statusLabel.setText("Status: Generating GFSK Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        gen_gfsk(SNRval)
        
    def handle_AMBDSB(self):
        self.statusLabel.setText("Status: Generating AMDSB Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        gen_amdsb(SNRval)
     
    def handle_AMSSB(self):
        self.statusLabel.setText("Status: Generating AMSSB Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        gen_amssb(SNRval)
        
    def handle_WBFM(self):
        self.statusLabel.setText("Status: Generating WBFM Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        src,mod,chan = gen_wbfm(SNRval)
        #rand_bits = np.random.randint(2, size=256)
        #randsrc = blocks.vector_source_b(rand_bits, True)
        sigsrc = analog.sig_source_c(200e3, analog.GR_COS_WAVE, 200e3, 1, 0)
        self.lock()
        print "Locked"
        self.disconnect(self.qtgui_freq_sink_x_0)
        convert = blocks.complex_to_float()
        self.connect((sigsrc, 0),(convert, 0), (mod, 0), (chan, 0), (self.qtgui_freq_sink_x_0, 0))
        self.unlock()
        print "Unlocked"
        
    def handle_8PSK(self):
        self.statusLabel.setText("Status: Generating 8PSK Data")
        SNRval = self.SNRSlider.value()
        if (SNRval % 2 != 0):
            SNRval = (SNRval + 1) % 20
        src = gen_8psk(SNRval)
        self.lock()
        self.disconnect(self.qtgui_freq_sink_x_0)
        convert = blocks.char_to_float()
        convert2 = blocks.float_to_complex()
        self.connect((src, 0), (convert, 0),(convert2, 0),(self.qtgui_freq_sink_x_0, 0))
        self.unlock()

def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
